import {
  mysqlTable,
  mysqlEnum,
  serial,
  varchar,
  text,
  timestamp,
  int,
  json,
  decimal,
  boolean,
  bigint,
  date,
} from "drizzle-orm/mysql-core";

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

export const prospects = mysqlTable("prospects", {
  id: serial("id").primaryKey(),
  company: varchar("company", { length: 255 }).notNull(),
  segment: mysqlEnum("segment", ["Marketing Agency", "Training", "B2B Services", "Other"]).notNull(),
  website: varchar("website", { length: 255 }),
  decisionMaker: varchar("decision_maker", { length: 255 }),
  pain: text("pain"),
  status: mysqlEnum("status", [
    "Target", "Researched", "Contacted", "Replied",
    "Discovery Booked", "Proposal Sent", "Won", "Lost", "Nurturing"
  ]).default("Target").notNull(),
  nextAction: varchar("next_action", { length: 500 }),
  nextDate: date("next_date"),
  offer: varchar("offer", { length: 255 }),
  lastTouch: date("last_touch"),
  score: int("score").default(5),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
});

export type Prospect = typeof prospects.$inferSelect;

export const followups = mysqlTable("followups", {
  id: serial("id").primaryKey(),
  prospectId: bigint("prospect_id", { mode: "number", unsigned: true }).references(() => prospects.id),
  company: varchar("company", { length: 255 }).notNull(),
  lastContact: date("last_contact"),
  nextDue: date("next_due").notNull(),
  status: mysqlEnum("status", ["pending", "sent", "completed", "overdue"]).default("pending").notNull(),
  draftMessage: text("draft_message"),
  channel: mysqlEnum("channel", ["email", "whatsapp", "phone"]).default("email").notNull(),
  priority: mysqlEnum("priority", ["low", "medium", "high"]).default("medium").notNull(),
  approved: boolean("approved").default(false),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const proposals = mysqlTable("proposals", {
  id: serial("id").primaryKey(),
  clientName: varchar("client_name", { length: 255 }).notNull(),
  service: varchar("service", { length: 255 }).notNull(),
  package: mysqlEnum("package", ["Basic", "Standard", "Premium"]).default("Standard").notNull(),
  valueSar: decimal("value_sar", { precision: 12, scale: 2 }).notNull(),
  status: mysqlEnum("status", ["draft", "pending_approval", "sent", "negotiating", "won", "lost"])
    .default("draft").notNull(),
  sentDate: date("sent_date"),
  expiryDate: date("expiry_date"),
  approver: varchar("approver", { length: 255 }),
  probability: decimal("probability", { precision: 3, scale: 2 }).default("0.50"),
  notes: text("notes"),
  deliverables: json("deliverables"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull().$onUpdate(() => new Date()),
});

export const payments = mysqlTable("payments", {
  id: serial("id").primaryKey(),
  invoiceId: varchar("invoice_id", { length: 100 }).notNull(),
  clientName: varchar("client_name", { length: 255 }).notNull(),
  amountSar: decimal("amount_sar", { precision: 12, scale: 2 }).notNull(),
  paymentDate: date("payment_date"),
  paymentMethod: mysqlEnum("payment_method", ["Bank Transfer", "Credit Card", "Cash", "Other"])
    .default("Bank Transfer").notNull(),
  status: mysqlEnum("status", ["Received", "Pending", "Overdue", "Cancelled"]).default("Pending").notNull(),
  reference: varchar("reference", { length: 255 }),
  notes: text("notes"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const approvalQueue = mysqlTable("approval_queue", {
  id: serial("id").primaryKey(),
  itemType: mysqlEnum("item_type", [
    "outreach_message", "proposal_pricing", "proof_pack", "followup_sequence", "governance_change"
  ]).notNull(),
  company: varchar("company", { length: 255 }).notNull(),
  risk: mysqlEnum("risk", ["low", "medium", "high", "critical"]).default("medium").notNull(),
  draft: text("draft"),
  requiresApproval: boolean("requires_approval").default(true),
  approved: boolean("approved").default(false),
  approvedBy: varchar("approved_by", { length: 255 }),
  approvedAt: timestamp("approved_at"),
  rejected: boolean("rejected").default(false),
  rejectionReason: text("rejection_reason"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

export const aiActionLedger = mysqlTable("ai_action_ledger", {
  id: serial("id").primaryKey(),
  time: timestamp("time").defaultNow().notNull(),
  agent: varchar("agent", { length: 255 }).notNull(),
  action: varchar("action", { length: 255 }).notNull(),
  company: varchar("company", { length: 255 }),
  risk: mysqlEnum("risk", ["low", "medium", "high", "critical"]).default("low").notNull(),
  requiresApproval: boolean("requires_approval").default(false),
  approved: boolean("approved").default(false),
  context: text("context"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});
