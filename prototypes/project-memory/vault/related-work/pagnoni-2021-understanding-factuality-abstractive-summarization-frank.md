---
added_by: claude
date: 2026-10-14
source: "[[sources/pagnoni-2021-understanding-factuality-abstractive-summarization-frank.pdf]]"
---

# FRANK: factuality in summarization (Pagnoni et al., 2021)

## Summary
A benchmark of human factuality ratings for model summaries, used to test automatic factuality metrics. Indirect (static human ratings, not experience), but metrics correlate poorly with them, and pooled correlations are inflated by differences between systems.

## Relevant findings
- **All automatic metrics correlate weakly with human factuality ratings; the best is r = 0.20 (Pearson), 0.30 (Spearman).**

> [!quote]- Source: Pagnoni et al. 2021, p. 7
> "From Table 2 we observe that all metrics exhibit low correlations with human judgements of factuality. The best metric overall is FactCC with 0.20 Pearson and 0.30 Spearman correlation."
>
> [[sources/pagnoni-2021-understanding-factuality-abstractive-summarization-frank.pdf]]

- **Correlations pooled across systems look higher than within each system, because system and dataset confound them.**

> [!quote]- Source: Pagnoni et al. 2021, p. 6
> "For both metrics, we notice that the slope (an unscaled measure of correlation) of the line fitted through the entire data (red line) is significantly larger. In FEQA, the dotted lines (fitted on subsets of the data of each model and dataset) are almost horizontal. This likely indicates the presence of a confounding variable associated with the properties of each system and dataset. This can lead to false measures of high correlation if not accounted for."
>
> [[sources/pagnoni-2021-understanding-factuality-abstractive-summarization-frank.pdf]]

## Connection to our investigations
Matches [[output-vs-interaction-quality-crossword]], where the link between [[ai-output-quality]] and [[interaction-quality]] comes mostly from differences between models.
