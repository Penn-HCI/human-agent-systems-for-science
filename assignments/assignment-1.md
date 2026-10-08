# Assignment 1 - Programming Your Scientific Twin

In this first assignment, you will make a basic scientific discovery agent. It will be capable of performing simple scientific analyses. You will try to program it so that it can produce results at a level that you would be comfortable submitting as your own.

While in theory this is something that Claude Code could do for you, and cheaply, it's advantageous for you to build your own here. In part, you get the most control over the constituent parts. Want to require the bot uses only AI APIs with zero data retention policies out of respect for your data? You can do that. Want to set a hard, firmly-enforced limit of the number of steps of analysis allowed? You can do that too. In your later projects, it will be useful to know how to wield these various kinds of control as you try to make systems that are better fit for your own research contexts.

You are expected to use Claude Code as part of this project to support your development. I estimate the basics will take students about 2h with Claude Code, even less if you're very familiar with it, and up 5-10h if you're using it for the first time.

A few constraints up front to guide your work:
* You will be asked to run this on study data of your own. Please do _not_ use protected data without first getting clearance.
* Our course provides a limited budget for AI access. It's been designed to be just enough to get through the basics of this assignment. But be careful not to blow through it. One of the first tasks I would recommend is using an agent to make a widget to keep track of how much cost you have used so that you can keep track of how close you are getting to your limits. I have a widget in my menu bar that tells me just this. If you blow through your course credits, you will need to pay for the additional credits to finish the assignment.
* Additionally, prompt your AI in a way that makes it clear from the start that you need to be conservative in your budget. Ask for switches that limit the budget of a particular run of your agent. In OpenRouter, add a budget limit to prevent you from burning too much in one run.

# Goal

Your bot should be able to take in a dataset, come up with interesting research questions, and produce a report about what it found. The report should be kind of like this (exact format does not matter):

```md
I analysed the 800 summary-editing interactions in this dataset, plus the 80 post-session surveys. Three findings stand out. Users' edits make summaries more relevant and more factually consistent, but users rate their own edited summaries as consistent far more often than independent raters do. Users spot factual errors fairly well but can't detect coherence problems. And the model that is most faithful to the source is not the one users find most helpful.

...

## Q1. Do edits really improve summaries, and do users overrate their own edits?
**Answer:** Yes on both counts. By the independent raters' measure, edits make summaries clearly more relevant and somewhat more consistent, with no change in coherence. But users rate their own edits as consistent far more often than the raters do.

Evidence from `q1_edits_vs_third_party.py`, comparing the same 390 summaries before and after editing:

| Measure | Original | Edited | Improved / worse | Test result |
|---|---|---|---|---|
| Consistency | 0.662 | 0.795 | 32% / 14% | p = 5e-11 |
| Relevance | 3.93 | 4.37 | 57% / 19% | p = 4e-22 |
| Coherence | 4.58 | 4.58 | — | p = 0.84 |

- **Gains go where users saw problems.** Where users had flagged the original as inconsistent, independent consistency rose from 0.46 to 0.80. Where users had called it consistent, editing left it unchanged (0.797 to 0.795).
- **Overconfidence:** users called 99.0% of their edited summaries consistent. All three raters agreed on only 61%, and a majority agreed on 83%.
- **More editing, more relevance:** relevance gains grow with edit distance (correlation 0.31, p = 3e-10). Consistency gains don't (0.10, p = 0.06).

**Caveats:**
- Independent ratings exist for only about half the rows.
- Each consistency score averages just 3 raters.
- Unedited summaries have identical before and after ratings, which suggests each unique text was rated once.
- 14% of edits made consistency worse, so editing can introduce errors.
```

And the analysis should be based on real analysis done in well-documented code files, e.g.:
```python
# Did edits fix the summaries the user themself flagged as inconsistent?
for flag, g in tp.groupby('original_consistency'):
    print(f'user flagged original consistent={flag}: n={len(g)}, TP cons orig={g.original_consistency_third_party.mean():.3f} '
          f'-> edited={g.edited_consistency_third_party.mean():.3f}, Wilcoxon p={stats.wilcoxon(g.edited_consistency_third_party, g.original_consistency_third_party).pvalue:.2g}')
```

Your bot should behave iteratively like a human analyst. It should read over the data files, come up with hypotheses, run exploratory analyses, and eventually answer research questions with appropriate analytic tests.

You will ultimately submit the GitHub code for your bot and files that it produced as part of its analysis.

# Ground rules

To help you think about architecting these tools, your bot must minimally do the following:

* it must have a switch that routes it to use solely **"zero data retention" models** (see [OpenRouter's page on ZDR](https://openrouter.ai/docs/guides/features/zdr)). These are more appropriate to call for more sensitive data. You don't need to call your agent with these if it's not processing sensitive data, but I want you to know how to put in the switch.
* it must do its exploration in **multiple steps**. No calling external agents to do the work, and no calling LLMs one-shot. This might work, but I want you to at least once build something where you can see and control how reasoning evolves over steps.
* it must be invocable from the **command line** so that we can run it.
* it must take the following as command line parameters:
  * a **data directory** containing all input data
  * an (optional) set of **research questions** that will be explored
* it must be able to create and run **code scripts** as part of its analysis (e.g., make Python stats scripts and run them)
* it must run code scripts in a **sandbox**. That means that your scripts will not be allowed to access files outside of a very limited set that you give it access to. This is a basic security feature and a good one to know for later projects.

Most of these should be relatively straightforward to implement with the help of a coding agent. _But_ I recommend you don't just accept what the agent suggests, but instead look over the code for the various pieces as it's generated. When in doubt, check your code out! You'll get a better sense for how these tools can be architected. _And_ you'll develop faith that you aren't accidentally going to leak a bunch of your personal files through an erratic agent call.

# Test setup

By the end of the assignment, you will ideally be running this bot on _your own_ scientific data. But we ask you to start out by running it on [this example data directory](assets/assignment1-summarization.zip).

## A bit about the example data

This data comes from the 2022 HALIE (Human-AI Language-based Interaction Evaluation) project from Stanford. It is a nice example set because it has a permissive distribution license, is de-identified, and contains multiple kinds of data---quantative, ordinal, qualitative, all about the same kind of thing. Pretty neat test set to work with, in that your bot can try to synthesize across all of these kinds of data!

For a bit more context about this data, we've given you the subset of this data that relates to a task where human participants are asked to rate and edit text summaries generated by a variety of different AIs. The original question asked by the authors was: "Are the models that produce the best outputs also those that lead to the best interaction experience?" Their exploration of that question can be found in Section 3.5 of [their paper](https://arxiv.org/pdf/2212.09746#page=21.70). You should program your agent to first answer that research question, and then come up with other research questions.

# Your task

The challenge is to develop a scientific twin that you would actually use to run and report analyses that you would fully stand behind, including the analytic choices, coding conventions, and wording of the report.

You will build this agent in layers of increasing sophistication. Implementng the basic levels of capability will get you to a full-credit 100 points. Though implementing more advanced capabilities will get you extra credit. There is no limit to the amount of extra credit you can claim.

* **Basics** (40 pts.) Build an agent that takes in the example dataset and a research question and produces findings in an `answer.md` file. It must adhere to all of the ["Ground Rules"](#ground-rules).

* **Run on your data** (20 pts.) Then, run your agent on a dataset you have previously analyzed in research. If you do not have a dataset that is suitable to use (identifiable/risky human subjects data/too big, etc.), find someone else in the class who has a dataset you can use. Share with us the command that you ran and the answer.md.

* **Clean outputs** (10 pts.) Update your agent design until it produces an answer.md that reflects stylistically how you report your results and test scripts that are clean enough that you would submit them in a replication package.

* **Exploration** (30 pts.) Let your agent figure out what is interesting to explore! Take away the constraint that it needs research questions as input, and instead have them come up with them based on exploring the data.

* **"Interactive" mode** (extra credit (EC) 5 pts.) This is a class about *human*-agent systems for science. Let's start to get the human in the loop. Program your agent so that it pauses to ask the human a question when it would help analysis. For instance, when it is uncertain about what a data field means, how the data was collected, what research questions to focus on, or what kinds of tests will be accepted.

* **Rubrics** (EC 5 pts.) Have your bot try to improve the quality of its work by having it create rubrics for outputs and evaluate its outputs against them, revising them if they are not good enough. Consider the guidance from or even [the tool](https://autorubric.org/docs/) published in the [Autorubric paper](https://arxiv.org/abs/2603.00077).

* **Falsify prior results** (EC 5 pts.) Did your agent happen falsify or complexify some of the published results on the dataset that you provided? If so, we'll give you an extra 5 points for deepening human knowledge through the construction of your bot.

# Submission

Fill out the submission form here. Be ready to provide a _public_ link to your GitHub repository (does not need to include your custom data if it is protected), answer files representing your bots' capabilities on the provided dataset and your own dataset, and to answer questions about any additional features you implemented or results you achieved.

<!-- # Debt

Need to figure out how sandboxing works on Mac.

Tips for students who are using Claude Code for the first time:
* I suggest beginning on a setting where you are accepting every suggestion (I still do this). Can ask for explanations of what is being done at each step.
* Somewhere, provide the guidance to "develop at your own risk". If you feel so in over your head that you think you might make a mistake, message me, we can get you additional days. I'm not assuming liability for what you do on your computer. But we do need to exercise the current tools to push ourselves to an interesting boundary.
* Additional tip --- use models like DeepSeek to lower the cost.

* In later assignments---connect in this discovery agent. Allow it to read from one's knowledge graph. Allow it to look at example files from the past.
* Add provenance into a later assignment
* Maybe the explainable report in the later assignment can also include visuals, and excerpts from related passages about the suitability of particular techniques? And a description of how widely a technique is used in related work? Maybe we could also have some way of testing the readability of those reports?
* Experimentation bots are just too darn expensive... is there some way I can get us to build them anyway?
* Check on quality of AutoRubric tool
* Create a submission form for the project. We'll connect this to Supabase and do backups. We'll strive to keep the code in the submission form as simple as humanly possible. -->