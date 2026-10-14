---
added_by: claude
date: 2026-10-14
source: "[[sources/bai-2022-training-helpful-harmless-assistant-reinforcement.pdf]]"
---

# Training a helpful and harmless assistant with RLHF (Bai et al., 2022)

## Summary
Anthropic trains a chat assistant from human preferences, scored by crowdworkers choosing between responses while chatting with the models. Mixed: offline preference-model scores overestimate gains in people's in-conversation preferences, and benchmark scores move with those preferences only for large models.

## Relevant findings
- **Offline preference-model scores overstate how much crowdworkers prefer the model when chatting with it.** Much of the gap comes from the shift between held-out prompts and real conversations.

> [!quote]- Source: Bai et al. 2022, p. 21
> "We see that models improve significantly during RLHF, but Elo scores from crowdworkers do not match predictions from PMs."
>
> [[sources/bai-2022-training-helpful-harmless-assistant-reinforcement.pdf]] · https://arxiv.org/abs/2204.05862

> [!quote]- Source: Bai et al. 2022, p. 46
> "We notice that the naive PM predictions significantly overestimate the empirical Elos."
>
> "the distributional shift between the held-out prompts and the actual crowdworker conversations was very significant, and explains a significant proportion of the discrepancy between RLHF learning curves and the Elo scores as measured from crowdworkers."
>
> [[sources/bai-2022-training-helpful-harmless-assistant-reinforcement.pdf]] · https://arxiv.org/abs/2204.05862

- **Training for human preference raises benchmark scores for large models but lowers them for small ones.** So benchmarks and preference can move in opposite directions.

> [!quote]- Source: Bai et al. 2022, p. 6
> "Smaller models experience severe ‘alignment taxes’ – their performance on a wide variety of evaluations declines after RLHF training. However, we find a variety of alignment bonuses, with our 13B and 52B⁵ RLHF-trained models performing better at zero-shot NLP evaluations, and the same at few-shot evaluations."
>
> [[sources/bai-2022-training-helpful-harmless-assistant-reinforcement.pdf]] · https://arxiv.org/abs/2204.05862

## Connection to our investigations
Like [[output-vs-interaction-quality-crossword]], an offline score of [[ai-output-quality]] tracks [[interaction-quality]] only partly.
