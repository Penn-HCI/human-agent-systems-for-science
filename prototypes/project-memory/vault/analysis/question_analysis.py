# /// script
# dependencies = ["pandas", "scipy", "statsmodels"]
# ///
"""AI output quality vs. interaction quality in the question-answering task.

Design: 331 sessions, one per worker. Each answers 10 of 30 multiple-choice
questions (plus an attention check): 5 with the AI available ("lm") and 5
without ("ctrl"). Every question is answered ~55 times each way.

AI output quality
- Measured, per response (question_judge.py): the response points to the
  correct choice, points to a wrong choice, or commits to none; degenerate
  (empty or >30% repeated word triples).
- Perceived (survey, 1-5): fluency, helpfulness.
Interaction quality
- Survey: ease. Process: queries per AI question.
- Task success: accuracy on AI questions; lift = accuracy with AI minus the
  same person's accuracy without it.

Run from the vault folder, after question_judge.py:
    uv run analysis/question_analysis.py
Writes: analysis/outputs/question_instances.csv, question_sessions.csv
"""
import re
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import spearmanr

from question_judge import responses

STD = Path("data/halie/data/std/question")
OUT = Path("analysis/outputs")


def is_degenerate(text):
    w = re.findall(r"[a-z]+", str(text).lower())
    t = [tuple(w[i: i + 3]) for i in range(len(w) - 2)]
    return len(w) == 0 or (len(t) > 0 and 1 - len(set(t)) / len(t) > 0.3)


def rho(data, x, y):
    pair = data[[x, y]].dropna().astype(float)
    r, p = spearmanr(pair[x], pair[y])
    return f"rho = {r:.2f}, p = {p:.3f}, n = {len(pair)}"


blocks = pd.read_csv(STD / "event_blocks.csv")
blocks = blocks[blocks["question_type"] != "attn"]

# Per response.
resp = responses().merge(pd.read_csv(OUT / "question_judgments.csv"), on="id")
answer = blocks.set_index(["session_id", "question_id"])["answer"]
resp["answer"] = [answer[s, q] for s, q in zip(resp["session_id"], resp["question_id"])]
resp["correct"] = (resp["choice"] == resp["answer"]).astype(int)
resp["wrong"] = (~resp["choice"].isin(["none", ""]) & (resp["choice"] != resp["answer"])).astype(int)
resp["degenerate"] = resp["response"].map(is_degenerate).astype(int)
print(f"{len(resp)} AI responses: {resp['correct'].mean():.2f} point to the correct choice, "
      f"{resp['wrong'].mean():.2f} to a wrong one, {resp['degenerate'].mean():.2f} degenerate\n")

# Per question answered with the AI available: what did the AI end up saying?
last = resp.sort_values("i").groupby(["session_id", "question_id"]).last()
inst = blocks[blocks["question_type"] == "lm"].set_index(["session_id", "question_id"])
inst["ai_last"] = last["choice"]
inst["ai_said"] = "not used"
inst.loc[inst["ai_last"].notna(), "ai_said"] = "nothing"
inst.loc[inst["ai_last"] == inst["answer"], "ai_said"] = "correct"
inst.loc[inst["ai_last"].isin(list("abcd")) & (inst["ai_last"] != inst["answer"]), "ai_said"] = "wrong"
inst["followed_ai"] = (inst["user_answer"] == inst["ai_last"]).astype(int)
inst = inst.reset_index()
# Baseline: how often people answer this question correctly without the AI.
baseline = blocks[blocks["question_type"] == "ctrl"].groupby("question_id")["user_correct"].mean()
inst["no_ai_accuracy"] = inst["question_id"].map(baseline)
inst.to_csv(OUT / "question_instances.csv", index=False)

print("== Per question: user accuracy by what the AI's last response said ==")
table = inst.groupby("ai_said").agg(n=("user_correct", "size"), accuracy=("user_correct", "mean"),
                                    same_question_without_ai=("no_ai_accuracy", "mean"),
                                    followed_ai=("followed_ai", "mean"))
print(table.round(2).to_string())
fit = smf.logit("user_correct ~ C(ai_said, Treatment('not used')) + C(question_id)", inst).fit(disp=0)
print("\nLogit, controlling for question (vs. AI not used):")
print(fit.params.filter(like="ai_said").round(2).to_string())
print(fit.pvalues.filter(like="ai_said").round(4).to_string())

# Per session.
acc = blocks.pivot_table(index="session_id", columns="question_type", values="user_correct", aggfunc="mean")
sessions = resp.groupby("session_id")[["correct", "wrong", "degenerate"]].mean().add_suffix("_rate")
sessions = acc.rename(columns={"lm": "acc_ai", "ctrl": "acc_no_ai"}).join(sessions)
sessions["lift"] = sessions["acc_ai"] - sessions["acc_no_ai"]
lm = blocks[blocks["question_type"] == "lm"].groupby("session_id")
sessions["queries"] = lm["num_queries"].mean()
sessions["ai_used"] = lm["lm_used"].mean()
survey = pd.read_csv(STD / "survey_responses.csv")[["session_id", "model", "fluency", "helpfulness", "ease"]]
sessions = survey.merge(sessions.reset_index(), on="session_id")
sessions.to_csv(OUT / "question_sessions.csv", index=False)

print(f"\n== Per session ({len(sessions)}) ==")
cols = ["correct_rate", "wrong_rate", "degenerate_rate", "fluency", "helpfulness", "ease",
        "queries", "ai_used", "acc_ai", "acc_no_ai", "lift"]
print(sessions.groupby("model")[cols].mean().round(2).to_string())
within = sessions.copy()
within[cols] = sessions.groupby("model")[cols].rank(pct=True)
for x in ["correct_rate", "wrong_rate", "degenerate_rate", "fluency", "helpfulness"]:
    for y in ["ease", "queries", "acc_ai", "lift"]:
        print(f"  {x:>15} vs {y:<8} all: {rho(sessions, x, y)} | within model: {rho(within, x, y)}")
for x, y in [("correct_rate", "fluency"), ("correct_rate", "helpfulness"),
             ("wrong_rate", "helpfulness"), ("degenerate_rate", "fluency")]:
    print(f"  {x:>15} vs {y:<11} all: {rho(sessions, x, y)} | within model: {rho(within, x, y)}")
