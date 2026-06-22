import { z } from "zod";
import { createRouter, publicQuery } from "./middleware";
import { getDb } from "./queries/connection";
import { drafts, prospects } from "@db/schema";
import { desc, eq, count, and } from "drizzle-orm";

export const commandRoomRouter = createRouter({
  // ─── Drafts Queue ──────────────────────────────────────────────────
  draftList: publicQuery.query(async () => {
    const db = getDb();
    return db
      .select()
      .from(drafts)
      .orderBy(desc(drafts.priority))
      .limit(100);
  }),

  draftByStatus: publicQuery
    .input(z.object({ status: z.string().optional() }))
    .query(async ({ input }) => {
      const db = getDb();
      let query;
      if (input.status === "approved") {
        query = db.select().from(drafts).where(eq(drafts.approved, true)).orderBy(desc(drafts.priority));
      } else if (input.status === "pending") {
        query = db.select().from(drafts).where(eq(drafts.approved, false)).orderBy(desc(drafts.priority));
      } else if (input.status === "sent") {
        query = db.select().from(drafts).where(eq(drafts.sent, true)).orderBy(desc(drafts.createdAt));
      } else {
        query = db.select().from(drafts).orderBy(desc(drafts.priority));
      }
      return query.limit(100);
    }),

  approveDraft: publicQuery
    .input(z.object({ id: z.number() }))
    .mutation(async ({ input }) => {
      const db = getDb();
      await db.update(drafts).set({ approved: true }).where(eq(drafts.id, input.id));
      return { success: true };
    }),

  rejectDraft: publicQuery
    .input(z.object({ id: z.number() }))
    .mutation(async ({ input }) => {
      const db = getDb();
      await db.delete(drafts).where(eq(drafts.id, input.id));
      return { success: true };
    }),

  markSent: publicQuery
    .input(z.object({ id: z.number() }))
    .mutation(async ({ input }) => {
      const db = getDb();
      await db.update(drafts).set({ sent: true }).where(eq(drafts.id, input.id));
      return { success: true };
    }),

  // ─── Draft Stats ─────────────────────────────────────────────────
  draftStats: publicQuery.query(async () => {
    const db = getDb();
    const total = await db.select({ count: count() }).from(drafts);
    const approved = await db.select({ count: count() }).from(drafts).where(eq(drafts.approved, true));
    const sent = await db.select({ count: count() }).from(drafts).where(eq(drafts.sent, true));
    const pending = await db.select({ count: count() }).from(drafts).where(and(eq(drafts.approved, false), eq(drafts.sent, false)));
    return {
      total: total[0]?.count ?? 0,
      approved: approved[0]?.count ?? 0,
      sent: sent[0]?.count ?? 0,
      pending: pending[0]?.count ?? 0,
    };
  }),

  // ─── Pospects Pipeline ───────────────────────────────────────────
  pipelineByStage: publicQuery.query(async () => {
    const db = getDb();
    const stages: string[] = ["target", "researched", "contacted", "replied", "discovery_booked", "proposal_sent", "won", "delivery", "retainer", "lost"];
    const counts: Record<string, number> = {};
    for (const stage of stages) {
      const c = await db.select({ count: count() }).from(prospects).where(eq(prospects.status, stage as any));
      counts[stage] = c[0]?.count ?? 0;
    }
    return counts;
  }),

  // ─── Top Opportunities ─────────────────────────────────────────
  topOpportunities: publicQuery.query(async () => {
    const db = getDb();
    return db
      .select()
      .from(prospects)
      .where(eq(prospects.status, "discovery_booked"))
      .orderBy(desc(prospects.value))
      .limit(10);
  }),
});
