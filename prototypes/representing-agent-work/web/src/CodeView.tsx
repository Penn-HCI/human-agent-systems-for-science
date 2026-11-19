import { Fragment, useContext, useEffect, useState } from "react";
import { Highlight, themes } from "prism-react-renderer";
import { NotesContext } from "./annotations";
import { AskContext } from "./ask";

// The DOM id of one code line, so notes can scroll to the lines they're about.
export function lineElementId(target: string, line: number): string {
  return `${target}-L${line}`;
}

// A note shown under the lines it's about: one line at first, click to see all of it.
function InlineNote({ text }: { text: string }) {
  const [open, setOpen] = useState(false);
  return (
    <div
      onClick={() => setOpen(!open)}
      style={{
        margin: "2px 0 4px 60px",
        padding: "2px 8px",
        background: "#fff8c4",
        borderLeft: "3px solid #e0b800",
        fontFamily: "system-ui, sans-serif",
        fontSize: 13,
        cursor: "pointer",
        whiteSpace: open ? "pre-wrap" : "nowrap",
        overflow: "hidden",
        textOverflow: "ellipsis",
      }}
    >
      💬 {text || "(empty note)"}
    </div>
  );
}

// The lines of `code` that a quote (e.g. from a citation) covers, found by its first line.
export function quoteLines(code: string, quote: string): [number, number] | undefined {
  const quoteLineList = quote.trim().split("\n");
  const at = code.indexOf(quoteLineList[0].trim());
  if (!quoteLineList[0].trim() || at < 0) return undefined;
  const start = code.slice(0, at).split("\n").length;
  return [start, start + quoteLineList.length - 1];
}

type Props = {
  code: string;
  target: string; // the id notes on this code are attached to
  label: string; // what to call this code when asking Claude
  focusLines?: [number, number]; // lines to highlight and scroll to (e.g. a cited passage)
};

// A syntax-highlighted Python listing. Click a line number (shift-click for a range)
// to select lines, then add a note anchored to them or ask Claude about them.
// Lines with notes are highlighted yellow; focused lines green.
export default function CodeView({ code, target, label, focusLines }: Props) {
  const { annotations, add } = useContext(NotesContext);
  const ask = useContext(AskContext);
  const [selected, setSelected] = useState<[number, number] | null>(null);

  // Scroll to the focused lines when they change.
  useEffect(() => {
    if (focusLines) document.getElementById(lineElementId(target, focusLines[0]))?.scrollIntoView({ block: "center" });
  }, [focusLines?.[0], target]);

  const askAboutSelection = ([start, end]: [number, number]) => {
    const numbered = code
      .split("\n")
      .slice(start - 1, end)
      .map((line, i) => `${start + i}: ${line}`);
    ask({ label: `${label}, lines ${start}–${end}`, target, text: numbered.join("\n") });
    setSelected(null);
  };

  // Lines that have notes, with those notes' text (shown when hovering the line),
  // and the notes to show under the last line of their range.
  const notedLines = new Map<number, string[]>();
  const notesAfterLine = new Map<number, string[]>();
  for (const a of annotations) {
    if (a.target !== target || !a.anchor || !("lines" in a.anchor)) continue;
    const [start, end] = a.anchor.lines;
    for (let n = start; n <= end; n++) notedLines.set(n, [...(notedLines.get(n) ?? []), a.text]);
    notesAfterLine.set(end, [...(notesAfterLine.get(end) ?? []), a.text]);
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
            <button onClick={() => askAboutSelection(selected)}>Ask Claude about these lines</button>{" "}
            <button onClick={() => setSelected(null)}>Clear</button>
          </>
        ) : (
          <span style={{ color: "#666" }}>
            Click a line number to select it (shift-click for a range), then add a note or ask Claude.
          </span>
        )}
      </div>
      <Highlight theme={themes.github} code={code} language="python">
        {({ style, tokens, getLineProps, getTokenProps }) => (
          <pre style={{ ...style, fontSize: 12, overflowX: "auto", padding: "8px 0" }}>
            {tokens.map((line, i) => {
              const n = i + 1;
              const isSelected = selected !== null && n >= selected[0] && n <= selected[1];
              const isFocused = focusLines !== undefined && n >= focusLines[0] && n <= focusLines[1];
              const notes = notedLines.get(n);
              const lineProps = getLineProps({ line });
              return (
                <Fragment key={i}>
                  <div
                    {...lineProps}
                    id={lineElementId(target, n)}
                    title={notes?.join("\n---\n")}
                    style={{ ...lineProps.style, background: isSelected ? "#cfe8ff" : isFocused ? "#c8f7c5" : notes ? "#fff3b0" : undefined }}
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
                  {notesAfterLine.get(n)?.map((text, j) => <InlineNote key={j} text={text} />)}
                </Fragment>
              );
            })}
          </pre>
        )}
      </Highlight>
    </div>
  );
}
