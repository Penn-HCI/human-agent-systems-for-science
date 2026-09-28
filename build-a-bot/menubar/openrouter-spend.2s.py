#!/usr/bin/env python3
# <xbar.title>OpenRouter spend</xbar.title>
# <xbar.desc>Today (local time) and all-time OpenRouter spend.</xbar.desc>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
"""SwiftBar plugin: shows today's OpenRouter spend in the menu bar (total in the dropdown).

Standard library only; runs on macOS's /usr/bin/python3 (3.9).
SwiftBar reruns this every 2 s (the ".2s." in the filename).

Two modes:

* Ledger only (default). Sums ~/.openrouter-spend/ledger.jsonl, which our
  client appends to after every request. Needs no API key, but only sees spend
  from code that writes to the ledger.

* Ledger + API. If ~/.openrouter-spend/.env contains OPENROUTER_API_KEY=...,
  GET /api/v1/key is also called every API_EVERY seconds. That catches spend
  from other tools on the same key (e.g. Claude Code); between calls, ledger
  entries newer than the last call are added on top so the number stays live.
  "Today" is local-midnight based: at the first API call of each local day we
  record baseline = key usage - ledger spend since midnight. Other tools' spend
  between midnight and that first call is missed for "today" (not for total).
"""

import datetime as dt
import json
import os
import time
import urllib.request
from pathlib import Path

API_EVERY = 300  # seconds between OpenRouter API calls
HOME = Path.home() / ".openrouter-spend"
LEDGER = Path(os.environ.get("OPENROUTER_LEDGER", HOME / "ledger.jsonl"))
KEY_FILE = HOME / ".env"
STATE = HOME / "menubar-state.json"


def api_key():
    try:
        for line in KEY_FILE.read_text().splitlines():
            k, _, v = line.partition("=")
            if k.strip() == "OPENROUTER_API_KEY" and v.strip():
                return v.strip().strip("'\"")
    except OSError:
        pass
    return None


def fetch_usage(key):
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/key", headers={"Authorization": "Bearer " + key}
    )
    with urllib.request.urlopen(req, timeout=5) as r:
        return float(json.load(r)["data"].get("usage") or 0)


def ledger_since(since=None):
    """Total and per-model ledger cost for entries after `since` (aware datetime; None = all)."""
    total, by_model = 0.0, {}
    try:
        f = LEDGER.open()
    except OSError:
        return total, by_model
    with f:
        for line in f:
            try:
                e = json.loads(line)
                if since and dt.datetime.fromisoformat(e["ts"]) <= since:
                    continue
                cost = float(e.get("cost_usd") or 0)
            except (ValueError, KeyError, TypeError):
                continue
            total += cost
            model = e.get("model") or "?"
            by_model[model] = by_model.get(model, 0.0) + cost
    return total, by_model


def load_state():
    try:
        return json.loads(STATE.read_text())
    except (OSError, ValueError):
        return {}


def save_state(state):
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state))
    tmp.replace(STATE)  # atomic, in case two runs overlap


def money(x):
    if x == 0 or abs(x) >= 1:
        return "${:.2f}".format(x)
    return "${:.3f}".format(x) if abs(x) >= 0.01 else "${:.4f}".format(x)


def main():
    now = dt.datetime.now().astimezone()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_str = now.date().isoformat()
    today_ledger, today_by_model = ledger_since(midnight)
    key = api_key()
    error = None

    if key is None:
        spent_today, total = today_ledger, ledger_since()[0]
        source = "local ledger only (no key in {})".format(KEY_FILE)
    else:
        state = load_state()
        # Throttle on the last attempt, not the last success, so errors don't retry every 2 s.
        if time.time() - state.get("attempted_at", 0) >= API_EVERY:
            state["attempted_at"] = time.time()
            state.pop("error", None)
            try:
                state["usage"] = fetch_usage(key)
                state["fetched_at"] = time.time()
                if state.get("day") != today_str:
                    state["day"] = today_str
                    state["baseline"] = state["usage"] - today_ledger
            except Exception as e:  # offline, bad key, ...: fall back to cached numbers
                state["error"] = "API error: {}".format(e)
            HOME.mkdir(exist_ok=True)
            save_state(state)
        error = state.get("error")
        if "usage" in state:
            fetched = dt.datetime.fromtimestamp(state["fetched_at"]).astimezone()
            total = state["usage"] + ledger_since(fetched)[0]
            spent_today = total - state["baseline"] if state.get("day") == today_str else today_ledger
            source = "API (last update {}) + ledger".format(fetched.strftime("%H:%M"))
        else:
            spent_today, total = today_ledger, ledger_since()[0]
            source = "local ledger only (API not reached yet)"

    print("{}{}".format(money(spent_today), " ⚠︎" if error else ""))
    print("---")
    print("Today (since local midnight): {}".format(money(spent_today)))
    print("All time: {}".format(money(total)))
    if today_by_model:
        print("Today by model (ledger)")
        for model, cost in sorted(today_by_model.items(), key=lambda kv: -kv[1]):
            print("--{}: {} | font=Menlo size=12".format(model, money(cost)))
    print("---")
    print("Source: " + source + " | size=11")
    if error:
        print(error + " | color=red size=11")
    print("OpenRouter activity | href=https://openrouter.ai/activity")


if __name__ == "__main__":
    main()
