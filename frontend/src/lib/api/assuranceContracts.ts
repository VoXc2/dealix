import { apiClient } from "@/lib/api";

export async function fetchAssuranceContractStatus() {
  const response = await apiClient.get("/api/v1/governance/risk-dashboard/status");
  return response.data;
}
