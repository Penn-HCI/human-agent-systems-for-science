# Blocks Claude from creating, changing, or removing [!affirmed] callouts.
import json
import re
import sys
from pathlib import Path

AFFIRMED = re.compile(r"^>\s*\[!affirmed\]", re.IGNORECASE)


def affirmed_blocks(text):
    """Return the affirmed callouts in a note, each as a string."""
    blocks = []
    current = None
    for line in text.splitlines():
        if AFFIRMED.match(line):
            current = [line]
            blocks.append(current)
        elif current is not None and line.startswith(">"):
            current.append(line)
        else:
            current = None
    return sorted("\n".join(block) for block in blocks)


def apply_edit(text, edit):
    if edit.get("replace_all"):
        return text.replace(edit["old_string"], edit["new_string"])
    return text.replace(edit["old_string"], edit["new_string"], 1)


tool = json.load(sys.stdin)
name = tool["tool_name"]
args = tool["tool_input"]
path = Path(args["file_path"])
before = path.read_text() if path.exists() else ""

if name == "Write":
    after = args["content"]
elif name == "Edit":
    after = apply_edit(before, args)
else:  # MultiEdit
    after = before
    for edit in args["edits"]:
        after = apply_edit(after, edit)

if affirmed_blocks(before) != affirmed_blocks(after):
    print(
        "Blocked: this edit would create, change, or remove an [!affirmed] callout. "
        "Only people can do that. Add an [!agent] callout instead.",
        file=sys.stderr,
    )
    sys.exit(2)
