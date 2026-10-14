---
added_by: claude
date: 2026-10-14
source: "[[sources/liang-2023-holistic-evaluation-language-models.pdf]]"
---

# Holistic Evaluation of Language Models (Liang et al., 2023)

## Summary
HELM benchmarks 30 language models across many scenarios and metrics. Indirect: it leaves interactive use to companion work (Lee et al., the HALIE paper), and only notes that ROUGE ranks models sensibly while underrating summaries.

## Relevant findings
- **ROUGE scores look much worse than the summaries read, but still rank models roughly right.**

> [!quote]- Source: Liang et al. 2023, p. 63
> "we begin by observing that the ROUGE scores tend to be much lower than our qualitative judgments of summary quality, consistent with Goyal et al. (2022). With that said, broadly, we did find that the ROUGE-2 scores did correlate with more accurate models across-the-board"
>
> [[sources/liang-2023-holistic-evaluation-language-models.pdf]] · https://arxiv.org/abs/2211.09110

- **HELM doesn't evaluate interaction; that is left to Lee et al.**

> [!quote]- Source: Liang et al. 2023, p. 19
> "We also do not study interactive tasks such as dialogue, which will be discuss in forthcoming companion work associated with this effort (Lee et al., Forthcoming)."
>
> [[sources/liang-2023-holistic-evaluation-language-models.pdf]] · https://arxiv.org/abs/2211.09110

## Connection to our investigations
HELM is the static [[ai-output-quality]] side; the HALIE data behind [[output-vs-interaction-quality-crossword]] is the interactive companion.
