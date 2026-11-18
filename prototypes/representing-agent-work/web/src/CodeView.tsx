import { useContext, useState } from "react";
import { Highlight, themes } from "prism-react-renderer";
import { NotesContext } from "./annotations";

// The DOM id of one code line, so notes can scroll to the lines they're about.
export function lineElementId(target: string, line: number): string {
  return `${target}-L${line}`;
}

// A syntax-highlighted Python listing. Click a line number (shift-click for a range)
// to select lines, then add a note anchored to them. Lines with notes are highlighted.
export default function CodeView({ code, target }: { code: string; target: string }) {
  const { annotations, add } = useContext(NotesContext);
  const [selected, setSelected] = useState<[number, number] | null>(null);

  // Lines that have notes, with those notes' text (shown when hovering the line).
  const notedLines = new Map<number, string[]>();
  for (const a of annotations) {
    if (a.target !== target || !a.anchor || !("lines" in a.anchor)) continue;
    const [start, end] = a.anchor.lines;
    for (let n = start; n <= end; n++) notedLines.set(n, [...(notedLines.get(n) ?? []), a.text]);
  }

  const clickLine = (n: number, extend: boolean) => {
    if (extend && selected) setSelected([Math.min(selected[0], n), Math.max(selected[1], n)]);
    else setSelected([n, n]);
  };

  return (
    <div>
      <div style={{ position: "sticky", top: 0, background: "#fff", padding: "6px 0", zIndex: 1 }}>
        {selected ? (
          <>
            Lines {selected[0]}–{selected[1]} selected{" "}
            <button
              onClick={() => {
                add(target, { lines: selected });
                setSelected(null);
              }}
            >
              Add note on these lines
            </button>{" "}
            <button onClick={() => setSelected(null)}>Clear</button>
          </>
        ) : (
          <span style={{ color: "#666" }}>
            Click a line number to select it (shift-click for a range), then add a note.
          </span>
        )}
      </div>
      <Highlight theme={themes.github} code={code} language="python">
        {({ style, tokens, getLineProps, getTokenProps }) => (
          <pre style={{ ...style, fontSize: 12, overflowX: "auto", padding: "8px 0" }}>
            {tokens.map((line, i) => {
              const n = i + 1;
              const isSelected = selected !== null && n >= selected[0] && n <= selected[1];
              const notes = notedLines.get(n);
              const lineProps = getLineProps({ line });
              return (
                <div
                  key={i}
                  {...lineProps}
                  id={lineElementId(target, n)}
                  title={notes?.join("\n---\n")}
                  style={{ ...lineProps.style, background: isSelected ? "#cfe8ff" : notes ? "#fff3b0" : undefined }}
                >
                  <span
                    onClick={(e) => clickLine(n, e.shiftKey)}
                    style={{
                      display: "inline-block",
                      width: 48,
                      paddingRight: 12,
                      textAlign: "right",
                      color: "#999",
                      cursor: "pointer",
                      userSelect: "none",
                    }}
                  >
                    {n}
                  </span>
                  {line.map((token, key) => (
                    <span key={key} {...getTokenProps({ token })} />
                  ))}
                </div>
              );
            })}
          </pre>
        )}
      </Highlight>
    </div>
  );
}
