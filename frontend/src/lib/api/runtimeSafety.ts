import { apiClient } from "@/lib/api";

export async function fetchRuntimeSafetyStatus() {
  const response = await apiClient.get("/api/v1/safety-v10/status");
  return response.data;
}

export async function runSafetyEval() {
  const response = await apiClient.post("/api/v1/safety-v10/run", {});
  return response.data;
}
