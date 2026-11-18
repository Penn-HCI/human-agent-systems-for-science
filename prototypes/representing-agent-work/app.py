"""Show the claim tree for an agent run: the claim and the subclaims it was broken into."""

import json
from pathlib import Path

import streamlit as st

EVENTS_FILE = Path(__file__).parent / "data/claim515-results/sandbox/events.jsonl"


def load_events(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def last_event(events, name):
    matches = [e for e in events if e["event"] == name]
    return matches[-1]["payload"] if matches else None


events = load_events(EVENTS_FILE)
claim = last_event(events, "run_started")["claim_text"]
subclaims = last_event(events, "decomposition")["subclaims"]

st.title("Claim tree")

st.subheader("Claim")
st.info(claim)

relations = {sc["relation"] for sc in subclaims}
if relations == {"AND"}:
    st.write(f"The agent split this into **{len(subclaims)} subclaims**. All of them must hold for the claim to hold.")
else:
    st.write(f"The agent split this into **{len(subclaims)} subclaims** (relations: {', '.join(sorted(relations))}).")

for sc in subclaims:
    with st.container(border=True):
        label = f"**{sc['id']}** · {sc['relation']} · {sc['tag'].lower()}"
        if sc["bottleneck"]:
            label += " · :red[bottleneck]"
        st.markdown(label)
        st.write(sc["text"])
        st.caption("How the agent planned to test it")
        st.write(sc["experiment_hint"])
