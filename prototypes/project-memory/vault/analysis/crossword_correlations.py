# /// script
# dependencies = ["pandas", "scipy"]
# ///
"""Does AI output quality correlate with interaction quality? (crossword task)

Spearman correlations across sessions, four ways:
- "all sessions": raw values.
- "within puzzle": each measure ranked within its puzzle, so puzzle
  difficulty doesn't drive the result.
- "within puzzle and model": ranked within each puzzle x model group, so
  differences between the four LMs don't drive the result either.
- "one session per worker": some workers did several puzzles, so this keeps
  only each worker's first session (raw values).

Run from the vault folder, after crossword_sessions.py:
    uv run analysis/crossword_correlations.py
Writes: analysis/outputs/crossword_correlations.csv
        analysis/outputs/crossword_by_model.csv
"""
from pathlib import Path

import pandas as pd
from scipy.stats import spearmanr

OUT = Path("analysis/outputs")
AI_OUTPUT = ["gave_answer_rate", "degenerate_rate", "fluency", "helpfulness"]
INTERACTION = ["ease", "joy", "num_queries", "letter_accuracy", "clue_accuracy"]

# AI output vs. interaction; do measured and perceived AI output agree;
# and does querying more go with lower task success?
PAIRS = [(out, inter) for out in AI_OUTPUT for inter in INTERACTION]
PAIRS += [(measured, perceived) for measured in AI_OUTPUT[:2] for perceived in AI_OUTPUT[2:]]
PAIRS += [("num_queries", "letter_accuracy")]

sessions = pd.read_csv(OUT / "crossword_sessions.csv")
sessions["worker"] = sessions["session_id"].str.split("_").str[1]
measures = AI_OUTPUT + INTERACTION


def ranked_within(groups):
    data = sessions.copy()
    data[measures] = sessions.groupby(groups)[measures].rank(pct=True)
    return data


analyses = [("all sessions", sessions),
            ("within puzzle", ranked_within(["puzzle"])),
            ("within puzzle and model", ranked_within(["puzzle", "model"])),
            ("one session per worker", sessions.drop_duplicates("worker"))]

rows = []
for label, data in analyses:
    for x, y in PAIRS:
        pair = data[[x, y]].dropna()
        rho, p = spearmanr(pair[x], pair[y])
        rows.append({"analysis": label, "x": x, "y": y,
                     "n": len(pair), "rho": round(rho, 3), "p": round(p, 4)})
correlations = pd.DataFrame(rows)
correlations.to_csv(OUT / "crossword_correlations.csv", index=False)

by_model = sessions.groupby("model")[measures].mean().round(3)
by_model.to_csv(OUT / "crossword_by_model.csv")

pd.set_option("display.width", 200)
print(correlations.to_string(index=False))
print()
print(by_model.to_string())
