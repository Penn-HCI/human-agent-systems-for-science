# Running Claude Code through OpenRouter with ZDR

Point Claude Code at OpenRouter and turn on ZDR-only routing for your account, so every model call goes only to zero-data-retention endpoints: https://openrouter.ai/docs/guides/guides/claude-code-integration

Caveats:
- Claude's ZDR endpoints on OpenRouter are Amazon Bedrock and Google Vertex, not Anthropic's own API. Features that only Anthropic's API offers (fast mode, server-side web search) won't work.
- ZDR covers inference only. It does not cover OpenRouter plugins or tools (e.g. its web search), and in-memory prompt caching is still allowed.
- ZDR is a contractual promise from each provider, not something you can verify technically.
