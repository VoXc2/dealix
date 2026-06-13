import { z } from "zod";
import { createRouter, publicQuery } from "./middleware";
import {
  findDeals,
  findDealById,
  createDeal,
  updateDeal,
  deleteDeal,
  getDealStats,
} from "./queries/dealQueries";

export const dealRouter = createRouter({
  list: publicQuery
    .input(z.object({ stage: z.string().optional(), type: z.string().optional() }).optional())
    .query(({ input }) => findDeals(input)),

  byId: publicQuery
    .input(z.object({ id: z.number() }))
    .query(({ input }) => findDealById(input.id)),

  create: publicQuery
    .input(z.object({
      prospectId: z.number(),
      name: z.string().min(1),
      type: z.enum(["p1_sprint", "p2_small", "p2_medium", "p2_enterprise"]),
      stage: z.enum(["lead", "qualified", "proposal", "negotiation", "won", "lost"]).optional(),
      value: z.string(),
      probability: z.number().min(0).max(100).optional(),
      expectedClose: z.date().optional(),
      description: z.string().optional(),
      createdBy: z.number().optional(),
    }))
    .mutation(({ input }) => createDeal(input)),

  update: publicQuery
    .input(z.object({
      id: z.number(),
      name: z.string().optional(),
      type: z.enum(["p1_sprint", "p2_small", "p2_medium", "p2_enterprise"]).optional(),
      stage: z.enum(["lead", "qualified", "proposal", "negotiation", "won", "lost"]).optional(),
      value: z.string().optional(),
      probability: z.number().min(0).max(100).optional(),
      expectedClose: z.date().optional(),
      actualClose: z.date().optional(),
      description: z.string().optional(),
    }))
    .mutation(({ input }) => updateDeal(input.id, input)),

  delete: publicQuery
    .input(z.object({ id: z.number() }))
    .mutation(({ input }) => deleteDeal(input.id)),

  stats: publicQuery.query(() => getDealStats()),
});
