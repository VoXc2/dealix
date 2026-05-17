import axios, { type AxiosInstance, type InternalAxiosRequestConfig } from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const TOKEN_KEY = "dealix_access_token";
const REFRESH_KEY = "dealix_refresh_token";

// Ops Console endpoints are admin-key gated on the backend. The operator
// console is an internal tool; the key is supplied via a build-time env var
// (same pattern as NEXT_PUBLIC_DEMO_API_KEY).
const ADMIN_API_KEY = process.env.NEXT_PUBLIC_ADMIN_API_KEY || "";
const opsHeaders = ADMIN_API_KEY ? { "X-Admin-API-Key": ADMIN_API_KEY } : {};

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

apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
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

  // ── Ops Console (admin-key gated) ──────────────────────────────
  getOpsCommandCenter: () =>
    apiClient.get("/api/v1/ops/command-center", { headers: opsHeaders }),

  getOpsCatalog: () =>
    apiClient.get("/api/v1/ops/catalog", { headers: opsHeaders }),

  getOpsMarketProof: () =>
    apiClient.get("/api/v1/ops/market-proof", { headers: opsHeaders }),

  getOpsRevenue: () =>
    apiClient.get("/api/v1/ops/revenue", { headers: opsHeaders }),

  getOpsEvidence: () =>
    apiClient.get("/api/v1/ops/evidence", { headers: opsHeaders }),

  getOpsEvidenceLevels: () =>
    apiClient.get("/api/v1/ops/evidence/levels", { headers: opsHeaders }),

  getOpsBilling: () =>
    apiClient.get("/api/v1/ops/billing", { headers: opsHeaders }),

  getOpsBoard: () =>
    apiClient.get("/api/v1/ops/board", { headers: opsHeaders }),

  getOpsProofPackTemplate: () =>
    apiClient.get("/api/v1/ops/proof-pack/template", { headers: opsHeaders }),

  postOpsProofPackPreview: (body: Record<string, unknown>) =>
    apiClient.post("/api/v1/ops/proof-pack/preview", body, { headers: opsHeaders }),
};

export default api;
