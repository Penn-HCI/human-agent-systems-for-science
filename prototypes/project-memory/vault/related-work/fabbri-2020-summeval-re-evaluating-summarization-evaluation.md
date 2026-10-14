---
added_by: claude
date: 2026-10-14
source: "[[sources/fabbri-2020-summeval-re-evaluating-summarization-evaluation.pdf]]"
---

# SummEval (Fabbri et al., 2020)

## Summary
A benchmark of 14 automatic summarization metrics against expert ratings of summaries. It doesn't test interactive experience (indirect); it only compares metrics with static ratings, which they match weakly to moderately for coherence.

## Relevant findings
- **Automatic metrics match expert ratings worst on coherence, at weak to moderate levels (e.g., ROUGE-L Kendall's τ = 0.07).**

> [!quote]- Source: Fabbri et al. 2020, pp. 9–10
> "We find that most metrics have the lowest correlation within the coherence dimension, where the correlation strength can be classified as weak or moderate."
>
> [[sources/fabbri-2020-summeval-re-evaluating-summarization-evaluation.pdf]] · https://arxiv.org/abs/2007.12626

## Connection to our investigations
Only touches the [[ai-output-quality]] side of [[output-vs-interaction-quality-crossword]]: automatic metrics and static human ratings already disagree.
