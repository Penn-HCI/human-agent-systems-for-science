---
added_by: claude
date: 2026-10-14
source: "[[sources/liu-2023-g-eval-nlg-evaluation-gpt.pdf]]"
---

# G-Eval (Liu et al., 2023)

## Summary
Uses GPT-4 as a judge of generated text. Answer: indirect. It compares the judge only with static human ratings of outputs, and the agreement is moderate. It doesn't measure user experience.

## Relevant findings
- **A GPT-4 judge agrees only moderately with human ratings of summaries (Spearman 0.514), though that beats earlier automatic metrics.**

> [!quote]- Source: Liu et al. 2023, p. 1
> "We show that G-Eval with GPT-4 as the backbone model achieves a Spearman correlation of 0.514 with human on summarization task, outperforming all previous methods by a large margin."
>
> [[sources/liu-2023-g-eval-nlg-evaluation-gpt.pdf]] · https://arxiv.org/abs/2303.16634

## Connection to our investigations
This is the output-level agreement that [[output-vs-interaction-quality-crossword]] goes beyond. Even here, the link between automatic and human [[ai-output-quality]] ratings is moderate.
