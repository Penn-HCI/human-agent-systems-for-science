---
added_by: claude
date: 2026-10-14
source: "[[sources/li-2024-iqa-eval-automatic-evaluation-human.pdf]]"
---

# IQA-Eval (Li et al., 2024)

## Summary
Uses LLM agents to simulate and rate human–AI question-answering interactions, checked against human ratings. Mixed: LLM judges match people only moderately on real human interactions, and interactive rankings differ from non-interactive ones.

## Relevant findings
- **On real human–AI interactions, LLM-judge scores correlate only moderately with people's own ratings (r = 0.28–0.42).**

> [!quote]- Source: Li et al. 2024, p. 6
> "ChatGPT demonstrates a stronger correlation with human ratings, recording a correlation score of 0.424 for fluency and a correlation score of 0.306 for helpfulness. In contrast, Claude shows slightly lower correlations (0.281 for fluency and 0.287 for helpfulness)."
>
> [[sources/li-2024-iqa-eval-automatic-evaluation-human.pdf]] · https://arxiv.org/abs/2408.13545

- **Model rankings on interactive helpfulness and fluency differ from non-interactive rankings (Chatbot Arena).**

> [!quote]- Source: Li et al. 2024, p. 10
> "IQA Model rankings on these two aspects differ from those in Chatbot Arena (non-interaction)."
>
> [[sources/li-2024-iqa-eval-automatic-evaluation-human.pdf]] · https://arxiv.org/abs/2408.13545

- **But non-interactive accuracy does predict accuracy after interaction (r = 0.77 and 0.87).**

> [!quote]- Source: Li et al. 2024, p. 10
> "The Pearson correlations of the accuracy between the tables are 0.77 and 0.87 on both datasets, respectively."
>
> [[sources/li-2024-iqa-eval-automatic-evaluation-human.pdf]] · https://arxiv.org/abs/2408.13545

## Connection to our investigations
Uses the same HALIE models (TextDavinci, TextBabbage, Davinci) as [[output-vs-interaction-quality-crossword]], on HALIE's QA (MMLU) data.
