// Builds the claim tree, with its evidence, from the claim 515 trace.
// The files are bundled in at build time (`?raw`, `virtual:`), so nothing is fetched at runtime.
import eventsText from "../../data/claim515-results/sandbox/events.jsonl?raw";
import outcomesText from "../../data/claim515-results/sandbox/sessions/20bd60ea8ef7.outcomes.json?raw";
import literatureText from "../../data/claim515-results/sandbox/literature_provenance.json?raw";
import writingInputs from "virtual:writing-inputs";

export type Status = "supported" | "not supported" | "unrun";

export interface Experiment {
  id: string; // e.g. "515-sc4"
  status: Status; // the agent's judgment of this experiment's result
  judgment: string; // the agent's reasoning when it checked the result
  plan: string;
  code: string;
  log: string;
  summary: Record<string, unknown>;
}

export interface Paper {
  id: string;
  title: string;
  url?: string;
  excerpt: string;
  why: string; // why the agent thought the passage was relevant
  score?: number; // the agent's relevance score
  fullText?: string;
}

export interface Subclaim {
  id: string;
  text: string;
  bottleneck: boolean;
  relation: string;
  status: Status;
  experiments: Experiment[];
  papers: Paper[];
}

export interface Score {
  likert: number;
  confidence: number;
}

export interface ClaimTree {
  claim: string;
  before: Score;
  after: Score;
  subclaims: Subclaim[];
  papers: Paper[]; // papers about the claim as a whole, not one subclaim
}

interface TraceEvent {
  event: string;
  payload: any;
}

interface Judgment {
  proposition_id: string;
  result_id: string;
  supersedes: string | null;
  conclusion: string;
  measurement_disposition: string;
  reason: string;
}

// Payload of the last event with this name (the final run comes last).
function lastPayload(events: TraceEvent[], name: string): any {
  return events.filter((e) => e.event === name).at(-1)!.payload;
}

function judgmentStatus(j: Judgment): Status {
  if (j.measurement_disposition !== "usable") return "unrun";
  if (j.conclusion.includes("NOT")) return "not supported";
  return "supported";
}

// The agent's final judgment of a subclaim, ignoring superseded results.
function subclaimStatus(judgments: Judgment[]): Status {
  const superseded = new Set(judgments.map((j) => j.supersedes));
  return judgmentStatus(judgments.filter((j) => !superseded.has(j.result_id)).at(-1)!);
}

function locatorUrl(locator: string): string | undefined {
  if (locator.startsWith("arxiv:")) return `https://arxiv.org/abs/${locator.slice(6)}`;
  if (locator.startsWith("doi:")) return `https://doi.org/${locator.slice(4)}`;
  if (locator.startsWith("http")) return locator;
}

// Passages found by the literature search, keyed by the subclaim they were found for
// ("claim", "method", ... for searches about the claim as a whole).
function loadLiterature(): { scope: string; paper: Paper }[] {
  return JSON.parse(literatureText).map((e: any) => ({
    scope: e.subclaim_id,
    paper: {
      id: e.evidence_ref.id,
      title: e.locator,
      url: locatorUrl(e.locator),
      // 11 passages were recorded without their text.
      excerpt: e.matched_text ?? "(The trace doesn't include the text of this passage.)",
      why: e.relevance_summary ?? "",
      score: e.relevance_score,
    },
  }));
}

// Sources the report writer found with its own web searches.
function loadWebSources(): Paper[] {
  return Object.entries(writingInputs.sources)
    .filter(([key]) => key.startsWith("web_"))
    .map(([key, s]) => ({
      id: key,
      title: s.title ?? key.slice(4).replaceAll("_", " "),
      url: s.source?.trim(),
      excerpt: s.citation ?? "",
      why: s.why ?? "",
      fullText: writingInputs.fulltext[key]?.text,
    }));
}

export function loadTree(): ClaimTree {
  const events: TraceEvent[] = eventsText
    .split("\n")
    .filter((line) => line.trim())
    .map((line) => JSON.parse(line));
  const outcomes = JSON.parse(outcomesText);

  // The agent's judgments of each experiment's result, recorded after its experiments.
  const judgments: Judgment[] = [];
  for (const action of outcomes.actions) {
    for (const check of action.checked ?? []) {
      if (check.obligation.startsWith("judgment.")) judgments.push(...check.basis.judgments);
    }
  }

  // Each experiment the agent designed, e.g. "515-sc4" (artifacts key "sc4", results key "4").
  const experiments = writingInputs.designs.map((design) => {
    const key = design.uid.replace("515-", "");
    const judgment = judgments.find((j) => j.result_id === design.uid)!;
    const experiment: Experiment = {
      id: design.uid,
      status: judgmentStatus(judgment),
      judgment: judgment.reason,
      plan: design.plan,
      code: writingInputs.artifacts[key].script,
      log: writingInputs.artifacts[key].log,
      summary: writingInputs.summaries[key.replace("sc", "")],
    };
    return { subclaims: design.subclaims, experiment };
  });

  const literature = loadLiterature();
  const subclaimIds = new Set<string>();

  const subclaims: Subclaim[] = lastPayload(events, "decomposition").subclaims.map((sc: any) => {
    subclaimIds.add(sc.id);
    return {
      id: sc.id,
      text: sc.text,
      bottleneck: sc.bottleneck,
      relation: sc.relation,
      status: subclaimStatus(judgments.filter((j) => j.proposition_id === sc.id)),
      experiments: experiments.filter((e) => e.subclaims.includes(sc.id)).map((e) => e.experiment),
      papers: literature.filter((l) => l.scope === sc.id).map((l) => l.paper),
    };
  });

  const before = lastPayload(events, "likert_estimated");
  const after = lastPayload(events, "assessment_final");
  return {
    claim: lastPayload(events, "run_started").claim_text,
    before: { likert: before.likert, confidence: before.confidence },
    after: { likert: after.likert_score, confidence: after.confidence },
    subclaims,
    papers: [
      ...literature.filter((l) => !subclaimIds.has(l.scope)).map((l) => l.paper),
      ...loadWebSources(),
    ],
  };
}
