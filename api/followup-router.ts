import { z } from "zod";
import { createRouter, publicQuery } from "./middleware";
import { getDb } from "./queries/connection";
import { followups } from "../db/schema";
import { desc } from "drizzle-orm";

export const followupRouter = createRouter({
  list: publicQuery.query(async () => {
    const db = getDb();
    return db.select().from(followups).orderBy(desc(followups.nextDue));
  }),
  create: publicQuery
    .input(z.object({ company: z.string(), nextDue: z.string(), draftMessage: z.string().optional(), priority: z.enum(["low", "medium", "high"]).default("medium") }))
    .mutation(async ({ input }) => {
      const db = getDb();
      const result = await db.insert(followups).values({ ...input, nextDue: new Date(input.nextDue) });
      return { id: Number(result[0].insertId) };
    }),
  stats: publicQuery.query(async () => {
    const db = getDb();
    const all = await db.select().from(followups);
    return { total: all.length, pending: all.filter(f => f.status === "pending").length };
  }),
});
