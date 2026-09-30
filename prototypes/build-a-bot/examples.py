"""Example requests through the ZDR-only client. Uses only synthetic prompts.

    uv run python examples.py
"""

from zdr_openrouter import chat, text_of


def show(label, data):
    u = data["usage"]
    print(f"--- {label}: {data['model']} via {data.get('provider')} "
          f"({u['prompt_tokens']} in / {u['completion_tokens']} out, ${u.get('cost', 0):.6f})")
    print(text_of(data).strip(), "\n")


# 1. Default model (Opus), plain question.
show("opus", chat(
    [{"role": "user", "content": "In two sentences: why might a within-subjects user study need counterbalancing?"}],
    max_tokens=200,
))

# 2. Budget model, cheapest ZDR provider first.
show("budget", chat(
    [{"role": "user", "content": "Name three common threats to validity in HCI lab studies. One line each."}],
    model="openai/gpt-oss-120b",
    provider={"sort": "price"},
    max_tokens=400,
))

# 3. Tool call: the building block of the agent loop we'll write next.
tools = [{
    "type": "function",
    "function": {
        "name": "read_csv_head",
        "description": "Return the first n rows of a CSV file in the data directory.",
        "parameters": {
            "type": "object",
            "properties": {"filename": {"type": "string"}, "n": {"type": "integer"}},
            "required": ["filename"],
        },
    },
}]
data = chat(
    [{"role": "user", "content": "Look at the first 5 rows of raw_timing.csv."}],
    tools=tools,
    max_tokens=200,
)
print("--- tool call:", data["choices"][0]["message"].get("tool_calls"), "\n")

# 4. Negative test: this model has no ZDR endpoint, so the request should be refused.
try:
    chat([{"role": "user", "content": "hi"}], model="qwen/qwen3.8-flash", max_tokens=10)
    print("--- negative test: UNEXPECTEDLY SUCCEEDED")
except RuntimeError as e:
    print("--- negative test refused as expected:", str(e)[:300])
