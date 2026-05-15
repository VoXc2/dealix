/**
 * Map backend payloads to frontend domain types (defensive; avoids silent mock drift).
 */
import type {
  AgentActivity,
  AgentType,
  ApprovalRequest,
  ApprovalStatus,
  Client,
  ClientStatus,
  Deal,
  DealStage,
  RiskLevel,
} from "@/types";

const LEAD_STATUS_TO_STAGE: Record<string, DealStage> = {
  new: "lead",
  contacted: "qualified",
  qualified: "proposal",
  converted: "closed_won",
  lost: "closed_lost",
};

export function leadInboxRecordToDeal(
  rec: Record<string, unknown>,
  index: number,
): Deal {
  const status = String(rec.status ?? "new");
  const stage = LEAD_STATUS_TO_STAGE[status] ?? "lead";
  const received = String(rec.received_at ?? "");
  return {
    id: String(rec.id ?? `lead_${index}`),
    title: String(rec.company ?? rec.name ?? "Lead"),
    company: String(rec.company ?? ""),
    value: typeof rec.budget === "number" ? rec.budget : Number(rec.budget) || 0,
    currency: "SAR",
    stage,
    probability:
      stage === "closed_won" ? 100 : stage === "closed_lost" ? 0 : 30,
    closeDate: received.slice(0, 10) || new Date().toISOString().slice(0, 10),
    assignedTo: String(rec.name ?? ""),
    lastActivity: received || new Date().toISOString(),
    tags: typeof rec.sector === "string" ? [rec.sector] : [],
    aiScore: 50,
  };
}

export function groupDealsByStage(deals: Deal[]): Record<DealStage, Deal[]> {
  const empty: Record<DealStage, Deal[]> = {
    lead: [],
    qualified: [],
    proposal: [],
    negotiation: [],
    closed_won: [],
    closed_lost: [],
  };
  for (const d of deals) {
    if (d.stage in empty) {
      empty[d.stage].push(d);
    }
  }
  return empty;
}

function agentIdToType(agentId: string): AgentType {
  const id = agentId.toLowerCase();
  if (id.includes("copy") || id.includes("outreach") || id.includes("email")) {
    return "outreach";
  }
  if (id.includes("score") || id.includes("bant") || id.includes("qualif")) {
    return "scoring";
  }
  if (id.includes("compliance") || id.includes("guard") || id.includes("legal")) {
    return "compliance";
  }
  if (id.includes("intel") || id.includes("radar") || id.includes("research")) {
    return "intelligence";
  }
  return "orchestrator";
}

export function workforceAgentToActivity(
  spec: Record<string, unknown>,
  isAr: boolean,
): AgentActivity {
  const agentId = String(spec.agent_id ?? "agent");
  return {
    id: agentId,
    agentType: agentIdToType(agentId),
    action: isAr
      ? String(spec.role_ar ?? spec.role_en ?? agentId)
      : String(spec.role_en ?? spec.role_ar ?? agentId),
    target: String(spec.default_action_mode ?? spec.autonomy_level ?? "—"),
    status: "completed",
    timestamp: new Date().toISOString(),
    requiresApproval: Boolean(spec.requires_approval),
  };
}

function mapRisk(level: string): RiskLevel {
  if (level === "high" || level === "medium" || level === "low") return level;
  return "low";
}

function mapApprovalStatus(s: string): ApprovalStatus {
  if (s === "pending" || s === "approved" || s === "rejected") return s;
  return "pending";
}

export function backendApprovalToUi(
  r: Record<string, unknown>,
): ApprovalRequest {
  const objectType = String(r.object_type ?? "action");
  const agentType = agentIdToType(objectType);

  return {
    id: String(r.approval_id ?? r.id ?? ""),
    agentType,
    action: String(r.summary_ar || r.summary_en || r.action_type || objectType),
    description: String(
      r.proof_impact || r.summary_en || r.summary_ar || "",
    ),
    riskLevel: mapRisk(String(r.risk_level ?? "low")),
    status: mapApprovalStatus(String(r.status ?? "pending")),
    requestedAt: String(r.created_at ?? new Date().toISOString()),
    reviewedAt: r.updated_at ? String(r.updated_at) : undefined,
    reviewedBy: undefined,
    target: String(r.object_id ?? r.channel ?? ""),
    metadata: { object_type: objectType, action_mode: r.action_mode },
    estimatedImpact: r.proof_target ? String(r.proof_target) : undefined,
  };
}

export function extractApprovalRows(data: unknown): Record<string, unknown>[] {
  if (!data || typeof data !== "object") return [];
  const root = data as Record<string, unknown>;
  const rows = root.approvals;
  return Array.isArray(rows) ? (rows as Record<string, unknown>[]) : [];
}

export function founderLeadToClient(
  rec: Record<string, unknown>,
  index: number,
): Client {
  const statusRaw = String(rec.status ?? "new");
  const statusMap: Record<string, ClientStatus> = {
    new: "prospect",
    contacted: "prospect",
    qualified: "active",
    converted: "active",
    lost: "churned",
  };
  return {
    id: String(rec.id ?? `c_${index}`),
    company: String(rec.company ?? "—"),
    contactName: String(rec.name ?? "—"),
    contactEmail: String(rec.email ?? ""),
    contactPhone: rec.phone ? String(rec.phone) : undefined,
    status: statusMap[statusRaw] ?? "prospect",
    industry: String(rec.sector ?? "—"),
    totalDeals: statusRaw === "converted" ? 1 : 0,
    totalRevenue: typeof rec.budget === "number" ? rec.budget : 0,
    lastActivity: String(rec.received_at ?? new Date().toISOString()),
    aiScore: 50,
    tags: typeof rec.region === "string" ? [rec.region] : [],
  };
}
