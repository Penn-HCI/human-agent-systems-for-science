---
added_by: claude
date: 2026-10-14
source: "[[sources/akoury-2020-storium-dataset-evaluation-platform-machine.pdf]]"
---

# STORIUM (Akoury et al., 2020)

## Summary
A story-writing platform where real writers edit model suggestions; a metric over their edits (USER) is compared with their ratings. Mixed: edit-based use correlates moderately with user ratings, but an automatic win (nucleus sampling) didn't carry over to users.

## Relevant findings
- **How much generated text writers keep correlates with their ratings, mostly relevance (r = 0.51 for top-k) and barely fluency (r = 0.13, n.s.).**

> [!quote]- Source: Akoury et al. 2020, p. 8
> "Fluency correlates only weakly with USER, which makes sense as most generated entries are fluent due to GPT-2's pretraining."
>
> [[sources/akoury-2020-storium-dataset-evaluation-platform-machine.pdf]]

- **Nucleus sampling beats top-k on automatic measures, but real users preferred top-k on every rating.**

> [!quote]- Source: Akoury et al. 2020, p. 7
> "Interestingly, while Holtzman et al. (2020) show that nucleus sampling improves over top-k sampling on measures like repetition, STORIUM users clearly prefer the top-k variant across all categories (last column of Table 5)."
>
> [[sources/akoury-2020-storium-dataset-evaluation-platform-machine.pdf]]

- **Offline crowd ratings of the same outputs were unreliable, with very low agreement.**

> [!quote]- Source: Akoury et al. 2020, p. 8
> "Table 6 (top) shows that workers have very low agreement (Fleiss' κ) for all properties, including even fluency."
>
> [[sources/akoury-2020-storium-dataset-evaluation-platform-machine.pdf]]

## Connection to our investigations
A counterpart to [[output-vs-interaction-quality-crossword]] for writing: here relevance, not fluency, predicted which [[ai-output-quality]] carried into use.
