// Core domain types for Dealix RevOps platform

export type Locale = "ar" | "en";

export interface User {
  id: string;
  email: string;
  fullName: string;
  company: string;
  role: "admin" | "manager" | "analyst";
  avatar?: string;
  createdAt: string;
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresAt: number;
}

// KPI & Revenue
export interface KPIMetric {
  label: string;
  value: number | string;
  change: number; // percentage change
  trend: "up" | "down" | "neutral";
  icon: string;
  format: "currency" | "number" | "percentage";
}

export interface RevenueDataPoint {
  month: string;
  revenue: number;
  target: number;
  deals: number;
}

// Deal / Lead Pipeline
export type DealStage = "lead" | "qualified" | "proposal" | "negotiation" | "closed_won" | "closed_lost";

export interface Deal {
  id: string;
  title: string;
  company: string;
  value: number;
  currency: "SAR" | "USD";
  stage: DealStage;
  probability: number;
  closeDate: string;
  assignedTo: string;
  lastActivity: string;
  tags: string[];
  aiScore: number; // 0-100
}

// AI Agents
export type AgentType = "outreach" | "scoring" | "compliance" | "intelligence" | "orchestrator";
export type AgentStatus = "running" | "completed" | "pending" | "failed";

export interface AgentActivity {
  id: string;
  agentType: AgentType;
  action: string;
  target: string;
  status: AgentStatus;
  timestamp: string;
  duration?: number; // ms
  metadata?: Record<string, unknown>;
  requiresApproval?: boolean;
}

// Approvals
export type RiskLevel = "high" | "medium" | "low";
export type ApprovalStatus = "pending" | "approved" | "rejected";

export interface ApprovalRequest {
  id: string;
  agentType: AgentType;
  action: string;
  description: string;
  riskLevel: RiskLevel;
  status: ApprovalStatus;
  requestedAt: string;
  reviewedAt?: string;
  reviewedBy?: string;
  target: string;
  metadata?: Record<string, unknown>;
  estimatedImpact?: string;
}

// Clients
export type ClientStatus = "active" | "inactive" | "prospect" | "churned";

export interface Client {
  id: string;
  company: string;
  contactName: string;
  contactEmail: string;
  contactPhone?: string;
  status: ClientStatus;
  industry: string;
  totalDeals: number;
  totalRevenue: number;
  lastActivity: string;
  aiScore: number;
  tags: string[];
}

// Analytics
export interface ConversionFunnelData {
  stage: string;
  count: number;
  conversionRate: number;
}

export interface AgentPerformanceData {
  agent: string;
  actionsCompleted: number;
  successRate: number;
  avgDuration: number;
}

// API Response wrappers
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: "success" | "error";
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  hasMore: boolean;
}

export interface ApiError {
  message: string;
  code?: string;
  details?: Record<string, string[]>;
}
