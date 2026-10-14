---
added_by: claude
date: 2026-10-14
source: "[[sources/chi-2025-copilot-arena-platform-code-llm.pdf]]"
---

# Copilot Arena (Chi et al., 2025)

## Summary
A platform that collects developers' pairwise preferences between code completions inside their own editor. Answer: in-use preferences don't correlate with static coding benchmarks, but they do correlate with other human-preference leaderboards.

## Relevant findings
- **The preference ranking from real use matches Chatbot Arena (rs = 0.62 coding, 0.48 general) but not most static benchmarks (rs ≤ 0.1).**

> [!quote]- Source: Chi et al. 2025, p. 8
> "We find the highest correlation (Spearman’s rank correlation (rs) of 0.62) with Chatbot Arena (coding) [9] and similarly high correlation (rs = 0.48) with Chatbot Arena (general). However, we find a low correlation (rs ≤ 0.1) with most static benchmarks."
>
> [[sources/chi-2025-copilot-arena-platform-code-llm.pdf]] · https://arxiv.org/abs/2502.09328

- **Smaller models look better on static benchmarks than in real use.**

> [!quote]- Source: Chi et al. 2025, p. 2
> "In general, we observe that smaller models seem to overperform in static benchmarks compared to our leaderboard, while performance among larger models is mixed"
>
> [[sources/chi-2025-copilot-arena-platform-code-llm.pdf]] · https://arxiv.org/abs/2502.09328

## Connection to our investigations
Like [[output-vs-interaction-quality-crossword]], it compares models, but finds benchmark [[ai-output-quality]] doesn't predict which model people prefer in use ([[interaction-quality]]).
