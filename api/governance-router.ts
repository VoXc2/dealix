import { z } from "zod";
import { createRouter, publicQuery } from "./middleware";
import { getDb } from "./queries/connection";
import { approvalQueue, aiActionLedger } from "../db/schema";
import { eq, desc } from "drizzle-orm";

export const governanceRouter = createRouter({
  approvalQueue: publicQuery.query(async () => {
    const db = getDb();
    return db.select().from(approvalQueue).orderBy(desc(approvalQueue.createdAt));
  }),
  pendingApprovals: publicQuery.query(async () => {
    const db = getDb();
    return db.select().from(approvalQueue).where(eq(approvalQueue.approved, false)).orderBy(desc(approvalQueue.createdAt));
  }),
  approve: publicQuery
    .input(z.object({ id: z.number(), approvedBy: z.string(), rejectionReason: z.string().optional() }))
    .mutation(async ({ input }) => {
      const db = getDb();
      const data = input.rejectionReason
        ? { approved: false, rejected: true, rejectionReason: input.rejectionReason, approvedBy: input.approvedBy, approvedAt: new Date() }
        : { approved: true, rejected: false, approvedBy: input.approvedBy, approvedAt: new Date() };
      await db.update(approvalQueue).set(data).where(eq(approvalQueue.id, input.id));
      return { success: true };
    }),
  ledger: publicQuery.query(async () => {
    const db = getDb();
    return db.select().from(aiActionLedger).orderBy(desc(aiActionLedger.time));
  }),
  stats: publicQuery.query(async () => {
    const db = getDb();
    const [approvals, ledger] = await Promise.all([
      db.select().from(approvalQueue),
      db.select().from(aiActionLedger),
    ]);
    return {
      approvals: { total: approvals.length, pending: approvals.filter(a => !a.approved && !a.rejected).length, approved: approvals.filter(a => a.approved).length },
      ledger: { total: ledger.length },
    };
  }),
});
