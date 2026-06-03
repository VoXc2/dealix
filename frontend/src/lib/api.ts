import axios, { type AxiosInstance, type InternalAxiosRequestConfig } from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const TOKEN_KEY = "dealix_access_token";
const REFRESH_KEY = "dealix_refresh_token";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(TOKEN_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function getRefreshToken(): string | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(REFRESH_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function setToken(token: string) {
  if (typeof window === "undefined") return;
  localStorage.setItem(TOKEN_KEY, JSON.stringify(token));
}

function clearTokens() {
  if (typeof window === "undefined") return;
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_KEY);
  localStorage.removeItem("dealix_expires_at");
  localStorage.removeItem("dealix_user");
}

export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
  timeout: 30_000,
});

const OPS_PROXY_PREFIXES = [
  "/api/v1/ops-autopilot",
  "/api/v1/evidence",
  "/api/v1/sales/pipeline",
  "/api/v1/support",
  "/api/v1/knowledge/search",
  "/api/v1/invoices",
];

apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const publicAdminKey = process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY || "";
  const useOpsProxy = process.env.NEXT_PUBLIC_USE_DEALIX_OPS_PROXY === "1";
  const url = config.url || "";
  if (
    typeof window !== "undefined" &&
    useOpsProxy &&
    !publicAdminKey &&
    OPS_PROXY_PREFIXES.some((p) => url.startsWith(p))
  ) {
    config.url = `/api/dealix-proxy${url}`;
    if (config.headers) {
      delete config.headers["X-Admin-API-Key"];
    }
  }
  const token = getToken();
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

let isRefreshing = false;
let pendingRequests: Array<{
  resolve: (token: string) => void;
  reject: (err: unknown) => void;
}> = [];

function processPending(token: string | null, error?: unknown) {
  pendingRequests.forEach(({ resolve, reject }) => {
    if (token) resolve(token);
    else reject(error);
  });
  pendingRequests = [];
}

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status !== 401 || original._retry) {
      return Promise.reject(error);
    }
    original._retry = true;

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        pendingRequests.push({
          resolve: (token: string) => {
            original.headers.Authorization = `Bearer ${token}`;
            resolve(apiClient(original));
          },
          reject,
        });
      });
    }

    isRefreshing = true;
    const refreshTokenValue = getRefreshToken();

    if (!refreshTokenValue) {
      clearTokens();
      isRefreshing = false;
      return Promise.reject(error);
    }

    try {
      const res = await axios.post(`${API_BASE}/api/v1/auth/refresh`, {
        refresh_token: refreshTokenValue,
      });
      const newToken: string = res.data.tokens.accessToken;
      setToken(newToken);
      processPending(newToken);
      original.headers.Authorization = `Bearer ${newToken}`;
      return apiClient(original);
    } catch (refreshError) {
      clearTokens();
      processPending(null, refreshError);
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  },
);

export const api = {
  health: () =>
    apiClient.get<{ status: string }>("/health"),

  getDashboardMetrics: () =>
    apiClient.get("/api/v1/dashboard/metrics"),

  getLeads: () =>
    apiClient.get("/api/v1/founder/leads"),

  submitLead: (data: Record<string, unknown>) =>
    apiClient.post("/api/v1/leads", data),

  getPricing: () =>
    apiClient.get("/api/v1/pricing/plans"),

  getCommandCenter: () =>
    apiClient.get("/api/v1/v3/command-center/snapshot"),

  getAIWorkforce: () =>
    apiClient.get("/api/v1/ai-workforce/agents"),

  getApprovals: () =>
    apiClient.get("/api/v1/approvals/pending"),

  getPipeline: () =>
    apiClient.get("/api/v1/revenue-pipeline/summary"),

  getDecisionPassportGoldenChain: () =>
    apiClient.get("/api/v1/decision-passport/golden-chain"),

  getEvidenceLevels: () =>
    apiClient.get("/api/v1/decision-passport/evidence-levels"),

  getRevenueOsCatalog: () =>
    apiClient.get("/api/v1/revenue-os/catalog"),

  getRevenueOsLearningWeeklyTemplate: () =>
    apiClient.get("/api/v1/revenue-os/learning/weekly-template"),

  postRevenueOsAntiWasteCheck: (body: Record<string, unknown>) =>
    apiClient.post("/api/v1/revenue-os/anti-waste/check", body),

  getApprovalsPending: () =>
    apiClient.get("/api/v1/approvals/pending"),

  getApprovalsHistory: (limit = 50) =>
    apiClient.get("/api/v1/approvals/history", { params: { limit } }),

  postApprovalApprove: (approvalId: string, who: string) =>
    apiClient.post(`/api/v1/approvals/${approvalId}/approve`, { who }),

  postApprovalReject: (approvalId: string, who: string, reason: string) =>
    apiClient.post(`/api/v1/approvals/${approvalId}/reject`, { who, reason }),

  getGmailDraftsToday: () =>
    apiClient.get("/api/v1/gmail/drafts/today"),

  getLinkedInDraftsToday: () =>
    apiClient.get("/api/v1/linkedin/drafts/today"),

  getChannelPolicyStatus: () =>
    apiClient.get("/api/v1/channel-policy/status"),

  getCustomerPortal: (handle = "Slot-A") =>
    apiClient.get(`/api/v1/customer-portal/${encodeURIComponent(handle)}`),

  getBusinessNowSnapshot: () => apiClient.get("/api/v1/business-now/snapshot"),

  getCommercialStrategy: () => apiClient.get("/api/v1/business-now/commercial-strategy"),

  postCommercialStrategySimulate: (body: Record<string, unknown>) =>
    apiClient.post("/api/v1/business-now/commercial-strategy/simulate", body),

  postBusinessVerticalRecommend: (body: Record<string, unknown>) =>
    apiClient.post("/api/v1/business/verticals/recommend", body),

  postBusinessRecommendPlan: (body: Record<string, unknown>) =>
    apiClient.post("/api/v1/business/recommend-plan", body),

  getBusinessGtmFirst10: () => apiClient.get("/api/v1/business/gtm/first-10"),

  getBusinessSalesScript: () => apiClient.get("/api/v1/business/sales-script"),

  getBusinessProofPackDemo: () => apiClient.get("/api/v1/business/proof-pack/demo"),

  getTransformationKpiSnapshot: () =>
    apiClient.get("/api/v1/transformation/kpi-snapshot"),

  getBusinessNowOperatorSignals: (adminApiKey: string) =>
    apiClient.get("/api/v1/business-now/operator-signals", {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  postPublicRiskScore: (body: Record<string, unknown>) =>
    apiClient.post("/api/v1/public/risk-score", body),

  postPublicLead: (body: Record<string, unknown>) =>
    apiClient.post("/api/v1/public/leads", body),

  getPublicKnowledgeAnswer: (q: string) =>
    apiClient.get("/api/v1/public/knowledge/answer", { params: { q } }),

  postPublicBooking: (body: Record<string, unknown>) =>
    apiClient.post("/api/v1/public/booking-request", body),

  getOpsFounderDashboard: (adminApiKey: string) =>
    apiClient.get("/api/v1/ops-autopilot/founder-dashboard", {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getWarRoom: (
    adminApiKey: string,
    params?: {
      due_today?: boolean;
      needs_follow_up?: boolean;
      top_n?: number;
      status_in?: string;
    },
  ) =>
    apiClient.get("/api/v1/ops-autopilot/war-room", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params,
    }),

  getWarRoomSummary: (adminApiKey: string) =>
    apiClient.get("/api/v1/ops-autopilot/war-room/summary", {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  patchWarRoom: (adminApiKey: string, leadId: string, body: Record<string, unknown>) =>
    apiClient.patch(`/api/v1/ops-autopilot/war-room/${encodeURIComponent(leadId)}`, body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  postWarRoomTarget: (adminApiKey: string, body: Record<string, unknown>) =>
    apiClient.post("/api/v1/ops-autopilot/war-room", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getSalesPipelineAutopilot: (adminApiKey: string) =>
    apiClient.get("/api/v1/sales/pipeline", {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getEvidenceLedger: (adminApiKey: string, limit = 80) =>
    apiClient.get("/api/v1/evidence/events", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params: { limit },
    }),

  getSupportTicketsAutopilot: (adminApiKey: string, limit = 80) =>
    apiClient.get("/api/v1/support/tickets", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params: { limit },
    }),

  kbSearch: (adminApiKey: string, q: string) =>
    apiClient.get("/api/v1/knowledge/search", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params: { q },
    }),

  invoiceDraftAutopilot: (adminApiKey: string, body: Record<string, unknown>) =>
    apiClient.post("/api/v1/invoices/draft", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getMarketingCalendar: (adminApiKey: string, limit = 80) =>
    apiClient.get("/api/v1/ops-autopilot/marketing/calendar", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params: { limit },
    }),

  buildMarketingUtm: (adminApiKey: string, body: Record<string, unknown>) =>
    apiClient.post("/api/v1/ops-autopilot/marketing/utm", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  applyMarketingWeeklyPack: (adminApiKey: string, body: Record<string, unknown>) =>
    apiClient.post("/api/v1/ops-autopilot/marketing/weekly-pack/apply", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getFullOpsHealth: (adminApiKey: string) =>
    apiClient.get("/api/v1/ops-autopilot/full-ops-health", {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getWarRoomTodayPack: (adminApiKey: string) =>
    apiClient.get("/api/v1/ops-autopilot/war-room/today-pack", {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getFounderDailyPack: (adminApiKey: string) =>
    apiClient.get("/api/v1/ops-autopilot/founder/daily-pack", {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getFounderValuePlan: (adminApiKey: string, topN = 5) =>
    apiClient.get("/api/v1/ops-autopilot/founder/value-plan", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params: { top_n: topN },
    }),

  getFounderGtmStack: (adminApiKey: string, topN = 10) =>
    apiClient.get("/api/v1/ops-autopilot/founder/gtm-stack", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params: { top_n: topN },
    }),

  getFounderFullAutonomousOps: (
    adminApiKey: string,
    topN = 15,
    opts?: { includeValuePlan?: boolean; includeNested?: boolean },
  ) =>
    apiClient.get("/api/v1/ops-autopilot/founder/full-autonomous-ops", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params: {
        top_n: topN,
        include_value_plan: opts?.includeValuePlan ?? false,
        include_nested: opts?.includeNested ?? false,
      },
    }),

  getFounderCockpit: (adminApiKey: string, topN = 15, mode = "morning") =>
    apiClient.get("/api/v1/ops-autopilot/founder/cockpit", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params: { top_n: topN, mode },
    }),

  postFounderCockpitRunMorning: (
    adminApiKey: string,
    body: { top_n?: number; run_optional_scripts?: boolean } = {},
  ) =>
    apiClient.post("/api/v1/ops-autopilot/founder/cockpit/run-morning", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  postFounderCockpitRunUnifiedDay: (
    adminApiKey: string,
    body: { top_n?: number; quick?: boolean; run_optional_scripts?: boolean } = {},
  ) =>
    apiClient.post("/api/v1/ops-autopilot/founder/cockpit/run-unified-day", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
      timeout: 120_000,
    }),

  postFounderCockpitRunEvening: (adminApiKey: string, body: { top_n?: number } = {}) =>
    apiClient.post("/api/v1/ops-autopilot/founder/cockpit/run-evening", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  postFounderCockpitRunWeekly: (
    adminApiKey: string,
    body: { top_n?: number; run_optional_scripts?: boolean } = {},
  ) =>
    apiClient.post("/api/v1/ops-autopilot/founder/cockpit/run-weekly", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
      timeout: 90_000,
    }),

  postFounderCompleteAutonomousDayRun: (
    adminApiKey: string,
    body: {
      weekly?: boolean;
      evening?: boolean;
      skip_commercial_day?: boolean;
      use_unified_in_process?: boolean;
      top_n?: number;
    } = {},
  ) =>
    apiClient.post("/api/v1/ops-autopilot/founder/complete-autonomous-day/run", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
      timeout: 180_000,
    }),

  postFounderFullAutonomousOpsRun: (
    adminApiKey: string,
    body: { dry_run?: boolean; top_n?: number; run_optional_scripts?: boolean } = {},
  ) =>
    apiClient.post("/api/v1/ops-autopilot/founder/full-autonomous-ops/run", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getFounderCommercialValueMap: (adminApiKey: string, topN = 5) =>
    apiClient.get("/api/v1/ops-autopilot/founder/commercial-value-map", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params: { top_n: topN, include_value_plan: true },
    }),

  getFounderStrongestPlan: (adminApiKey: string) =>
    apiClient.get("/api/v1/ops-autopilot/founder/strongest-plan", {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getFounderStrongestOps: (adminApiKey: string, mode = "morning") =>
    apiClient.get("/api/v1/ops-autopilot/founder/strongest-ops", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params: { mode },
    }),

  postFounderStrongestOpsRun: (
    adminApiKey: string,
    body: { mode?: string; run_checks?: boolean; write_brief?: boolean } = {},
  ) =>
    apiClient.post("/api/v1/ops-autopilot/founder/strongest-ops/run", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
      timeout: 120_000,
    }),

  getFounderExpansionStatus: (adminApiKey: string, topN = 10) =>
    apiClient.get("/api/v1/ops-autopilot/founder/expansion-status", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params: { top_n: topN },
    }),

  postFounderEvidenceCsvAppend: (
    adminApiKey: string,
    body: {
      event_type: string;
      company: string;
      notes?: string;
      motion?: string;
      offer_id?: string;
    },
  ) =>
    apiClient.post("/api/v1/ops-autopilot/founder/evidence/csv-append", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  importWarRoomTargets: (adminApiKey: string, body: Record<string, unknown>) =>
    apiClient.post("/api/v1/ops-autopilot/war-room/import-targets", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getMarketingSocialToday: (adminApiKey: string) =>
    apiClient.get("/api/v1/ops-autopilot/marketing/social-today", {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  postMarketingSocialMark: (adminApiKey: string, body: Record<string, unknown>) =>
    apiClient.post("/api/v1/ops-autopilot/marketing/social-today/mark", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  postMarketingQueueApproval: (adminApiKey: string) =>
    apiClient.post(
      "/api/v1/ops-autopilot/marketing/queue-approval",
      {},
      { headers: { "X-Admin-API-Key": adminApiKey } },
    ),

  getSalesObjections: (adminApiKey: string) =>
    apiClient.get("/api/v1/ops-autopilot/sales/objections", {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getLeadMeetingBrief: (adminApiKey: string, leadId: string, locale = "ar") =>
    apiClient.get(
      `/api/v1/ops-autopilot/leads/${encodeURIComponent(leadId)}/meeting-brief`,
      { headers: { "X-Admin-API-Key": adminApiKey }, params: { locale } },
    ),

  advanceLeadStage: (
    adminApiKey: string,
    leadId: string,
    body: Record<string, unknown>,
  ) =>
    apiClient.post(
      `/api/v1/ops-autopilot/leads/${encodeURIComponent(leadId)}/advance-stage`,
      body,
      { headers: { "X-Admin-API-Key": adminApiKey } },
    ),

  getMarketingObjectionDraft: (adminApiKey: string, slug: string) =>
    apiClient.get("/api/v1/ops-autopilot/marketing/objection-draft", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params: { slug },
    }),

  classifySupportTicket: (adminApiKey: string, ticketId: string) =>
    apiClient.post(
      `/api/v1/support/tickets/${encodeURIComponent(ticketId)}/classify`,
      {},
      { headers: { "X-Admin-API-Key": adminApiKey } },
    ),

  draftSupportResponse: (adminApiKey: string, ticketId: string) =>
    apiClient.post(
      `/api/v1/support/tickets/${encodeURIComponent(ticketId)}/draft-response`,
      {},
      { headers: { "X-Admin-API-Key": adminApiKey } },
    ),

  getOpsLeads: (adminApiKey: string, limit = 80) =>
    apiClient.get("/api/v1/ops-autopilot/leads", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params: { limit },
    }),

  getTargetingToday: (adminApiKey: string, topN = 5) =>
    apiClient.get("/api/v1/ops-autopilot/targeting/today", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params: { top_n: topN },
    }),

  getTargetingPool: (adminApiKey: string) =>
    apiClient.get("/api/v1/ops-autopilot/targeting/pool", {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getTargetingP0Today: (adminApiKey: string, topN = 10) =>
    apiClient.get("/api/v1/ops-autopilot/targeting/p0-today", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params: { top_n: topN },
    }),

  postWarRoomGenerateOutreach: (adminApiKey: string, leadId: string) =>
    apiClient.post(
      `/api/v1/ops-autopilot/war-room/${encodeURIComponent(leadId)}/generate-outreach`,
      {},
      { headers: { "X-Admin-API-Key": adminApiKey } },
    ),

  postClientPackGenerate: (
    adminApiKey: string,
    body: { company?: string; lead_id?: string; write_disk?: boolean },
  ) =>
    apiClient.post("/api/v1/ops-autopilot/client-pack/generate", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  postTargetingImport: (adminApiKey: string, body: { csv_text: string }) =>
    apiClient.post("/api/v1/ops-autopilot/targeting/import", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  patchMarketingCalendar: (
    adminApiKey: string,
    slotId: string,
    body: Record<string, unknown>,
  ) =>
    apiClient.patch(`/api/v1/ops-autopilot/marketing/calendar/${encodeURIComponent(slotId)}`, body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getMarketingPublishKit: (adminApiKey: string, slotId: string) =>
    apiClient.get(
      `/api/v1/ops-autopilot/marketing/calendar/${encodeURIComponent(slotId)}/publish-kit`,
      { headers: { "X-Admin-API-Key": adminApiKey } },
    ),

  // ── Wave 15 Commercial Chain (13 endpoints, all approval-gated) ────────

  postCommercialDiagnosticGenerate: (
    adminApiKey: string,
    body: {
      company_name: string;
      sector?: string;
      pain_points?: string[];
      website_url?: string;
      contact_name?: string;
      notes?: string;
    },
  ) =>
    apiClient.post("/api/v1/commercial/diagnostic/generate", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  postCommercialWarmIntroDraft: (
    adminApiKey: string,
    body: {
      prospect_name: string;
      company_name: string;
      sector?: string;
      pain_context?: string;
      previous_interaction?: string;
      founder_name?: string;
    },
  ) =>
    apiClient.post("/api/v1/commercial/warm-intro/draft", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  postCommercialPilotStart: (
    adminApiKey: string,
    body: {
      account_id: string;
      company_name: string;
      contact_name?: string;
      sector?: string;
      pain_points?: string[];
      diagnostic_id?: string;
      start_date?: string;
    },
  ) =>
    apiClient.post("/api/v1/commercial/pilot/start", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  postCommercialProofBuild: (
    adminApiKey: string,
    body: {
      account_id: string;
      company_name: string;
      pilot_id?: string;
      events?: Array<{
        event_type: string;
        description_ar: string;
        description_en: string;
        metric_before?: string;
        metric_after?: string;
        delta_pct?: number;
        evidence_url?: string;
        source_ref?: string;
      }>;
      approved_by_founder?: boolean;
      customer_consent?: boolean;
    },
  ) =>
    apiClient.post("/api/v1/commercial/proof/build", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  postCommercialPaymentLink: (
    adminApiKey: string,
    body: {
      service_tier: string;
      customer_name: string;
      customer_email?: string;
      account_id?: string;
      pilot_id?: string;
      callback_url?: string;
      notes?: string;
    },
  ) =>
    apiClient.post("/api/v1/commercial/payment/link", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getCommercialPaymentTiers: (adminApiKey: string) =>
    apiClient.get("/api/v1/commercial/payment/tiers", {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  postCommercialUpsellCheck: (
    adminApiKey: string,
    body: {
      account_id: string;
      company_name: string;
      proof_event_count: number;
      proof_level?: string;
      monthly_revenue_sar?: number;
    },
  ) =>
    apiClient.post("/api/v1/commercial/upsell/check", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  postCommercialCaseStudyGenerate: (
    adminApiKey: string,
    body: {
      account_id: string;
      company_name: string;
      sector?: string;
      proof_pack_id?: string;
      customer_consent?: boolean;
      anonymize?: boolean;
      challenge_ar?: string;
      challenge_en?: string;
      approach_ar?: string;
      approach_en?: string;
      result_ar?: string;
      result_en?: string;
      customer_quote_ar?: string;
      customer_quote_en?: string;
    },
  ) =>
    apiClient.post("/api/v1/commercial/case-study/generate", body, {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getCommercialDailyBrief: (adminApiKey: string) =>
    apiClient.get("/api/v1/commercial/daily-brief", {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getCommercialZatcaInvoice: (adminApiKey: string, params?: { account_id?: string; pilot_id?: string }) =>
    apiClient.get("/api/v1/commercial/zatca/invoice", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params,
    }),

  getCommercialGovernanceDecision: (
    adminApiKey: string,
    params: { action: string; account_id?: string },
  ) =>
    apiClient.get("/api/v1/commercial/governance/decision", {
      headers: { "X-Admin-API-Key": adminApiKey },
      params,
    }),

  getCommercialStatus: (adminApiKey: string) =>
    apiClient.get("/api/v1/commercial/status", {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),

  getCommercialChainStatus: (adminApiKey: string) =>
    apiClient.get("/api/v1/commercial/chain-status", {
      headers: { "X-Admin-API-Key": adminApiKey },
    }),
};

export default api;
