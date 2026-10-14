---
added_by: claude
date: 2026-10-14
source: "[[sources/dibia-2022-aligning-offline-metrics-human-judgments.pdf]]"
---

# Offline metrics vs. judged value of code (Dibia et al., 2022)

## Summary
49 programmers rated how valuable code generations would be, compared with offline metrics (unit tests, edit similarity, BLEU). Answer: mixed — metrics correlate moderately (r ≤ 0.66), and miss much code people value. Ratings are of static outputs, not use.

## Relevant findings
- **Passing unit tests correlates best with perceived value (r = 0.62); BLEU is weakest (r = 0.36).**

> [!quote]- Source: Dibia et al. 2022, p. 6
> "PASS is also the most strongly correlated metric to both EFFORT and VALUE (r = 0.62; p < 0.001, and r = 0.62; p < 0.001 respectively). [...] With a correlation of r = 0.36; p < 0.001, BLEU under-performs all other metrics."
>
> [[sources/dibia-2022-aligning-offline-metrics-human-judgments.pdf]] · https://arxiv.org/abs/2210.16494

- **42% of code that fails unit tests is still rated at least somewhat useful.**

> [!quote]- Source: Dibia et al. 2022, p. 6
> "When functions fail unit tests, they are somewhat more likely to have lower VALUE scores, but 90 generations (42%) are still considered “somewhat useful” by participants. The metric misses many high-value generations."
>
> [[sources/dibia-2022-aligning-offline-metrics-human-judgments.pdf]] · https://arxiv.org/abs/2210.16494

- **Value tracks the effort to fix the code (r = 0.94) more than its correctness (r = 0.87).**

> [!quote]- Source: Dibia et al. 2022, p. 5
> "the VALUE of a generation is nearly perfectly correlated with the perceived EFFORT needed to correct a generation (Pearson r = 0.94; 95%-confidence interval [0.92 − 0.95])."
>
> [[sources/dibia-2022-aligning-offline-metrics-human-judgments.pdf]] · https://arxiv.org/abs/2210.16494

## Connection to our investigations
Echoes [[output-vs-interaction-quality-crossword]]: correctness-style [[ai-output-quality]] relates only moderately to how useful people find the AI.
