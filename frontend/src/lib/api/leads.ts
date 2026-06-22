import apiClient from "./client";
import type { Deal, DealStage, PaginatedResponse } from "@/types";

export interface DealsFilter {
  stage?: DealStage;
  assignedTo?: string;
  minValue?: number;
  maxValue?: number;
  page?: number;
  pageSize?: number;
}

export const dealsApi = {
  list: async (filters?: DealsFilter): Promise<PaginatedResponse<Deal>> => {
    const response = await apiClient.get<PaginatedResponse<Deal>>("/deals", {
      params: filters,
    });
    return response.data;
  },

  get: async (id: string): Promise<Deal> => {
    const response = await apiClient.get<Deal>(`/deals/${id}`);
    return response.data;
  },

  create: async (deal: Omit<Deal, "id" | "lastActivity" | "aiScore">): Promise<Deal> => {
    const response = await apiClient.post<Deal>("/deals", deal);
    return response.data;
  },

  update: async (id: string, updates: Partial<Deal>): Promise<Deal> => {
    const response = await apiClient.patch<Deal>(`/deals/${id}`, updates);
    return response.data;
  },

  updateStage: async (id: string, stage: DealStage): Promise<Deal> => {
    const response = await apiClient.patch<Deal>(`/deals/${id}/stage`, { stage });
    return response.data;
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/deals/${id}`);
  },

  // Kanban grouped by stage
  kanban: async (): Promise<Record<DealStage, Deal[]>> => {
    const response = await apiClient.get<Record<DealStage, Deal[]>>("/deals/kanban");
    return response.data;
  },
};

// Revenue & KPI data
export const revenueApi = {
  kpis: async () => {
    const response = await apiClient.get("/revenue/kpis");
    return response.data;
  },
  monthly: async (year?: number) => {
    const response = await apiClient.get("/revenue/monthly", { params: { year } });
    return response.data;
  },
};
