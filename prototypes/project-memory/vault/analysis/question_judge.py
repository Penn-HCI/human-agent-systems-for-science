# /// script
# dependencies = ["pandas"]
# ///
"""Label which answer choice each AI response in the QA task points to.

Simple word matching was too noisy (it counted "No, the SEC is not a
government agency" as picking SEC), so an LLM judge (Claude Haiku, through the
`claude` CLI) reads each response and says which choice, if any, it asserts.
The judge isn't asked whether that choice is right; that comes from the key.

Results are cached, so re-running only labels responses not yet labeled.

Run from the vault folder:  uv run analysis/question_judge.py
Writes:                     analysis/outputs/question_judgments.csv
"""
import ast
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

STD = Path("data/halie/data/std/question/event_blocks.csv")
OUT = Path("analysis/outputs/question_judgments.csv")
BATCH = 40

PROMPT = """Each item below has a multiple-choice quiz question, a query a person typed to an AI, and the AI's response.
For each item, say which choice (a, b, c or d) the AI's response states or clearly implies is the answer to the quiz question.
Say "none" if the response doesn't commit to one of the choices (off-topic, evasive, only repeats the query, or names something that isn't a choice).
Don't use your own knowledge of the right answer; only report what the response says.
Reply with only a JSON list like [{"id": "...", "choice": "a"}, ...], one entry per item.

"""


def responses():
    """One row per AI response to a question where the AI was available."""
    blocks = pd.read_csv(STD)
    rows = []
    for _, b in blocks[blocks["question_type"] == "lm"].iterrows():
        queries, answers = ast.literal_eval(b["user_queries"]), ast.literal_eval(b["lm_responses"])
        for i, (query, response) in enumerate(zip(queries, answers)):
            rows.append({"id": f"{b['session_id']}-{b['question_id']}-{i}",
                         "session_id": b["session_id"], "question_id": b["question_id"], "i": i,
                         "question": b["question_text"],
                         **{c: b[f"choice_{c}"] for c in "abcd"},
                         "query": query, "response": response})
    return pd.DataFrame(rows)


def judge(batch):
    items = [{"id": r["id"], "question": r["question"],
              "choices": {c: r[c] for c in "abcd"},
              "query": r["query"], "response": r["response"][:1200]} for _, r in batch.iterrows()]
    text = PROMPT + json.dumps(items, ensure_ascii=False, indent=1)
    out = subprocess.run(["claude", "-p", "--model", "haiku"], input=text,
                         capture_output=True, text=True).stdout
    out = out[out.find("["): out.rfind("]") + 1]
    try:
        labels = {x["id"]: str(x["choice"]).lower() for x in json.loads(out)}
    except json.JSONDecodeError:
        return []
    return [{"id": i, "choice": labels[i]} for i in batch["id"] if labels.get(i) in {"a", "b", "c", "d", "none"}]


def main():
    todo = responses()
    done = pd.read_csv(OUT) if OUT.exists() else pd.DataFrame(columns=["id", "choice"])
    todo = todo[~todo["id"].isin(done["id"])]
    print(f"{len(done)} labeled, {len(todo)} to go")
    batches = [todo.iloc[i: i + BATCH] for i in range(0, len(todo), BATCH)]
    with ThreadPoolExecutor(6) as pool:
        for labels in pool.map(judge, batches):
            done = pd.concat([done, pd.DataFrame(labels)])
            done.to_csv(OUT, index=False)
    print(f"{len(done)} labeled")


if __name__ == "__main__":
    main()
