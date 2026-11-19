import { useEffect, useState } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  buildPrompt,
  checkCitations,
  streamAnswer,
  type AskAnchor,
  type Citation,
  type EvidenceIndex,
} from "./ask";

type Message =
  | { role: "user"; text: string; anchor: AskAnchor | null }
  | { role: "assistant"; text: string; tools: string[]; citations: Citation[]; done: boolean; error?: string };

// The conversation is kept in localStorage, like notes, so it survives refreshes.
const STORAGE_KEY = "claim515-chat";

function loadChat(): { messages: Message[]; sessionId?: string } {
  try {
    const chat = JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "");
    // An answer still streaming when the page was reloaded won't finish.
    const messages = chat.messages.map((m: Message) =>
      m.role === "assistant" && !m.done ? { ...m, done: true, error: "Interrupted by a page reload." } : m,
    );
    return { ...chat, messages };
  } catch {
    return { messages: [] };
  }
}

type Props = {
  index: EvidenceIndex;
  anchor: AskAnchor | null; // what the next question is about
  onClearAnchor: () => void;
  onOpen: (target: string, quote: string) => void; // show cited evidence in the app
};

function CitationList({ citations, index, onOpen }: { citations: Citation[]; index: EvidenceIndex; onOpen: Props["onOpen"] }) {
  return (
    <ol style={{ paddingLeft: 0, listStyle: "none", fontSize: 14 }}>
      {citations.map((c) => {
        const source = c.target ? index[c.target]?.label ?? c.target : c.file;
        return (
          <li key={c.n} style={{ marginBottom: 8 }}>
            <strong>[{c.n}]</strong> {source}{" "}
            {c.valid ? (
              <span style={{ color: "#2e7d32" }} title="The quote was found in this source">
                ✓
              </span>
            ) : (
              <span style={{ color: "#c62828" }}>⚠ quote not found in this source</span>
            )}
            {c.link && c.valid && (
              <>
                {" "}
                <button onClick={() => onOpen(c.link!, c.quote)}>Show</button>
              </>
            )}
            <blockquote style={{ margin: "4px 0", paddingLeft: 8, borderLeft: "3px solid #ccc", color: "#333" }}>
              {c.quote}
            </blockquote>
            {c.why && <div style={{ color: "#555" }}>{c.why}</div>}
          </li>
        );
      })}
    </ol>
  );
}

// Turn inline citation markers like [1] or [1, 2] into links to "#cite-1", ... (leaving code alone),
// so AnswerText can make them clickable. Only numbers that match a citation are linked.
function linkCitations(text: string, citations: Citation[]): string {
  const numbers = new Set(citations.map((c) => String(c.n)));
  return text
    .split(/(```[\s\S]*?```|`[^`]*`)/) // odd parts are code
    .map((part, i) =>
      i % 2 === 1
        ? part
        : part.replace(/\[(\d+(?:\s*,\s*\d+)*)\]/g, (marker, list: string) => {
            const ns = list.split(",").map((n) => n.trim());
            if (!ns.every((n) => numbers.has(n))) return marker;
            return "[" + ns.map((n) => `[${n}](#cite-${n})`).join(", ") + "]";
          }),
    )
    .join("");
}

// A finished answer as Markdown, with clickable citation markers that show the cited evidence.
function AnswerText({ text, citations, onOpen }: { text: string; citations: Citation[]; onOpen: Props["onOpen"] }) {
  return (
    <Markdown
      remarkPlugins={[remarkGfm]}
      components={{
        a: ({ href, children }) => {
          if (!href?.startsWith("#cite-")) {
            return (
              <a href={href} target="_blank" rel="noreferrer">
                {children}
              </a>
            );
          }
          const c = citations.find((c) => `#cite-${c.n}` === href);
          if (!c?.valid || !c.link) {
            return <span title={c?.valid ? "Not shown in the app; see the list below" : "Quote not found in its source"}>{children}</span>;
          }
          return (
            <a
              href={href}
              title={c.why}
              onClick={(e) => {
                e.preventDefault();
                onOpen(c.link!, c.quote);
              }}
            >
              {children}
            </a>
          );
        },
      }}
    >
      {linkCitations(text, citations)}
    </Markdown>
  );
}

// Chat with Claude about the trace. Answers stream in, then show their checked citations.
export default function ChatPane({ index, anchor, onClearAnchor, onOpen }: Props) {
  const [chat, setChat] = useState(loadChat);
  const [question, setQuestion] = useState("");
  const busy = chat.messages.at(-1)?.role === "assistant" && !(chat.messages.at(-1) as { done: boolean }).done;

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(chat));
    } catch {
      // Storage unavailable: the chat lasts only this session.
    }
  }, [chat]);

  // Update the last (assistant) message as events arrive.
  const updateAnswer = (change: (m: Extract<Message, { role: "assistant" }>) => Partial<Message>) =>
    setChat((c) => {
      const last = c.messages.at(-1) as Extract<Message, { role: "assistant" }>;
      return { ...c, messages: [...c.messages.slice(0, -1), { ...last, ...change(last) } as Message] };
    });

  const send = async () => {
    if (!question.trim() || busy) return;
    const prompt = buildPrompt(question, anchor, index, !chat.sessionId);
    setChat((c) => ({
      ...c,
      messages: [
        ...c.messages,
        { role: "user", text: question, anchor },
        { role: "assistant", text: "", tools: [], citations: [], done: false },
      ],
    }));
    setQuestion("");
    onClearAnchor();

    try {
      await streamAnswer(prompt, chat.sessionId, (e) => {
        if (e.type === "text") updateAnswer((m) => ({ text: m.text + e.text }));
        else if (e.type === "tool") updateAnswer((m) => ({ tools: [...m.tools, e.text] }));
        else if (e.type === "error") updateAnswer(() => ({ error: e.message, done: true }));
        else if (e.type === "done") {
          updateAnswer(() => ({ text: e.answer, citations: checkCitations(e.citations, index), done: true }));
          setChat((c) => ({ ...c, sessionId: e.sessionId }));
        }
      });
    } catch (err) {
      updateAnswer(() => ({ error: String(err), done: true }));
    }
    updateAnswer(() => ({ done: true })); // in case the stream ended without a "done" event
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h2 style={{ margin: "8px 0" }}>Ask Claude</h2>
        <button onClick={() => setChat({ messages: [] })} disabled={busy}>
          New chat
        </button>
      </div>

      <div style={{ flex: 1, overflowY: "auto" }}>
        {chat.messages.length === 0 && (
          <p style={{ color: "#666" }}>
            Ask a question about the trace. Use "Ask Claude" on a card, an experiment, selected text, or
            selected code lines to ask about something specific.
          </p>
        )}
        {chat.messages.map((m, i) =>
          m.role === "user" ? (
            <div key={i} style={{ background: "#eef3fb", borderRadius: 6, padding: "6px 10px", margin: "10px 0" }}>
              {m.anchor && <div style={{ fontSize: 13, color: "#555" }}>About {m.anchor.label}</div>}
              {m.text}
            </div>
          ) : (
            <div key={i}>
              {/* While streaming, hide the citations block Claude writes at the end. */}
              {m.done ? (
                <AnswerText text={m.text} citations={m.citations} onOpen={onOpen} />
              ) : (
                <Markdown remarkPlugins={[remarkGfm]}>{m.text.split("```citations")[0]}</Markdown>
              )}
              {!m.done && (
                <div style={{ color: "#777", fontSize: 13 }}>
                  Claude is working… {m.tools.length > 0 && `(${m.tools.at(-1)!.slice(0, 120)})`}
                </div>
              )}
              {m.error && <div style={{ color: "#c62828" }}>Error: {m.error}</div>}
              {m.done && !m.error && m.citations.length > 0 && (
                <CitationList citations={m.citations} index={index} onOpen={onOpen} />
              )}
            </div>
          ),
        )}
      </div>

      <div style={{ borderTop: "1px solid #ddd", paddingTop: 6 }}>
        {anchor && (
          <div style={{ fontSize: 13, background: "#fff8e1", padding: "2px 8px", marginBottom: 4 }}>
            Asking about {anchor.label} <button onClick={onClearAnchor}>✕</button>
          </div>
        )}
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              send();
            }
          }}
          placeholder="Ask a question (Enter to send, Shift+Enter for a new line)"
          rows={2}
          style={{ width: "100%", boxSizing: "border-box", font: "inherit" }}
          disabled={busy}
        />
      </div>
    </div>
  );
}
