# /// script
# dependencies = ["pandas", "scipy", "statsmodels"]
# ///
"""AI output quality vs. interaction quality in the metaphor task.

Design: 80 sessions from 32 workers; each writes ~9 metaphorical sentences
for a seed ("progress", "theory", "life", "idea"), optionally querying a model.

AI output quality
- Measured: LLM-judge ratings (apt, specific, imageable) of the AI's
  suggestion for each sentence (metaphor_judge.py).
- Perceived: survey fluency, helpfulness ("helped me come up with new
  ideas"), better_alone ("would have done better alone", from the raw survey).
Interaction quality
- Survey: ease, enjoyment, satisfaction, ownership, reuse.
- Process: share of sentences where the AI was used, queries, acceptance,
  and whether the final sentence is the suggestion word for word.
- Task success: third-party ratings of the final sentence (`overall`, the mean
  of apt, specific, imageable), for about half of the sentences.

Run from the vault folder, after metaphor_judge.py:
    uv run analysis/metaphor_analysis.py
Writes: analysis/outputs/metaphor_sessions.csv
"""
from pathlib import Path

import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import spearmanr

STD = Path("data/halie/data/std/metaphor")
RAW = Path("data/halie/data/raw/metaphor/survey_responses.csv")
OUT = Path("analysis/outputs")
CRITERIA = ["apt", "specific", "imageable"]


def rho(data, x, y):
    pair = data[[x, y]].dropna().astype(float)
    r, p = spearmanr(pair[x], pair[y])
    return f"rho = {r:.2f}, p = {p:.3f}, n = {len(pair)}"


blocks = pd.read_csv(STD / "event_blocks.csv")
blocks["ai_used"] = blocks["model_completion"].notna().astype(int)
blocks["verbatim"] = (blocks["final_sentence"].str.strip() == blocks["model_completion"].str.strip()).astype(int)
blocks["tp_overall"] = blocks["overall"]

judged = pd.read_csv(OUT / "metaphor_judgments.csv")
judged["score"] = judged[CRITERIA].mean(axis=1)
judged[["kind", "row"]] = judged["id"].str.split("-", expand=True)
judged["row"] = judged["row"].astype(int)
for kind in ["suggestion", "final"]:
    blocks[f"judge_{kind}"] = judged[judged["kind"] == kind].set_index("row")["score"]

print("== Check: LLM judge vs. third-party raters on final sentences ==")
print(f"  overall: {rho(blocks, 'judge_final', 'tp_overall')}")

print("\n== Sentence level ==")
print("Third-party quality of the final sentence, by whether the AI was used:")
print(blocks.groupby("ai_used")["tp_overall"].agg(["mean", "count"]).round(3))
rated = blocks.dropna(subset=["tp_overall"])
fit = smf.mixedlm("tp_overall ~ ai_used + C(prompt)", rated, groups=rated["worker_id"]).fit()
print(f"  within worker (mixed model): ai_used coef = {fit.params['ai_used']:.3f}, p = {fit.pvalues['ai_used']:.3f}")
used = blocks[blocks["ai_used"] == 1]
print(f"  among AI-used sentences, judge(suggestion) vs third-party(final): {rho(used, 'judge_suggestion', 'tp_overall')}")
print(f"  kept word for word: {used['verbatim'].mean():.2f} of AI-used sentences")
print(used.groupby("verbatim")["tp_overall"].agg(["mean", "count"]).round(3))

# Session level.
raw = pd.read_csv(RAW)
raw = raw.rename(columns={raw.columns[2]: "session_id", raw.columns[6]: "better_alone"})
raw = raw.drop_duplicates("session_id", keep="last")[["session_id", "better_alone"]]
survey = pd.read_csv(STD / "survey_responses.csv").merge(raw, on="session_id", how="left")

sessions = blocks.groupby(["session_id", "worker_id", "model", "prompt"]).agg(
    judge_suggestion=("judge_suggestion", "mean"), ai_used=("ai_used", "mean"),
    num_queries=("num_queries", "mean"), verbatim=("verbatim", "mean"),
    tp_overall=("tp_overall", "mean"), judge_final=("judge_final", "mean"),
).reset_index()
sessions = sessions.merge(survey.drop(columns=["worker_id", "model", "prompt"]), on="session_id")
sessions.to_csv(OUT / "metaphor_sessions.csv", index=False)

print(f"\n== Session level ({len(sessions)} sessions, {sessions['worker_id'].nunique()} workers) ==")
cols = ["judge_suggestion", "fluency", "helpfulness", "better_alone", "ease", "enjoyment",
        "satisfaction", "ownership", "reuse", "ai_used", "verbatim", "tp_overall"]
print(sessions.groupby("model")[cols].mean().round(2).to_string())
one = sessions.drop_duplicates("worker_id")
for x in ["judge_suggestion", "fluency", "helpfulness", "better_alone", "ai_used", "verbatim"]:
    for y in ["ease", "enjoyment", "satisfaction", "ownership", "reuse", "tp_overall"]:
        print(f"  {x:>16} vs {y:<12} all: {rho(sessions, x, y)} | one per worker: {rho(one, x, y)}")
