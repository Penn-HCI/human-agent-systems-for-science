---
added_by: claude
date: 2026-10-14
source: "[[sources/deriu-2020-spot-bot-robust-efficient-framework.pdf]]"
---

# Spot The Bot (Deriu et al., 2020)

## Summary
A chatbot evaluation where people read bot-bot conversations and judge whether each speaker is human. Mixed and mostly indirect: it notes that automatic and single-turn scores diverge from multi-turn quality, and its own ranking only partly matches rankings from people chatting with the bots.

## Relevant findings
- **Automatic metrics and single-turn ratings miss multi-turn quality.** A bot that repeats itself can score well per turn but badly over a conversation (cited, not tested here).

> [!quote]- Source: Deriu et al. 2020, p. 2
> "Automatic evaluation metrics for chatbots are known to correlate poorly with human ratings (Liu et al., 2016; Lowe et al., 2017; Mehri and Eskenazi, 2020)"
>
> "A system that tends to produce repeated answers can obtain a high single-turn score, albeit a low multi-turn one (See et al., 2019)."
>
> [[sources/deriu-2020-spot-bot-robust-efficient-framework.pdf]]

- **Observer-based rankings only partly match rankings from people who chatted with the bots (ConvAI2).**

> [!quote]- Source: Deriu et al. 2020, p. 6
> "Furthermore, the LC model is ranked very highly. This corresponds to the findings of the ConvAI2 challenge (Dinan et al., 2020a). However, in Spot The Bot, the KV is ranked much higher than the HF model, which is not in line with the ConvAI2 evaluation."
>
> [[sources/deriu-2020-spot-bot-robust-efficient-framework.pdf]]

## Connection to our investigations
Supports checking per-turn [[ai-output-quality]] against whole-session [[interaction-quality]], as in [[output-vs-interaction-quality-crossword]].
