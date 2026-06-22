import {
  mysqlTable,
  mysqlEnum,
  serial,
  varchar,
  text,
  timestamp,
  bigint,
  int,
  decimal,
  json,
  boolean,
} from "drizzle-orm/mysql-core";

// ─── Users (Auth) ──────────────────────────────────────────
export const users = mysqlTable("users", {
  id: serial("id").primaryKey(),
  unionId: varchar("unionId", { length: 255 }).notNull().unique(),
  name: varchar("name", { length: 255 }),
  email: varchar("email", { length: 320 }),
  avatar: text("avatar"),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().notNull().$onUpdate(() => new Date()),
  lastSignInAt: timestamp("lastSignInAt").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

// ─── Prospects ─────────────────────────────────────────────
export const prospects = mysqlTable("prospects", {
  id: serial("id").primaryKey(),
  company: varchar("company", { length: 255 }).notNull(),
  segment: mysqlEnum("segment", ["marketing_agency", "training_company", "b2b_services", "other"]).default("other").notNull(),
  website: varchar("website", { length: 255 }),
  decisionMaker: varchar("decision_maker", { length: 255 }),
  email: varchar("email", { length: 320 }),
  phone: varchar("phone", { length: 50 }),
  pain: text("pain"),
  status: mysqlEnum("status", [
    "target",
    "researched",
    "contacted",
    "replied",
    "discovery_booked",
    "proposal_sent",
    "won",
    "delivery",
    "retainer",
    "lost",
  ]).default("target").notNull(),
  score: int("score").default(5).notNull(),
  offer: varchar("offer", { length: 255 }),
  value: decimal("value", { precision: 12, scale: 2 }).default("0"),
  notes: text("notes"),
  source: varchar("source", { length: 100 }),
  createdBy: bigint("created_by", { mode: "number", unsigned: true }).references(() => users.id),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
  lastContact: timestamp("last_contact"),
});

export type Prospect = typeof prospects.$inferSelect;
export type InsertProspect = typeof prospects.$inferInsert;

// ─── Activities ────────────────────────────────────────────
export const activities = mysqlTable("activities", {
  id: serial("id").primaryKey(),
  prospectId: bigint("prospect_id", { mode: "number", unsigned: true }).references(() => prospects.id),
  type: mysqlEnum("type", ["email", "call", "meeting", "followup", "note", "proposal", "payment", "delivery"]).notNull(),
  direction: mysqlEnum("direction", ["inbound", "outbound"]).default("outbound"),
  subject: varchar("subject", { length: 500 }),
  body: text("body"),
  status: mysqlEnum("activity_status", ["pending", "completed", "cancelled", "overdue"]).default("pending"),
  scheduledAt: timestamp("scheduled_at"),
  completedAt: timestamp("completed_at"),
  aiGenerated: boolean("ai_generated").default(false),
  approved: boolean("approved").default(true),
  createdBy: bigint("created_by", { mode: "number", unsigned: true }).references(() => users.id),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type Activity = typeof activities.$inferSelect;
export type InsertActivity = typeof activities.$inferInsert;

// ─── Deals ─────────────────────────────────────────────────
export const deals = mysqlTable("deals", {
  id: serial("id").primaryKey(),
  prospectId: bigint("prospect_id", { mode: "number", unsigned: true }).references(() => prospects.id).notNull(),
  name: varchar("name", { length: 255 }).notNull(),
  type: mysqlEnum("deal_type", ["p1_sprint", "p2_small", "p2_medium", "p2_enterprise"]).default("p1_sprint").notNull(),
  stage: mysqlEnum("stage", ["lead", "qualified", "proposal", "negotiation", "won", "lost"]).default("lead").notNull(),
  value: decimal("value", { precision: 12, scale: 2 }).notNull(),
  probability: int("probability").default(10).notNull(),
  expectedClose: timestamp("expected_close"),
  actualClose: timestamp("actual_close"),
  description: text("description"),
  createdBy: bigint("created_by", { mode: "number", unsigned: true }).references(() => users.id),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
});

export type Deal = typeof deals.$inferSelect;
export type InsertDeal = typeof deals.$inferInsert;

// ─── War Room Snapshots ────────────────────────────────────
export const warRoomSnapshots = mysqlTable("war_room_snapshots", {
  id: serial("id").primaryKey(),
  date: varchar("date", { length: 10 }).notNull(), // YYYY-MM-DD
  type: mysqlEnum("snapshot_type", ["daily", "weekly"]).default("daily").notNull(),
  metrics: json("metrics").$type<{
    newProspects: number;
    outreachSent: number;
    followupsDone: number;
    callsBooked: number;
    proposalsSent: number;
    dealsClosed: number;
    revenueCollected: number;
  }>().notNull(),
  topActions: json("top_actions").$type<string[]>(),
  risks: json("risks").$type<string[]>(),
  notes: text("notes"),
  createdBy: bigint("created_by", { mode: "number", unsigned: true }).references(() => users.id),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type WarRoomSnapshot = typeof warRoomSnapshots.$inferSelect;
export type InsertWarRoomSnapshot = typeof warRoomSnapshots.$inferInsert;

// ─── Bookings (Built-in Booking System) ────────────────────
export const bookings = mysqlTable("bookings", {
  id: serial("id").primaryKey(),
  name: varchar("name", { length: 255 }).notNull(),
  company: varchar("company", { length: 255 }).notNull(),
  role: varchar("role", { length: 255 }).notNull(),
  website: varchar("website", { length: 255 }),
  pain: varchar("pain", { length: 255 }),
  currentSystems: varchar("current_systems", { length: 255 }),
  consentEmail: boolean("consent_email").default(false),
  scheduledAt: timestamp("scheduled_at"),
  status: mysqlEnum("status", ["scheduled", "completed", "cancelled"]).default("scheduled").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type Booking = typeof bookings.$inferSelect;
export type InsertBooking = typeof bookings.$inferInsert;

// ─── Drafts (Outreach Approval Queue) ──────────────────────
export const drafts = mysqlTable("drafts", {
  id: serial("id").primaryKey(),
  prospectId: bigint("prospect_id", { mode: "number", unsigned: true }).references(() => prospects.id),
  type: mysqlEnum("draft_type", ["email", "linkedin", "whatsapp", "proposal"]).notNull(),
  contentAr: text("content_ar"),
  contentEn: text("content_en"),
  priority: int("priority").default(5).notNull(),
  recommendedSendDate: varchar("recommended_send_date", { length: 10 }),
  approved: boolean("approved").default(false),
  sent: boolean("sent").default(false),
  outboundMode: varchar("outbound_mode", { length: 50 }).default("draft_only"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type Draft = typeof drafts.$inferSelect;
export type InsertDraft = typeof drafts.$inferInsert;

// ─── Settings ──────────────────────────────────────────────
export const settings = mysqlTable("settings", {
  id: serial("id").primaryKey(),
  key: varchar("key", { length: 255 }).notNull().unique(),
  value: text("value"),
  category: varchar("category", { length: 100 }).default("general"),
  updatedAt: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
});

export type Setting = typeof settings.$inferSelect;
export type InsertSetting = typeof settings.$inferInsert;

// ─── Company Signals (Brain OS) ────────────────────────────
export const companySignals = mysqlTable("company_signals", {
  id: serial("id").primaryKey(),
  signalType: mysqlEnum("signal_type", ["revenue", "pain", "opportunity", "risk", "market", "competitor", "bottleneck"]).notNull(),
  source: varchar("source", { length: 255 }),
  description: text("description").notNull(),
  strength: int("strength").default(5).notNull(),
  confidence: decimal("confidence", { precision: 3, scale: 2 }).default("0.50"),
  verified: boolean("verified").default(false),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type CompanySignal = typeof companySignals.$inferSelect;
export type InsertCompanySignal = typeof companySignals.$inferInsert;

// ─── Decisions Log (Brain OS) ──────────────────────────────
export const decisionsLog = mysqlTable("decisions_log", {
  id: serial("id").primaryKey(),
  decision: text("decision").notNull(),
  owner: varchar("owner", { length: 255 }).notNull(),
  metric: varchar("metric", { length: 255 }),
  assumption: text("assumption"),
  nextAction: text("next_action").notNull(),
  priority: int("priority").default(5).notNull(),
  status: mysqlEnum("decision_status", ["pending", "in_progress", "completed", "cancelled", "deferred"]).default("pending").notNull(),
  dueDate: varchar("due_date", { length: 10 }),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type DecisionLog = typeof decisionsLog.$inferSelect;
export type InsertDecisionLog = typeof decisionsLog.$inferInsert;

// ─── Assumptions Log (Brain OS) ────────────────────────────
export const assumptionsLog = mysqlTable("assumptions_log", {
  id: serial("id").primaryKey(),
  assumption: text("assumption").notNull(),
  source: varchar("source", { length: 255 }),
  validated: boolean("validated").default(false),
  validationDate: timestamp("validation_date"),
  impact: mysqlEnum("impact", ["high", "medium", "low"]).default("medium").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type AssumptionLog = typeof assumptionsLog.$inferSelect;
export type InsertAssumptionLog = typeof assumptionsLog.$inferInsert;

// ─── Experiments Log (Brain OS) ────────────────────────────
export const experimentsLog = mysqlTable("experiments_log", {
  id: serial("id").primaryKey(),
  name: varchar("name", { length: 255 }).notNull(),
  hypothesis: text("hypothesis").notNull(),
  status: mysqlEnum("experiment_status", ["planned", "running", "completed", "cancelled"]).default("planned").notNull(),
  result: text("result"),
  metric: varchar("metric", { length: 255 }),
  startDate: varchar("start_date", { length: 10 }),
  endDate: varchar("end_date", { length: 10 }),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type ExperimentLog = typeof experimentsLog.$inferSelect;
export type InsertExperimentLog = typeof experimentsLog.$inferInsert;

// ─── Risk Register (Brain OS) ──────────────────────────────
export const riskRegister = mysqlTable("risk_register", {
  id: serial("id").primaryKey(),
  risk: text("risk").notNull(),
  probability: int("probability").default(3).notNull(),
  impact: int("impact").default(3).notNull(),
  severity: int("severity").default(9).notNull(),
  mitigation: text("mitigation"),
  owner: varchar("owner", { length: 255 }),
  status: mysqlEnum("risk_status", ["active", "mitigated", "accepted", "transferred"]).default("active").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type RiskRegister = typeof riskRegister.$inferSelect;
export type InsertRiskRegister = typeof riskRegister.$inferInsert;

// ─── Opportunity Register (Brain OS) ───────────────────────
export const opportunityRegister = mysqlTable("opportunity_register", {
  id: serial("id").primaryKey(),
  opportunity: text("opportunity").notNull(),
  potentialValue: decimal("potential_value", { precision: 12, scale: 2 }).default("0"),
  confidence: decimal("confidence", { precision: 3, scale: 2 }).default("0.50"),
  effort: mysqlEnum("effort", ["low", "medium", "high"]).default("medium").notNull(),
  priority: int("priority").default(5).notNull(),
  owner: varchar("owner", { length: 255 }),
  status: mysqlEnum("opp_status", ["new", "evaluating", "approved", "rejected"]).default("new").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export type OpportunityRegister = typeof opportunityRegister.$inferSelect;
export type InsertOpportunityRegister = typeof opportunityRegister.$inferInsert;
