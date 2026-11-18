import { createContext, useContext, useEffect, useState } from "react";
import dagre from "@dagrejs/dagre";
import {
  ReactFlow,
  ReactFlowProvider,
  Controls,
  Handle,
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
import { NotesContext, useAnnotations } from "./annotations";
import NotesPane from "./NotesPane";
import EvidencePane, { type Evidence } from "./EvidencePane";

const STATUS_COLORS: Record<Status, string> = {
  supported: "#c8e6c9",
  "not supported": "#ffcdd2",
  unrun: "#e0e0e0",
};

// What the right-hand pane shows: all notes, one piece of evidence, or nothing.
type Panel = { kind: "notes" } | { kind: "evidence"; evidence: Evidence } | null;
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

function useNoteCount(targets: string[]): number {
  const { annotations } = useContext(NotesContext);
  return annotations.filter((a) => targets.includes(a.target)).length;
}

function noteCountText(count: number): string {
  return `${count} ${count === 1 ? "note" : "notes"}`;
}

// The claim or a subclaim: a bold title, a few detail lines, (for the claim) its text, then notes.
function ClaimNodeView({ id, data }: NodeProps<ClaimNode>) {
  const active = useContext(ActiveSubclaim);
  const phrases = active ? CLAIM_SPANS[active] ?? [] : [];
  const { add } = useContext(NotesContext);
  const setPanel = useContext(SetPanel);
  const count = useNoteCount([id]);
  return (
    <div
      style={{
        width: data.width,
        padding: 14,
        background: data.color,
        border: `${data.bottleneck ? 4 : 1}px solid #555`,
        borderRadius: 8,
        fontSize: 16,
        lineHeight: 1.35,
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
        {noteCountText(count)}
      </div>
      <Handle type="source" position={Position.Right} style={{ opacity: 0 }} />
    </div>
  );
}

// An experiment or a group of papers. Clicking it opens the evidence pane.
function EvidenceNodeView({ data }: NodeProps<EvidenceNode>) {
  const count = useNoteCount(data.noteTargets);
  return (
    <div
      style={{
        width: 220,
        padding: 10,
        background: data.color,
        border: "1px solid #888",
        borderRadius: 6,
        fontSize: 15,
        lineHeight: 1.3,
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
      <div style={{ marginTop: 6, fontSize: 13, color: "#666" }}>Click to open · {noteCountText(count)}</div>
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

  return (
    <div style={{ fontFamily: "system-ui, sans-serif", padding: "0 24px" }}>
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
      </button>
      <NotesContext.Provider value={notes}>
        <SetPanel.Provider value={setPanel}>
          <div style={{ display: "flex", height: "80vh", border: "1px solid #ddd" }}>
            <div style={{ flex: 1, minWidth: 0 }}>
              <ReactFlowProvider>
                <ClaimTreeGraph />
              </ReactFlowProvider>
            </div>
            {panel && (
              <div
                style={{
                  width: panel.kind === "notes" ? 380 : "45%",
                  overflowY: "auto",
                  borderLeft: "1px solid #ddd",
                  padding: "0 16px",
                }}
              >
                <div style={{ textAlign: "right", marginTop: 8 }}>
                  <button onClick={() => setPanel(null)}>Close</button>
                </div>
                {panel.kind === "notes" ? (
                  <NotesPane labels={noteLabels} />
                ) : (
                  <EvidencePane evidence={panel.evidence} />
                )}
              </div>
            )}
          </div>
        </SetPanel.Provider>
      </NotesContext.Provider>
    </div>
  );
}
