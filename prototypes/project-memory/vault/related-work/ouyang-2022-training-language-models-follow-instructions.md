---
added_by: claude
date: 2026-10-14
source: "[[sources/ouyang-2022-training-language-models-follow-instructions.pdf]]"
---

# InstructGPT (Ouyang et al., 2022)

## Summary
Trains GPT-3 with human feedback (RLHF) and compares labeler preferences with public benchmark scores. Don't correlate: preference rose while some benchmark scores fell. Preferences are labeler ratings of outputs on real user prompts, not users' experience in use.

## Relevant findings
- **Labelers preferred a 1.3B InstructGPT over the 100x larger GPT-3; 175B InstructGPT won 85% of the time.**

> [!quote]- Source: Ouyang et al. 2022, p. 3
> "Outputs from our 175B InstructGPT are preferred to 175B GPT-3 outputs 85 ± 3% of the time, and preferred 71 ± 4% of the time to few-shot 175B GPT-3."
>
> [[sources/ouyang-2022-training-language-models-follow-instructions.pdf]] · https://arxiv.org/abs/2203.02155

- **RLHF made outputs more preferred but lowered scores on some public benchmarks (the "alignment tax").**

> [!quote]- Source: Ouyang et al. 2022, p. 3
> "During RLHF fine-tuning, we observe performance regressions compared to GPT-3 on certain public NLP datasets, notably SQuAD (Rajpurkar et al., 2018), DROP (Dua et al., 2019), HellaSwag (Zellers et al., 2019), and WMT 2015 French to English translation (Bojar et al., 2015)."
>
> [[sources/ouyang-2022-training-language-models-follow-instructions.pdf]] · https://arxiv.org/abs/2203.02155

- **Models tuned on public NLP tasks (FLAN, T0) were much less preferred on real user prompts.**

> [!quote]- Source: Ouyang et al. 2022, p. 4
> "On our API prompt distribution, our FLAN and T0 models perform slightly worse than our SFT baseline, and labelers significantly prefer InstructGPT to these models (InstructGPT has a 73.4 ±2% winrate vs. our baseline, compared to 26.8 ±2% and 29.8 ±2% for our version of T0 and FLAN, respectively)."
>
> [[sources/ouyang-2022-training-language-models-follow-instructions.pdf]] · https://arxiv.org/abs/2203.02155

## Connection to our investigations
`text-davinci` in [[output-vs-interaction-quality-crossword]] is an instruction-tuned model of this kind; it beats base `davinci` on every measure there too.
