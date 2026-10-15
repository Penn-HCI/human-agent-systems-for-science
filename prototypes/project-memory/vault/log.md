# Log

## [2026-10-14] investigation | Output vs. interaction quality (crossword)
- Added [[output-vs-interaction-quality-crossword]], [[halie-crossword-raw]], [[output-quality]] and [[interaction-quality]].
- Added `analysis/crossword_sessions.py` and `analysis/crossword_correlations.py`.
- Saved the session log to [[2026-10-14-output-vs-interaction-quality-crossword]].

## [2026-10-14] revision | Rewrote notes to follow the new CLAUDE.md guidance
- Kept main notes short, with collapsed `[!evidence]` callouts and moved details to [[output-vs-interaction-quality-crossword-details]].
- Added `analysis/crossword_check_cutoff.py` and `analysis/crossword_solved_without_ai.py` so every finding can be re-run.
- Added a one-session-per-worker check (305 sessions come from 189 workers). Results held, except that the answer-rate correlation is no longer significant.

## [2026-10-14] revision | Reframed around AI output quality vs. interaction quality
- "Output quality" had measured task success. It now means the quality of the AI's responses: [[ai-output-quality]]. Task success moved into [[interaction-quality]], and `concepts/output-quality.md` was removed.
- Replaced the substring answer match with `gave_answer_rate`, and added `degenerate_rate`. Added `analysis/crossword_response_samples.py` and `outputs/crossword_responses.csv`.
- Rewrote [[output-vs-interaction-quality-crossword]] and its details note. Saved [[2026-10-14-ai-output-quality-measures]].

## [2026-10-14] related-work | Added the papers in `sources/`
- Added 43 notes to `related-work/`, read only for: do output quality metrics correlate with the human experience?
- Listed them in [[index]] by answer: don't correlate (7), mixed (9), indirect (27).

## [2026-10-14] revision | Removed the HALIE paper from the wiki
- So that analysis of the other HALIE tasks is de novo, moved the HALIE paper and its note to `../excluded-halie-paper/`.
- Removed its index line and a HALIE QA result from [[li-2024-iqa-eval-automatic-evaluation-human]]. Mixed is now 8 papers.

## [2026-10-14] investigation | Output vs. interaction quality (other four tasks)
- Proposed which slices count as AI output vs. interaction quality for dialogue, QA, summarization and metaphor. The user wasn't satisfied with it, but said to proceed; noted in [[ai-output-quality]] and [[interaction-quality]].
- Added [[output-vs-interaction-quality-other-tasks]], its details note, and [[halie-other-tasks]].
- Added `analysis/{question,metaphor}_judge.py` (Claude Haiku labels via `claude -p`) and `analysis/{question,dialogue,summarization,metaphor}_analysis.py`.
- The session transcript wasn't saved: the sandbox blocks reading `~/.claude`.
