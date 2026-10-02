# Course Description

**Building Human-Agent Systems for Science**

Imagine we had perfect agents for doing science. What then would good science process look like? In this class, we try to answer this question. We look at the seams where people will work with agents and develop new kinds of infrastructure to help them work together better. We start by building a simple scientific discovery agent and exploring mechanisms for human steering and review of agentic work. Then we expand focus. We review the broad array of processes where agents may disrupt scientific workflows, like collaborative sensemaking over data, sharing results, and building repositories of knowledge for the lab and community. In a series of assignments, we build prototype infrastructure to support envisioned scientific workflows and use them on example research problems. In a final project, students build pieces of agentic scientific infrastructure inspired by their own research or interests.

**Semester**: Spring 2027

**When**: Mondays and Wednesdays, 1:45-3:15pm

**Location**: TBD

**Audience**: Ph.D. students, Master's and Bachelor's students engaged in research. This course is for researchers who are interested in trying out new processes for themselves and their group. Those not actively engaged in research might still be considered but will be given lower priority.

**Prerequisites**: We welcome students from the gamut of fields! But — you must know your Python. We expect you to be able to write Python yourself, pick and call programming libraries, and inspect what your code is doing. That's not because you'll be writing much code yourself. But you will be on the hook for checking that your agentic tools aren't leaking your precious research data or running up a huge bill you have to pay.

**Format**: Every week, there will be 1 instructor-led lecture on Monday, and 1 discussion section where we discuss papers on the week's lecture topic on Wednesday.

## Schedule

This is a rough schedule, and it will be continually updated for the next few weeks (this message written on Oct. 2, 2026).

| Date | Format | Topic |
|---|---|---|
| Wed, Jan 20 | Lecture | Introduction |
| Mon, Jan 25 | Discussion | Example Scientific Discovery Agents |
| Wed, Jan 27 | Lecture | Explainability and Steering |
| Mon, Feb 1 | Discussion | Explainability and Steering |
| Wed, Feb 3 | Lecture | Memory Stores |
| Mon, Feb 8 | Discussion | Memory Stores |
| Wed, Feb 10 | Lecture | Collaborative Scientific Sensemaking - Models |
| Mon, Feb 15 | Discussion | Collaborative Scientific Sensemaking - Models |
| Wed, Feb 17 | Lecture | Collaborative Scientific Sensemaking - Tools |
| Mon, Feb 22 | Discussion | Collaborative Scientific Sensemaking - Tools |
| Wed, Feb 24 | Lecture | Argumentation |
| Mon, Mar 1 | Discussion | Argumentation |
| Wed, Mar 3 | Lecture | Literature |
| Mon, Mar 8 |  | No class — spring break |
| Wed, Mar 10 |  | No class — spring break |
| Mon, Mar 15 | Discussion | Literature |
| Wed, Mar 17 | Lecture | Ex silico |
| Mon, Mar 22 | Discussion | Project pitches |
| Wed, Mar 24 | Lecture | Ex silico (continued) |
| Mon, Mar 29 | Discussion | Ex silico |
| Wed, Mar 31 | Lecture | Knowledge Commons |
| Mon, Apr 5 | Discussion | Knowledge Commons |
| Wed, Apr 7 | Lecture | Scientific Values |
| Mon, Apr 12 | Discussion | Scientific Values |
| Wed, Apr 14 | Lecture | Publication |
| Mon, Apr 19 | Discussion | Publication |
| Wed, Apr 21 | Lecture | Peer Review |
| Mon, Apr 26 | Discussion | Peer Review |
| Wed, Apr 28 |  | Final project presentations |
| Mon, May 3 |  | Final project presentations |

## Assignments

This class will have 8 assignments (also liable to be updated). Assignment #1-4 focus on augmenting _individual_ scientific activity, and #5-6 on _collaborative_ and _community_-level activity. Almost all assignments will provide opportunities for students to use the systems they are building in their own research.

* **Assignment 1. Build your scientific "digital twin."** This is a guided activity in building a scientific discovery agent. It will take in a dataset as input, come up with research questions, explore them, and report out results. Tune it until it resembles your scientific "digital twin," producing results and outputs you fully stand behind without intervention.

* **Assignment 2. Ideate with a custom LLM wiki.** Agents are supposed to help us keep track of more information in knowledge-intensive tasks. Build up a local knowledge base that actually does this for you. Three UI requirements: it has to be dead easy to add data to it; it has to produce an compact and accurate wiki that you actually want to use use; it has to ask for clarification when it doesn't know what's in your data; and you have to be able to query against it. Test it out by using it as a partner in ideating research project ideas.

* **Assignment 3. Make agentic output make sense.** You will be given an output trace from a scientific discovery agent from a domain you have never worked in before. Put it in an interface that makes it make sense. A non-expert should be able to quickly assess: Does it come up with a valid result? Use appropriate methods? Does its result really matter? But they don't have the expertise! Figure out what explanations and context you have to provide in the interface so that it doesn't matter.

* **Assignment 4. A norm-enforcing analysis environment.** Analyses have norms. One such analysis is qualitative analysis, where it is expected that a _human_ reviews data, comes to an _independent_ judgment of the how to describe it, and bases that judgment on a _complete_ reading of the data. Is it possible to build AI tools that provide AI support while ensuring the norms are upheld? Build a qualitative analysis environment that allows the use of AI but structures the way that data is shown and processed to guarantee the norms are upheld.

* **Assignment 5. A proactive knowledge base with many humans and agents.** Turn your wiki from Assignment 2 into a substrate that can (and will!) support collaborative science among you and your final project teammates. It must have features for---descriptions of claims you are working on, evidence you have collected, ability to collaboratively edit the wiki without conflict, agents can contribute to wiki, and participants are notified when new evidence is brought to bear on key claims. Use this wiki to support your group's creation of a final project proposal.

* **Assignment 6. Bifurcating the research report.** Create a set of publications that represent one possibility of the future of publication. Given a trace of scientific activity, generate (1) a document that represents the sophistication of _human_ decisions of the scientist, which could be used in training and promotion settings (2) a document representing the actual results in a more compact but expandable form. Could this be the future of scientific publishing?

* **Assignment 7. Final project.** To be worked on in the last 2 months of the class. Develop a piece of scientific infrastructure designed to fit a human-agent scientific future. Work on something inspired by your own research or interests—you are strongly encouraged to make something that you yourself or your lab would use.