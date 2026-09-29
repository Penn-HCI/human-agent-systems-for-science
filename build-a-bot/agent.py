"""Scientific discovery agent: writes data processing scripts, runs them, reads
the outputs, and answers research questions about the files in data/.

    uv run python agent.py "Which task took participants longest on average?"
    uv run python agent.py --questions questions.md --budget 2.00

Each run gets a folder runs/<timestamp>/ holding the scripts the model wrote,
their outputs, the full message transcript, and the final answer.

Scripts run under macOS's sandbox (sandbox-exec) with no network access and
can't launch other programs or send requests to other apps. They
can read data/ and the Python install, but nothing else in your home folder;
they can write only inside the run folder. They get a stripped environment, so
the API key is never visible to them. All model calls go through
zdr_openrouter.chat(), which only routes to zero-data-retention endpoints.
"""

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from zdr_openrouter import DEFAULT_MODEL, chat

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RUNS = ROOT / "runs"
SCRIPT_TIMEOUT = 300  # seconds
MAX_TOOL_OUTPUT = 20_000  # characters of tool output sent back to the model

PROMPTS = ROOT / "prompts"


def prompt(filename, **values):
    """Read prompts/<filename>, filling in {name} placeholders (other braces are left alone)."""
    text = (PROMPTS / filename).read_text()
    values = {"script_timeout": SCRIPT_TIMEOUT, "max_tool_output": MAX_TOOL_OUTPUT, **values}
    for name, value in values.items():
        text = text.replace("{" + name + "}", str(value))
    return text


def sandbox_profile(run_dir):
    """Seatbelt profile: no network; read data/, the run folder and Python only; write the run folder only."""
    readable = [p.resolve() for p in (DATA, run_dir, Path(sys.prefix), Path(sys.base_prefix))]
    home = Path.home()
    # Folders between home and each readable path (e.g. ~/github): scripts may stat
    # them so path lookups work, but not list their contents.
    ancestors = sorted({a for p in readable for a in p.parents if a == home or home in a.parents})
    return "\n".join([
        "(version 1)",
        "(allow default)",
        "(deny network*)",
        "(deny file-write*)",
        '(allow file-write* (subpath "{}") (literal "/dev/null"))'.format(run_dir.resolve()),
        '(deny file-read* (subpath "{}"))'.format(home),
        "(allow file-read* {})".format(" ".join('(subpath "{}")'.format(p) for p in readable)),
        "(allow file-read-metadata {})".format(" ".join('(literal "{}")'.format(a) for a in ancestors)),
        # No app-to-app requests: an unsandboxed app (e.g. Terminal) could run commands for us.
        "(deny appleevent-send)",
        "(deny mach-lookup)",  # no macOS system services at all, which includes opening apps
        # Scripts may start Python (e.g. multiprocessing) but no other programs (osascript, open, sh, ...).
        "(deny process-exec)",
        '(allow process-exec (literal "{}") (literal "{}"))'.format(sys.executable, Path(sys.executable).resolve()),
    ])


class Workspace:
    def __init__(self, run_dir):
        self.dir = run_dir
        (run_dir / "scripts").mkdir(parents=True)
        (run_dir / "outputs").mkdir()
        (run_dir / "data").symlink_to(DATA)
        self.profile = run_dir / "sandbox.sb"
        self.profile.write_text(sandbox_profile(run_dir))

    def resolve(self, rel):
        """Resolve a model-supplied path, refusing anything outside the run folder or data/."""
        p = (self.dir / (rel or ".")).resolve()
        for root in (self.dir.resolve(), DATA.resolve()):
            if p == root or root in p.parents:
                return p
        raise ValueError("path is outside the working directory: " + rel)

    def list_files(self, path="."):
        p = self.resolve(path)
        lines = []
        for child in sorted(p.iterdir()):
            if child.name.startswith(".") or child.name == "sandbox.sb":
                continue
            kind = "dir " if child.is_dir() else "{:>9}".format(child.stat().st_size)
            lines.append("{}  {}{}".format(kind, child.name, "/" if child.is_dir() else ""))
        return "\n".join(lines) or "(empty)"

    def read_file(self, path, offset=0, max_chars=5000):
        text = self.resolve(path).read_text(errors="replace")
        max_chars = min(int(max_chars), MAX_TOOL_OUTPUT)
        chunk = text[offset:offset + max_chars]
        end = offset + len(chunk)
        note = "\n[chars {}-{} of {}]".format(offset, end, len(text)) if end < len(text) or offset else ""
        return chunk + note

    def run_python(self, name, code):
        name = "".join(c for c in name if c.isalnum() or c in "_-") or "script"
        script = self.dir / "scripts" / (name + ".py")
        script.write_text(code)
        env = {  # stripped: scripts never see OPENROUTER_API_KEY or other secrets
            "PATH": "/usr/bin:/bin",
            "HOME": str(self.dir),
            # Set so user lookups don't need the (blocked) macOS directory service.
            "USER": os.environ.get("USER", "user"),
            "LOGNAME": os.environ.get("USER", "user"),
            "LANG": "en_US.UTF-8",
            "PYTHONDONTWRITEBYTECODE": "1",
            "MPLCONFIGDIR": str(self.dir / ".mpl"),
        }
        try:
            r = subprocess.run(
                ["/usr/bin/sandbox-exec", "-f", str(self.profile), sys.executable, str(script)],
                cwd=self.dir, env=env, capture_output=True, text=True, timeout=SCRIPT_TIMEOUT,
            )
            result = "exit code {}\n--- stdout\n{}\n--- stderr\n{}".format(r.returncode, r.stdout, r.stderr)
        except subprocess.TimeoutExpired:
            result = "timed out after {}s".format(SCRIPT_TIMEOUT)
        (self.dir / "outputs" / (name + ".log")).write_text(result)
        return truncate(result)


def truncate(text, limit=MAX_TOOL_OUTPUT):
    if len(text) <= limit:
        return text
    half = limit // 2
    return text[:half] + "\n[... {} chars omitted ...]\n".format(len(text) - limit) + text[-half:]


def call_tool(ws, call):
    fn = call["function"]
    try:
        args = json.loads(fn.get("arguments") or "{}")
        tool = {"list_files": ws.list_files, "read_file": ws.read_file, "run_python": ws.run_python}[fn["name"]]
        return tool(**args)
    except Exception as e:  # report errors to the model so it can correct itself
        return "error: {}: {}".format(type(e).__name__, e)


def describe(call):
    fn = call["function"]
    try:
        args = json.loads(fn.get("arguments") or "{}")
    except ValueError:
        args = {}
    if fn["name"] == "run_python":
        return "run_python scripts/{}.py ({} lines)".format(args.get("name"), len(args.get("code", "").splitlines()))
    return "{}({})".format(fn["name"], ", ".join("{}={!r}".format(k, v) for k, v in args.items()))


def run(questions, model=DEFAULT_MODEL, max_steps=30, budget=1.00):
    run_dir = RUNS / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    ws = Workspace(run_dir)
    shutil.copytree(PROMPTS, run_dir / "prompts")  # record the prompts this run used
    tools = json.loads(prompt("tools.json"))
    messages = [
        {"role": "system", "content": prompt("system.md")},
        {"role": "user", "content": prompt("task.md", questions=questions)},
    ]
    spent = 0.0
    print("run folder:", run_dir.relative_to(ROOT))

    for step in range(1, max_steps + 1):
        out_of_room = step == max_steps or spent >= budget
        if out_of_room:
            messages.append({"role": "user", "content": prompt("wrap_up.md")})
        data = chat(messages, model=model, tools=tools, tool_choice="none" if out_of_room else "auto", max_tokens=8000)
        spent += data["usage"].get("cost", 0)
        msg = data["choices"][0]["message"]
        messages.append({k: v for k, v in msg.items() if k in ("role", "content", "tool_calls")})
        save_transcript(run_dir, messages)

        calls = msg.get("tool_calls") or []
        if not calls:
            answer = msg.get("content") or ""
            (run_dir / "answer.md").write_text(answer)
            print("\n" + answer)
            print("\n[{} steps, ${:.4f}] answer saved to {}".format(step, spent, (run_dir / "answer.md").relative_to(ROOT)))
            return answer
        for call in calls:
            print("  step {:>2} ${:.4f}  {}".format(step, spent, describe(call)))
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": call_tool(ws, call)})
        save_transcript(run_dir, messages)


def save_transcript(run_dir, messages):
    (run_dir / "transcript.json").write_text(json.dumps(messages, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("question", nargs="?", help="research question(s)")
    ap.add_argument("--questions", type=Path, help="file of research questions")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--max-steps", type=int, default=30)
    ap.add_argument("--budget", type=float, default=1.00, help="USD; the agent wraps up once this is spent")
    a = ap.parse_args()
    if not (a.question or a.questions):
        ap.error("give a question or --questions FILE")
    run(a.questions.read_text() if a.questions else a.question, a.model, a.max_steps, a.budget)
