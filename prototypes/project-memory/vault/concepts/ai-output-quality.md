---
added_by: claude
date: 2026-10-14
---

# AI output quality

How good the AI's responses are, as opposed to how the interaction went ([[interaction-quality]]).

## Crossword ([[halie-crossword-raw]])
The dataset has no per-response quality labels, so the measured versions come from the logs.

- **Measured** (per response, averaged per session):
  - `gave_answer_rate`: the response contains the selected clue's answer as a whole word, or a run of up to 3 words, and the query didn't already contain it. This only means the answer appears in the response, not that the response is correct. It also misses hints and plurals.
  - `degenerate_rate`: the response is empty, or more than 30% of its word triples repeat.
- **Perceived** (survey, 1–5): `fluency` ("How clear were the responses"), `helpfulness`.

> [!evidence]- Code, from `analysis/crossword_sessions.py`
> ```python
> "gave_answer": contains_answer(answer, response) and answer not in letters(query),
> "degenerate": is_degenerate(response),
> ```
> ```python
> def is_degenerate(response):
>     """Empty, or more than 30% of its word triples are repeats."""
>     w = words(response)
>     triples = [tuple(w[i : i + 3]) for i in range(len(w) - 2)]
>     repetitive = len(triples) > 0 and 1 - len(set(triples)) / len(triples) > 0.3
>     return len(w) == 0 or repetitive
> ```

> [!evidence]- Check the measures by eye
> 760 of 10,163 responses gave the answer, and 1,830 were degenerate. To print random examples:
> ```
> uv run analysis/crossword_sessions.py
> uv run analysis/crossword_response_samples.py gave_answer 20
> uv run analysis/crossword_response_samples.py degenerate 20
> ```
> Examples (from `analysis/outputs/crossword_responses.csv`):
> - gave answer, `[OAHU]` "Honolulu's island" → "of Oahu  The island of Oahu is located in the state of Hawaii…"
> - gave answer but wrong, `[AARON]` "the brother of Moses" → "…and the son of Amram (the brother of Aaron)…"
> - degenerate, `[COOS]` "what are pigeon sounds called" → "what are pigeon sounds called  what are pigeon sounds called…"

An earlier version used a plain substring match. About 14% of its hits matched inside other words (`AGE` in "eeks"), and another 14% only echoed the query.

Used in: [[output-vs-interaction-quality-crossword]]

> [!agent] Other HALIE tasks (2026-10-14)
> Claude proposed which slices count as AI output quality for dialogue, QA, summarization and metaphor. The user was not satisfied with the proposal, but said to proceed with it for now. See [[output-vs-interaction-quality-other-tasks]].
