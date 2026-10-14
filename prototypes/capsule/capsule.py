# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp", "mlx-lm==0.32.0"]
# ///
"""Capsule: research data that only a local LLM reads.

Claude calls `ask`. A local model (MLX) answers using the data. You see the
answer in a popup, can edit it, and decide whether it goes back to Claude.

Test without Claude: uv run capsule.py "your question"
"""

import functools
import os
import subprocess
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mlx_lm import generate, load

DATA_DIR = Path(os.environ.get("CAPSULE_DIR", "~/capsule-data")).expanduser()
MODEL = os.environ.get("CAPSULE_MODEL", "mlx-community/Olmo-3-7B-Instruct-4bit")

mcp = MCPServer("capsule")


def read_data():
    parts = []
    for path in sorted(DATA_DIR.rglob("*")):
        if path.is_file() and not path.name.startswith("."):
            parts.append(f"=== {path.name} ===\n{path.read_text(errors='ignore')}")
    return "\n\n".join(parts)


@functools.cache
def get_model():
    return load(MODEL)


def ask_local_llm(question):
    model, tokenizer = get_model()
    messages = [
        {"role": "system", "content": "Answer the question using the research data below. "
                                      "Summarize; do not quote participants verbatim or include names.\n\n"
                                      + read_data()},
        {"role": "user", "content": question},
    ]
    prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True)
    return generate(model, tokenizer, prompt=prompt, max_tokens=1000)


def human_review(question, answer):
    """Popup showing the answer. Returns the (possibly edited) text, or None if blocked."""
    script = """
    on run argv
        set r to display dialog "Claude asked: " & item 1 of argv & return & return & ¬
            "Edit if needed. Send this to Claude?" default answer item 2 of argv ¬
            buttons {"Block", "Send"} default button "Send" with title "Capsule"
        if button returned of r is "Send" then return text returned of r
        return ""
    end run
    """
    result = subprocess.run(["osascript", "-e", script, question, answer], capture_output=True, text=True)
    sent = result.stdout.strip()
    return sent or None


@mcp.tool()
def ask(question: str) -> str:
    """Ask a question about the private research data in the capsule.
    A local model answers; a human approves the answer before you see it."""
    answer = ask_local_llm(question)
    approved = human_review(question, answer)
    return approved if approved else "The researcher blocked this response."


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(ask(" ".join(sys.argv[1:])))
    else:
        mcp.run()
