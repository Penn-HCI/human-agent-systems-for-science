---
added_by: claude
date: 2026-10-14
data: data/halie/data/raw/crossword
---

# HALIE crossword data (raw)

People solved a crossword with an "AI Teammate" (one of four LMs) that they could query, then filled out a survey. From the HALIE paper (Lee et al., 2022, [arXiv:2212.09746](https://arxiv.org/abs/2212.09746)).

## Files (in `data/halie/data/raw/crossword/`)
- `logs.zip`: one JSON event log per session.
- `session_ids.txt`: the 305 sessions the authors kept (out of 347 logs).
- `survey_responses.json`: fluency, helpfulness, ease, joy (1–5), and free text.
- `puzzles/*.puz`: 5 puzzles with answer keys.

## Quirks
- **The published accuracies score the grid at about 31 minutes**, not at the end of the session.

> [!evidence]- Evidence
> Scoring the last grid at or before 31 minutes matches `std/crossword/accuracies.csv` for 301 of 304 sessions. The end of the session matches 189.
> ```
> uv run analysis/crossword_check_cutoff.py
> ```

- **Workers repeat:** 305 sessions come from 189 workers.
- **Timestamps:** these are minutes since the start, but at least one log ends at about 47,000 minutes, so don't trust session length.
- **Missing joy:** `joy` is `-1` when the question wasn't asked.

> [!quote]- Source: dataset README (`data/halie/data/README.md`)
> "`joy`: user's survey response to the question "How enjoyable was it to interact with the AI Teammate?" on 5-point Likert scale
> It contains a value of `-1` if the score is unavailable (due to the late addition of the question)."

## Log events
- `Ask` (`lm-query`) is followed by `Model Answer` (`lm-response`).
- Other events: `CellUpdate`, `NewClueSelected`, `GiveUp`, `Solved`.
- Every event carries the full `crossword-state` grid and the selected clue.
