import { z } from "zod";
import { createRouter, publicQuery } from "./middleware";
import { getDb } from "./queries/connection";
import { prospects } from "../db/schema";
import { eq, desc } from "drizzle-orm";

export const prospectRouter = createRouter({
  list: publicQuery.query(async () => {
    const db = getDb();
    return db.select().from(prospects).orderBy(desc(prospects.score));
  }),
  create: publicQuery
    .input(z.object({
      company: z.string().min(1),
      segment: z.enum(["Marketing Agency", "Training", "B2B Services", "Other"]),
      website: z.string().optional(),
      decisionMaker: z.string().optional(),
      pain: z.string().optional(),
      status: z.enum(["Target", "Researched", "Contacted", "Replied", "Discovery Booked", "Proposal Sent", "Won", "Lost", "Nurturing"]).default("Target"),
      nextAction: z.string().optional(),
      score: z.number().min(1).max(10).default(5),
    }))
    .mutation(async ({ input }) => {
      const db = getDb();
      const result = await db.insert(prospects).values(input);
      return { id: Number(result[0].insertId) };
    }),
  delete: publicQuery
    .input(z.object({ id: z.number() }))
    .mutation(async ({ input }) => {
      const db = getDb();
      await db.delete(prospects).where(eq(prospects.id, input.id));
      return { success: true };
    }),
  stats: publicQuery.query(async () => {
    const db = getDb();
    const all = await db.select().from(prospects);
    const byStatus: Record<string, number> = {};
    const bySegment: Record<string, number> = {};
    for (const p of all) {
      byStatus[p.status] = (byStatus[p.status] || 0) + 1;
      bySegment[p.segment] = (bySegment[p.segment] || 0) + 1;
    }
    return { total: all.length, byStatus, bySegment };
  }),
});
