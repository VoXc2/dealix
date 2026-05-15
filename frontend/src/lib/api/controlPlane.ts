import { apiClient } from "@/lib/api";

export async function fetchControlPlaneRuns() {
  const response = await apiClient.get("/api/v1/founder-dashboard/launch-status");
  return response.data;
}

export async function fetchRunTrace(customerId: string) {
  const response = await apiClient.get(`/api/v1/audit/${encodeURIComponent(customerId)}`);
  return response.data;
}

export async function requestRollback(approvalId: string, who: string) {
  const response = await apiClient.post(`/api/v1/approvals/${approvalId}/approve`, { who });
  return response.data;
}
