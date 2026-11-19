// Dev-server endpoint that lets the app ask Claude Code questions about the trace.
// POST /api/ask {prompt, sessionId?} runs `claude -p` in the trace folder and streams back
// newline-delimited JSON events: {type: "text" | "tool" | "done" | "error", ...}.
//
// This is the app's only link to Claude. `claude -p` sends the question, and any trace files
// Claude reads, to Anthropic like any Claude Code session. Claude can only read files inside
// DATA_DIR: it gets just the Read/Grep/Glob tools, `--restricted` confines them to DATA_DIR,
// `--permission-mode dontAsk` denies anything that would need approval, and no MCP servers load.
import { spawn } from "node:child_process";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import type { IncomingMessage, ServerResponse } from "node:http";
import type { Plugin } from "vite";

const DATA_DIR = fileURLToPath(new URL("../data/claim515-results", import.meta.url));

const CLAUDE_ARGS = [
  "-p",
  "--tools", "Read", "Grep", "Glob",
  "--permission-mode", "dontAsk",
  "--restricted",
  "--strict-mcp-config",
  "--output-format", "stream-json",
  "--verbose",
  "--include-partial-messages",
];

type Citation = { n: number; target?: string; file?: string; quote: string; why?: string; valid?: boolean };

// Collapse whitespace so quotes match regardless of line breaks and indentation.
const normalize = (s: string) => s.replace(/\s+/g, " ").trim();

// Undo JSON string escapes, so a quote can match text stored inside a JSON file.
const unescapeJson = (s: string) =>
  s.replace(/\\n/g, "\n").replace(/\\t/g, "\t").replace(/\\"/g, '"').replace(/\\\\/g, "\\");

// Normalized file contents (raw and with JSON escapes undone), cached since files don't change.
const fileTexts = new Map<string, string[]>();
function readTraceFile(file: string): string[] | null {
  const full = path.resolve(DATA_DIR, file);
  if (!full.startsWith(DATA_DIR + path.sep)) return null; // only files in the trace folder
  if (!fileTexts.has(full)) {
    try {
      const raw = readFileSync(full, "utf8");
      fileTexts.set(full, [normalize(raw), normalize(unescapeJson(raw))]);
    } catch {
      return null;
    }
  }
  return fileTexts.get(full)!;
}

// Mark whether a file citation's quote really appears in that file. (The browser checks
// citations of app items, since it has their text.)
function checkFileCitation(c: Citation): Citation {
  if (!c.file) return c;
  const texts = readTraceFile(c.file);
  const quote = normalize(c.quote ?? "");
  return { ...c, valid: !!texts && quote.length > 0 && texts.some((t) => t.includes(quote)) };
}

// Claude ends its answer with a ```citations block holding a JSON list; split it off.
function splitCitations(text: string): { answer: string; citations: Citation[] } {
  const match = text.match(/```citations\s*([\s\S]*?)```\s*$/);
  if (!match) return { answer: text.trim(), citations: [] };
  let citations: Citation[] = [];
  try {
    citations = JSON.parse(match[1]);
  } catch {
    // A malformed block: show the answer without citations.
  }
  return { answer: text.slice(0, match.index).trim(), citations };
}

function runClaude(prompt: string, sessionId: string | undefined, res: ServerResponse) {
  res.setHeader("Content-Type", "application/x-ndjson");
  const send = (event: object) => res.write(JSON.stringify(event) + "\n");

  const args = [...CLAUDE_ARGS];
  if (sessionId) args.push("--resume", sessionId);
  const child = spawn("claude", args, { cwd: DATA_DIR });
  child.stdin.end(prompt); // the prompt goes in on stdin, so its length doesn't matter
  res.on("close", () => child.kill()); // stop Claude if the browser goes away

  // Turn Claude's stream-json events into the app's simpler events.
  const handle = (e: any) => {
    if (e.type === "stream_event" && e.event.type === "content_block_delta" && e.event.delta.type === "text_delta") {
      send({ type: "text", text: e.event.delta.text });
    } else if (e.type === "assistant") {
      for (const c of e.message.content) {
        if (c.type === "tool_use") send({ type: "tool", text: `${c.name} ${JSON.stringify(c.input)}` });
      }
    } else if (e.type === "result") {
      const { answer, citations } = splitCitations(e.result ?? "");
      send({ type: "done", sessionId: e.session_id, answer, citations: citations.map(checkFileCitation) });
    }
  };

  let buffer = "";
  child.stdout.on("data", (chunk) => {
    buffer += chunk;
    const lines = buffer.split("\n");
    buffer = lines.pop()!;
    for (const line of lines) {
      try {
        if (line.trim()) handle(JSON.parse(line));
      } catch {
        // Skip a line that isn't JSON rather than crash the dev server.
      }
    }
  });
  let stderr = "";
  child.stderr.on("data", (chunk) => (stderr += chunk));
  child.on("error", (err) => {
    send({ type: "error", message: `Couldn't start claude: ${err.message}` });
    res.end();
  });
  child.on("close", (code) => {
    if (code !== 0) send({ type: "error", message: stderr.trim() || `claude exited with code ${code}` });
    res.end();
  });
}

function handleAsk(req: IncomingMessage, res: ServerResponse) {
  // Only accept JSON POSTs from this app's own page. (Requiring JSON makes browsers check with
  // the server before another website could send one.)
  const origin = req.headers.origin;
  const fromThisApp = !origin || origin === `http://${req.headers.host}`;
  if (req.method !== "POST" || req.headers["content-type"] !== "application/json" || !fromThisApp) {
    res.statusCode = 403;
    return res.end();
  }
  let body = "";
  req.on("data", (chunk) => (body += chunk));
  req.on("end", () => {
    let prompt: unknown, sessionId: unknown;
    try {
      ({ prompt, sessionId } = JSON.parse(body));
    } catch {
      res.statusCode = 400;
      return res.end();
    }
    // Session ids are UUIDs; checking keeps anything else out of claude's arguments.
    const validSession = sessionId === undefined || (typeof sessionId === "string" && /^[0-9a-f-]{36}$/.test(sessionId));
    if (typeof prompt !== "string" || !validSession) {
      res.statusCode = 400;
      return res.end();
    }
    runClaude(prompt, sessionId as string | undefined, res);
  });
}

export function askClaude(): Plugin {
  return {
    name: "ask-claude",
    configureServer(server) {
      server.middlewares.use("/api/ask", handleAsk);
    },
  };
}
