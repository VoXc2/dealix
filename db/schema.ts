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
