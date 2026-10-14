---
added_by: claude
date: 2026-10-14
---

# Interaction quality

How the human-AI interaction went, including whether the task got done. Compare [[ai-output-quality]], which is about the AI's responses themselves.

## Crossword ([[halie-crossword-raw]])
- **Experience (survey, 1–5):** `ease`, `joy`.
- **Process:** `num_queries`, the number of queries in the first 31 minutes.
- **Task success:** `letter_accuracy` is the share of cells that are correct. `clue_accuracy` is the share of clues that are fully correct. Both are scored at 31 minutes, and the `final_*` columns score the end of the session.

> [!evidence]- Code, from `accuracy` in `analysis/crossword_sessions.py`
> ```python
> white = [(r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch != "."]
> correct = {(r, c) for r, c in white if (state[r][c] or "").upper() == grid[r][c]}
> letter_accuracy = len(correct) / len(white)
> clue_accuracy = sum(all(cell in correct for cell in cells) for cells in clues.values()) / len(clues)
> ```

Used in: [[output-vs-interaction-quality-crossword]]

> [!agent] Other HALIE tasks (2026-10-14)
> Claude proposed which slices count as interaction quality for dialogue, QA, summarization and metaphor. The user was not satisfied with the proposal, but said to proceed with it for now. See [[output-vs-interaction-quality-other-tasks]].
