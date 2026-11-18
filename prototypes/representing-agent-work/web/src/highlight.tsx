import type { ReactNode } from "react";

// Wrap every occurrence of the given phrases in `text` in <mark> tags.
export function highlight(text: string, phrases: string[]): ReactNode[] {
  const marked = new Array<boolean>(text.length).fill(false);
  for (const phrase of phrases) {
    if (!phrase) continue;
    for (let start = text.indexOf(phrase); start >= 0; start = text.indexOf(phrase, start + 1)) {
      marked.fill(true, start, start + phrase.length);
    }
  }

  // Split the text into runs of marked and unmarked characters.
  const parts: ReactNode[] = [];
  let runStart = 0;
  for (let i = 1; i <= text.length; i++) {
    if (i === text.length || marked[i] !== marked[runStart]) {
      const run = text.slice(runStart, i);
      parts.push(marked[runStart] ? <mark key={runStart}>{run}</mark> : run);
      runStart = i;
    }
  }
  return parts;
}
