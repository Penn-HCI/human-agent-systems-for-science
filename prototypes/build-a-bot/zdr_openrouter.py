"""Minimal OpenRouter client that only routes to Zero Data Retention endpoints.

Every request carries provider.zdr=true and provider.data_collection="deny",
so OpenRouter refuses to route it to any endpoint that retains or trains on
prompts. If no ZDR endpoint serves the requested model, the request fails
rather than silently falling back to one that retains data.

Every successful call appends one line to a local spend ledger
(~/.openrouter-spend/ledger.jsonl) so a separate budget widget can total it.

Put OPENROUTER_API_KEY=sk-or-... in .env next to this file (gitignored), then:
    uv run python zdr_openrouter.py "What is a p-value?"
"""

import datetime as dt
import json
import os
import sys
from pathlib import Path

import requests

API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "anthropic/claude-opus-5.5"
LEDGER = Path(os.environ.get("OPENROUTER_LEDGER", Path.home() / ".openrouter-spend" / "ledger.jsonl"))


def _load_dotenv(path=Path(__file__).with_name(".env")):
    """Load KEY=VALUE lines from .env into os.environ (real env vars win)."""
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("'\""))


_load_dotenv()

# Always sent. Callers can't override it: chat() merges these keys in last.
ZDR_PROVIDER_PREFS = {"zdr": True, "data_collection": "deny"}


def chat(messages, model=DEFAULT_MODEL, *, provider=None, timeout=300, **params):
    """Send a chat completion restricted to ZDR endpoints. Returns the response JSON.

    `provider` holds extra routing preferences (e.g. {"sort": "price"});
    the ZDR flags are always added on top. `params` go straight into the
    request body (max_tokens, temperature, tools, ...).
    """
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("Set OPENROUTER_API_KEY (create one at https://openrouter.ai/settings/keys).")

    body = {
        "model": model,
        "messages": messages,
        "provider": {**(provider or {}), **ZDR_PROVIDER_PREFS},
        **params,
    }
    resp = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            # Optional attribution header; shows up in the OpenRouter activity page.
            "X-Title": "build-a-bot",
        },
        json=body,
        timeout=timeout,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"OpenRouter {resp.status_code}: {resp.text}")
    data = resp.json()
    # A request can return 200 with an error in the body (e.g. a provider failed mid-request).
    if "error" in data:
        raise RuntimeError(f"OpenRouter error: {data['error']}")
    _log_spend(data)
    return data


def _log_spend(data):
    usage = data.get("usage") or {}
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "id": data.get("id"),
        "model": data.get("model"),
        "provider": data.get("provider"),
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "cost_usd": usage.get("cost", 0.0),
        "app": "build-a-bot",
    }
    with LEDGER.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def text_of(data):
    return data["choices"][0]["message"].get("content") or ""


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) or "In one sentence, what is zero data retention?"
    data = chat([{"role": "user", "content": prompt}], max_tokens=300)
    usage = data["usage"]
    print(text_of(data))
    print(
        f"\n[{data['model']} via {data.get('provider')}] "
        f"{usage['prompt_tokens']} in / {usage['completion_tokens']} out, ${usage.get('cost', 0):.6f}"
    )
