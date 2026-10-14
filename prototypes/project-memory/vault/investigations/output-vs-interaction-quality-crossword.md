---
added_by: claude
date: 2026-10-14
data: data/halie/data/raw/crossword
---

# Does AI output quality correlate with interaction quality? (crossword)

## Question
In the crossword task, do sessions with better [[ai-output-quality]] have better [[interaction-quality]]?


**Short answer:** [!affirmed] Yes for how the interaction felt, but no for task success. Much of the link to experience comes from differences between models.

## Findings
- **Measured and perceived AI output quality agree.** Helpfulness tracks how often the AI gave the answer (ρ = 0.44), and fluency tracks how often it was degenerate (ρ = −0.46). Both hold within puzzle and model (0.32 and −0.16).

> [!evidence]- Evidence
> **Re-run** (from the vault folder)
> ```
> uv run analysis/crossword_sessions.py
> uv run analysis/crossword_correlations.py | grep -E "(gave_answer_rate|degenerate_rate) +(fluency|helpfulness)"
> ```
> **Code**, from `analysis/crossword_correlations.py`
> ```python
> analyses = [("all sessions", sessions),
>             ("within puzzle", ranked_within(["puzzle"])),
>             ("within puzzle and model", ranked_within(["puzzle", "model"])),
>             ("one session per worker", sessions.drop_duplicates("worker"))]
> ```

- **Better AI output goes with a better experience, mostly between models.** The measured AI output quality relates to ease and joy at |ρ| = 0.19–0.32. Within puzzle and model, only "gave the answer" and joy remain (ρ = 0.17, p = .007). The perceived measures relate much more strongly (ρ = 0.46–0.72), but they come from the same survey as ease and joy.

> [!evidence]- Evidence
> **Re-run**
> ```
> uv run analysis/crossword_correlations.py | grep -E "(gave_answer_rate|degenerate_rate) +(ease|joy)"
> uv run analysis/crossword_correlations.py | grep -E "(fluency|helpfulness) +(ease|joy)"
> ```

- **AI output quality doesn't predict task success.** All four AI-output measures correlate with letter accuracy at |ρ| ≤ 0.09 (p > .12). One exception: degenerate responses within puzzle and model, ρ = −0.12, p = .04, which is likely noise given 100 tests. For example, 18 people scored at least 95% while rating helpfulness 1.

> [!evidence]- Evidence
> **Re-run**
> ```
> uv run analysis/crossword_correlations.py | grep -E "(gave_answer_rate|degenerate_rate|fluency|helpfulness) +letter_accuracy"
> uv run analysis/crossword_solved_without_ai.py
> ```
> **Raw data**, from `helpfulness_freetext` in `survey_responses.json`
> - `61_b3d7cef6…_ai2-jumbo` (accuracy 0.99): "The AI was talking mostly nonsense and didn't give me any good answers."
> - `61_69b5bd57…_ai2-jumbo` (accuracy 1.00): "I wanted to do the puzzle by myself, but I forced myself to use the AI."

- **The models differ sharply.** `text-davinci` is best on every measure. The base models (`davinci`, `ai2-jumbo`) are degenerate about a third of the time. `text-babbage` is rarely degenerate but also rarely gives the answer.

> [!evidence]- Evidence
> **Re-run**
> ```
> uv run analysis/crossword_correlations.py | tail -6
> ```
> | model | gave answer | degenerate | fluency | helpfulness | joy | letter acc. |
> | -- | -- | -- | -- | -- | -- | -- |
> | text-davinci | 0.13 | 0.05 | 3.65 | 3.14 | 3.42 | 0.63 |
> | davinci | 0.06 | 0.34 | 2.26 | 1.92 | 2.18 | 0.56 |
> | ai2-jumbo | 0.07 | 0.32 | 2.30 | 2.20 | 2.23 | 0.55 |
> | text-babbage | 0.04 | 0.02 | 3.14 | 2.27 | 2.76 | 0.47 |

- **Also: asking more queries goes with lower task success.** ρ = −0.33 to −0.36 in every analysis (p < .001). This is correlational: people who are struggling may simply ask more.

> [!evidence]- Evidence
> **Re-run**
> ```
> uv run analysis/crossword_correlations.py | grep -E "num_queries +letter_accuracy"
> ```

## Open questions
- Does task success depend on whether people use a response that gave the answer, i.e., type it into the grid?
- Do degenerate responses make people re-ask? Within each model, they go with more queries (ρ = 0.19).
- How does this compare with the HALIE paper's own results?

## More
- Methods, full results and caveats: [[output-vs-interaction-quality-crossword-details]]
- Session logs: [[2026-10-14-output-vs-interaction-quality-crossword]], [[2026-10-14-ai-output-quality-measures]]
