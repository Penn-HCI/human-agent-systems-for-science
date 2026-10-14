---
added_by: claude
date: 2026-10-14
source: "[[sources/xu-2023-critical-evaluation-evaluations-long-form.pdf]]"
---

# Evaluating long-form QA evaluations (Xu et al., 2023)

## Summary
Tests 12 automatic metrics against expert and crowd preferences between long-form answers. It doesn't test interactive experience (indirect); no metric predicts static human preferences well.

## Relevant findings
- **No metric reliably predicts which answer people prefer; most are 0.5–0.6 accurate vs. 0.73–0.80 human agreement, and "pick the longer answer" often does as well or better.**

> [!quote]- Source: Xu et al. 2023, p. 1
> "None of these metrics reliably matches human judgments of overall answer quality."
>
> [[sources/xu-2023-critical-evaluation-evaluations-long-form.pdf]]

## Connection to our investigations
Only touches the [[ai-output-quality]] side of [[output-vs-interaction-quality-crossword]]: automatic metrics don't match even static human preferences.
