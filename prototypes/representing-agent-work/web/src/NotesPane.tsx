import { useContext } from "react";
import { NotesContext, type Anchor } from "./annotations";
import { lineElementId } from "./CodeView";

// Shows what part of an element a note is anchored to. Line anchors scroll to their lines
// (when the code is open).
function AnchorLabel({ target, anchor }: { target: string; anchor: Anchor }) {
  if ("quote" in anchor) {
    const quote = anchor.quote.length > 200 ? anchor.quote.slice(0, 200) + "…" : anchor.quote;
    return <div style={{ color: "#555", fontStyle: "italic", marginBottom: 4 }}>“{quote}”</div>;
  }
  const [start, end] = anchor.lines;
  const scrollToLines = () =>
    document.getElementById(lineElementId(target, start))?.scrollIntoView({ block: "center" });
  return (
    <button onClick={scrollToLines} style={{ marginBottom: 4 }}>
      Lines {start}–{end}
    </button>
  );
}

// The notes about one element, editable, with a button to add another.
export function NotesBlock({ target }: { target: string }) {
  const { annotations, add, update, remove } = useContext(NotesContext);
  return (
    <div>
      {annotations
        .filter((a) => a.target === target)
        .map((a) => (
          <div key={a.id} style={{ marginBottom: 8 }}>
            {a.anchor && <AnchorLabel target={target} anchor={a.anchor} />}
            <textarea
              value={a.text}
              onChange={(e) => update(a.id, e.target.value)}
              autoFocus={a.text === ""}
              rows={3}
              style={{ width: "100%", boxSizing: "border-box", font: "inherit" }}
            />
            <button onClick={() => remove(a.id)}>Delete</button>
          </div>
        ))}
      <button onClick={() => add(target)}>Add note</button>
    </div>
  );
}

// Every element that has notes, with its notes. `labels` names each element.
export default function NotesPane({ labels }: { labels: Record<string, string> }) {
  const { annotations } = useContext(NotesContext);
  const targets = [...new Set(annotations.map((a) => a.target))];
  return (
    <div>
      <h2>All notes</h2>
      {targets.length === 0 && <p>No notes yet. Use "Add note" on any card or piece of evidence.</p>}
      {targets.map((target) => (
        <section key={target} style={{ marginBottom: 20 }}>
          <h3 style={{ fontSize: 15, marginBottom: 6 }}>{labels[target] ?? target}</h3>
          <NotesBlock target={target} />
        </section>
      ))}
    </div>
  );
}
