import axios, { type AxiosInstance, type InternalAxiosRequestConfig } from "axios";
import {
  clearAuthStorage,
  getStoredAccessToken,
  getStoredRefreshToken,
  persistAuthResponse,
  type LoginResponse,
} from "@/lib/auth-storage";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE,
  headers: { "Content-Type": "application/json" },
  timeout: 30_000,
});

apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = getStoredAccessToken();
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
    const reqUrl = String(original.url ?? "");
    if (
      reqUrl.includes("/auth/refresh") ||
      reqUrl.includes("/auth/login") ||
      reqUrl.includes("/auth/register")
    ) {
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
    const refreshTokenValue = getStoredRefreshToken();

    if (!refreshTokenValue) {
      clearAuthStorage();
      isRefreshing = false;
      return Promise.reject(error);
    }

    try {
      const res = await axios.post<LoginResponse>(
        `${API_BASE}/api/v1/auth/refresh`,
        { refresh_token: refreshTokenValue },
        { headers: { "Content-Type": "application/json" }, timeout: 30_000 },
      );
      persistAuthResponse(res.data);
      const newToken = res.data.tokens.accessToken;
      processPending(newToken);
      original.headers.Authorization = `Bearer ${newToken}`;
      return apiClient(original);
    } catch (refreshError) {
      clearAuthStorage();
      processPending(null, refreshError);
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  },
);

export const api = {
  health: () => apiClient.get<{ status: string }>("/health"),

  getDashboardMetrics: () => apiClient.get("/api/v1/dashboard/metrics"),

  getLeads: () => apiClient.get("/api/v1/founder/leads"),

  submitLead: (data: Record<string, unknown>) =>
    apiClient.post("/api/v1/leads", data),

  getPricing: () => apiClient.get("/api/v1/pricing/plans"),

  getCommandCenter: () => apiClient.get("/api/v1/v3/command-center/snapshot"),

  getAIWorkforce: () => apiClient.get("/api/v1/ai-workforce/agents"),

  getApprovals: () => apiClient.get("/api/v1/approvals/pending"),

  getApprovalsHistory: (limit = 50) =>
    apiClient.get("/api/v1/approvals/history", { params: { limit } }),

  approveApproval: (approvalId: string, who: string) =>
    apiClient.post(`/api/v1/approvals/${approvalId}/approve`, { who }),

  rejectApproval: (approvalId: string, who: string, reason: string) =>
    apiClient.post(`/api/v1/approvals/${approvalId}/reject`, {
      who,
      reason,
    }),

  getPipeline: () => apiClient.get("/api/v1/revenue-pipeline/summary"),

  getDecisionPassportGoldenChain: () =>
    apiClient.get("/api/v1/decision-passport/golden-chain"),

  getEvidenceLevels: () =>
    apiClient.get("/api/v1/decision-passport/evidence-levels"),

  getRevenueOsCatalog: () => apiClient.get("/api/v1/revenue-os/catalog"),

  getRevenueOsLearningWeeklyTemplate: () =>
    apiClient.get("/api/v1/revenue-os/learning/weekly-template"),
};

export default api;
