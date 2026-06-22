import apiClient from "./client";
import type { ApprovalRequest, PaginatedResponse } from "@/types";

export const approvalsApi = {
  list: async (params?: {
    status?: "pending" | "approved" | "rejected";
    riskLevel?: string;
    page?: number;
    pageSize?: number;
  }): Promise<PaginatedResponse<ApprovalRequest>> => {
    const response = await apiClient.get<PaginatedResponse<ApprovalRequest>>(
      "/approvals",
      { params }
    );
    return response.data;
  },

  approve: async (id: string, comment?: string): Promise<ApprovalRequest> => {
    const response = await apiClient.post<ApprovalRequest>(`/approvals/${id}/approve`, {
      comment,
    });
    return response.data;
  },

  reject: async (id: string, reason: string): Promise<ApprovalRequest> => {
    const response = await apiClient.post<ApprovalRequest>(`/approvals/${id}/reject`, {
      reason,
    });
    return response.data;
  },

  get: async (id: string): Promise<ApprovalRequest> => {
    const response = await apiClient.get<ApprovalRequest>(`/approvals/${id}`);
    return response.data;
  },
};
