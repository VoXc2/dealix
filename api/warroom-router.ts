import { z } from "zod";
import { createRouter, publicQuery } from "./middleware";
import { getDb } from "./queries/connection";
import { warRoomSnapshots, prospects, deals, activities } from "@db/schema";
import { eq, desc, count, sql } from "drizzle-orm";

export const warRoomRouter = createRouter({
  // Get today's war room data
  today: publicQuery.query(async () => {
    const db = getDb();
    // Pipeline health
    const pipelineByStatus = await db
      .select({ status: prospects.status, count: count(), totalValue: sql<number>`COALESCE(SUM(${prospects.value}), 0)` })
      .from(prospects)
      .groupBy(prospects.status);
    
    // Recent activities
    const recentActivities = await db
      .select()
      .from(activities)
      .orderBy(desc(activities.createdAt))
      .limit(10);
    
    // Deals summary
    const dealsSummary = await db
      .select({ stage: deals.stage, count: count(), value: sql<number>`COALESCE(SUM(${deals.value}), 0)` })
      .from(deals)
      .groupBy(deals.stage);
    
    // Key metrics
    const totalProspects = await db.select({ count: count() }).from(prospects);
    const totalDeals = await db.select({ count: count() }).from(deals);
    const totalActivities = await db.select({ count: count() }).from(activities);
    const revenueWon = await db
      .select({ total: sql<number>`COALESCE(SUM(${deals.value}), 0)` })
      .from(deals)
      .where(eq(deals.stage, "won"));
    
    // Hot prospects (score >= 8)
    const hotProspects = await db
      .select()
      .from(prospects)
      .where(sql`${prospects.score} >= 8`)
      .orderBy(desc(prospects.score))
      .limit(5);
    
    return {
      pipeline: pipelineByStatus,
      recentActivities,
      dealsSummary,
      metrics: {
        totalProspects: totalProspects[0]?.count ?? 0,
        totalDeals: totalDeals[0]?.count ?? 0,
        totalActivities: totalActivities[0]?.count ?? 0,
        revenueWon: revenueWon[0]?.total ?? 0,
      },
      hotProspects,
    };
  }),

  // Save a snapshot
  saveSnapshot: publicQuery
    .input(z.object({
      date: z.string(),
      type: z.enum(["daily", "weekly"]),
      metrics: z.object({
        newProspects: z.number(),
        outreachSent: z.number(),
        followupsDone: z.number(),
        callsBooked: z.number(),
        proposalsSent: z.number(),
        dealsClosed: z.number(),
        revenueCollected: z.number(),
      }),
      topActions: z.array(z.string()).optional(),
      risks: z.array(z.string()).optional(),
      notes: z.string().optional(),
      createdBy: z.number().optional(),
    }))
    .mutation(({ input }) => {
      const db = getDb();
      return db.insert(warRoomSnapshots).values(input);
    }),

  // Get snapshots history
  snapshots: publicQuery
    .input(z.object({ type: z.enum(["daily", "weekly"]).optional() }).optional())
    .query(async ({ input }) => {
      const db = getDb();
      if (input?.type) {
        return db.select().from(warRoomSnapshots).where(eq(warRoomSnapshots.type, input.type)).orderBy(desc(warRoomSnapshots.createdAt)).limit(30);
      }
      return db.select().from(warRoomSnapshots).orderBy(desc(warRoomSnapshots.createdAt)).limit(30);
    }),

  // Seed sample data
  seed: publicQuery.mutation(async () => {
    const db = getDb();
    
    // Check if data already exists
    const existing = await db.select({ count: count() }).from(prospects);
    if ((existing[0]?.count ?? 0) > 0) {
      return { message: "Data already exists, skipping seed" };
    }
    
    // Seed prospects
    const sampleProspects = [
      { company: "Digital Rise Agency", segment: "marketing_agency" as const, decisionMaker: "Ahmed Al-Rashid", email: "ahmed@digitalrise.sa", pain: "Leads not converting, no follow-up system", status: "contacted" as const, score: 9, offer: "Revenue Intelligence Sprint", value: "5000", notes: "Responsive, interested in sprint" },
      { company: "TrainMe KSA", segment: "training_company" as const, decisionMaker: "Khalid Al-Saud", email: "khalid@trainme.sa", pain: "WhatsApp inquiries lost, low conversion", status: "researched" as const, score: 8, offer: "Revenue Intelligence Sprint", value: "5000", notes: "Seasonal campaigns failing" },
      { company: "CloudShift Consulting", segment: "b2b_services" as const, decisionMaker: "Fahd Al-Harbi", email: "fahd@cloudshift.sa", pain: "Slow deal closure, weak CRM", status: "discovery_booked" as const, score: 7, offer: "Revenue Intelligence Sprint", value: "7500", notes: "Discovery call scheduled for next week" },
      { company: "Growth Labs SA", segment: "marketing_agency" as const, decisionMaker: "Sami Al-Otaibi", email: "sami@growthlabs.sa", pain: "No follow-up system", status: "contacted" as const, score: 9, offer: "Revenue Intelligence Sprint", value: "2500", notes: "Discounted first client" },
      { company: "SkillUp Arabia", segment: "training_company" as const, decisionMaker: "Mohaned Al-Qahtani", email: "mohaned@skillup.sa", pain: "Low registration rate", status: "target" as const, score: 7, offer: "Revenue Intelligence Sprint", value: "5000" },
      { company: "Nexus IT Solutions", segment: "b2b_services" as const, decisionMaker: "Omar Al-Zahrani", email: "omar@nexusit.sa", pain: "Weak CRM usage", status: "researched" as const, score: 6, offer: "Revenue Intelligence Sprint", value: "5000" },
      { company: "MediaPulse Agency", segment: "marketing_agency" as const, decisionMaker: "Tariq Al-Shammari", email: "tariq@mediapulse.sa", pain: "No proof for clients", status: "proposal_sent" as const, score: 8, offer: "AI Sales Ops Retainer", value: "8000" },
      { company: "Elevate Training", segment: "training_company" as const, decisionMaker: "Yasser Al-Mutairi", email: "yasser@elevate.sa", pain: "Seasonal campaigns fail", status: "target" as const, score: 7, offer: "Revenue Intelligence Sprint", value: "5000" },
    ];
    
    for (const p of sampleProspects) {
      await db.insert(prospects).values(p);
    }
    
    // Seed deals
    const sampleDeals = [
      { prospectId: 1, name: "Digital Rise - P1 Sprint", type: "p1_sprint" as const, stage: "negotiation" as const, value: "5000", probability: 70 },
      { prospectId: 4, name: "Growth Labs - P1 Sprint", type: "p1_sprint" as const, stage: "proposal" as const, value: "2500", probability: 50 },
      { prospectId: 3, name: "CloudShift - P1 Sprint", type: "p1_sprint" as const, stage: "won" as const, value: "7500", probability: 100 },
      { prospectId: 7, name: "MediaPulse - P2 Medium", type: "p2_medium" as const, stage: "lead" as const, value: "8000", probability: 30 },
    ];
    
    for (const d of sampleDeals) {
      await db.insert(deals).values(d);
    }
    
    // Seed activities
    const sampleActivities = [
      { prospectId: 1, type: "email" as const, direction: "outbound" as const, subject: "P1 Sprint Introduction", body: "Introduced our Revenue Intelligence Sprint...", status: "completed" as const },
      { prospectId: 1, type: "call" as const, direction: "outbound" as const, subject: "Discovery Call", body: "Discussed pain points and objectives", status: "completed" as const },
      { prospectId: 3, type: "meeting" as const, direction: "inbound" as const, subject: "Proposal Review", body: "Client accepted proposal with minor changes", status: "completed" as const },
      { prospectId: 4, type: "email" as const, direction: "outbound" as const, subject: "Follow-up: Sprint Details", body: "Sent detailed sprint breakdown", status: "completed" as const },
      { prospectId: 7, type: "followup" as const, direction: "outbound" as const, subject: "Weekly Follow-up", body: "Checking on proposal status", status: "pending" as const },
    ];
    
    for (const a of sampleActivities) {
      await db.insert(activities).values(a);
    }
    
    return { message: "Sample data seeded successfully" };
  }),
});
