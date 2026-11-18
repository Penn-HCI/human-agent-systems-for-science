In the future, maybe some scientific discoveries will come from agents that run entirely autonomously. After all, agents seem to be getting much better at autonomous scientific work.

But if they do — what are people going to _do_ with an agent-generated finding?

Well, some findings can be "used" without looking at them very closely. For instance, if an agent can discover a theorem and prove it with Lean, then it can add it to a repository of theorems that can be used in future proofs. Maybe it needs to be cleaned up and optimized, but it is more or less ready to be useful as is.

Other findings, while not self-verifying, will be easy enough to check. Maybe the agent finds a factoid from an old book, and shows you the clipping --- great, you can use this insight. Or it does some stats on dataset it finds, and the stats code is straightforward, and the dataset is good.

And yet other findings it might not be that important to understand if they're accurate --- later you'll see the "proof in the pudding" if you take the finding as a given and then can run cheap experiments to help you test it. For instance, I imagine that if an agent proposes a new drug, it might be cheap enough to synthesize and test is low-fi lab experiments to assess its promise.

But --- I think for a significant amount of these discoveries, we will care if they are accurate and they won't be particularly be easy to verify. I equate this with the experience of read a paper abstract and saying "These claims look cool!" only to get partly in to the paper and say "Oh... this isn't very good." The finding is technically correct but is so underpowered once you take into account all of the context of how the research was run.

If the devil is in the details then there's no substitute for showing the details. But there are so many details! If you were compare the agent output to that you would see from a human collaborator, agents produce weeks' worth of human output in terms of the sources they've read and the experiments they have run. It's not going to be easy to get into the details.

In this assignment, we'll explore how to help someone get into the details. We'll be working with a long trace from a real scientific discovery agent. You'll be building a tool for inspecting the trace and forming opinions about what helps you actually get to the bottom of it. Then you'll run that tool against a trace from an agent run on your data. By the end of this assignment, you'll have a sense of whether there is any hope in helping people get to the bottom of agent traces and if so what are the tools by which we'll help people do it.

# The trace

Folder `data/claim515-results` contains all outputs from the run of a single agent. This agent took about 8 hours to do a scientific experimentation. It's task was to assess this claim:

```
On 1,200 held-out file-transfer problems balanced between permitted and forbidden requests, with four files and four recipients, linear decoders of Qwen2.5-7B-Instruct's final prompt-token residual state identify the requested file and its permitted recipient with at least 90% accuracy each, even among incorrect authorization decisions. Patching a fixed set of at most 12 attention heads from correct runs containing the same permission facts in reordered table rows corrects at least 30% of all initial errors while changing no more than 3% of correct decisions. Decoders, heads, and donor-selection rules are fixed on separate development data, with decoders trained on both correct and incorrect development runs; test names and permission assignments are unseen.
```

Few of us in this class are likely experts in the domain of the claim, so let's unpack it together a little. (And I know this is a lot of technical detail... but contending with this detail is part of the point! Agents are going to be testing specific hypotheses like these with detailed assumptions).

- it assumes an authorization task, where an AI model (Qwen2.5-7B-Instruct) is supposed to predict whether a file can be sent to a particular recipient
- it asks **if it is possible to infer what the model "knows" during prediction from the model's internal state**, in particular what the requested file is and who is the permitted recipient
- there are a bunch of stipulations on how to test --- this is tested on 1,200 test cases, you try to read off the internal state using linear decoders, it should be possible to recover the correct information even the final prediction fails
- additionally, it should be possible to fix predictions by modestly patching model activity by copying model activation patterns from successful predictions

This is a big, complex claim. Apparently, this bot spent 8 hours trying to figure out whether or not it was true by reviewing a bunch of literature and running a bunch of AI experiments. At the end of it's prediction it said "it's probably true." (a score of +1 on a feasibility scale from -2 to +2) Why does it do it, and should we believe it?

Spend a couple of minutes looking at this claim. If you don't understand it, ask an LLM to help you unpack it in terms familiar to you. You'll be trying to decide whether you think the agent actually proved anything about it.

To force some understanding, write out what kinds of things you'll look for in a trace to see if the claim is correct. There's no right answer at this point, just collect your thoughts: ✏️

# Lesson 1. What can I do with the agent's outputs?

The first thing we can do is to read the outputs that the agent put out. These aren't always intended for human consumption. But together they contain all the context we have about what the agent did. Develop a sensitivity for what you can and _can't_ learn from the outputs by spending a time-boxed 10 minutes looking through them (no AI use yet). You might be surprised what you _can_ learn.

During the 10 minutes, try to answer:

What kinds of things did the agent do? ✏️ [Andrew answer - look at the literature, run experiments]
What evidence is it basing its "+1" off of? ✏️ [running experiments, including one with 95% accuracy, and a couple with 60-70%. I'm not quite sure what it means]
How likely do _you_ think the claim is to be true (-2 = very unlikely, -1 = somewhat unlikely, 0 = neither likely nor unlikely, +1 = somewhat likely, +2 = very likely)? ✏️ [0]
What is _your_ confidence (from 0–100%)? ✏️ [25%]
Why? ✏️ [I'm thrown off by the 60 and 70% numbers]
Did you find any useful files? What were they? What did they contain? ✏️ [the problem_515_final.md files]
Are there any other files you would be interested in looking into if you had more time? ✏️

# Lesson 2. What can I do with Q&A?

Okay, so that's what you were able to learn through the logs. Now let's give us the next most basic AI capability we have at our disposal — AI Q&A. Time boxing yourself to 10 minutes again, talk with Claude Code about the data and try to learn as much as you can to answer (mostly) the same questions. 

In each of these stages, try to pay attention to what you're learning that you _didn't already know_. We're trying to build up a mental model of what kinds of tools we need to understand different parts of an agent's results.

What kinds of things did the agent do (only write changes in what you know)? ✏️ 
What evidence is it basing its "+1" off of (ditto)? ✏️
How likely do _you_ think the claim is to be true (-2 to 2)? ✏️ [0]
What is _your_ confidence (from 0–100%)? ✏️ [25%]
Why? ✏️ [I'm thrown off by the 60 and 70% numbers]
Did you find any useful files? What were they? What did they contain? ✏️ [the problem_515_final.md files]
Are there any other files you would be interested in looking into if you had more time? ✏️

# Lesson 3. What can I do with a claim tree?

# Lesson 4. What can I do with evidence views?

# Lesson 5. What can I do with evidence-review assistance?

# Lesson 5.1. What can I do with annotation ability?

# Lesson 6. What can I learn about a scientific discovery trace run on my own data?

Ask the agent to find something surprising in your data, and produce it in a trace with this format:

TODO: generate JSON format that involves:
- claims that were proven
  - for each one, subclaims that need to be assumed, confirmed, or ruled out
  - the status of each of these claims
- for each step of analysis...
  - the alternatives that were considered as next steps
  - if a step was ruled out and not taken, why --- made irrelevant by another step, low priority, error
  - what claim / subclaim was it addressing. Okay if it was addressing multiple.
  - why the step was taken --- why it was thought useful to the subclaim, why this particular approach
  - the plan - what needed to happen in that step - look up literature, analyze data, produce a visualization, etc.
  - the inputs to the step - (data files, input from previous steps, etc.; for files, include a specific path)
  - the outputs of the step - (new files (include specific path))
    - pointers to short verbatim excerpts of the files that can be consulted for context
  - the degree of force the evidence has on the claim - strongly supports, weakly support, weakly contradicts, strongly contradicts, equivocal

Plug it into your interface above.

```json
```

Probably have people send Xiaorui a message with your reflections so he can check.
We are going to talk about this during discussion time in class.

# Old content