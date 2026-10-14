"""Save one prompt's worth of a Claude Code session into the vault.

Claude Code keeps each session at ~/.claude/projects/<project>/<session-id>.jsonl.
This copies the records from a given user prompt up to the next user prompt,
as raw JSONL and as a readable Markdown log.

Usage (from the vault folder):
    python3 tools/save_transcript.py <session.jsonl> "<start of the prompt>" transcripts/<name>
Writes transcripts/<name>.jsonl and transcripts/<name>.md
"""
import json
import sys
from pathlib import Path


def is_prompt(record):
    """A user message typed by a person (not a tool result)."""
    content = record.get("message", {}).get("content") if record.get("type") == "user" else None
    if isinstance(content, str):
        return True
    return isinstance(content, list) and any(block["type"] == "text" for block in content)


def prompt_text(record):
    content = record["message"]["content"]
    if isinstance(content, str):
        return content
    return "\n".join(block["text"] for block in content if block["type"] == "text")


def fenced(text):
    return f"~~~~\n{text.rstrip()}\n~~~~\n"


def to_markdown(records):
    lines = []
    for record in records:
        if record.get("type") not in ("user", "assistant"):
            continue
        content = record["message"]["content"]
        if isinstance(content, str):
            content = [{"type": "text", "text": content}]
        for block in content:
            if record["type"] == "user" and block["type"] == "text":
                lines.append(f"## Prompt\n\n{block['text']}\n")
            elif block["type"] == "text":
                lines.append(f"**Claude:** {block['text']}\n")
            elif block["type"] == "tool_use":
                args = dict(block["input"])
                body = args.pop("command", None) or args.pop("content", None) or ""
                summary = args.pop("description", None) or args.get("file_path", "")
                lines.append(f"### {block['name']}: {summary}\n")
                lines.append(fenced(body or json.dumps(args, indent=1)))
            elif block["type"] == "tool_result":
                result = block["content"]
                if isinstance(result, list):
                    result = "\n".join(part.get("text", "") for part in result)
                lines.append("Output:\n")
                lines.append(fenced(result or "(no output)"))
    return "\n".join(lines)


def main():
    session, start, out = Path(sys.argv[1]).expanduser(), sys.argv[2], Path(sys.argv[3])
    records = [json.loads(line) for line in session.read_text().splitlines()]

    begin = next(i for i, r in enumerate(records) if is_prompt(r) and start in prompt_text(r))
    end = next((i for i in range(begin + 1, len(records)) if is_prompt(records[i])), len(records))
    selected = records[begin:end]

    out.parent.mkdir(parents=True, exist_ok=True)
    out.with_suffix(".jsonl").write_text("".join(json.dumps(r) + "\n" for r in selected))
    out.with_suffix(".md").write_text(to_markdown(selected))
    print(f"Saved {len(selected)} records to {out}.md and {out}.jsonl")


if __name__ == "__main__":
    main()
