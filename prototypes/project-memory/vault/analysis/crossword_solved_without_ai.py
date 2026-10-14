# /// script
# dependencies = ["pandas"]
# ///
"""Sessions with high accuracy but the lowest helpfulness rating, with what
people wrote about why the AI was (un)helpful.

Run from the vault folder, after crossword_sessions.py:
    uv run analysis/crossword_solved_without_ai.py
"""
import json

import pandas as pd

from crossword_sessions import OUT, RAW

sessions = pd.read_csv(OUT / "crossword_sessions.csv")
survey = pd.DataFrame(json.loads((RAW / "survey_responses.json").read_text()))
survey["session_id"] = survey["gid"].astype(str) + "_" + survey["username"] + "_" + survey["model"]
survey = survey.drop_duplicates("session_id", keep="last")

selected = sessions.query("letter_accuracy > 0.95 and helpfulness <= 1")
selected = selected.merge(survey[["session_id", "helpfulness_freetext"]], on="session_id")

print(f"{len(selected)} sessions with letter accuracy > 0.95 and helpfulness = 1\n")
for row in selected.itertuples():
    print(f"{row.session_id} (accuracy {row.letter_accuracy:.2f}, {row.num_queries} queries)")
    print(f"  {row.helpfulness_freetext}\n")
