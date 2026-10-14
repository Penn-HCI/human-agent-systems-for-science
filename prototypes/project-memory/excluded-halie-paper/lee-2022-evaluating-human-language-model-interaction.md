---
added_by: claude
date: 2026-10-14
source: "[[sources/lee-2022-evaluating-human-language-model-interaction.pdf]]"
---

# Evaluating human-LM interaction / HALIE (Lee et al., 2022)

## Summary
The HALIE paper: 1015 interaction traces across five tasks with four LMs. Its answer is "not always": better non-interactive performance often but not always gives better interaction.

## Relevant findings
- **In QA, the model with the worst zero-shot accuracy can be the best interactive assistant.**

> [!quote]- Source: Lee et al. 2022, p. 8
> "we observe that the worst-performing model in non-interactive settings can perform as well as or better than other models in interactive settings. Specifically, TextBabbage had the worst accuracy as a zero-shot QA system, but achieved the best performance as an interactive LM assistant for the Nutrition category (Figure 5)."
>
> [[sources/lee-2022-evaluating-human-language-model-interaction.pdf]] · https://arxiv.org/abs/2212.09746

- **In crosswords, users found TextDavinci most helpful, but it improved accuracy on only one of five puzzles.**

> [!quote]- Source: Lee et al. 2022, p. 8
> "users significantly preferred TextDavinci over other models (Figure 8). However, assistance from TextDavinci led to statistically significantly higher crossword letter accuracy only for one of the five crossword puzzles"
>
> [[sources/lee-2022-evaluating-human-language-model-interaction.pdf]] · https://arxiv.org/abs/2212.09746

- **In metaphor writing, the model users found most satisfying produced the outputs third-party raters liked least.**

> [!quote]- Source: Lee et al. 2022, p. 27
> "users found TextDavinci to be most helpful and satisfactory according to the survey responses (Table 9). However, third-party evaluators considered sentences written with the same model to be the worst among the four models (Table 10)."
>
> [[sources/lee-2022-evaluating-human-language-model-interaction.pdf]] · https://arxiv.org/abs/2212.09746

## Connection to our investigations
Source of the crossword data in [[output-vs-interaction-quality-crossword]]. Its crossword finding matches ours: perceived helpfulness doesn't predict task success.
