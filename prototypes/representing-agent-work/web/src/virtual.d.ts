// Provided by the writingInputs() plugin in vite.config.ts.
declare module "virtual:writing-inputs" {
  const inputs: {
    designs: { uid: string; subclaims: string[]; plan: string }[];
    artifacts: Record<string, { script: string; log: string }>;
    summaries: Record<string, Record<string, unknown>>;
    sources: Record<string, { source?: string; citation?: string; why?: string; title?: string }>;
    fulltext: Record<string, { text: string }>;
  };
  export default inputs;
}
