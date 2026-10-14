# /// script
# dependencies = ["pandas", "scipy", "statsmodels"]
# ///
"""AI output quality vs. interaction quality in the dialogue task.

Design: 189 sessions (one per worker, the ones kept in std/), each a ~10-turn
chat with one of 4 models about a given scenario.

AI output quality, per AI turn
- Perceived: the user flagged each turn while chatting. runs.csv stores the
  flags in `turn-binary` and the same answers inverted in `final`; we use
  `final` (1 = sensible, specific, ...). Checked by eye: turns with
  sensibility 0 are off-topic replies.
- Measured: length; degenerate (empty or >30% repeated word triples);
  repeats_self (>50% of its word triples appeared in an earlier AI turn).
Interaction quality
- `quality-overall` (1-5), asked at the end of the chat.
- Engagement: the user's words per message.

Run from the vault folder:  uv run analysis/dialogue_analysis.py
Writes:                     analysis/outputs/dialogue_turns.csv, dialogue_sessions.csv
"""
import re
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import spearmanr

RAW = Path("data/halie/data/raw/dialogue/runs.csv")
STD = Path("data/halie/data/std/dialogue/survey_responses.csv")
OUT = Path("analysis/outputs")
RATINGS = {"sensibility-utterances": "sensible", "specificity-utterances": "specific",
           "humanness-utterances": "humanlike", "preference-utterances": "preferred",
           "interesting-utterances": "interesting", "boring-utterances": "boring"}


def words(text):
    return re.findall(r"[a-z']+", str(text).lower())


def triples(text):
    w = words(text)
    return [tuple(w[i: i + 3]) for i in range(len(w) - 2)]


def is_degenerate(text):
    t = triples(text)
    return len(words(text)) == 0 or (len(t) > 0 and 1 - len(set(t)) / len(t) > 0.3)


def rho(data, x, y):
    pair = data[[x, y]].dropna().astype(float)
    r, p = spearmanr(pair[x], pair[y])
    return f"rho = {r:.2f}, p = {p:.3f}, n = {len(pair)}"


runs = pd.read_csv(RAW)
runs = runs[runs["trace_id"].isin(pd.read_csv(STD)["session_id"])]
runs["v"] = pd.to_numeric(runs["value"].replace({"True": 1, "False": 0}), errors="coerce")

# One row per AI turn.
turns = (runs[(runs["type"] == "final") & (runs["round_id"] >= 0) & runs["metric"].isin(RATINGS)]
         .pivot_table(index=["trace_id", "round_id"], columns="metric", values="v", aggfunc="first")
         .rename(columns=RATINGS))
meta = (runs[runs["round_id"] >= 0].drop_duplicates(["trace_id", "round_id"])
        .set_index(["trace_id", "round_id"])[["model", "scenario", "user_input", "completion"]])
turns = turns.join(meta, how="inner").reset_index().sort_values(["trace_id", "round_id"])
turns["length"] = turns["completion"].map(lambda t: len(words(t)))
turns["user_words"] = turns["user_input"].map(lambda t: len(words(t)))
turns["degenerate"] = turns["completion"].map(is_degenerate).astype(int)


def repeats(group):
    seen, out = set(), []
    for text in group["completion"]:
        t = triples(text)
        out.append(int(len(t) > 0 and sum(x in seen for x in t) / len(t) > 0.5))
        seen |= set(t)
    return pd.Series(out, index=group.index)


turns["repeats_self"] = turns.groupby("trace_id", group_keys=False).apply(repeats)
turns["bad"] = ((turns["sensible"] == 0) | (turns["specific"] == 0)).astype(int)
# The user's next message, to see whether a bad AI turn changes how the user writes.
turns["next_user_words"] = turns.groupby("trace_id")["user_words"].shift(-1)
turns.to_csv(OUT / "dialogue_turns.csv", index=False)

overall = runs[(runs["metric"] == "quality-overall") & (runs["type"] == "likert")].set_index("trace_id")["v"]
perceived = list(RATINGS.values()) + ["bad"]
sessions = turns.groupby(["trace_id", "model", "scenario"]).agg(
    **{p: (p, "mean") for p in perceived},
    length=("length", "mean"), degenerate=("degenerate", "mean"), repeats_self=("repeats_self", "mean"),
    user_words=("user_words", "mean"), n_turns=("round_id", "count"),
).reset_index()
last = turns.groupby("trace_id").tail(3).groupby("trace_id")["bad"].mean().rename("bad_last3")
first = turns.groupby("trace_id").head(3).groupby("trace_id")["bad"].mean().rename("bad_first3")
sessions = sessions.join(last, on="trace_id").join(first, on="trace_id")
sessions["any_bad"] = (sessions["bad"] > 0).astype(int)
sessions["quality"] = sessions["trace_id"].map(overall)
sessions.to_csv(OUT / "dialogue_sessions.csv", index=False)

print(f"{len(sessions)} sessions, {len(turns)} AI turns\n")
print(sessions.groupby("model")[["sensible", "specific", "interesting", "bad", "repeats_self",
                                  "degenerate", "length", "user_words", "quality"]].mean().round(2).to_string())

print("\n== AI output (session means) vs. overall quality ==")
within_model = sessions.copy()
cols = perceived + ["length", "degenerate", "repeats_self", "user_words", "quality", "bad_last3", "bad_first3"]
within_model[cols] = sessions.groupby("model")[cols].rank(pct=True)
for x in perceived + ["length", "degenerate", "repeats_self", "user_words", "bad_first3", "bad_last3", "any_bad"]:
    print(f"  {x:>13} vs quality  all: {rho(sessions, x, 'quality')} | within model: {rho(within_model, x, 'quality')}")

print("\n== Which turns matter? quality ~ share of bad turns early vs. late (OLS) ==")
fit = smf.ols("quality ~ bad_first3 + bad_last3 + C(model)", data=sessions).fit()
print(fit.summary().tables[1])

print("\n== After a bad AI turn, does the user write less? (within session) ==")
t = turns.dropna(subset=["next_user_words"]).copy()
t["next_minus_mean"] = t["next_user_words"] - t.groupby("trace_id")["user_words"].transform("mean")
print(t.groupby("bad")["next_minus_mean"].agg(["mean", "count"]).round(2))
fit = smf.mixedlm("next_user_words ~ bad + user_words + round_id", t, groups=t["trace_id"]).fit()
print(fit.summary().tables[1].loc[["bad", "user_words", "round_id"]])
