# /// script
# dependencies = ["pandas"]
# ///
"""Rate metaphor sentences with an LLM judge (Claude Haiku, via the `claude` CLI).

Third-party raters only scored the final sentences people wrote, not the AI's
suggestions. So the judge rates both, on the raters' three yes/no criteria
(apt, specific, imageable). Its ratings of final sentences can be checked
against the third-party ratings; its ratings of suggestions are our measured
AI output quality.

Results are cached, so re-running only rates new sentences.

Run from the vault folder:  uv run analysis/metaphor_judge.py
Writes:                     analysis/outputs/metaphor_judgments.csv
"""
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

STD = Path("data/halie/data/std/metaphor/event_blocks.csv")
OUT = Path("analysis/outputs/metaphor_judgments.csv")
BATCH = 40

PROMPT = """Each item is a sentence someone wrote (or an AI suggested) as a metaphor built on a seed metaphor, e.g. seed "progress", meaning the metaphor "progress is ...".
Rate each sentence yes (1) or no (0) on:
- apt: the metaphor fits and makes sense for the seed concept.
- specific: it is concrete and particular, not vague or generic.
- imageable: it evokes a clear mental image.
Reply with only a JSON list like [{"id": "...", "apt": 1, "specific": 0, "imageable": 1}, ...], one entry per item.

"""
SEEDS = {"progress": "progress", "theory": "a theory", "life": "life", "idea": "an idea"}


def sentences():
    blocks = pd.read_csv(STD)
    rows = []
    for kind, col in [("suggestion", "model_completion"), ("final", "final_sentence")]:
        b = blocks.dropna(subset=[col])
        rows += [{"id": f"{kind}-{i}", "kind": kind, "seed": SEEDS[r["prompt"]], "sentence": r[col]}
                 for i, r in b.iterrows()]
    return pd.DataFrame(rows)


def judge(batch):
    items = [{"id": r["id"], "seed": r["seed"], "sentence": r["sentence"]} for _, r in batch.iterrows()]
    text = PROMPT + json.dumps(items, ensure_ascii=False, indent=1)
    out = subprocess.run(["claude", "-p", "--model", "haiku"], input=text,
                         capture_output=True, text=True).stdout
    try:
        labels = json.loads(out[out.find("["): out.rfind("]") + 1])
    except json.JSONDecodeError:
        return []
    keep = set(batch["id"])
    return [{k: x[k] for k in ["id", "apt", "specific", "imageable"]} for x in labels
            if x.get("id") in keep and all(x.get(k) in (0, 1) for k in ["apt", "specific", "imageable"])]


def main():
    todo = sentences()
    done = pd.read_csv(OUT) if OUT.exists() else pd.DataFrame(columns=["id", "apt", "specific", "imageable"])
    todo = todo[~todo["id"].isin(done["id"])]
    print(f"{len(done)} rated, {len(todo)} to go")
    # Shuffle so each batch mixes suggestions and final sentences.
    todo = todo.sample(frac=1, random_state=0)
    batches = [todo.iloc[i: i + BATCH] for i in range(0, len(todo), BATCH)]
    with ThreadPoolExecutor(4) as pool:
        for labels in pool.map(judge, batches):
            done = pd.concat([done, pd.DataFrame(labels)])
            done.to_csv(OUT, index=False)
    print(f"{len(done)} rated")


if __name__ == "__main__":
    main()
