import { z } from "zod";
import { createRouter, publicQuery } from "./middleware";
import { getDb } from "./queries/connection";
import { companySignals, decisionsLog, assumptionsLog, experimentsLog, riskRegister, opportunityRegister } from "@db/schema";
import { desc, eq, count, sql } from "drizzle-orm";

export const brainRouter = createRouter({
  // ─── Signals ─────────────────────────────────
  signalList: publicQuery.query(async () => {
    const db = getDb();
    return db.select().from(companySignals).orderBy(desc(companySignals.createdAt)).limit(100);
  }),

  signalByType: publicQuery.query(async () => {
    const db = getDb();
    const revenue = await db.select({ count: count() }).from(companySignals).where(eq(companySignals.signalType, "revenue"));
    const pain = await db.select({ count: count() }).from(companySignals).where(eq(companySignals.signalType, "pain"));
    const opportunity = await db.select({ count: count() }).from(companySignals).where(eq(companySignals.signalType, "opportunity"));
    const risk = await db.select({ count: count() }).from(companySignals).where(eq(companySignals.signalType, "risk"));
    const bottleneck = await db.select({ count: count() }).from(companySignals).where(eq(companySignals.signalType, "bottleneck"));
    return { revenue: revenue[0]?.count ?? 0, pain: pain[0]?.count ?? 0, opportunity: opportunity[0]?.count ?? 0, risk: risk[0]?.count ?? 0, bottleneck: bottleneck[0]?.count ?? 0 };
  }),

  signalCreate: publicQuery
    .input(z.object({ signalType: z.string().length(), source: z.string().optional(), description: z.string(), strength: z.number().default(5), confidence: z.number().default(0.5) }))
    .mutation(async ({ input }) => {
      const db = getDb();
      const result = await db.insert(companySignals).values({ ...input });
      return { success: true, id: Number(result[0].insertId) };
    }),

  // ─── Decisions ───────────────────────────────
  decisionList: publicQuery.query(async () => {
    const db = getDb();
    return db.select().from(decisionsLog).orderBy(desc(decisionsLog.createdAt)).limit(100);
  }),

  decisionCreate: publicQuery
    .input(z.object({ decision: z.string(), owner: z.string(), metric: z.string().optional(), assumption: z.string().optional(), nextAction: z.string(), priority: z.number().default(5), status: z.string().default("pending"), dueDate: z.string().optional() }))
    .mutation(async ({ input }) => {
      const db = getDb();
      const result = await db.insert(decisionsLog).values({ ...input });
      return { success: true, id: Number(result[0].insertId) };
    }),

  decisionStats: publicQuery.query(async () => {
    const db = getDb();
    const pending = await db.select({ count: count() }).from(decisionsLog).where(eq(decisionsLog.status, "pending"));
    const inProgress = await db.select({ count: count() }).from(decisionsLog).where(eq(decisionsLog.status, "in_progress"));
    const completed = await db.select({ count: count() }).from(decisionsLog).where(eq(decisionsLog.status, "completed"));
    return { pending: pending[0]?.count ?? 0, inProgress: inProgress[0]?.count ?? 0, completed: completed[0]?.count ?? 0, total: (pending[0]?.count ?? 0) + (inProgress[0]?.count ?? 0) + (completed[0]?.count ?? 0) };
  }),

  // ─── Assumptions ─────────────────────────────
  assumptionList: publicQuery.query(async () => {
    const db = getDb();
    return db.select().from(assumptionsLog).orderBy(desc(assumptionsLog.createdAt)).limit(100);
  }),

  assumptionCreate: publicQuery
    .input(z.object({ assumption: z.string(), source: z.string().optional(), impact: z.string().default("medium") }))
    .mutation(async ({ input }) => {
      const db = getDb();
      const result = await db.insert(assumptionsLog).values({ ...input });
      return { success: true, id: Number(result[0].insertId) };
    }),

  // ─── Risks ────────────────────────────────────
  riskList: publicQuery.query(async () => {
    const db = getDb();
    return db.select().from(riskRegister).orderBy(desc(riskRegister.severity)).limit(100);
  }),

  riskCreate: publicQuery
    .input(z.object({ risk: z.string(), probability: z.number().default(3), impact: z.number().default(3), mitigation: z.string().optional(), owner: z.string().optional() }))
    .mutation(async ({ input }) => {
      const db = getDb();
      const severity = input.probability * input.impact;
      const result = await db.insert(riskRegister).values({ ...input, severity });
      return { success: true, id: Number(result[0].insertId) };
    }),

  // ─── Opportunities ──────────────────────────
  opportunityList: publicQuery.query(async () => {
    const db = getDb();
    return db.select().from(opportunityRegister).orderBy(desc(opportunityRegister.status)).limit(100);
  }),

  opportunityCreate: publicQuery
    .input(z.object({ opportunity: z.string(), potentialValue: z.string().default("0"), confidence: z.number().default(0.5), effort: z.string().default("medium"), owner: z.string().optional() }))
    .mutation(async ({ input }) => {
      const db = getDb();
      const result = await db.insert(opportunityRegister).values({ ...input });
      return { success: true, id: Number(result[0].insertId) };
    }),

  // ─── Dashboard Stats ────────────────────────
  dashboardStats: publicQuery.query(async () => {
    const db = getDb();
    const signals = await db.select({ count: count() }).from(companySignals);
    const decisions = await db.select({ count: count() }).from(decisionsLog);
    const highRisks = await db.select({ count: count() }).from(riskRegister).where(eq(riskRegister.status, "active"));
    const opps = await db.select({ count: count() }).from(opportunityRegister);
    const totalExperiments = await db.select({ count: count() }).from(experimentsLog);
    return {
      signals: signals[0]?.count ?? 0,
      decisions: decisions[0]?.count ?? 0,
      activeRisks: highRisks[0]?.count ?? 0,
      opportunities: opps[0]?.count ?? 0,
      experiments: totalExperiments[0]?.count ?? 0,
    };
  }),
});
