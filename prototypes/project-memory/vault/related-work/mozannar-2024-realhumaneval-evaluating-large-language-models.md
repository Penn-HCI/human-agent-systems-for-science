---
added_by: claude
date: 2026-10-14
source: "[[sources/mozannar-2024-realhumaneval-evaluating-large-language-models.pdf]]"
---

# RealHumanEval (Mozannar et al., 2024)

## Summary
A coding study (N = 243) with seven LLMs. Mixed: benchmark gains bring productivity gains, but with diminishing returns, and preference measures track perceived helpfulness rather than productivity.

## Relevant findings
- **Benchmark gains help productivity, but not proportionally.** A 19% HumanEval gain made people 22.8% faster, but an 85% gain made them only 8.3% faster.

> [!quote]- Source: Mozannar et al. 2024, p. 10
> "CodeLlama-34b (chat) is 19% better over CodeLlama-7b (chat) models on HumanEval, and participants are 22.8% (95% CI [2.8, 38.7]) faster on average to complete a task with 34b vs 7b. Yet, GPT-3.5 (chat) model outperforms CodeLlama-34b (chat) by 85% on HumanEval, and yet participants equipped with GPT-3.5 (chat) models are only 8.3% (95% CI [-11.2, 24.6]) faster than those with CodeLlama-34b (chat)."
>
> [[sources/mozannar-2024-realhumaneval-evaluating-large-language-models.pdf]] · https://arxiv.org/abs/2404.02806

- **Acceptance and copy rates track perceived helpfulness, not actual performance.**

> [!quote]- Source: Mozannar et al. 2024, p. 3
> "we find that they are only correlated with programmer perceptions of LLM helpfulness but not necessarily with actual programmer performance."
>
> [[sources/mozannar-2024-realhumaneval-evaluating-large-language-models.pdf]] · https://arxiv.org/abs/2404.02806

- **A model that does better on benchmarks was rated less helpful.** CodeLlama-34b got 3.3/10, below CodeLlama-7b at 4.19.

> [!quote]- Source: Mozannar et al. 2024, p. 11
> "Again, we observe that CodeLlama-34b models tend to be rated as less helpful (3.3 out of 10), than the other two models (4.19 and 5.09 out of 10 for CodeLlama-7b and GPT-3.5)."
>
> [[sources/mozannar-2024-realhumaneval-evaluating-large-language-models.pdf]] · https://arxiv.org/abs/2404.02806

## Connection to our investigations
Parallels [[output-vs-interaction-quality-crossword]]: [[ai-output-quality]] and perceived helpfulness go together, but perceptions don't predict task success.
