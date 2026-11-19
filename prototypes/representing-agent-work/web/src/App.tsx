import { createContext, useContext, useEffect, useState } from "react";
import dagre from "@dagrejs/dagre";
import {
  ReactFlow,
  ReactFlowProvider,
  Controls,
  Handle,
  NodeToolbar,
  Position,
  useNodesState,
  useEdgesState,
  useNodesInitialized,
  useReactFlow,
  type Node,
  type Edge,
  type NodeProps,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { loadTree, type ClaimTree, type Paper, type Score, type Status } from "./tree";
import { CLAIM_SPANS } from "./claimSpans";
import { highlight } from "./highlight";
import { NotesContext, anchorSummary, useAnnotations } from "./annotations";
import NotesPane from "./NotesPane";
import EvidencePane, { type Evidence, type Focus } from "./EvidencePane";
import ChatPane from "./ChatPane";
import { AskContext, buildIndex, type AskAnchor } from "./ask";

const STATUS_COLORS: Record<Status, string> = {
  supported: "#c8e6c9",
  "not supported": "#ffcdd2",
  unrun: "#e0e0e0",
};

// What the right-hand pane shows: all notes, one piece of evidence, or nothing.
type Panel = { kind: "notes" } | { kind: "evidence"; evidence: Evidence; focus?: Focus } | null;
const SetPanel = createContext<(panel: Panel) => void>(() => {});

type ClaimNodeData = {
  title: string;
  details: string[];
  text?: string;
  color: string;
  width: number;
  bottleneck: boolean;
};
type ClaimNode = Node<ClaimNodeData, "claim">;

type EvidenceNodeData = {
  title: string;
  details: string[];
  color: string;
  evidence: Evidence;
  noteTargets: string[]; // the ids its notes are attached to (e.g. each paper)
};
type EvidenceNode = Node<EvidenceNodeData, "evidence">;

type TreeNode = ClaimNode | EvidenceNode;

// The subclaim currently hovered or selected, if any.
const ActiveSubclaim = createContext<string | null>(null);

function noteCountText(count: number): string {
  return `${count} ${count === 1 ? "note" : "notes"}`;
}

// A one-line preview of the notes on a card. Clicking it opens all the notes in a popover
// below the card. The line is always shown so cards keep the same size (and layout) as notes change.
function NotesPreview({ targets }: { targets: string[] }) {
  const { annotations } = useContext(NotesContext);
  const [open, setOpen] = useState(false);
  const notes = annotations.filter((a) => targets.includes(a.target));
  const lineStyle = { marginTop: 6, fontSize: 13, color: "#555" } as const;
  if (notes.length === 0) return <div style={lineStyle}>No notes yet</div>;

  return (
    <>
      <div
        className="nodrag"
        onClick={(e) => {
          e.stopPropagation(); // don't also open the evidence pane
          setOpen(!open);
        }}
        style={{ ...lineStyle, cursor: "pointer", whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}
      >
        {open ? "▾" : "▸"} {noteCountText(notes.length)}: {notes.at(-1)!.text || "(empty)"}
      </div>
      {/* NodeToolbar draws above all cards, so opening it doesn't disturb the layout. */}
      <NodeToolbar isVisible={open} position={Position.Bottom}>
        <div
          className="nowheel"
          style={{
            width: 340,
            maxHeight: 300,
            overflowY: "auto",
            background: "#fffde7",
            border: "1px solid #bbb",
            borderRadius: 6,
            padding: 10,
            fontSize: 14,
            lineHeight: 1.5,
          }}
        >
          {notes.map((a) => (
            <div key={a.id} style={{ marginBottom: 10 }}>
              {targets.length > 1 && <div style={{ color: "#777", fontSize: 12 }}>{noteLabels[a.target]}</div>}
              {a.anchor && <div style={{ color: "#555", fontStyle: "italic" }}>{anchorSummary(a.anchor)}</div>}
              <div style={{ whiteSpace: "pre-wrap" }}>{a.text || "(empty)"}</div>
            </div>
          ))}
        </div>
      </NodeToolbar>
    </>
  );
}

// The claim or a subclaim: a bold title, a few detail lines, (for the claim) its text, then notes.
function ClaimNodeView({ id, data }: NodeProps<ClaimNode>) {
  const active = useContext(ActiveSubclaim);
  const phrases = active ? CLAIM_SPANS[active] ?? [] : [];
  const { add } = useContext(NotesContext);
  const setPanel = useContext(SetPanel);
  const ask = useContext(AskContext);
  return (
    <div
      style={{
        width: data.width,
        padding: 14,
        background: data.color,
        border: `${data.bottleneck ? 4 : 1}px solid #555`,
        borderRadius: 8,
        fontSize: 16,
        lineHeight: 1.5,
      }}
    >
      <Handle type="target" position={Position.Left} style={{ opacity: 0 }} />
      <strong>{data.title}</strong>
      {data.details.map((line) => (
        <div key={line} style={{ color: "#444", marginTop: 6 }}>
          {line}
        </div>
      ))}
      {data.text && <p style={{ margin: "10px 0 0" }}>{highlight(data.text, phrases)}</p>}
      <div style={{ marginTop: 10, fontSize: 14, color: "#444" }}>
        {/* "nodrag" stops React Flow from treating the click as dragging the card. */}
        <button
          className="nodrag"
          onClick={() => {
            add(id);
            setPanel({ kind: "notes" });
          }}
        >
          Add note
        </button>{" "}
        <button
          className="nodrag"
          onClick={() =>
            ask({
              label: id === "root" ? "the claim" : `subclaim ${id}`,
              target: id,
              text: [data.title, ...data.details, data.text ?? ""].join("\n"),
            })
          }
        >
          Ask Claude
        </button>
        <NotesPreview targets={[id]} />
      </div>
      <Handle type="source" position={Position.Right} style={{ opacity: 0 }} />
    </div>
  );
}

// An experiment or a group of papers. Clicking it opens the evidence pane.
function EvidenceNodeView({ data }: NodeProps<EvidenceNode>) {
  return (
    <div
      style={{
        width: 220,
        padding: 10,
        background: data.color,
        border: "1px solid #888",
        borderRadius: 6,
        fontSize: 15,
        lineHeight: 1.45,
        cursor: "pointer",
      }}
    >
      <Handle type="target" position={Position.Left} style={{ opacity: 0 }} />
      <strong>{data.title}</strong>
      {data.details.map((line) => (
        <div key={line} style={{ color: "#444", marginTop: 4 }}>
          {line}
        </div>
      ))}
      <div style={{ marginTop: 6, fontSize: 13, color: "#666" }}>Click to open</div>
      <NotesPreview targets={data.noteTargets} />
    </div>
  );
}

const nodeTypes = { claim: ClaimNodeView, evidence: EvidenceNodeView };

function formatScore(score: Score): string {
  const sign = score.likert > 0 ? "+" : "";
  return `${sign}${score.likert} (confidence ${score.confidence.toFixed(2)})`;
}

const NOTE_TABS = ["output", "plan", "code"];

function papersNode(id: string, label: string, papers: Paper[]): EvidenceNode {
  return {
    id,
    type: "evidence",
    position: { x: 0, y: 0 },
    data: {
      title: `Papers (${papers.length})`,
      details: [`Passages the agent retrieved ${label}`],
      color: "#fff8e1",
      evidence: { kind: "papers", label: `Papers ${label}`, papers },
      noteTargets: papers.map((p) => p.id),
    },
  };
}

// Nodes start at (0, 0); layoutNodes() positions them once their sizes are known.
function toFlow(tree: ClaimTree): { nodes: TreeNode[]; edges: Edge[] } {
  const nodes: TreeNode[] = [
    {
      id: "root",
      type: "claim",
      position: { x: 0, y: 0 },
      data: {
        title: "Claim",
        details: [
          `Agent's score (-2 to +2) before exploration: ${formatScore(tree.before)}`,
          `Agent's score after exploration: ${formatScore(tree.after)}`,
        ],
        text: tree.claim,
        color: "#e3f2fd",
        width: 560,
        bottleneck: false,
      },
    },
    papersNode("papers:root", "about the claim as a whole", tree.papers),
  ];
  const edges: Edge[] = [{ id: "root-papers", source: "root", target: "papers:root" }];

  for (const sc of tree.subclaims) {
    nodes.push({
      id: sc.id,
      type: "claim",
      position: { x: 0, y: 0 },
      data: {
        title: sc.text,
        details: [`${sc.id}${sc.bottleneck ? " (bottleneck)" : ""} · Agent's verdict: ${sc.status}`],
        color: STATUS_COLORS[sc.status],
        width: 240,
        bottleneck: sc.bottleneck,
      },
    });
    edges.push({ id: `root-${sc.id}`, source: "root", target: sc.id, label: sc.relation, type: "smoothstep" });

    for (const experiment of sc.experiments) {
      nodes.push({
        id: experiment.id,
        type: "evidence",
        position: { x: 0, y: 0 },
        data: {
          title: `Experiment ${experiment.id}`,
          details: [`Agent's verdict: ${experiment.status}`],
          color: STATUS_COLORS[experiment.status],
          evidence: { kind: "experiment", experiment },
          noteTargets: NOTE_TABS.map((tab) => `${experiment.id}:${tab}`),
        },
      });
      edges.push({ id: `${sc.id}-${experiment.id}`, source: sc.id, target: experiment.id });
    }

    nodes.push(papersNode(`papers:${sc.id}`, `for ${sc.id}`, sc.papers));
    edges.push({ id: `${sc.id}-papers`, source: sc.id, target: `papers:${sc.id}` });
  }
  return { nodes, edges };
}

// Position nodes left-to-right with dagre, using each node's rendered size.
function layoutNodes(nodes: TreeNode[], edges: Edge[]): TreeNode[] {
  const g = new dagre.graphlib.Graph();
  g.setGraph({ rankdir: "LR", nodesep: 12, ranksep: 60 });
  g.setDefaultEdgeLabel(() => ({}));
  for (const node of nodes) {
    g.setNode(node.id, { width: node.measured?.width ?? 0, height: node.measured?.height ?? 0 });
  }
  for (const edge of edges) {
    g.setEdge(edge.source, edge.target);
  }
  dagre.layout(g);

  // dagre gives node centers; React Flow wants top-left corners.
  return nodes.map((node) => {
    const { x, y, width, height } = g.node(node.id);
    return { ...node, position: { x: x - width / 2, y: y - height / 2 } };
  });
}

const tree = loadTree();
const initial = toFlow(tree);

// A readable name for everything that can have notes, for the notes pane.
const noteLabels: Record<string, string> = { root: "Claim" };
for (const sc of tree.subclaims) {
  noteLabels[sc.id] = `${sc.id}: ${sc.text}`;
  for (const experiment of sc.experiments) {
    for (const tab of NOTE_TABS) noteLabels[`${experiment.id}:${tab}`] = `Experiment ${experiment.id} · ${tab}`;
  }
  for (const paper of sc.papers) noteLabels[paper.id] = `Paper ${paper.title} (for ${sc.id})`;
}
for (const paper of tree.papers) noteLabels[paper.id] = `Paper ${paper.title} (whole claim)`;

// Every app item Claude can cite, and the evidence pane that shows each one.
const evidenceIndex = buildIndex(tree, noteLabels);
const evidenceFor: Record<string, Evidence> = {};
for (const node of initial.nodes) {
  if (node.type !== "evidence") continue;
  const evidence = node.data.evidence;
  if (evidence.kind === "experiment") {
    for (const tab of NOTE_TABS) evidenceFor[`${evidence.experiment.id}:${tab}`] = evidence;
  } else {
    for (const paper of evidence.papers) evidenceFor[paper.id] = evidence;
  }
}

function ClaimTreeGraph() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initial.nodes);
  const [edges, , onEdgesChange] = useEdgesState(initial.edges);
  const nodesInitialized = useNodesInitialized();
  const { getNodes, fitView } = useReactFlow<TreeNode>();
  const setPanel = useContext(SetPanel);

  // Once React Flow has measured every node, lay them out and fit them on screen.
  useEffect(() => {
    if (!nodesInitialized) return;
    setNodes(layoutNodes(getNodes(), edges));
    requestAnimationFrame(() => fitView({ padding: 0.05 }));
  }, [nodesInitialized, edges, getNodes, setNodes, fitView]);

  // Highlight the hovered subclaim, or else the one selected by clicking.
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const selectedId = nodes.find((n) => n.selected)?.id ?? null;
  const activeId = hoveredId ?? selectedId;

  return (
    <ActiveSubclaim.Provider value={activeId}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeMouseEnter={(_, node) => setHoveredId(node.id)}
        onNodeMouseLeave={() => setHoveredId(null)}
        onNodeClick={(_, node) => {
          if (node.type === "evidence") setPanel({ kind: "evidence", evidence: node.data.evidence });
        }}
        nodesConnectable={false}
        minZoom={0.2}
        maxZoom={2}
      >
        <Controls showInteractive={false} />
      </ReactFlow>
    </ActiveSubclaim.Provider>
  );
}

export default function App() {
  const notes = useAnnotations();
  const [panel, setPanel] = useState<Panel>(null);
  const [chatOpen, setChatOpen] = useState(false);
  const [askAnchor, setAskAnchor] = useState<AskAnchor | null>(null);

  const ask = (anchor: AskAnchor) => {
    setAskAnchor(anchor);
    setChatOpen(true);
  };
  // Show a cited passage in the evidence pane, if the app has a pane for it.
  const openCited = (target: string, quote: string) => {
    if (evidenceFor[target]) setPanel({ kind: "evidence", evidence: evidenceFor[target], focus: { target, quote } });
  };

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", lineHeight: 1.6, padding: "0 24px" }}>
      <h1>Claim 515: claim tree</h1>
      <p style={{ color: "#555" }}>
        Colors show the agent's judgment: green = supported, red = not supported, gray = experiment
        didn't run. Thick borders mark subclaims the agent flagged as bottlenecks. Hover over or click a
        subclaim to highlight the parts of the claim it covers. Click an experiment or papers card to
        see its details. Scroll to zoom, drag to pan, and use the "fit view" button (bottom left) to
        see the whole tree again.
      </p>
      <button onClick={() => setPanel(panel?.kind === "notes" ? null : { kind: "notes" })} style={{ marginBottom: 8 }}>
        {panel?.kind === "notes" ? "Hide notes" : `Show all notes (${notes.annotations.length})`}
      </button>{" "}
      <button onClick={() => setChatOpen(!chatOpen)} style={{ marginBottom: 8 }}>
        {chatOpen ? "Hide chat" : "Ask Claude"}
      </button>
      <NotesContext.Provider value={notes}>
        <SetPanel.Provider value={setPanel}>
          <AskContext.Provider value={ask}>
            {/* Graph on top, details pane below (suits a vertical screen). */}
            <div style={{ display: "flex", flexDirection: "column", height: "90vh", border: "1px solid #ddd" }}>
              <div style={{ flex: 1, minHeight: 0 }}>
                <ReactFlowProvider>
                  <ClaimTreeGraph />
                </ReactFlowProvider>
              </div>
              {/* Bottom pane: evidence or notes on the left, chat with Claude on the right. */}
              {(panel || chatOpen) && (
                <div style={{ height: "55%", display: "flex", borderTop: "1px solid #ddd" }}>
                  {panel && (
                    <div style={{ flex: 1, minWidth: 0, overflowY: "auto", padding: "0 16px" }}>
                      <div style={{ textAlign: "right", marginTop: 8 }}>
                        <button onClick={() => setPanel(null)}>Close</button>
                      </div>
                      {panel.kind === "notes" ? (
                        <NotesPane labels={noteLabels} />
                      ) : (
                        <EvidencePane evidence={panel.evidence} focus={panel.focus} />
                      )}
                    </div>
                  )}
                  {chatOpen && (
                    <div style={{ flex: 1, minWidth: 0, borderLeft: "1px solid #ddd", padding: "0 16px 8px" }}>
                      <ChatPane
                        index={evidenceIndex}
                        anchor={askAnchor}
                        onClearAnchor={() => setAskAnchor(null)}
                        onOpen={openCited}
                      />
                    </div>
                  )}
                </div>
              )}
            </div>
          </AskContext.Provider>
        </SetPanel.Provider>
      </NotesContext.Provider>
    </div>
  );
}
