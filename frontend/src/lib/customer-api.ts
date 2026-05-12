/**
 * Typed wrappers over the customer/billing/audit endpoints, intended to
 * be consumed by TanStack Query hooks. Uses the existing apiClient
 * (axios) from `lib/api.ts` so auth + refresh stay in one place.
 */

import { apiClient } from "@/lib/api";

export interface CustomerSummary {
  tenant_id: string;
  users_active: number;
  leads_total: number;
  leads_7d: number;
  deals_open: number;
  deals_won_30d: number;
  last_active_at: string | null;
}

export interface Subscription {
  tenant_id: string;
  name: string;
  plan: string;
  status: string;
  currency: string;
  max_users: number;
  max_leads_per_month: number;
  renewal_at: string;
  features: Record<string, unknown>;
  billing_provider: string;
}

export interface Invoice {
  id: string;
  action: string;
  status: string;
  amount_sar?: number;
  amount_usd?: number;
  provider: string;
  issued_at: string;
}

export interface TeamMember {
  id: string;
  email: string;
  name: string;
  is_active: boolean;
  is_verified: boolean;
  mfa_enabled: boolean;
  last_login_at: string | null;
  created_at: string;
}

export interface AuditRow {
  id: string;
  tenant_id: string;
  user_id: string | null;
  action: string;
  entity_type: string;
  entity_id: string | null;
  status: string;
  ip_address: string | null;
  request_id: string | null;
  created_at: string;
}

export const customerKeys = {
  summary: (tenantId: string) => ["customer", tenantId, "summary"] as const,
  subscription: (tenantId: string) =>
    ["customer", tenantId, "subscription"] as const,
  invoices: (tenantId: string) => ["customer", tenantId, "invoices"] as const,
  team: (tenantId: string) => ["customer", tenantId, "team"] as const,
  audit: (filters: Record<string, string>) => ["audit", filters] as const,
};

export const customerApi = {
  summary: (tenantId: string) =>
    apiClient
      .get<CustomerSummary>(`/api/v1/customers/${tenantId}/summary`)
      .then((r) => r.data),
  subscription: (tenantId: string) =>
    apiClient
      .get<Subscription>(`/api/v1/customers/${tenantId}/subscription`)
      .then((r) => r.data),
  invoices: (tenantId: string) =>
    apiClient
      .get<{ invoices: Invoice[] }>(`/api/v1/customers/${tenantId}/invoices`)
      .then((r) => r.data.invoices),
  team: (tenantId: string) =>
    apiClient
      .get<{ members: TeamMember[]; pending_invites: any[] }>(
        `/api/v1/customers/${tenantId}/team/members`
      )
      .then((r) => r.data),
  invite: (
    tenantId: string,
    body: { email: string; role?: string; name?: string }
  ) =>
    apiClient
      .post(`/api/v1/customers/${tenantId}/team/invite`, body)
      .then((r) => r.data),
  revoke: (tenantId: string, userId: string) =>
    apiClient
      .delete(`/api/v1/customers/${tenantId}/team/members/${userId}`)
      .then((r) => r.data),
  audit: (params: Record<string, string>) =>
    apiClient
      .get<{ items: AuditRow[] }>("/api/v1/audit-logs", { params })
      .then((r) => r.data.items),
};
