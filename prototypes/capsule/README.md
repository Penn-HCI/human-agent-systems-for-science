# Capsule

Research data that only a local LLM reads. Claude asks questions through an MCP tool; you approve (or edit) each answer in a popup before Claude sees it.

## Setup

1. Put data in `~/capsule-data/`
2. Optional test without Claude: `cd prototypes/capsule && uv run capsule.py "your question"`
3. Start `claude` from the repo root — approve the `capsule` MCP server when asked

Model: MLX, default `mlx-community/Olmo-3-7B-Instruct-4bit`; set `CAPSULE_MODEL` to change.

## Known gaps

- Claude can still edit `capsule.py` (e.g., remove the popup); changes apply when the server restarts.
