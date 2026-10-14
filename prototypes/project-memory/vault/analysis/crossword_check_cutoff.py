# /// script
# dependencies = ["pandas"]
# ///
"""Which grid state does the published accuracies.csv score?

Scores each session's grid at several time cutoffs and counts how many
match the published letter accuracy.

Run from the vault folder:  uv run analysis/crossword_check_cutoff.py
"""
import json
import zipfile

import pandas as pd

from crossword_sessions import RAW, accuracy, read_puzzle

STD = "data/halie/data/std/crossword/accuracies.csv"
CUTOFFS = [25, 30, 30.5, 31, 31.5, 32, 35, None]  # None = end of session

puzzles = {p.stem: read_puzzle(p) for p in (RAW / "puzzles").glob("*.puz")}
published = pd.read_csv(STD).set_index("session_id")["letter_accuracy"]
logs = zipfile.ZipFile(RAW / "logs.zip")

sessions = {}
for name in (RAW / "session_ids.txt").read_text().split():
    session_id = "_".join(name.split("_")[:3])
    if session_id in published.index:
        sessions[session_id] = json.loads(logs.read(f"logs/{name}.json"))

for cutoff in CUTOFFS:
    mismatches = []
    for session_id, events in sessions.items():
        if cutoff is not None:
            events = [e for e in events if e["timestamp"] <= cutoff]
        grid, clues = puzzles[session_id.split("_")[0]]
        letter_accuracy, _ = accuracy(events[-1]["crossword-state"], grid, clues)
        if abs(letter_accuracy - published[session_id]) >= 0.01:
            mismatches.append(session_id)
    label = "end of session" if cutoff is None else f"{cutoff} min"
    print(f"{label:>15}: {len(sessions) - len(mismatches)} / {len(sessions)} match")
    if len(mismatches) <= 5:
        print("                 mismatches:", ", ".join(mismatches))
