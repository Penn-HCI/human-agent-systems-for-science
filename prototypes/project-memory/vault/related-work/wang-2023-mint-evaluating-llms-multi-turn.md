---
added_by: claude
date: 2026-10-14
source: "[[sources/wang-2023-mint-evaluating-llms-multi-turn.pdf]]"
---

# MINT (Wang et al., 2023)

## Summary
A benchmark of multi-turn problem solving with tools and GPT-4-simulated user feedback. Indirect: it measures task success with simulated users, not experience, but finds single-turn scores don't predict multi-turn success.

## Relevant findings
- **Better single-turn performance doesn't guarantee better multi-turn performance.**

> [!quote]- Source: Wang et al. 2023, p. 2
> "Better single-turn performance does not necessarily entail better multi-turn performance. For example, while Claude-2 outperforms its predecessor Claude-1 in single-turn evaluation, the latter benefit more from interaction and performs better with > 2 turns."
>
> [[sources/wang-2023-mint-evaluating-llms-multi-turn.pdf]] · https://arxiv.org/abs/2309.10691

## Connection to our investigations
Echoes [[output-vs-interaction-quality-crossword]], where AI output quality didn't predict task success.
