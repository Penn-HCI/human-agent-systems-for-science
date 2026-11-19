// Asking Claude about the trace: building the prompt, streaming the answer from the dev server
// (see askClaude.ts), and checking the answer's citations against the app's own text.
import { createContext } from "react";
import type { ClaimTree, Experiment } from "./tree";

// What a question is about: a card, an experiment, selected text, or selected code lines.
export type AskAnchor = { label: string; target?: string; text: string };

// One piece of evidence Claude cites: an app item (`target`) or a trace file (`file`),
// with a quote from it. `valid` says whether the quote was found there; `link` is the app
// item that shows it, if any.
export type Citation = {
  n: number;
  target?: string;
  file?: string;
  quote: string;
  why?: string;
  valid?: boolean;
  link?: string;
};

// Events streamed back by the dev server.
export type AskEvent =
  | { type: "text"; text: string }
  | { type: "tool"; text: string }
  | { type: "done"; sessionId: string; answer: string; citations: Citation[] }
  | { type: "error"; message: string };

// Opens the chat with a question anchored on something.
export const AskContext = createContext<(anchor: AskAnchor) => void>(() => {});

// The text of an experiment's output tab, as the app shows it.
export function outputText(experiment: Experiment): string {
  return [experiment.judgment, JSON.stringify(experiment.summary, null, 2), experiment.log].join("\n\n");
}

// Collapse whitespace so quotes match regardless of line breaks and indentation.
export const normalize = (s: string) => s.replace(/\s+/g, " ").trim();

const unescapeJson = (s: string) =>
  s.replace(/\\n/g, "\n").replace(/\\t/g, "\t").replace(/\\"/g, '"').replace(/\\\\/g, "\\");

// Every app item Claude can cite, by id: its label and (normalized) text.
export type EvidenceIndex = Record<string, { label: string; text: string }>;

export function buildIndex(tree: ClaimTree, labels: Record<string, string>): EvidenceIndex {
  const texts: Record<string, string> = { root: tree.claim };
  for (const sc of tree.subclaims) {
    texts[sc.id] = sc.text;
    for (const e of sc.experiments) {
      texts[`${e.id}:plan`] = e.plan;
      texts[`${e.id}:code`] = e.code;
      texts[`${e.id}:output`] = outputText(e);
    }
    for (const p of sc.papers) texts[p.id] = [p.excerpt, p.why, p.fullText ?? ""].join("\n");
  }
  for (const p of tree.papers) texts[p.id] = [p.excerpt, p.why, p.fullText ?? ""].join("\n");

  const index: EvidenceIndex = {};
  for (const [id, text] of Object.entries(texts)) index[id] = { label: labels[id] ?? id, text: normalize(text) };
  return index;
}

// Check app-item citations (the server already checked file citations), and link file
// citations to an app item that shows the same text, when there is one.
export function checkCitations(citations: Citation[], index: EvidenceIndex): Citation[] {
  return citations.map((c) => {
    const quote = normalize(c.quote ?? "");
    if (c.target) {
      const valid = quote.length > 0 && !!index[c.target]?.text.includes(quote);
      return { ...c, valid, link: index[c.target] ? c.target : undefined };
    }
    if (!c.valid) return c;
    const unescaped = normalize(unescapeJson(c.quote));
    const link = Object.keys(index).find((id) => index[id].text.includes(unescaped));
    return { ...c, link };
  });
}

const CITATION_EXAMPLE = [
  "```citations",
  '[{"n": 1, "target": "515-sc4:code", "quote": "exact text copied from that item", "why": "what it shows"},',
  ' {"n": 2, "file": "sandbox/events.jsonl", "quote": "exact text copied from that file", "why": "what it shows"}]',
  "```",
].join("\n");

// Instructions sent with the first question of a conversation.
function instructions(index: EvidenceIndex): string {
  const items = Object.entries(index).map(([id, { label }]) => `- ${id}: ${label}`);
  return [
    "You are helping a person review the trace of an AI agent that assessed a scientific claim (claim 515).",
    "Your working directory holds the agent's trace files (reports/ and sandbox/). Answer using those files.",
    "The experiment plans, code, and run logs shown in the app come from sandbox/sessions/bbc19fc7c78b.json " +
      "(context.writing_inputs); the paper passages come from sandbox/literature_provenance.json.",
    "",
    "Answer as if the person is not an AI scientist but a computer science Bachelor's graduate who has",
    "gotten rusty over the last 10 years.",
    "",
    "Assume they stepped away from their desk and forgot the details. Start each answer with one or two",
    "sentences that page them back in: which subclaim the question concerns and how it fits into the",
    "overall claim. Then answer.",
    "",
    `The overall claim: ${index.root.text}`,
    "",
    "Write your answer in Markdown. Support factual statements with citations: mark them inline as [1], [2], ...",
    "and end your answer with one fenced block in exactly this form:",
    "",
    CITATION_EXAMPLE,
    "",
    'Each "quote" must be copied exactly from its source; a short phrase or a single line is best.',
    'Use "target" for an item the app shows (listed below) and "file" (a path relative to your working',
    "directory) for anything else. If nothing needs citing, end with an empty list.",
    "",
    "Items the app shows:",
    ...items,
  ].join("\n");
}

export function buildPrompt(question: string, anchor: AskAnchor | null, index: EvidenceIndex, first: boolean): string {
  const parts = first ? [instructions(index), ""] : [];
  if (anchor) {
    parts.push(
      `The person is asking about ${anchor.label}${anchor.target ? ` (app item ${anchor.target})` : ""}:`,
      '"""',
      anchor.text,
      '"""',
      "",
    );
  }
  parts.push(`Question: ${question}`);
  return parts.join("\n");
}

// Send a prompt to the dev server and call `onEvent` for each event as it streams back.
export async function streamAnswer(prompt: string, sessionId: string | undefined, onEvent: (e: AskEvent) => void) {
  const res = await fetch("/api/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt, sessionId }),
  });
  if (!res.ok || !res.body) {
    onEvent({ type: "error", message: `The dev server refused the request (${res.status}).` });
    return;
  }
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop()!;
    for (const line of lines) if (line.trim()) onEvent(JSON.parse(line));
  }
}
