import { readFileSync } from "node:fs";
import { defineConfig, type Plugin } from "vite";
import react from "@vitejs/plugin-react";

const WRITER_SESSION = "../data/claim515-results/sandbox/sessions/bbc19fc7c78b.json";

// The writer's session file is ~50 MB, too big to send to the browser. This plugin reads it
// when the app is built and passes along only the parts the app uses, as `virtual:writing-inputs`.
function writingInputs(): Plugin {
  const id = "virtual:writing-inputs";
  return {
    name: "writing-inputs",
    resolveId: (source) => (source === id ? "\0" + id : null),
    load(loadId) {
      if (loadId !== "\0" + id) return null;
      const inputs = JSON.parse(readFileSync(WRITER_SESSION, "utf8")).context.writing_inputs;
      const summaries = Object.fromEntries(
        Object.entries(inputs.results).map(([key, result]: [string, any]) => [key, result.summary]),
      );
      const picked = {
        designs: inputs.designs,
        artifacts: inputs.artifacts,
        summaries,
        sources: inputs.sources,
        fulltext: inputs.fulltext,
      };
      return `export default ${JSON.stringify(picked)};`;
    },
  };
}

export default defineConfig({
  plugins: [react(), writingInputs()],
  // The trace data lives one folder up, in ../data.
  server: { fs: { allow: [".."] } },
});
