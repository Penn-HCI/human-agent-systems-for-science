---
added_by: claude
date: 2026-10-14
source: "[[sources/ji-2022-achieving-reliable-human-assessment-open.pdf]]"
---

# Reliable human assessment of open-domain dialogue (Ji et al., 2022)

## Summary
Crowd workers chat live with five dialogue models and rate the conversations. Automatic metrics mostly don't correlate with these ratings.

## Relevant findings
- **Word-overlap metrics correlate negatively with live human ratings of the models (e.g., BLEU-4 r = −0.88, ROUGE-L r = −0.80).**

> [!quote]- Source: Ji et al. 2022, p. 9
> "unfortunately no word-overlap metric achieves a strong positive correlation with human assessment"
>
> [[sources/ji-2022-achieving-reliable-human-assessment-open.pdf]]

- **Reference-free metrics do somewhat better but are inconsistent. FED tracks repetitiveness (r = 0.84) but not most other criteria.**

> [!quote]- Source: Ji et al. 2022, p. 9
> "FED has the ability of distinguishing “repetitive” models, but for other criteria, it correlates weakly or even negatively with human."
>
> [[sources/ji-2022-achieving-reliable-human-assessment-open.pdf]]

## Connection to our investigations
Like [[output-vs-interaction-quality-crossword]], it compares [[ai-output-quality]] measures with ratings from the people who interacted. Note the correlations are over only five models.
