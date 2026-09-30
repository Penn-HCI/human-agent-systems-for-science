"""Scientific discovery agent: writes data processing scripts, runs them, reads
the outputs, and answers research questions about a dataset in data/<name>/.

    uv run python agent.py --data study1 "Which task took participants longest on average?"
    uv run python agent.py --data study1 --questions questions.md --budget 2.00
    uv run python agent.py --resume runs/20260929-153432 --from-step 13

Each run gets a folder runs/<timestamp>/ holding the scripts the model wrote,
their outputs, the full message transcript, the final answer, and steps.txt
(what happened at each step, for choosing a --from-step).

Scripts run under macOS's sandbox (sandbox-exec) with no network access and
can't launch other programs or send requests to other apps. They
can read their one dataset and the Python install, but nothing else in your home folder;
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
# Skip providers that compress open-weight models below fp8 (e.g. fp4), which hurts multi-step tool use.
# Claude endpoints don't report a precision, so this isn't applied to them.
MIN_FP8 = {"quantizations": ["fp8", "bf16", "fp16", "fp32"]}

PROMPTS = ROOT / "prompts"


def prompt(filename, **values):
    """Read prompts/<filename>, filling in {name} placeholders (other braces are left alone)."""
    text = (PROMPTS / filename).read_text()
    values = {"script_timeout": SCRIPT_TIMEOUT, "max_tool_output": MAX_TOOL_OUTPUT, **values}
    for name, value in values.items():
        text = text.replace("{" + name + "}", str(value))
    return text


def sandbox_profile(run_dir, dataset):
    """Seatbelt profile: no network; read the dataset, the run folder and Python only; write the run folder only."""
    readable = [p.resolve() for p in (dataset, run_dir, Path(sys.prefix), Path(sys.base_prefix))]
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
    def __init__(self, run_dir, dataset):
        """A run folder whose data/ link points at one dataset folder, e.g. data/study1."""
        self.dir = run_dir
        self.dataset = dataset.resolve()
        (run_dir / "scripts").mkdir(parents=True)
        (run_dir / "outputs").mkdir()
        (run_dir / "data").symlink_to(self.dataset)
        (run_dir / "dataset.txt").write_text(dataset.name + "\n")
        self.profile = run_dir / "sandbox.sb"
        self.profile.write_text(sandbox_profile(run_dir, self.dataset))

    def resolve(self, rel):
        """Resolve a model-supplied path, refusing anything outside the run folder or its dataset."""
        p = (self.dir / (rel or ".")).resolve()
        for root in (self.dir.resolve(), self.dataset):
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
        # Show paths relative to the run folder, so output reads the same in every run folder.
        result = result.replace(str(self.dir.resolve()) + "/", "")
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


def dataset_dir(name):
    """data/<name>, or exit with a list of the datasets that exist."""
    d = DATA / (name or "")
    if name and d.parent == DATA and d.is_dir():
        return d
    names = sorted(p.name for p in DATA.iterdir() if p.is_dir())
    sys.exit("choose a dataset in data/ with --data: " + ", ".join(names))


def new_workspace(dataset):
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir, n = RUNS / stamp, 2
    while run_dir.exists():  # two runs started in the same second
        run_dir, n = RUNS / "{}-{}".format(stamp, n), n + 1
    ws = Workspace(run_dir, dataset_dir(dataset))
    shutil.copytree(PROMPTS, ws.dir / "prompts")  # record the prompts this run used
    print("run folder:", ws.dir.relative_to(ROOT), "| dataset:", dataset)
    return ws


def start(questions, dataset, system="system.md"):
    """A fresh run: returns its workspace and opening messages."""
    messages = [
        {"role": "system", "content": prompt(system)},
        {"role": "user", "content": prompt("task.md", questions=questions)},
    ]
    return new_workspace(dataset), messages


def resume(old_run, from_step, system="system.md", dataset=None):
    """Fork `old_run` just before its step `from_step`, with the current system prompt.

    Uses the old run's dataset unless `dataset` is given.
    """
    if dataset is None and (old_run / "dataset.txt").exists():
        dataset = (old_run / "dataset.txt").read_text().strip()
    old = json.loads((old_run / "transcript.json").read_text())
    step_starts = [i for i, m in enumerate(old) if m["role"] == "assistant"]
    if not 1 <= from_step <= len(step_starts):
        sys.exit("{} has steps 1-{}".format(old_run, len(step_starts)))
    messages = old[:step_starts[from_step - 1]]
    messages[0] = {"role": "system", "content": prompt(system)}

    ws = new_workspace(dataset)
    (ws.dir / "resumed_from.txt").write_text("{} step {}\n".format(old_run, from_step))
    # Recreate the files the earlier steps made by rerunning their scripts (no model calls),
    # and warn if a script's output changed, e.g. because data/ changed since the original run.
    old_prefix = str(old_run.resolve()) + "/"  # runs before paths were made relative
    recorded = {m["tool_call_id"]: m["content"].replace(old_prefix, "") for m in messages if m["role"] == "tool"}
    for m in messages:
        for call in m.get("tool_calls") or []:
            if call["function"]["name"] == "run_python" and call_tool(ws, call) != recorded.get(call["id"]):
                print("  warning: replayed {} gave different output than the original run".format(describe(call)))
    return ws, messages


def run(ws, messages, first_step=1, model=DEFAULT_MODEL, max_steps=30, budget=1.00):
    """The agent loop: call the model, run the tools it asks for, repeat until it answers."""
    run_dir = ws.dir
    tools = json.loads(prompt("tools.json"))
    provider = {"sort": "throughput"}  # prefer the fastest provider
    if not model.startswith("anthropic/"):
        provider.update(MIN_FP8)
    spent = 0.0

    for step in range(first_step, max_steps + 1):
        out_of_room = step == max_steps or spent >= budget
        if out_of_room:
            messages.append({"role": "user", "content": prompt("wrap_up.md")})
        data = chat(messages, model=model, provider=provider, tools=tools, tool_choice="none" if out_of_room else "auto", max_tokens=8000)
        spent += data["usage"].get("cost", 0)
        msg = data["choices"][0]["message"]
        # Keep reasoning_details so reasoning models (e.g. DeepSeek) see their earlier thinking.
        messages.append({k: v for k, v in msg.items() if k in ("role", "content", "tool_calls", "reasoning_details")})
        save_transcript(run_dir, messages)

        calls = msg.get("tool_calls") or []
        if not calls:
            answer = msg.get("content") or ""
            (run_dir / "answer.md").write_text(answer)
            log_step(run_dir, step, spent, "final answer")
            print("\n" + answer)
            print("\n[${:.4f}] answer saved to {}".format(spent, (run_dir / "answer.md").relative_to(ROOT)))
            return answer
        for call in calls:
            log_step(run_dir, step, spent, describe(call))
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": call_tool(ws, call)})
        save_transcript(run_dir, messages)


def log_step(run_dir, step, spent, what):
    """Print a step line and add it to steps.txt, for picking a --from-step later."""
    line = "step {:>2} ${:.4f}  {}".format(step, spent, what)
    print("  " + line)
    with (run_dir / "steps.txt").open("a") as f:
        f.write(line + "\n")


def save_transcript(run_dir, messages):
    (run_dir / "transcript.json").write_text(json.dumps(messages, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("question", nargs="?", help="research question(s)")
    ap.add_argument("--questions", type=Path, help="file of research questions")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--max-steps", type=int, default=30)
    ap.add_argument("--budget", type=float, default=1.00, help="USD; the agent wraps up once this is spent")
    ap.add_argument("--data", metavar="NAME", help="dataset folder in data/ (resumed runs default to the original's)")
    ap.add_argument("--system", default="system.md", help="system prompt file in prompts/")
    ap.add_argument("--resume", type=Path, metavar="RUN_FOLDER", help="continue an earlier run (with --from-step)")
    ap.add_argument("--from-step", type=int, help="step of the earlier run to redo onward (see its steps.txt)")
    a = ap.parse_args()
    if a.resume:
        if not a.from_step:
            ap.error("--resume needs --from-step")
        ws, messages = resume(a.resume, a.from_step, a.system, a.data)
        first_step = a.from_step
    elif a.question or a.questions:
        ws, messages = start(a.questions.read_text() if a.questions else a.question, a.data, a.system)
        first_step = 1
    else:
        ap.error("give a question, --questions FILE, or --resume RUN_FOLDER")
    run(ws, messages, first_step, a.model, a.max_steps, a.budget)
