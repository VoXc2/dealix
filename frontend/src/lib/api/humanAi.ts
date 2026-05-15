import { apiClient } from "@/lib/api";

export async function fetchOversightQueue() {
  const response = await apiClient.get("/api/v1/approvals/pending");
  return response.data;
}

export async function grantOversightApproval(approvalId: string, who: string) {
  const response = await apiClient.post(`/api/v1/approvals/${encodeURIComponent(approvalId)}/approve`, { who });
  return response.data;
}

export async function rejectOversightApproval(approvalId: string, who: string, reason: string) {
  const response = await apiClient.post(`/api/v1/approvals/${encodeURIComponent(approvalId)}/reject`, {
    who,
    reason,
  });
  return response.data;
}
