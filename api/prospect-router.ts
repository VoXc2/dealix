import { z } from "zod";
import { createRouter, publicQuery } from "./middleware";
import {
  findProspects,
  findProspectById,
  createProspect,
  updateProspect,
  deleteProspect,
  getProspectStats,
} from "./queries/prospectQueries";

export const prospectRouter = createRouter({
  list: publicQuery
    .input(z.object({ segment: z.string().optional(), status: z.string().optional(), search: z.string().optional() }).optional())
    .query(({ input }) => findProspects(input)),

  byId: publicQuery
    .input(z.object({ id: z.number() }))
    .query(({ input }) => findProspectById(input.id)),

  create: publicQuery
    .input(z.object({
      company: z.string().min(1),
      segment: z.enum(["marketing_agency", "training_company", "b2b_services", "other"]).optional(),
      website: z.string().optional(),
      decisionMaker: z.string().optional(),
      email: z.string().email().optional(),
      phone: z.string().optional(),
      pain: z.string().optional(),
      status: z.enum(["target", "researched", "contacted", "replied", "discovery_booked", "proposal_sent", "won", "delivery", "retainer", "lost"]).optional(),
      score: z.number().min(1).max(10).optional(),
      offer: z.string().optional(),
      value: z.string().optional(),
      notes: z.string().optional(),
      source: z.string().optional(),
      createdBy: z.number().optional(),
    }))
    .mutation(({ input }) => createProspect(input)),

  update: publicQuery
    .input(z.object({
      id: z.number(),
      company: z.string().optional(),
      segment: z.enum(["marketing_agency", "training_company", "b2b_services", "other"]).optional(),
      website: z.string().optional(),
      decisionMaker: z.string().optional(),
      email: z.string().email().optional(),
      phone: z.string().optional(),
      pain: z.string().optional(),
      status: z.enum(["target", "researched", "contacted", "replied", "discovery_booked", "proposal_sent", "won", "delivery", "retainer", "lost"]).optional(),
      score: z.number().min(1).max(10).optional(),
      offer: z.string().optional(),
      value: z.string().optional(),
      notes: z.string().optional(),
      lastContact: z.date().optional(),
    }))
    .mutation(({ input }) => updateProspect(input.id, input)),

  delete: publicQuery
    .input(z.object({ id: z.number() }))
    .mutation(({ input }) => deleteProspect(input.id)),

  stats: publicQuery.query(() => getProspectStats()),
});
