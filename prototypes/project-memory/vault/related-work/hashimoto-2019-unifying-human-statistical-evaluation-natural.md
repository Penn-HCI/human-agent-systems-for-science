---
added_by: claude
date: 2026-10-14
source: "[[sources/hashimoto-2019-unifying-human-statistical-evaluation-natural.pdf]]"
---

# HUSE (Hashimoto et al., 2019)

## Summary
Proposes HUSE, combining human ratings and model probabilities to measure both quality and diversity. Indirect: it compares offline metrics with offline ratings, not user experience.

## Relevant findings
- **Per-output human ratings miss diversity, so tricks that raise rated quality (e.g., annealing) can make a model worse overall.**

> [!quote]- Source: Hashimoto et al. 2019, p. 1
> "On summarization and chit-chat dialogue, we show that (i) HUSE detects diversity defects which fool pure human evaluation and that (ii) techniques such as annealing for improving quality actually decrease HUSE due to decreased diversity."
>
> [[sources/hashimoto-2019-unifying-human-statistical-evaluation-natural.pdf]]

## Connection to our investigations
None directly; it is a caution that static ratings of [[ai-output-quality]] can miss things.
