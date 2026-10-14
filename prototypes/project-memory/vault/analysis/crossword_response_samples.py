# /// script
# dependencies = ["pandas"]
# ///
"""Print random AI responses flagged by each measure, to check them by eye.

Run from the vault folder, after crossword_sessions.py:
    uv run analysis/crossword_response_samples.py [gave_answer|degenerate] [n]
"""
import sys

import pandas as pd

from crossword_sessions import OUT

measure = sys.argv[1] if len(sys.argv) > 1 else "gave_answer"
n = int(sys.argv[2]) if len(sys.argv) > 2 else 20

responses = pd.read_csv(OUT / "crossword_responses.csv")
flagged = responses[responses[measure]]
print(f"{len(flagged)} of {len(responses)} responses flagged {measure}; {n} at random:\n")
for r in flagged.sample(n, random_state=0).itertuples():
    print(f"[{r.answer}] Q: {r.query[:80]}")
    print(f"    R: {r.response[:160]}\n")
