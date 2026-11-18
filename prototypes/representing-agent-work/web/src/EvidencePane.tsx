import { useContext, useRef, useState } from "react";
import type { Experiment, Paper } from "./tree";
import { NotesBlock } from "./NotesPane";
import { NotesContext } from "./annotations";
import CodeView from "./CodeView";
import LatexText from "./latex";

export type Evidence =
  | { kind: "experiment"; experiment: Experiment }
  | { kind: "papers"; label: string; papers: Paper[] };

const preStyle = {
  background: "#f6f8fa",
  padding: 10,
  fontSize: 12,
  overflowX: "auto",
  whiteSpace: "pre",
} as const;

const TABS = ["output", "plan", "code"] as const;
type Tab = (typeof TABS)[number];

function ExperimentView({ experiment }: { experiment: Experiment }) {
  const [tab, setTab] = useState<Tab>("output");
  return (
    <div>
      <h2>Experiment {experiment.id}</h2>
      <p>Agent's verdict: <strong>{experiment.status}</strong></p>
      <div style={{ display: "flex", gap: 6 }}>
        {TABS.map((t) => (
          <button key={t} onClick={() => setTab(t)} style={{ fontWeight: t === tab ? "bold" : "normal" }}>
            {t[0].toUpperCase() + t.slice(1)}
          </button>
        ))}
      </div>

      <h3>Notes on the {tab}</h3>
      <NotesBlock target={`${experiment.id}:${tab}`} />

      {tab === "output" && (
        <>
          <h3>Agent's check of the result</h3>
          <p>{experiment.judgment}</p>
          <h3>Result summary</h3>
          <pre style={preStyle}>{JSON.stringify(experiment.summary, null, 2)}</pre>
          <h3>Run log</h3>
          <pre style={preStyle}>{experiment.log}</pre>
        </>
      )}
      {tab === "plan" && (
        <>
          <h3>Plan</h3>
          <div style={{ whiteSpace: "pre-wrap" }}>{experiment.plan}</div>
        </>
      )}
      {tab === "code" && (
        <>
          <h3>Code</h3>
          <CodeView code={experiment.code} target={`${experiment.id}:code`} />
        </>
      )}
    </div>
  );
}

// One paper: link, why the agent picked it, the excerpt, and (if the trace has it) the full text.
// Select text in the excerpt or full text, then "Note on selected text" to anchor a note to it.
function PaperView({ paper }: { paper: Paper }) {
  const { annotations, add } = useContext(NotesContext);
  const textArea = useRef<HTMLDivElement>(null);
  const quotes = annotations.flatMap((a) =>
    a.target === paper.id && a.anchor && "quote" in a.anchor ? [a.anchor.quote] : [],
  );

  const noteOnSelection = () => {
    const selection = window.getSelection();
    const quote = selection?.toString().trim();
    if (!quote || !textArea.current?.contains(selection!.anchorNode)) {
      alert("First select some text in this paper's excerpt or full text.");
      return;
    }
    add(paper.id, { quote });
  };

  return (
    <section style={{ borderTop: "1px solid #ddd", padding: "12px 0" }}>
      <h3 style={{ fontSize: 16, margin: 0 }}>
        {paper.url ? (
          <a href={paper.url} target="_blank" rel="noreferrer">
            {paper.title}
          </a>
        ) : (
          paper.title
        )}
        {paper.score !== undefined && (
          <span style={{ fontWeight: "normal", color: "#666" }}> · relevance {paper.score}</span>
        )}
      </h3>
      {paper.why && (
        <p>
          <em>Why the agent picked it:</em> {paper.why}
        </p>
      )}
      <div ref={textArea}>
        <blockquote style={{ margin: "8px 0", paddingLeft: 10, borderLeft: "3px solid #ccc", color: "#333" }}>
          <LatexText text={paper.excerpt} quotes={quotes} />
        </blockquote>
        {paper.fullText && (
          <details>
            <summary>Full text</summary>
            <div style={{ whiteSpace: "pre-wrap" }}>
              <LatexText text={paper.fullText} quotes={quotes} />
            </div>
          </details>
        )}
      </div>
      {/* preventDefault keeps the text selection when the button is pressed. */}
      <button onMouseDown={(e) => e.preventDefault()} onClick={noteOnSelection} style={{ marginBottom: 8 }}>
        Note on selected text
      </button>
      <NotesBlock target={paper.id} />
    </section>
  );
}

// Side pane showing one piece of evidence in full.
export default function EvidencePane({ evidence }: { evidence: Evidence }) {
  if (evidence.kind === "experiment") return <ExperimentView key={evidence.experiment.id} experiment={evidence.experiment} />;
  return (
    <div>
      <h2>{evidence.label}</h2>
      {evidence.papers.map((paper) => (
        <PaperView key={paper.id} paper={paper} />
      ))}
    </div>
  );
}
