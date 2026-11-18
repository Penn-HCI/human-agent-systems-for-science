import katex from "katex";
import "katex/dist/katex.min.css";
import { highlight } from "./highlight";

// Math in LaTeX source: $$...$$, \[...\], \(...\), or $...$ (but not an escaped \$).
const MATH = /(\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)|(?<!\\)\$[^$]+?\$)/;

// Tidy up LaTeX commands that appear in ordinary (non-math) text.
function tidy(text: string): string {
  return text
    .replace(/\\(citep|citet|cite|Cref|cref|ref)\{([^}]*)\}/g, "[$2]")
    .replace(/\\(emph|textbf|textit)\{([^}]*)\}/g, "$2")
    .replace(/``/g, "“")
    .replace(/''/g, "”")
    .replace(/~/g, " ")
    .replace(/\\([%$])/g, "$1");
}

function renderMath(source: string): { html: string; display: boolean } {
  const display = source.startsWith("$$") || source.startsWith("\\[");
  const inner = source.startsWith("$") && !source.startsWith("$$") ? source.slice(1, -1) : source.slice(2, -2);
  return { html: katex.renderToString(inner, { displayMode: display, throwOnError: false }), display };
}

// Text that may contain LaTeX: math is rendered with KaTeX, and `quotes` are highlighted in the
// rest of the text (quotes that run into math aren't highlighted).
export default function LatexText({ text, quotes = [] }: { text: string; quotes?: string[] }) {
  // split() with a capturing group alternates: text, math, text, math, ...
  const parts = text.split(MATH);
  return (
    <>
      {parts.map((part, i) => {
        if (i % 2 === 0) return <span key={i}>{highlight(tidy(part), quotes)}</span>;
        const { html, display } = renderMath(part);
        const Tag = display ? "div" : "span";
        return <Tag key={i} dangerouslySetInnerHTML={{ __html: html }} />;
      })}
    </>
  );
}
