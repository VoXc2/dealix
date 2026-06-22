import { z } from "zod";
import { createRouter, publicQuery } from "./middleware";
import { getDb } from "./queries/connection";
import { bookings } from "@db/schema";
import { desc, count, eq } from "drizzle-orm";

export const bookingRouter = createRouter({
  // Create a booking (public)
  create: publicQuery
    .input(
      z.object({
        name: z.string().min(2),
        company: z.string().min(2),
        role: z.string().min(2),
        website: z.string().optional(),
        pain: z.string().optional(),
        currentSystems: z.string().optional(),
        consentEmail: z.boolean().default(false),
        scheduledAt: z.string().optional(), // ISO date string
      })
    )
    .mutation(async ({ input }) => {
      const db = getDb();
      const result = await db.insert(bookings).values({
        name: input.name,
        company: input.company,
        role: input.role,
        website: input.website || null,
        pain: input.pain || null,
        currentSystems: input.currentSystems || null,
        consentEmail: input.consentEmail,
        status: "scheduled",
      });
      return { success: true, bookingId: Number(result[0].insertId) };
    }),

  // List bookings (admin only in production, public for demo)
  list: publicQuery.query(async () => {
    const db = getDb();
    return db
      .select()
      .from(bookings)
      .orderBy(desc(bookings.createdAt))
      .limit(100);
  }),

  // Get booking stats
  stats: publicQuery.query(async () => {
    const db = getDb();
    const total = await db.select({ count: count() }).from(bookings);
    const todayStr = new Date().toISOString().split("T")[0];
    const today = await db
      .select({ count: count() })
      .from(bookings)
      .where(eq(bookings.status, "scheduled"));
    return {
      total: total[0]?.count ?? 0,
      scheduled: today[0]?.count ?? 0,
    };
  }),
});
