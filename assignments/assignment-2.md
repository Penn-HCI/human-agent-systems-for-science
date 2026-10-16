**Under construction**

In 2025, the internet was abuzz with the talk of LLM wikis following Andrej Karpathy's sketch of the idea in a [GitHub Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) describing the approach. The idea of an LLM wiki was a personal knowledge base that maintained itself. One of the great challenges of maintaining one's own documentation has always been maintenance. Karpathy asked, can we delegate to our LLMs the ingest, organization, and upkeep of raw data, ultimately putting it in a form so that high-quality data is at your and the AI's fingertips when it is needed?

The LLM wiki idea, I think, hasn't been a total hit... You'll find plenty of tutorials on creating them on the web that feel more like marketing material than a justified endorsement. Still, it feels like there's really something to this idea. It _should_ be possible to reduce some of the fuss of accessing your own information and of helping your AI tools know your context.

So in this homework, you'll be working to build an LLM wiki that could usefully maintain your personal knowledge base. You'll exercise this wiki in two ways:

- as a **personal knowledge base**. This wiki should be something you can actually navigate and review in order to remind yourself of information that's important to you.
- as **project memory for your agent**. The wiki should externalize your thinking and explorations in a way that gives your agent more context for how to be a better partner in ideation and discovery.

Ideally, you will build this LLM wiki over your own scientific materials (notes, papers, data, agent outputs, etc.) If you are able to do this and excited to, please go ahead! We'll give you extra credit if you try this and submit a reflection on the usefulness of the wiki you've built.

That said, we know some of you won't be able to do this, whether for data protection reasons or just because your records are in a format that makes ingest impossible. That's fine — for you, we provide a scenario where you can build up a knowledge base to help you ideate for final projects for this course.

But before you start, get some inspiration. Read these examples of LLM wikis, which should pay off in helping you think of what your LLM wiki should actually be optimized to help you with.

- Karpathy's original posting on [LLM wikis](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- Journalist Casey Newton's [reflection](https://www.platformer.news/karpathy-llm-wiki-journalism-productivity/) of the LLM wiki he built to support his work
- And optionally, these reflections ([1](https://joonanlab.github.io/notes/llm-wiki-lab-mentoring-en), [2](https://github.com/scunning1975/MixtapeTools/blob/main/workflow.md)) from academic labs that have put together something like an LLM wiki to support their lab activities

# Trajectory of this assignment

In this assignment you will:

1. Define a research question that you want to explore
2. Create a bare LLM wiki inside of the Obsidian note-taking tool
3. Populate your LLM wiki with literature
4. Add data to your LLM wiki from a small empirical investigation
5. Evolve and use your wiki in ways that get you closer to an answer to your research question

The meat of the assignment will be in step 5. We provide guidance on steps 1-4 to more quickly get you to the interesting part of the assignment.

# Step 1. Define a research question you want to explore

You'll be attempting to use your LLM wiki as an accelerant for a bit of your own scientific work. If you are able to ingest data from your own current research, define a research question you are currently trying to answer. If you aren't, then use this assignment as an opportunity to ideate a final project idea for this class. Your research question would be something like...

```
What kinds of tools or processes could make it easier for humans and agents to work together in the wet lab?
```

The research question can either be broad (like the one above) or specific ("Could introducing timed reflections into human-agent data analysis help researchers catch subtle flaws in scripts?").

# Step 2. Create a bare LLM wiki in Obsidian

We recommend you host your LLM wiki in [Obsidian](https://obsidian.md/). Obsidian is a note-taking app that provides lightweight markup formats for defining wiki pages. Its advantages are that it is free, widely-used (and hence stable and with a crisp design), and it is extensible if you want to customize aspects of the wiki UI.

So, start by downloading and installing Obsidian.

While you will use Obsidian to read your wiki, I actually recommend you construct and maintain the wiki using agents _outside_ of Obsidian. This gives you more flexibility to use the tools thare most familiar and useful to you. When doing this assignment myself, I used the [Claude Code extension in VSCode](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code), asking Claude to create the initial wiki and add and maintain notes to it based on my literature and data. I'll assume you're also using Claude Code throughout the instructions in this doc, but feel free to use any other agents and/or do some of these steps manually.

Create a new folder, and ask your Claude Code to create a new LLM wiki inside of it. In your prompt...

(spend a little bit of time thinking about what kind of format you think you will find readable. do raw sources need to be quoted, etc...)

<!--
(continually tune the directions you give to Claude to make this wiki useful. Need to throw it away midway through? Np, go for it, these things are cheap to produce.)

=====

Ground rules:
- at least _some_ empirical data
- at least _some_ literature
- some real thing you want to explore

Trajectory:
- create an Obsidian Vault
- define a research question you are interested in
- fetch some literature
  - side-bar, here is my MCP
- explore until you've "found" something
  - might be drafting an intro for a paper you're working on, if it's your own data

Tailor a couple of things:
- kinds of evidence you want to be pulled out
- traceability features you want it to have
- come up with a mechanism for keeping track of what you've actually believe or have checked yourself

Reflection:
- are you going to keep using your LLM wiki?
- are you going to change anything about the way you create your personal "knowledge base"?

# Basic setup 



As Karpathy put it in his sketch of an LLM wiki, "the exact directly structure, the schema conventions, the page formats, the tooling — all of that will depend on your domain, your preferences, and your LLM choice... instantiate a version that fits your needs." Since this class is about unleashing your imagination about what workflows should look like in your line of work, bend the pattern until it actually works for you.



Get this running on the Halie data.
Should be able to accept both experimental data and input from other papers.

Then, use it on a new vault.
Get this system to help you ideate future directions for this course.
Agents produce concepts they've found.
They don't get to tell you what you found interesting, inspiring.

May want to run experiments.
Ask it to find additional open data related to your topic.
Ask it to reproduce the results.

An example query to find empirical data to process:
I'm doing a final project for Andrew Head's Building Human-Agent Systems for Science course https://www.pennhci.com/human-agent-systems-for-science/. I'm thinking of doing a project on helping come up with human-agent processes that can ease the peer review workflow. I'd like to find some empirical data I can analyze from past experiments to learn what has worked, and what does not work, in human, AI, and human-AI-based peer review. Can you help me find this?

Reflections — what is working well for you in this wiki format? What is *not*? Describe an updated record-keeping workflow that would give you the advantages without the disadvantages.
-->