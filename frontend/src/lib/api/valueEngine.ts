import { apiClient } from "@/lib/api";

export async function fetchValueReport(customerId: string) {
  const response = await apiClient.get(`/api/v1/value/${encodeURIComponent(customerId)}/report/monthly`);
  return response.data;
}
