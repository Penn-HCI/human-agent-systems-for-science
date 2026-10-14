---
added_by: claude
date: 2026-10-14
source: "[[sources/stiennon-2020-learning-summarize-human-feedback.pdf]]"
---

# Learning to summarize from human feedback (Stiennon et al., 2020)

## Summary
Trains summarizers on human preferences instead of ROUGE. It doesn't test interactive experience (indirect); it only compares metrics with static human preferences, and ROUGE stops tracking them as models get better.

## Relevant findings
- **ROUGE agrees with human preferences ~57% of the time on weaker models, falling to chance (~50%) on better ones.**

> [!quote]- Source: Stiennon et al. 2020, p. 9
> "While ROUGE has ~57% agreement with labelers when comparing samples from our supervised baseline models, this drops to ~50% for samples from our human feedback model."
>
> [[sources/stiennon-2020-learning-summarize-human-feedback.pdf]] · https://arxiv.org/abs/2009.01325

## Connection to our investigations
Only touches the [[ai-output-quality]] side of [[output-vs-interaction-quality-crossword]]: a standard metric can fail to track even static human judgments.
