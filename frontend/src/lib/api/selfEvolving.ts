import { apiClient } from "@/lib/api";

export async function fetchSelfEvolvingStatus() {
  const response = await apiClient.get("/api/v1/self-improvement-os/status");
  return response.data;
}

export async function fetchWeeklyLearning() {
  const response = await apiClient.get("/api/v1/self-improvement-os/weekly-learning");
  return response.data;
}
