---
added_by: claude
date: 2026-10-14
source: "[[sources/ye-2023-flask-fine-grained-language-model.pdf]]"
---

# FLASK (Ye et al., 2023)

## Summary
A fine-grained, skill-based scoring rubric for LLM outputs, used by humans and LLM judges. Indirect: it compares LLM-judge scores with offline human ratings of outputs, not with experience.

## Relevant findings
- **A GPT-4 judge agrees fairly well with human raters (ρ = 0.68), and ROUGE-L agrees worst (ρ = 0.33).**

> [!quote]- Source: Ye et al. 2023, p. 6
> "We first observe that using an automatic metric (ROUGE-L) results in the lowest correlation."
>
> [[sources/ye-2023-flask-fine-grained-language-model.pdf]] · https://arxiv.org/abs/2307.10928

## Connection to our investigations
Background on how far LLM-judge [[ai-output-quality]] scores can stand in for human ratings of outputs.
