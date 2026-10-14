---
added_by: claude
date: 2026-10-14
source: "[[sources/dubois-2023-alpacafarm-simulation-framework-methods-that.pdf]]"
---

# AlpacaFarm (Dubois et al., 2023)

## Summary
A simulator that uses LLM judges in place of human preference labels. Answer: indirect. LLM-judge rankings match crowdworkers' side-by-side preferences, but it never measures people's interactive experience. Its instructions are also single-turn.

## Relevant findings
- **Model rankings from the LLM judge match rankings from crowdworkers' pairwise preferences (Spearman 0.98).**

> [!quote]- Source: Dubois et al. 2023, p. 7
> "We see that the rankings have a Spearman correlation of 0.98, which suggests that AlpacaFarm faithfully captures the rankings among different LPF methods."
>
> [[sources/dubois-2023-alpacafarm-simulation-framework-methods-that.pdf]] · https://arxiv.org/abs/2305.14387

## Connection to our investigations
Shows that one kind of [[ai-output-quality]] measure agrees with another. It doesn't test [[interaction-quality]], which is the gap in [[output-vs-interaction-quality-crossword]].
