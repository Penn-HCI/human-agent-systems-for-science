// Which phrases of the original claim each subclaim corresponds to.
// Hand-written (by Claude Code), not taken from the trace: the trace doesn't record this.
// Each phrase must appear word for word in the claim text.

const decoders = "linear decoders of Qwen2.5-7B-Instruct's final prompt-token residual state identify";
const accuracy = "with at least 90% accuracy each";
const testSet = "On 1,200 held-out file-transfer problems";
const onErrors = "even among incorrect authorization decisions";
const patching = "Patching a fixed set of at most 12 attention heads";

export const CLAIM_SPANS: Record<string, string[]> = {
  sc1: [testSet, decoders, "the requested file", accuracy],
  sc2: [testSet, decoders, "its permitted recipient", accuracy],
  sc3: [decoders, "the requested file", accuracy, onErrors],
  sc4: [decoders, "its permitted recipient", accuracy, onErrors],
  sc5: [
    patching,
    "from correct runs containing the same permission facts in reordered table rows",
    "corrects at least 30% of all initial errors",
  ],
  sc6: [patching, "while changing no more than 3% of correct decisions"],
};
