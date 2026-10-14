# /// script
# dependencies = ["pandas", "scipy"]
# ///
"""AI output quality vs. interaction quality in the summarization task.

Design: 80 sessions; each edits 10 pre-generated news summaries (20 document
sets x 4 models, one fixed summary per document x model).

AI output quality (of the original summary)
- Third-party: consistency (share of 3 raters), relevance, coherence (1-5),
  for about half of the summaries.
- Perceived: the user's own yes/no consistency, relevance, coherence.
- Survey: helpfulness.
Interaction quality
- Effort: edit distance (words), editing time; survey `edit`, `improvement`.
- Task success: third-party ratings of the edited summary.

Run from the vault folder:  uv run analysis/summarization_analysis.py
Writes:                     analysis/outputs/summarization_sessions.csv
"""
import re
from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr, wilcoxon

STD = Path("data/halie/data/std/summarization")
OUT = Path("analysis/outputs")
DIMS = ["consistency", "relevance", "coherency"]


def rho(data, x, y):
    pair = data[[x, y]].dropna().astype(float)
    r, p = spearmanr(pair[x], pair[y])
    return f"rho = {r:.2f}, p = {p:.3f}, n = {len(pair)}"


def within(data, cols, group):
    """Subtract each group's mean, so differences between groups drop out."""
    data = data.copy()
    data[cols] = data[cols].astype(float) - data.groupby(group)[cols].transform("mean").astype(float)
    return data


blocks = pd.read_csv(STD / "event_blocks.csv")
survey = pd.read_csv(STD / "survey_responses.csv")
for d in DIMS:
    for side in ["original", "edited"]:
        blocks[f"{side}_{d}"] = blocks[f"{side}_{d}"].astype(float)
blocks["edited_at_all"] = (blocks["distance"] > 0).astype(float)


def copied(summary, document):
    """Share of the summary's word triples that appear in the document."""
    words = lambda t: re.findall(r"[a-z0-9]+", str(t).lower())
    s, d = words(summary), words(document)
    doc = {tuple(d[i: i + 3]) for i in range(len(d) - 2)}
    tri = [tuple(s[i: i + 3]) for i in range(len(s) - 2)]
    return sum(t in doc for t in tri) / len(tri) if tri else None


blocks["copied"] = [copied(s, d) for s, d in zip(blocks["original_summary"], blocks["document"])]
print("== Copying: share of the AI summary's word triples found in the article ==")
print(blocks.groupby("model")["copied"].mean().round(2).to_string())
print(f"  copied vs third-party consistency: {rho(blocks, 'copied', 'original_consistency_third_party')}")
print(f"  copied vs third-party relevance:   {rho(blocks, 'copied', 'original_relevance_third_party')}\n")

print("== Summary level (800 summaries) ==")
print("User vs. third-party ratings of the same original summary:")
for d in DIMS:
    print(f"  {d}: {rho(blocks, f'original_{d}', f'original_{d}_third_party')}")

print("\nUser's own rating vs. third-party rating, before and after editing (means):")
both = blocks.dropna(subset=["original_consistency_third_party", "edited_consistency_third_party"])
for d in DIMS:
    o, e = both[f"original_{d}_third_party"], both[f"edited_{d}_third_party"]
    print(f"  {d}: user {both[f'original_{d}'].mean():.2f} -> {both[f'edited_{d}'].mean():.2f}; "
          f"third party {o.mean():.2f} -> {e.mean():.2f} (Wilcoxon p = {wilcoxon(o, e).pvalue:.3g}, n = {len(both)})")

flagged = both[both["original_consistency_third_party"] < 0.5]
print(f"\nOriginals most third-party raters called inconsistent (n = {len(flagged)}):")
print(f"  user also called it inconsistent: {1 - flagged['original_consistency'].mean():.2f}")
print(f"  user left it unedited: {1 - flagged['edited_at_all'].mean():.2f}")
print(f"  user rated the edited version consistent: {flagged['edited_consistency'].mean():.2f}")
print(f"  most third-party raters call the edited version consistent: "
      f"{(flagged['edited_consistency_third_party'] > 0.5).mean():.2f}")

print("\nDoes editing effort follow the original's quality? (within document, i.e. comparing the 4 models' summaries)")
w = within(blocks, ["distance", "elapsed_time", *[f"original_{d}" for d in DIMS],
                    *[f"original_{d}_third_party" for d in DIMS]], "document")
for d in DIMS:
    print(f"  distance vs third-party {d}: {rho(w, 'distance', f'original_{d}_third_party')}")
    print(f"  distance vs user {d}:        {rho(w, 'distance', f'original_{d}')}")

# Session level.
sessions = blocks.groupby(["session_id", "model", "prompt"]).agg(
    tp_consistency=("original_consistency_third_party", "mean"),
    tp_relevance=("original_relevance_third_party", "mean"),
    tp_coherency=("original_coherency_third_party", "mean"),
    user_consistency=("original_consistency", "mean"),
    user_relevance=("original_relevance", "mean"),
    user_coherency=("original_coherency", "mean"),
    length=("original_length", "mean"),
    distance=("distance", "mean"),
    minutes=("elapsed_time", "mean"),
    edited_tp_consistency=("edited_consistency_third_party", "mean"),
    edited_tp_relevance=("edited_relevance_third_party", "mean"),
).reset_index()
sessions = sessions.merge(survey[["session_id", "worker_id", "helpfulness", "edit", "improvement"]], on="session_id")
sessions.to_csv(OUT / "summarization_sessions.csv", index=False)

print("\n== Session level (80 sessions) ==")
print(sessions.groupby("model")[["tp_consistency", "tp_relevance", "user_consistency", "length",
                                 "distance", "helpfulness", "edit", "improvement"]].mean().round(2).to_string())
pairs = [(x, y) for x in ["tp_consistency", "tp_relevance", "user_consistency", "user_relevance", "length"]
         for y in ["helpfulness", "edit", "distance"]]
pairs += [("distance", "edit"), ("distance", "helpfulness"), ("edit", "helpfulness")]
numeric = sessions.columns.drop(["session_id", "model", "prompt", "worker_id"])
ws = within(sessions, list(numeric), "prompt")
one = sessions.drop_duplicates("worker_id")  # one worker did 11 of the 80 sessions
for x, y in pairs:
    print(f"  {x:>17} vs {y:<12} all: {rho(sessions, x, y)} | within doc set: {rho(ws, x, y)}"
          f" | one per worker: {rho(one, x, y)}")
