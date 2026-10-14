# /// script
# dependencies = ["pandas"]
# ///
"""Build one row per crossword session (and per AI response) from the raw HALIE data.

AI output quality
- Measured, per response then averaged per session:
  - gave_answer: the response contains the selected clue's answer as a whole
    word (or a run of up to 3 words), and the user's query didn't already.
  - degenerate: the response is empty or repeats itself.
- Perceived, from the survey: fluency, helpfulness.

Interaction quality
- Survey: ease, joy.
- Process: num_queries.
- Task success: letter and clue accuracy of the grid at the 31-minute mark
  (this reproduces the dataset's published accuracies.csv for 301 of 304
  sessions), and at the end of the session (final_*).

Everything except final_* uses only the first 31 minutes.

Run from the vault folder:  uv run analysis/crossword_sessions.py
Writes:                     analysis/outputs/crossword_sessions.csv
                            analysis/outputs/crossword_responses.csv
"""
import json
import re
import zipfile
from pathlib import Path

import pandas as pd

RAW = Path("data/halie/data/raw/crossword")
OUT = Path("analysis/outputs")
CUTOFF_MINUTES = 31


def read_puzzle(path):
    """Return the solution grid (list of strings, '.' = black) and clue answers."""
    data = path.read_bytes()
    width, height = data[0x2C], data[0x2D]
    solution = data[0x34 : 0x34 + width * height].decode("latin1")
    grid = [solution[r * width : (r + 1) * width] for r in range(height)]
    return grid, clue_cells(grid)


def clue_cells(grid):
    """Map (number, 'across'|'down') to the list of cells in that answer."""
    height, width = len(grid), len(grid[0])
    white = lambda r, c: 0 <= r < height and 0 <= c < width and grid[r][c] != "."
    clues, number = {}, 0
    for r in range(height):
        for c in range(width):
            if not white(r, c):
                continue
            starts_across = not white(r, c - 1) and white(r, c + 1)
            starts_down = not white(r - 1, c) and white(r + 1, c)
            if starts_across or starts_down:
                number += 1
            if starts_across:
                cells, cc = [], c
                while white(r, cc):
                    cells.append((r, cc))
                    cc += 1
                clues[(number, "across")] = cells
            if starts_down:
                cells, rr = [], r
                while white(rr, c):
                    cells.append((rr, c))
                    rr += 1
                clues[(number, "down")] = cells
    return clues


def words(text):
    return re.findall(r"[A-Z]+", (text or "").upper())


def letters(text):
    return "".join(words(text))


def contains_answer(answer, text, max_words=3):
    """True if a run of up to max_words consecutive words spells the answer."""
    w = words(text)
    return any("".join(w[i : i + n]) == answer
               for n in range(1, max_words + 1) for i in range(len(w) - n + 1))


def is_degenerate(response):
    """Empty, or more than 30% of its word triples are repeats."""
    w = words(response)
    triples = [tuple(w[i : i + 3]) for i in range(len(w) - 2)]
    repetitive = len(triples) > 0 and 1 - len(set(triples)) / len(triples) > 0.3
    return len(w) == 0 or repetitive


def accuracy(state, grid, clues):
    """Return (letter accuracy, clue accuracy) of a grid state."""
    white = [(r, c) for r, row in enumerate(grid) for c, ch in enumerate(row) if ch != "."]
    correct = {(r, c) for r, c in white if (state[r][c] or "").upper() == grid[r][c]}
    letter_accuracy = len(correct) / len(white)
    clue_accuracy = sum(all(cell in correct for cell in cells) for cells in clues.values()) / len(clues)
    return letter_accuracy, clue_accuracy


def score_responses(events, grid, clues):
    """One row per AI response. Each "Ask" is followed by a "Model Answer"."""
    rows, query, selected = [], None, None
    for e in events:
        if e["event-type"] == "Ask":
            query = e["lm-query"] or ""
            selected = (int(e["selected-clue-number"]), e["selected-clue-direction"].strip())
        elif e["event-type"] == "Model Answer" and query is not None and selected in clues:
            answer = "".join(grid[r][c] for r, c in clues[selected])
            response = e["lm-response"] or ""
            rows.append({
                "minute": round(e["timestamp"], 2),
                "clue": f"{selected[0]} {selected[1]}",
                "answer": answer,
                "query": query.strip(),
                "response": response.strip(),
                "gave_answer": contains_answer(answer, response) and answer not in letters(query),
                "degenerate": is_degenerate(response),
            })
            query = None
    return rows


def score_session(all_events, grid, clues):
    final_letter, final_clue = accuracy(all_events[-1]["crossword-state"], grid, clues)
    events = [e for e in all_events if e["timestamp"] <= CUTOFF_MINUTES]
    letter_accuracy, clue_accuracy = accuracy(events[-1]["crossword-state"], grid, clues)
    responses = score_responses(events, grid, clues)
    n = len(responses)
    session = {
        "gave_answer_rate": sum(r["gave_answer"] for r in responses) / n if n else None,
        "degenerate_rate": sum(r["degenerate"] for r in responses) / n if n else None,
        "num_queries": sum(e["event-type"] == "Ask" for e in events),
        "letter_accuracy": letter_accuracy,
        "clue_accuracy": clue_accuracy,
        "final_letter_accuracy": final_letter,
        "final_clue_accuracy": final_clue,
    }
    return session, responses


def main():
    puzzles = {p.stem: read_puzzle(p) for p in (RAW / "puzzles").glob("*.puz")}
    survey = pd.DataFrame(json.loads((RAW / "survey_responses.json").read_text()))
    survey["session_id"] = survey["gid"].astype(str) + "_" + survey["username"] + "_" + survey["model"]

    # session_ids.txt lists the sessions kept by the dataset authors.
    kept = (RAW / "session_ids.txt").read_text().split()
    logs = zipfile.ZipFile(RAW / "logs.zip")

    sessions, responses = [], []
    for name in kept:
        events = json.loads(logs.read(f"logs/{name}.json"))
        gid, user, model = name.split("_")[:3]
        grid, clues = puzzles[gid]
        session_id = f"{gid}_{user}_{model}"
        session, session_responses = score_session(events, grid, clues)
        sessions.append({"session_id": session_id, "log_file": f"logs/{name}.json",
                         "puzzle": gid, "model": model, **session})
        responses += [{"session_id": session_id, "model": model, **r} for r in session_responses]
    sessions = pd.DataFrame(sessions)

    ratings = ["fluency", "helpfulness", "ease", "joy"]
    survey = survey.drop_duplicates("session_id", keep="last")[["session_id", *ratings]]
    sessions = sessions.merge(survey, on="session_id", how="left")
    sessions["joy"] = sessions["joy"].where(sessions["joy"] != -1)

    OUT.mkdir(parents=True, exist_ok=True)
    sessions.to_csv(OUT / "crossword_sessions.csv", index=False)
    pd.DataFrame(responses).to_csv(OUT / "crossword_responses.csv", index=False)
    print(f"{len(sessions)} sessions ({sessions['fluency'].notna().sum()} with surveys), "
          f"{len(responses)} AI responses")


if __name__ == "__main__":
    main()
