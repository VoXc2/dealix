import apiClient from "./client";
import type { AgentActivity, PaginatedResponse } from "@/types";

export const agentsApi = {
  activities: async (params?: {
    page?: number;
    pageSize?: number;
    agentType?: string;
    status?: string;
  }): Promise<PaginatedResponse<AgentActivity>> => {
    const response = await apiClient.get<PaginatedResponse<AgentActivity>>(
      "/agents/activities",
      { params }
    );
    return response.data;
  },

  // Trigger a specific agent run
  trigger: async (agentType: string, payload: Record<string, unknown>) => {
    const response = await apiClient.post(`/agents/${agentType}/run`, payload);
    return response.data;
  },

  // Get agent status / stats
  stats: async () => {
    const response = await apiClient.get("/agents/stats");
    return response.data;
  },
};
