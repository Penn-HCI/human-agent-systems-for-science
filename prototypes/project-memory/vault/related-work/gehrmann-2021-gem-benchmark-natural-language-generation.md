---
added_by: claude
date: 2026-10-14
source: "[[sources/gehrmann-2021-gem-benchmark-natural-language-generation.pdf]]"
---

# GEM benchmark (Gehrmann et al., 2021)

## Summary
A benchmark for text generation and its metrics. It doesn't test the question directly; it only notes, citing others, that word-overlap metrics agree poorly with human ratings of outputs.

## Relevant findings
- **Word-overlap metrics like ROUGE and BLEU correlate weakly with human judgments.**

> [!quote]- Source: Gehrmann et al. 2021, p. 4
> "While multiple references alleviate the issue somewhat, these metrics still have a low correlation with human judgments (Reiter, 2018; Fabbri et al., 2020)."
>
> [[sources/gehrmann-2021-gem-benchmark-natural-language-generation.pdf]]

## Connection to our investigations
Background only: these human judgments are offline ratings of outputs, not [[interaction-quality]].
