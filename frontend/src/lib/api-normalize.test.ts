import { describe, expect, it } from "vitest";
import {
  backendApprovalToUi,
  extractApprovalRows,
  founderLeadToClient,
  groupDealsByStage,
  leadInboxRecordToDeal,
} from "./api-normalize";

describe("leadInboxRecordToDeal", () => {
  it("maps qualified status to proposal stage", () => {
    const d = leadInboxRecordToDeal(
      {
        id: "l1",
        company: "Acme",
        status: "qualified",
        received_at: "2026-01-01T00:00:00Z",
        name: "Sami",
      },
      0,
    );
    expect(d.stage).toBe("proposal");
    expect(d.company).toBe("Acme");
  });
});

describe("groupDealsByStage", () => {
  it("groups by stage", () => {
    const a = leadInboxRecordToDeal(
      { id: "1", company: "A", status: "new", received_at: "2026-01-01T00:00:00Z" },
      0,
    );
    const b = leadInboxRecordToDeal(
      { id: "2", company: "B", status: "converted", received_at: "2026-01-02T00:00:00Z" },
      1,
    );
    const g = groupDealsByStage([a, b]);
    expect(g.lead.length).toBe(1);
    expect(g.closed_won.length).toBe(1);
  });
});

describe("founderLeadToClient", () => {
  it("maps inbox record to client shape", () => {
    const c = founderLeadToClient(
      {
        id: "x",
        company: "Co",
        name: "N",
        email: "n@co.sa",
        status: "new",
        sector: "tech",
        received_at: "2026-01-01T00:00:00Z",
      },
      0,
    );
    expect(c.status).toBe("prospect");
    expect(c.company).toBe("Co");
  });
});

describe("backendApprovalToUi", () => {
  it("maps approval store payload", () => {
    const raw = {
      approval_id: "apr_test",
      object_type: "draft_email",
      object_id: "obj1",
      action_type: "draft_email",
      summary_ar: "مسودة",
      summary_en: "Draft",
      risk_level: "medium",
      status: "pending",
      created_at: "2026-01-01T00:00:00Z",
      action_mode: "draft_only",
    };
    const u = backendApprovalToUi(raw);
    expect(u.id).toBe("apr_test");
    expect(u.status).toBe("pending");
  });
});

describe("extractApprovalRows", () => {
  it("returns empty for bad input", () => {
    expect(extractApprovalRows(null)).toEqual([]);
    expect(extractApprovalRows({})).toEqual([]);
  });

  it("reads approvals array", () => {
    const rows = extractApprovalRows({
      approvals: [{ approval_id: "a1" }],
    });
    expect(rows.length).toBe(1);
  });
});
