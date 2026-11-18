"""Claim tree viewer for the claim 515 trace.

Run with:  streamlit run app.py
"""

import html
import json
import textwrap
from pathlib import Path

import streamlit as st

DATA = Path(__file__).parent / "data" / "claim515-results" / "sandbox"
EVENTS = DATA / "events.jsonl"
OUTCOMES = DATA / "sessions" / "20bd60ea8ef7.outcomes.json"

STATUS_COLORS = {
    "supported": "#c8e6c9",
    "not supported": "#ffcdd2",
    "unrun": "#e0e0e0",
}


def last_event(events, name):
    """Payload of the last event with this name (the final run comes last)."""
    return [e["payload"] for e in events if e["event"] == name][-1]


def subclaim_status(judgments):
    """The agent's final judgment of a subclaim, ignoring superseded results."""
    superseded = {j["supersedes"] for j in judgments}
    final = [j for j in judgments if j["result_id"] not in superseded][-1]
    if final["measurement_disposition"] != "usable":
        return "unrun"
    if "NOT" in final["conclusion"]:
        return "not supported"
    return "supported"


def load_tree():
    events = [json.loads(line) for line in EVENTS.open()]
    outcomes = json.loads(OUTCOMES.read_text())

    # The agent's per-subclaim judgments, recorded after its experiments.
    judgments = {}
    for action in outcomes["actions"]:
        for check in action.get("checked", []):
            if check["obligation"].startswith("judgment."):
                for j in check["basis"]["judgments"]:
                    judgments.setdefault(j["proposition_id"], []).append(j)

    subclaims = last_event(events, "decomposition")["subclaims"]
    for sc in subclaims:
        sc["status"] = subclaim_status(judgments.get(sc["id"], []))

    before = last_event(events, "likert_estimated")
    after = last_event(events, "assessment_final")
    return {
        "claim": last_event(events, "run_started")["claim_text"],
        "before": (before["likert"], before["confidence"]),
        "after": (after["likert_score"], after["confidence"]),
        "subclaims": subclaims,
    }


BR = '<br align="left"/>'  # Graphviz line break that left-aligns the line before it


def wrap(text, width=40):
    """Escape text for a Graphviz HTML label and break it into left-aligned lines."""
    return BR.join(html.escape(line, quote=False) for line in textwrap.wrap(text, width)) + BR


def to_dot(tree):
    (b_score, b_conf), (a_score, a_conf) = tree["before"], tree["after"]
    root_label = (
        f"<b>Claim</b>{BR}{BR}"
        + wrap(tree["claim"])
        + BR
        + f"<b>Agent's score</b> (-2 to +2){BR}"
        + f"before exploration: {b_score:+d} (confidence {b_conf:.2f}){BR}"
        + f"after exploration: {a_score:+d} (confidence {a_conf:.2f}){BR}"
    )
    lines = [
        "digraph {",
        "rankdir=LR; ranksep=0.4; nodesep=0.15;",
        'node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=20, margin=0.2];',
        f'root [label=<{root_label}>, fillcolor="#e3f2fd"];',
    ]
    for sc in tree["subclaims"]:
        heading = f"<b>Subclaim {sc['id']}</b>"
        if sc["bottleneck"]:
            heading += " (bottleneck)"
        label = f"{heading}{BR}Agent's verdict: <b>{sc['status']}</b>{BR}{BR}{wrap(sc['text'])}"
        border = "penwidth=3" if sc["bottleneck"] else "penwidth=1"
        color = STATUS_COLORS[sc["status"]]
        lines.append(f'{sc["id"]} [label=<{label}>, fillcolor="{color}", {border}];')
        lines.append(f'root -> {sc["id"]} [label="{sc["relation"]}", fontsize=18];')
    lines.append("}")
    return "\n".join(lines)


st.set_page_config(page_title="Claim 515", layout="wide")
st.title("Claim 515: claim tree")
st.caption(
    "Subclaim colors show the agent's final judgment: green = supported, "
    "red = not supported, gray = experiment didn't run. "
    "Thick borders mark subclaims the agent flagged as bottlenecks."
)

tree = load_tree()
st.graphviz_chart(to_dot(tree), width="stretch")
