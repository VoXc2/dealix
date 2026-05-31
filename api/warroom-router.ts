import { createRouter, publicQuery } from "./middleware";
import { getDb } from "./queries/connection";
import { prospects, followups, proposals, payments, approvalQueue } from "../db/schema";

export const warRoomRouter = createRouter({
  dashboard: publicQuery.query(async () => {
    const db = getDb();
    const [allProspects, allFollowups, allProposals, allPayments, allApprovals] = await Promise.all([
      db.select().from(prospects),
      db.select().from(followups),
      db.select().from(proposals),
      db.select().from(payments),
      db.select().from(approvalQueue),
    ]);
    const revenueCollected = allPayments.filter(p => p.status === "Received").reduce((s, p) => s + Number(p.amountSar), 0);
    const pendingFollowups = allFollowups.filter(f => f.status === "pending").sort((a, b) => +new Date(a.nextDue) - +new Date(b.nextDue)).slice(0, 10);
    const activeProposals = allProposals.filter(p => ["pending_approval", "sent", "negotiating"].includes(p.status)).slice(0, 10);
    const pendingApprovals = allApprovals.filter(a => !a.approved && !a.rejected).slice(0, 10);
    const topProspects = allProspects.filter(p => (p.score || 0) >= 6).sort((a, b) => (b.score || 0) - (a.score || 0)).slice(0, 10);
    return {
      summary: { totalProspects: allProspects.length, pendingFollowups: allFollowups.filter(f => f.status === "pending").length, activeProposals: activeProposals.length, pendingApprovals: pendingApprovals.length, revenueCollected, mrr: 0, wonDeals: allProposals.filter(p => p.status === "won").length },
      pipeline: { target: allProspects.filter(p => p.status === "Target").length, researched: allProspects.filter(p => p.status === "Researched").length, contacted: allProspects.filter(p => p.status === "Contacted").length, replied: allProspects.filter(p => p.status === "Replied").length, discoveryBooked: allProspects.filter(p => p.status === "Discovery Booked").length, proposalSent: allProspects.filter(p => p.status === "Proposal Sent").length, won: allProspects.filter(p => p.status === "Won").length },
      topProspects, pendingFollowups, activeProposals, pendingApprovals,
    };
  }),
  dailyTargets: publicQuery.query(() => ({ cashTarget: 5000, meetingsTarget: 3, proposalsTarget: 1, outreachTarget: 5, followupsTarget: 5, prospectsTarget: 10, proofEventsTarget: 1 })),
});
