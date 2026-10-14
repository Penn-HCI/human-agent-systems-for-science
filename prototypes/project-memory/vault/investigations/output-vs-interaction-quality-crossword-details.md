---
added_by: claude
date: 2026-10-14
data: data/halie/data/raw/crossword
---

# Details: AI output vs. interaction quality (crossword)

Supplement to [[output-vs-interaction-quality-crossword]].

## Method
- One row per session: 305 sessions (from `session_ids.txt`), 304 with surveys, and 264 with `joy`. There are 10,163 AI responses.
- Measures: see [[ai-output-quality]] and [[interaction-quality]]. Everything uses the first 31 minutes, to match the published accuracies. See [[halie-crossword-raw]].
- Spearman correlations are computed four ways:
  - across all sessions
  - ranked within each puzzle
  - ranked within each puzzle × model group
  - with only one session per worker

> [!evidence]- Re-run everything
> ```
> uv run analysis/crossword_sessions.py      # writes crossword_sessions.csv, crossword_responses.csv
> uv run analysis/crossword_correlations.py  # writes crossword_correlations.csv, crossword_by_model.csv
> uv run analysis/crossword_response_samples.py gave_answer 20
> uv run analysis/crossword_solved_without_ai.py
> uv run analysis/crossword_check_cutoff.py
> ```

## Results (ρ)
Cells show: all sessions / within puzzle and model / one per worker. Bold means p < .05 in all three.

| AI output ↓ / interaction → | ease | joy | num_queries | letter accuracy |
| -- | -- | -- | -- | -- |
| gave_answer_rate | 0.19 / 0.08 / 0.20 | **0.29 / 0.17 / 0.20** | 0.08 / 0.10 / 0.07 | 0.09 / −0.01 / 0.05 |
| degenerate_rate | −0.32 / −0.09 / −0.42 | −0.32 / −0.09 / −0.40 | 0.08 / 0.19 / 0.05 | −0.03 / −0.12 / −0.02 |
| fluency | **0.57 / 0.47 / 0.55** | **0.63 / 0.53 / 0.58** | 0.08 / 0.07 / 0.08 | 0.03 / −0.01 / 0.05 |
| helpfulness | **0.48 / 0.38 / 0.46** | **0.72 / 0.64 / 0.67** | 0.17 / 0.17 / 0.13 | −0.01 / −0.07 / −0.04 |

Clue accuracy and end-of-session accuracy give the same pattern. See `analysis/outputs/crossword_correlations.csv`.

## Caveats
- About 100 correlations were run, with no correction for multiple comparisons.
- Fluency, helpfulness, ease and joy all come from the same survey, so part of their correlation is likely shared response style.
- `gave_answer_rate` means the answer appears in the response, not that the response is correct. Its value also depends on how well the person asked.
- The 30% repetition threshold for `degenerate` was set by eye.
- 305 sessions come from 189 workers. The one-per-worker check gives similar results.
- The 31-minute cutoff was reverse-engineered, and 3 sessions still don't match the published scores.
