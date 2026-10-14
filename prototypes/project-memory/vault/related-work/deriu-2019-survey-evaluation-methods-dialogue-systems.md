---
added_by: claude
date: 2026-10-14
source: "[[sources/deriu-2019-survey-evaluation-methods-dialogue-systems.pdf]]"
---

# Dialogue evaluation survey (Deriu et al., 2019)

## Summary
A survey of dialogue system evaluation. Mixed: task success and expert ratings predict user satisfaction moderately, while word-overlap metrics don't track human judgments.

## Relevant findings
- **In PARADISE, task success and dialogue costs explain about half of user satisfaction (R² = 0.50), but the model fails to transfer from novice to expert users (R² = 0.04).**

> [!quote]- Source: Deriu et al. 2019, p. 18
> "The results show that the model is able to explain R2 = 50% of the variance, which is considered to be a good predictor by the authors."
>
> [[sources/deriu-2019-survey-evaluation-methods-dialogue-systems.pdf]] · https://arxiv.org/abs/1905.04071

- **Expert ratings of dialogues correlate with users' own ratings (ρ = 0.66).**

> [!quote]- Source: Deriu et al. 2019, p. 16
> "Their results showed that the user ratings and the expert ratings are highly correlated with a Spearman's ρ score of ρ = 0.66(p < 0.01)."
>
> [[sources/deriu-2019-survey-evaluation-methods-dialogue-systems.pdf]] · https://arxiv.org/abs/1905.04071

- **Word-overlap metrics like BLEU don't correlate with human judgments of responses.**

> [!quote]- Source: Deriu et al. 2019, p. 29
> "However, Liu et al. (2016) showed that neither of the word-overlap based scores have any correlation to human judgments."
>
> [[sources/deriu-2019-survey-evaluation-methods-dialogue-systems.pdf]] · https://arxiv.org/abs/1905.04071

## Connection to our investigations
Its "Interaction Quality" measure is an expert proxy for [[interaction-quality]]. The PARADISE result is a reference point for how much task outcomes explain satisfaction in [[output-vs-interaction-quality-crossword]].
