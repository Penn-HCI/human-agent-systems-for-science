import { useContext, useEffect, useRef, useState, type ReactNode } from "react";
import { NotesContext } from "./annotations";
import { AskContext } from "./ask";

// Wraps text so that selecting part of it pops up buttons to comment on the selection
// (a note anchored to it) or ask Claude about it. `target` is the element the notes belong to.
export default function Selectable({ target, label, children }: { target: string; label: string; children: ReactNode }) {
  const { add } = useContext(NotesContext);
  const ask = useContext(AskContext);
  const box = useRef<HTMLDivElement>(null);
  const [widget, setWidget] = useState<{ quote: string; top: number; left: number } | null>(null);

  // Returns the selected text if the selection is inside this box, else null.
  const selectedQuote = (): string | null => {
    const selection = window.getSelection();
    const quote = selection?.toString().trim();
    return quote && box.current?.contains(selection!.anchorNode) ? quote : null;
  };

  // After a drag, show the buttons just below the selection.
  const showWidget = () => {
    const quote = selectedQuote();
    if (!quote) return setWidget(null);
    const rect = window.getSelection()!.getRangeAt(0).getBoundingClientRect();
    const boxRect = box.current!.getBoundingClientRect();
    setWidget({ quote, top: rect.bottom - boxRect.top + 4, left: rect.left - boxRect.left });
  };

  // Hide the buttons once the selection is cleared or moves elsewhere.
  useEffect(() => {
    const hideIfDeselected = () => {
      if (!selectedQuote()) setWidget(null);
    };
    document.addEventListener("selectionchange", hideIfDeselected);
    return () => document.removeEventListener("selectionchange", hideIfDeselected);
  }, []);

  const finish = () => {
    window.getSelection()?.removeAllRanges();
    setWidget(null);
  };

  return (
    <div ref={box} onMouseUp={showWidget} style={{ position: "relative" }}>
      {children}
      {widget && (
        // preventDefault keeps the text selected while a button is pressed.
        <div style={{ position: "absolute", top: widget.top, left: widget.left, zIndex: 2, display: "flex", gap: 4 }}>
          <button
            onMouseDown={(e) => e.preventDefault()}
            onClick={() => {
              add(target, { quote: widget.quote });
              finish();
            }}
          >
            Add comment
          </button>
          <button
            onMouseDown={(e) => e.preventDefault()}
            onClick={() => {
              ask({ label: `selected text from ${label}`, target, text: widget.quote });
              finish();
            }}
          >
            Ask Claude
          </button>
        </div>
      )}
    </div>
  );
}
