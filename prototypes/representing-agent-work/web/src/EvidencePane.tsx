import { useContext, useEffect, useRef, useState } from "react";
import type { Experiment, Paper } from "./tree";
import { NotesBlock } from "./NotesPane";
import { NotesContext, quotesFor } from "./annotations";
import { AskContext } from "./ask";
import CodeView, { quoteLines } from "./CodeView";
import LatexText from "./latex";
import Selectable from "./Selectable";
import { highlight } from "./highlight";

export type Evidence =
  | { kind: "experiment"; experiment: Experiment }
  | { kind: "papers"; label: string; papers: Paper[] };

// A passage to show and highlight, e.g. when a citation in the chat is clicked.
export type Focus = { target: string; quote: string };

const preStyle = {
  background: "#f6f8fa",
  padding: 10,
  fontSize: 12,
  overflowX: "auto",
  whiteSpace: "pre",
} as const;

const TABS = ["output", "plan", "code"] as const;
type Tab = (typeof TABS)[number];

// Scroll to the first highlight inside `container` that is part of the focused quote.
function scrollToFocus(container: HTMLElement | null, focus: Focus | undefined) {
  const marks = [...(container?.querySelectorAll("mark") ?? [])];
  marks.find((m) => focus?.quote.includes(m.textContent ?? ""))?.scrollIntoView({ block: "center" });
}

function ExperimentView({ experiment, focus }: { experiment: Experiment; focus?: Focus }) {
  const { annotations } = useContext(NotesContext);
  const ask = useContext(AskContext);
  const focusTab = TABS.find((t) => focus?.target === `${experiment.id}:${t}`);
  const [tab, setTab] = useState<Tab>(focusTab ?? "output");
  const content = useRef<HTMLDivElement>(null);

  // Switch to the focused tab and scroll to the focused passage.
  useEffect(() => {
    if (focusTab) setTab(focusTab);
  }, [focus, focusTab]);
  useEffect(() => scrollToFocus(content.current, focus), [focus, tab]);

  const target = `${experiment.id}:${tab}`;
  const quotes = [...quotesFor(annotations, target), ...(focus?.target === target ? [focus.quote] : [])];
  const label = `the ${tab} of experiment ${experiment.id}`;

  return (
    <div>
      <h2>Experiment {experiment.id}</h2>
      <p>
        Agent's verdict: <strong>{experiment.status}</strong>{" "}
        <button
          onClick={() =>
            ask({
              label: `experiment ${experiment.id}`,
              target: `${experiment.id}:output`,
              text: [experiment.judgment, JSON.stringify(experiment.summary, null, 2)].join("\n\n"),
            })
          }
        >
          Ask Claude about this experiment
        </button>
      </p>
      <div style={{ display: "flex", gap: 6 }}>
        {TABS.map((t) => (
          <button key={t} onClick={() => setTab(t)} style={{ fontWeight: t === tab ? "bold" : "normal" }}>
            {t[0].toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      <h3>Notes on the {tab}</h3>
      <NotesBlock target={target} />

      <div ref={content}>
        {tab === "output" && (
          <Selectable target={target} label={label}>
            <h3>Agent's check of the result</h3>
            <p>{highlight(experiment.judgment, quotes)}</p>
            <h3>Result summary</h3>
            <pre style={preStyle}>{highlight(JSON.stringify(experiment.summary, null, 2), quotes)}</pre>
            <h3>Run log</h3>
            <pre style={preStyle}>{highlight(experiment.log, quotes)}</pre>
          </Selectable>
        )}
        {tab === "plan" && (
          <Selectable target={target} label={label}>
            <h3>Plan</h3>
            <div style={{ whiteSpace: "pre-wrap" }}>{highlight(experiment.plan, quotes)}</div>
          </Selectable>
        )}
        {tab === "code" && (
          <>
            <h3>Code</h3>
            <CodeView
              code={experiment.code}
              target={target}
              label={label}
              focusLines={focus?.target === target ? quoteLines(experiment.code, focus.quote) : undefined}
            />
          </>
        )}
      </div>
    </div>
  );
}

// One paper: the excerpt, why the agent picked it, the link, and (if the trace has it) the full text.
// Selecting text pops up buttons to comment on it or ask Claude about it.
function PaperView({ paper, focusQuote }: { paper: Paper; focusQuote?: string }) {
  const { annotations } = useContext(NotesContext);
  const section = useRef<HTMLElement>(null);
  const quotes = [...quotesFor(annotations, paper.id), ...(focusQuote ? [focusQuote] : [])];

  // Scroll to this paper (and the focused passage in it) when it's focused.
  useEffect(() => {
    if (!focusQuote) return;
    section.current?.scrollIntoView({ block: "start" });
    scrollToFocus(section.current, { target: paper.id, quote: focusQuote });
  }, [focusQuote, paper.id]);

  return (
    <section ref={section} style={{ borderTop: "1px solid #ddd", padding: "12px 0" }}>
      <Selectable target={paper.id} label={`paper ${paper.title}`}>
        <blockquote style={{ margin: "0 0 8px", paddingLeft: 10, borderLeft: "3px solid #ccc", color: "#333" }}>
          <LatexText text={paper.excerpt} quotes={quotes} />
        </blockquote>
        {paper.why && (
          <p style={{ margin: "0 0 8px" }}>
            <em>Why the agent picked it:</em> {highlight(paper.why, quotes)}
          </p>
        )}
        <div style={{ marginBottom: 8 }}>
          {paper.url ? (
            <a href={paper.url} target="_blank" rel="noreferrer">
              {paper.title}
            </a>
          ) : (
            paper.title
          )}
          {paper.score !== undefined && <span style={{ color: "#666" }}> · relevance {paper.score}</span>}
        </div>
        {paper.fullText && (
          // Opened automatically when a focused passage is only in the full text.
          <details open={(focusQuote && !paper.excerpt.includes(focusQuote)) || undefined} style={{ marginBottom: 8 }}>
            <summary>Full text</summary>
            <div style={{ whiteSpace: "pre-wrap" }}>
              <LatexText text={paper.fullText} quotes={quotes} />
            </div>
          </details>
        )}
      </Selectable>
      <NotesBlock target={paper.id} />
    </section>
  );
}

// Pane showing one piece of evidence in full, optionally scrolled to a focused passage.
export default function EvidencePane({ evidence, focus }: { evidence: Evidence; focus?: Focus }) {
  if (evidence.kind === "experiment") {
    return <ExperimentView key={evidence.experiment.id} experiment={evidence.experiment} focus={focus} />;
  }
  return (
    <div>
      <h2>{evidence.label}</h2>
      {evidence.papers.map((paper) => (
        <PaperView key={paper.id} paper={paper} focusQuote={focus?.target === paper.id ? focus.quote : undefined} />
      ))}
    </div>
  );
}
