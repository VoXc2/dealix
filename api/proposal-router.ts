import { z } from "zod";
import { createRouter, publicQuery } from "./middleware";
import { getDb } from "./queries/connection";
import { proposals } from "../db/schema";
import { desc } from "drizzle-orm";

export const proposalRouter = createRouter({
  list: publicQuery.query(async () => {
    const db = getDb();
    return db.select().from(proposals).orderBy(desc(proposals.createdAt));
  }),
  create: publicQuery
    .input(z.object({
      clientName: z.string().min(1),
      service: z.string().min(1),
      package: z.enum(["Basic", "Standard", "Premium"]).default("Standard"),
      valueSar: z.string(),
      status: z.enum(["draft", "pending_approval", "sent", "negotiating", "won", "lost"]).default("draft"),
      probability: z.string().optional(),
      notes: z.string().optional(),
    }))
    .mutation(async ({ input }) => {
      const db = getDb();
      const result = await db.insert(proposals).values({ ...input, probability: input.probability || "0.50" });
      return { id: Number(result[0].insertId) };
    }),
  stats: publicQuery.query(async () => {
    const db = getDb();
    const all = await db.select().from(proposals);
    const totalValue = all.reduce((s, p) => s + Number(p.valueSar), 0);
    return { total: all.length, totalValue, won: all.filter(p => p.status === "won").length };
  }),
});
