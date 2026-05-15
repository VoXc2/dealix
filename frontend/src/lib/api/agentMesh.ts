import { apiClient } from "@/lib/api";

export async function fetchAgents() {
  const response = await apiClient.get("/api/v1/agents");
  return response.data;
}

export async function isolateAgent(agentId: string, reason: string) {
  const response = await apiClient.post(`/api/v1/agents/${encodeURIComponent(agentId)}/kill`, { reason });
  return response.data;
}
