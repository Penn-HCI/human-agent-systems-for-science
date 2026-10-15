# Index

## Investigations
- [[output-vs-interaction-quality-crossword]] — Crossword: better AI output goes with a better experience (mostly between models), but not with task success.
- [[output-vs-interaction-quality-crossword-details]] — Methods, the full results table and caveats for the investigation above.
- [[output-vs-interaction-quality-other-tasks]] — Dialogue, QA, summarization, metaphor: independent quality scores rarely track experience; in QA, people followed the AI's answer, right or wrong.
- [[output-vs-interaction-quality-other-tasks-details]] — Measures on each side, LLM judges, checks and caveats for the investigation above.

## Concepts
- [[ai-output-quality]] — How good the AI's responses are: measured from the logs (gave the answer, degenerate) and perceived (fluency, helpfulness).
- [[interaction-quality]] — How the interaction went: ease, joy, number of queries and task success (grid accuracy).

## Datasets
- [[halie-crossword-raw]] — The raw HALIE crossword logs, puzzles and survey, and their quirks.
- [[halie-other-tasks]] — HALIE dialogue, QA, summarization and metaphor data, and their quirks.

## Related work
Grouped by how each paper answers: do output quality metrics correlate with the human experience?

### Don't correlate
- [[chi-2025-copilot-arena-platform-code-llm]] — Developers' in-editor preferences match Chatbot Arena (rs = 0.62) but not static benchmarks (rs ≤ 0.1).
- [[clark-2018-creative-writing-machine-loop-case]] — Writers' self-ratings barely track crowd ratings (r ≈ 0.04–0.13); AI slogan writers were more satisfied despite weaker outputs.
- [[ji-2022-achieving-reliable-human-assessment-open]] — Automatic metrics correlate poorly or negatively with live chat ratings (BLEU-4 r = −0.88, 5 systems).
- [[kelly-2009-methods-evaluating-interactive-information-retrieval]] — Systems that win offline tests don't always win with users; objective and self-reported performance correlate only slightly.
- [[liu-2016-evaluate-your-dialogue-system-empirical]] — BLEU and embedding metrics barely track human ratings of dialogue responses (static ratings).
- [[ouyang-2022-training-language-models-follow-instructions]] — Labeler preference rose while some benchmark scores fell (labelers rate outputs, not use).
- [[pagnoni-2021-understanding-factuality-abstractive-summarization-frank]] — Factuality metrics correlate weakly with static human ratings (best r = 0.20).

### Mixed
- [[akoury-2020-storium-dataset-evaluation-platform-machine]] — How much text writers keep tracks their ratings; users prefer the decoding that scores worse automatically.
- [[bai-2022-training-helpful-harmless-assistant-reinforcement]] — Offline preference-model scores overestimate crowdworkers' preference in chat.
- [[deriu-2019-survey-evaluation-methods-dialogue-systems]] — Task success explains about half of user satisfaction; BLEU doesn't track human judgments.
- [[deriu-2020-spot-bot-robust-efficient-framework]] — Automatic and single-turn scores miss multi-turn quality.
- [[dibia-2022-aligning-offline-metrics-human-judgments]] — Unit-test pass rate correlates moderately with perceived value (r = 0.62); 42% of failing code is still useful.
- [[li-2024-iqa-eval-automatic-evaluation-human]] — LLM judges match people only moderately on real interactions; uses HALIE QA data.
- [[mozannar-2024-realhumaneval-evaluating-large-language-models]] — Benchmarks predict productivity with diminishing returns; preferences track perceived helpfulness.
- [[smith-2022-human-evaluation-conversations-open-problem]] — Side-by-side response judgments and post-chat ratings can rank chatbots differently.

### Indirect
- [[clark-2021-choose-your-own-adventure-paired]] — Writers preferred GPT-2's suggestions despite a worse repetition metric.
- [[dang-2023-choice-over-control-users-write]] — Same model, different interface: one suggestion rated less helpful than three.
- [[dubois-2023-alpacafarm-simulation-framework-methods-that]] — LLM-judge rankings match crowd pairwise preferences (ρ = 0.98); interaction not tested.
- [[fabbri-2020-summeval-re-evaluating-summarization-evaluation]] — Summarization metrics match expert ratings weakly to moderately.
- [[gehrmann-2021-gem-benchmark-natural-language-generation]] — Cites work showing word-overlap metrics correlate weakly with human judgments.
- [[hashimoto-2019-unifying-human-statistical-evaluation-natural]] — Ratings of single outputs miss diversity.
- [[horvitz-1999-principles-mixed-initiative-user-interfaces]] — Wrong AI guesses can still help if users can easily refine them.
- [[ibrahim-2024-towards-interactive-evaluations-interaction-harms]] — Static tests miss harms that emerge over sustained interaction.
- [[ippolito-2022-creative-writing-ai-powered-writing]] — Pro writers find the qualities models are tuned for misaligned with their needs.
- [[jakesch-2023-co-writing-opinionated-language-models]] — Users rated a biased assistant knowledgeable even when it argued against them.
- [[kiela-2021-dynabench-rethinking-benchmarking-nlp]] — Models beat humans on benchmarks yet fail when people probe them live.
- [[kumar-2023-guiding-students-llms-supported-learning]] — Direct LLM answers raised scores slightly; refining students' own work built more trust.
- [[langevin-2021-heuristic-evaluation-conversational-agents]] — Good chatbot experience requires evaluating interaction, not just content.
- [[lee-2022-coauthor-designing-human-ai-collaborative]] — Writing more yourself goes with ownership (r = 0.3), not satisfaction (r ≈ 0).
- [[liang-2023-holistic-evaluation-language-models]] — HELM: static benchmark; leaves interactive evaluation to HALIE.
- [[liu-2023-g-eval-nlg-evaluation-gpt]] — GPT-4 judge moderately matches static human ratings (ρ = 0.514).
- [[ma-2025-sphere-evaluation-card-human-ai]] — Review: benchmarks and user preferences may not track users' task performance.
- [[shaikh-2025-navigating-rifts-human-llm-grounding]] — Strong instruction-following LLMs score below random on grounding in real conversations.
- [[stiennon-2020-learning-summarize-human-feedback]] — ROUGE's agreement with human preferences falls to chance on better models.
- [[vafa-2024-large-language-models-perform-way]] — Higher-benchmark GPT-4 does worst where people choose to use it.
- [[wang-2023-mint-evaluating-llms-multi-turn]] — Better single-turn scores don't predict multi-turn success (simulated users).
- [[wang-2024-task-supportive-personalized-human-large]] — Small study: satisfaction stayed high despite wrong outputs.
- [[williams-ceci-2026-biased-ai-writing-assistants-shift]] — Users rated biased suggestions as balanced, yet were swayed by them.
- [[xiao-2024-human-centered-evaluation-auditing-language]] — Benchmarks and output ratings unvalidated as predictors of real-world use.
- [[xu-2023-critical-evaluation-evaluations-long-form]] — No metric predicts long-form answer preferences well; length often beats them.
- [[ye-2023-flask-fine-grained-language-model]] — GPT-4 judge matches static human ratings fairly well (ρ = 0.68).
- [[zhou-2023-sotopia-interactive-evaluation-social-intelligence]] — GPT-4 judge tracks human raters on goal completion only.

## Transcripts
- [[2026-10-14-output-vs-interaction-quality-crossword]] — The first crossword analysis session.
- [[2026-10-14-ai-output-quality-measures]] — Checking which measures capture AI output quality.
