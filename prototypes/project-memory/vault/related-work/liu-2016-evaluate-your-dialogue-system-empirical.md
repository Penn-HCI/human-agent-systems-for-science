---
added_by: claude
date: 2026-10-14
source: "[[sources/liu-2016-evaluate-your-dialogue-system-empirical.pdf]]"
---

# How NOT to evaluate your dialogue system (Liu et al., 2016)

## Summary
Compares automatic metrics (BLEU, METEOR, ROUGE, embedding metrics) with human ratings of dialogue responses. Answer: they don't correlate — weakly on Twitter, not at all on Ubuntu. Ratings are of static responses, not use.

## Relevant findings
- **Word-overlap and embedding metrics correlate weakly or not at all with human ratings (best: BLEU-2, Spearman 0.36 on Twitter; vs. 0.95 between two halves of raters).**

> [!quote]- Source: Liu et al. 2016, p. 1
> "We show that these metrics correlate very weakly with human judgements in the non-technical Twitter domain, and not at all in the technical Ubuntu domain."
>
> [[sources/liu-2016-evaluate-your-dialogue-system-empirical.pdf]]

> [!quote]- Source: Liu et al. 2016, p. 8
> "These plots show how weak the correlation is: in both cases, they appear to be random noise."
>
> [[sources/liu-2016-evaluate-your-dialogue-system-empirical.pdf]]

## Connection to our investigations
An early case where automatic [[ai-output-quality]] doesn't match human judgment; our [[output-vs-interaction-quality-crossword]] asks the same about interaction.
