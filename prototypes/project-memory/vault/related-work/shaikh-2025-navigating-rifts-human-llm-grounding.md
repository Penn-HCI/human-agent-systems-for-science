---
added_by: claude
date: 2026-10-14
source: "[[sources/shaikh-2025-navigating-rifts-human-llm-grounding.pdf]]"
---

# Rifts in human-LLM grounding (Shaikh et al., 2025)

## Summary
Analyzes chat logs for grounding (clarifying, following up) and builds a benchmark, RIFTS. Indirect: strong instruction-following models do almost perfectly when no grounding is needed but worse than random when it is.

## Relevant findings
- **Frontier models score 23% on RIFTS (random is 33%), despite 96% on tasks that need no grounding.**

> [!quote]- Source: Shaikh et al. 2025, pp. 8–9
> "We find that all off-the-shelf instruction-following models (avg. 23.23% acc.) perform worse than random (33%)." [...] "evaluated LLMs perform near perfectly for tasks that require no grounding initiative (No Grounding category, 96.09%)"
>
> [[sources/shaikh-2025-navigating-rifts-human-llm-grounding.pdf]] · https://arxiv.org/abs/2503.13975

## Connection to our investigations
Suggests good single-turn [[ai-output-quality]] can coexist with poor [[interaction-quality]]; relevant to [[output-vs-interaction-quality-crossword]].
