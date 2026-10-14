---
added_by: claude
date: 2026-10-14
data: data/halie/data
---

# Does AI output quality correlate with interaction quality? (dialogue, QA, summarization, metaphor)

## Question
Across the other four HALIE tasks, do sessions with better [[ai-output-quality]] have better [[interaction-quality]]? Follows [[output-vs-interaction-quality-crossword]].

**Short answer:** It depends on who judges the output. Independent and automatic quality scores mostly don't track how people felt. Users' own judgments of the AI do, but those often don't track task success. The clearest link to task success is in QA: whether the AI's answer was right decided whether the person got it right.

The split between the two sides is provisional (see the details note).

## Findings
- **QA: people mostly took the AI's answer, right or wrong.** When the AI's last response pointed to the correct choice, people answered correctly 92% of the time, vs. 53% for others answering the same questions without the AI. When it pointed to a wrong choice, 88% picked that choice, and accuracy fell to 8% (vs. 32% without the AI).

> [!evidence]- Evidence
> **Re-run** (from the vault folder; see the details note for the `uv` cache workaround)
> ```
> uv run analysis/question_analysis.py | sed -n '/Per question/,/Per session/p'
> ```
> **Code**, from `analysis/question_analysis.py`
> ```python
> baseline = blocks[blocks["question_type"] == "ctrl"].groupby("question_id")["user_correct"].mean()
> fit = smf.logit("user_correct ~ C(ai_said, Treatment('not used')) + C(question_id)", inst).fit(disp=0)
> ```
> Controlling for question, a wrong AI answer lowers the log-odds of a correct answer by 2.16 (p < .001) relative to not using the AI.

- **QA: measured correctness predicts task success, but perceived helpfulness doesn't.** Within each model, the share of responses pointing to the correct choice tracks the person's gain from having the AI (ρ = 0.34). Helpfulness ratings don't (ρ = 0.04). Wrong answers didn't lower helpfulness (ρ = 0.11, n.s.), and base `Davinci` gave no gain at all (−0.01) while still being rated 3.5/5 helpful.

> [!evidence]- Evidence
> **Re-run**
> ```
> uv run analysis/question_analysis.py | grep -E "(correct_rate|wrong_rate|helpfulness) +vs (lift|helpfulness)"
> ```

- **Summarization: independent quality scores don't predict helpfulness; perceived editing effort does.** Third-party consistency and relevance relate to helpfulness at ρ = −0.10 to 0.02 in every analysis. How much users felt they had to edit relates at ρ = −0.43 to −0.48.

> [!evidence]- Evidence
> **Re-run**
> ```
> uv run analysis/summarization_analysis.py | grep -E "vs helpfulness"
> ```

- **Summarization: the most "consistent" summaries were mostly copied, and users edited them more.** InstructBabbage copies 76% of its word triples from the article (others ~25%), and copying predicts third-party consistency (ρ = 0.65). Sessions with more consistent summaries had more editing (ρ = 0.55, one session per worker).

> [!evidence]- Evidence
> **Re-run**
> ```
> uv run analysis/summarization_analysis.py | head -8
> uv run analysis/summarization_analysis.py | grep "tp_consistency vs distance"
> ```
> **Raw data** (InstructBabbage original → user's edit): "A forward has scored 12 goals in 10 games for Bristol City in Women's Super League Two last season." → user added "The forward is very happy to be with Manchester City."

- **Summarization: after editing, users think their summaries are consistent, but third parties often don't.** Users rate 99% of their edits consistent, vs. 80% by third parties. Of the originals most third-party raters called inconsistent, users edited 91%, yet a third were still inconsistent afterward.

> [!evidence]- Evidence
> **Re-run**
> ```
> uv run analysis/summarization_analysis.py | sed -n '/before and after/,/Does editing/p'
> ```

- **Dialogue: users' turn-by-turn judgments track the overall rating; automatic measures don't.** Within model, the share of turns flagged sensible relates to the end-of-chat rating at ρ = 0.41, and "preferred" at 0.51. Interestingness, a common target for chatbots, relates at only 0.10 (n.s.). Length and repetition relate at |ρ| ≤ 0.07. Bad turns early and late in the chat count about equally.

> [!evidence]- Evidence
> **Re-run**
> ```
> uv run analysis/dialogue_analysis.py | sed -n '/vs. overall quality/,/After a bad/p'
> ```

- **Metaphor: perceived fluency tracks experience, but nothing tracks the quality of the sentences people wrote.** Fluency relates to ease, enjoyment and satisfaction at ρ = 0.52–0.69. Neither fluency, helpfulness nor judged suggestion quality relates to third-party ratings of the final sentences (|ρ| ≤ 0.24, n.s.). Using the AI didn't change those ratings either (within worker, p = .45).

> [!evidence]- Evidence
> **Re-run**
> ```
> uv run analysis/metaphor_analysis.py | grep -E "vs (enjoyment|satisfaction|tp_overall)"
> uv run analysis/metaphor_analysis.py | grep "within worker"
> ```

- **Metaphor: keeping suggestions word for word goes with lower ownership, not lower satisfaction.** ρ = −0.35 for ownership (−0.44 one session per worker), and −0.09 for satisfaction.

> [!evidence]- Evidence
> **Re-run**
> ```
> uv run analysis/metaphor_analysis.py | grep "verbatim vs"
> ```

## Open questions
- Which slices count as AI output vs. interaction quality? The user wasn't satisfied with the current split.
- QA: do people follow wrong answers more when the model is usually right (InstructDavinci)?
- Summarization: do users notice that copied summaries are copied, and is that why they edit them?

## More
- Measures, LLM judges, checks and caveats: [[output-vs-interaction-quality-other-tasks-details]]
- Data quirks: [[halie-other-tasks]]
