---
added_by: claude
date: 2026-10-14
data: data/halie/data
---

# Details: AI output vs. interaction quality (dialogue, QA, summarization, metaphor)

Supplement to [[output-vs-interaction-quality-other-tasks]]. Data quirks: [[halie-other-tasks]].

## Which measures go on which side
This is Claude's proposal. The user wasn't satisfied with it, but said to proceed for now.

| task | AI output: measured | AI output: perceived | interaction quality |
| -- | -- | -- | -- |
| dialogue | length, degenerate, repeats an earlier turn | per-turn flags while chatting: sensible, specific, humanlike, preferred, interesting, boring | end-of-chat `quality-overall`; user's words per message |
| QA | LLM judge: the response points to the correct / a wrong choice; degenerate | fluency, helpfulness | ease; queries; accuracy with the AI; lift over the same person without it |
| summarization | third-party consistency, relevance, coherence of the original; copying from the article | user's own ratings of the original; helpfulness | edit distance, editing time, survey `edit`; third-party ratings of the edited summary |
| metaphor | LLM judge: apt, specific, imageable of each suggestion | fluency, helpfulness, "better alone" | ease, enjoyment, satisfaction, ownership, reuse; AI used, kept word for word; third-party ratings of the final sentence |

## LLM judges
No dataset labels AI responses directly in QA or metaphor, so Claude Haiku (through `claude -p`) labels them.
- **QA** (`analysis/question_judge.py`): the judge says which choice, if any, each response asserts, and the answer key decides correctness. In a by-eye check of 20 labels, about 18 were right, and the misses leaned toward "none".
- **Metaphor** (`analysis/metaphor_judge.py`): the judge rates apt, specific and imageable. On final sentences it agrees only weakly with the third-party raters (ρ = 0.33, n = 357), so treat the suggestion scores as a rough measure.

One of 3,163 QA responses is still unlabeled, because the sandbox later blocked the `claude` CLI. The analysis skips it.

> [!evidence]- Re-run everything
> Inside Claude Code's sandbox, first point `uv` at writable folders: `export UV_CACHE_DIR="$TMPDIR/uv-cache" UV_PYTHON_INSTALL_DIR="$TMPDIR/uv-python"`.
> ```
> uv run analysis/question_judge.py     # cached; only labels what's missing
> uv run analysis/metaphor_judge.py
> uv run analysis/question_analysis.py
> uv run analysis/dialogue_analysis.py
> uv run analysis/summarization_analysis.py
> uv run analysis/metaphor_analysis.py
> ```

## Robustness checks
- Dialogue and QA have one session per worker. Results are also reported ranked within model.
- Summarization: within document set, and one session per worker (39 workers; one did 11 sessions).
- Metaphor: one session per worker (32 workers), and a mixed model with worker as the group for sentence-level results.

## Caveats
- Survey items and per-turn flags come from the same person, so part of their correlation is likely shared response style. Dialogue flags were given turn by turn, before the overall rating, which helps only somewhat.
- Many tests, with no correction for multiple comparisons.
- Summarization (80) and metaphor (80 sessions, 32 workers) are small.
- Third-party metaphor scores are near ceiling (mean 0.83).
