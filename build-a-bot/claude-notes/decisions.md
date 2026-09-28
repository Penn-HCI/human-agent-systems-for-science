# Decisions

## Why
- Build custom solutions so that, mainly, we can get the benefits of zero data retention.

## API
- Use OpenRouter for API requests, as I might seek out budget API backends.
- Every request is ZDR-only; fail rather than fall back to a non-ZDR endpoint.
- Use requests, not httpx: less certain what's in the code.
- Use Opus as the default model to start with.
- API key goes in a .env file.

## Agent
- The agent writes data processing scripts that answer the research questions, reads the outputs, and provides responses.
- Scripts run sandboxed: no network, read-only data/, write only to the run folder.
- The agent must _not_ be allowed to list files in my home folder.
- The sandbox folder sticks around post-execution so I can look at the files produced.
