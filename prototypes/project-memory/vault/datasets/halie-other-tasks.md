---
added_by: claude
date: 2026-10-14
data: data/halie/data
---

# HALIE dialogue, QA, summarization and metaphor data

The four non-crossword HALIE tasks. Used in [[output-vs-interaction-quality-other-tasks]]. We use the `std/` files, plus raw files where noted.

## Dialogue
- 189 sessions, one per worker, ~11 turns each, 4 models. Per-turn ratings and the end-of-chat `quality-overall` (1–5) come from `raw/dialogue/runs.csv`.
- **Each turn was rated once, while chatting.** `runs.csv` stores those flags as `turn-binary` and again as `final` with every value flipped. We use `final`, where 1 means sensible, specific, and so on.
- The question wording for `quality-overall` and `preference` isn't in the data.
- `whitelist.txt` and `blocklist.txt` are profanity word lists, not session lists.

> [!evidence]- Evidence
> `turn-binary` and `final` never agree, and their means sum to 1 (sensibility 0.12 vs. 0.88). Turns with `final` sensibility 0 read as off-topic, e.g., "Where are you going?" → "I don't know."

## Question answering
- 331 sessions, one per worker. Each person answers 5 questions with the AI and 5 without, out of 30 questions, plus an attention check. Each question gets ~55 answers each way.

## Summarization
- 80 sessions from 39 workers (one did 11). Each edits 10 news summaries.
- **The summaries were generated in advance:** there is one fixed summary per document × model. So the survey item "the AI assistant improved as I edited more" describes a system that couldn't change.
- Third-party ratings cover about half the summaries, both before and after editing.

## Metaphor
- 80 sessions from 32 workers, with ~9 sentences each, on 4 seeds.
- Third-party ratings (apt, specific, imageable) are of the **final sentences only** (395 of 745), not of the AI's suggestions.
- `std/` drops the survey item "I would have come up with better sentences alone"; it's in `raw/metaphor/survey_responses.csv`.
