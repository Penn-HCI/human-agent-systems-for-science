---
added_by: claude
date: 2026-10-14
source: "[[sources/vafa-2024-large-language-models-perform-way.pdf]]"
---

# Do LLMs perform the way people expect? (Vafa et al., 2024)

## Summary
Models how people decide where to use an LLM after seeing some of its answers, across 79 MMLU and BIG-Bench tasks. Indirect: it doesn't measure experience, but shows higher benchmark accuracy can mean worse results where people choose to use the model.

## Relevant findings
- **When mistakes are costly, GPT-4 does worst on the questions people would choose to use it for.**

> [!quote]- Source: Vafa et al. 2024, p. 8
> "As the relative weight on incorrect LLM responses increases, GPT-4’s performance under human deployment deteriorates; it has the worst generalized accuracy for the highest-stakes setting."
>
> [[sources/vafa-2024-large-language-models-perform-way.pdf]] · https://arxiv.org/abs/2406.01382

## Connection to our investigations
One possible reason [[ai-output-quality]] doesn't predict task success in [[output-vs-interaction-quality-crossword]]: people may over-trust better models.
