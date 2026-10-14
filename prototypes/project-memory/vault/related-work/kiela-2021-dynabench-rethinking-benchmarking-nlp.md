---
added_by: claude
date: 2026-10-14
source: "[[sources/kiela-2021-dynabench-rethinking-benchmarking-nlp.pdf]]"
---

# Dynabench (Kiela et al., 2021)

## Summary
A platform where people try to write examples that fool models live, as an alternative to static benchmarks. Indirect: it argues high benchmark scores overstate how models do with real people, but doesn't measure user experience.

## Relevant findings
- **Models beat humans on benchmarks yet fail on simple examples and in real use; people interacting live still find errors in 33–44% of their attempts.**

> [!quote]- Source: Kiela et al. 2021, p. 1
> "Models that achieve super-human performance on benchmark tasks (according to the narrow criteria used to define human performance) nonetheless fail on simple challenge examples and falter in real-world scenarios."
>
> [[sources/kiela-2021-dynabench-rethinking-benchmarking-nlp.pdf]]

> [!quote]- Source: Kiela et al. 2021, p. 7
> "As we can see, the validated model error rate (vMER; the number of human-validated model errors divided by the total number of examples—note that the error rates are not necessarily comparable across tasks, since the interfaces and in-the-loop models are not identical) is still very high across all tasks, clearly demonstrating that NLP is far from solved."
>
> (Table 1: vMER 33.24% NLI, 33.74% QA, 35.00% sentiment, 43.90% hate speech.)
>
> [[sources/kiela-2021-dynabench-rethinking-benchmarking-nlp.pdf]]

## Connection to our investigations
A reason to expect benchmark-style [[ai-output-quality]] to overstate quality in use, as tested in [[output-vs-interaction-quality-crossword]].
