import { z } from "zod";
import { createRouter, publicQuery } from "./middleware";
import { getDb } from "./queries/connection";
import { payments } from "../db/schema";
import { desc } from "drizzle-orm";

export const financeRouter = createRouter({
  payments: publicQuery.query(async () => {
    const db = getDb();
    return db.select().from(payments).orderBy(desc(payments.createdAt));
  }),
  createPayment: publicQuery
    .input(z.object({ invoiceId: z.string(), clientName: z.string(), amountSar: z.string(), status: z.enum(["Received", "Pending", "Overdue"]).default("Pending"), notes: z.string().optional() }))
    .mutation(async ({ input }) => {
      const db = getDb();
      const result = await db.insert(payments).values(input);
      return { id: Number(result[0].insertId) };
    }),
  stats: publicQuery.query(async () => {
    const db = getDb();
    const all = await db.select().from(payments);
    return { totalRevenue: all.filter(p => p.status === "Received").reduce((s, p) => s + Number(p.amountSar), 0), pendingRevenue: all.filter(p => p.status === "Pending").reduce((s, p) => s + Number(p.amountSar), 0), totalPayments: all.length };
  }),
});
