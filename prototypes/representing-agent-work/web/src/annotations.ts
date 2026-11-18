// Notes the user writes about parts of the view, saved in the browser's localStorage
// so they survive page refreshes. Each note points at an element by id ("root", "sc1", ...),
// so any new kind of element can get notes the same way.
import { createContext, useEffect, useState } from "react";

// What part of an element a note is about: a quoted passage, or a range of code lines.
export type Anchor = { quote: string } | { lines: [number, number] };

export type Annotation = {
  id: string;
  target: string;
  text: string;
  anchor?: Anchor;
};

const STORAGE_KEY = "claim515-annotations";

function loadAnnotations(): Annotation[] {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) ?? "[]");
  } catch {
    return [];
  }
}

export function useAnnotations() {
  const [annotations, setAnnotations] = useState<Annotation[]>(loadAnnotations);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(annotations));
    } catch {
      // Storage can be unavailable (e.g. private windows); notes then last only this session.
    }
  }, [annotations]);

  const add = (target: string, anchor?: Anchor) =>
    setAnnotations((all) => [...all, { id: crypto.randomUUID(), target, text: "", anchor }]);
  const update = (id: string, text: string) =>
    setAnnotations((all) => all.map((a) => (a.id === id ? { ...a, text } : a)));
  const remove = (id: string) => setAnnotations((all) => all.filter((a) => a.id !== id));

  return { annotations, add, update, remove };
}

// Shares the notes (and ways to change them) with any component that shows them.
export const NotesContext = createContext<ReturnType<typeof useAnnotations>>({
  annotations: [],
  add: () => {},
  update: () => {},
  remove: () => {},
});
