import { z } from "zod";
import { createRouter, publicQuery } from "./middleware";
import {
  findActivities,
  createActivity,
  updateActivity,
  deleteActivity,
  getActivityStats,
} from "./queries/activityQueries";

export const activityRouter = createRouter({
  list: publicQuery
    .input(z.object({ prospectId: z.number().optional(), type: z.string().optional() }).optional())
    .query(({ input }) => findActivities(input)),

  create: publicQuery
    .input(z.object({
      prospectId: z.number().optional(),
      type: z.enum(["email", "call", "meeting", "followup", "note", "proposal", "payment", "delivery"]),
      direction: z.enum(["inbound", "outbound"]).optional(),
      subject: z.string().optional(),
      body: z.string().optional(),
      status: z.enum(["pending", "completed", "cancelled", "overdue"]).optional(),
      scheduledAt: z.date().optional(),
      aiGenerated: z.boolean().optional(),
      approved: z.boolean().optional(),
      createdBy: z.number().optional(),
    }))
    .mutation(({ input }) => createActivity(input)),

  update: publicQuery
    .input(z.object({
      id: z.number(),
      subject: z.string().optional(),
      body: z.string().optional(),
      status: z.enum(["pending", "completed", "cancelled", "overdue"]).optional(),
      completedAt: z.date().optional(),
      approved: z.boolean().optional(),
    }))
    .mutation(({ input }) => updateActivity(input.id, input)),

  delete: publicQuery
    .input(z.object({ id: z.number() }))
    .mutation(({ input }) => deleteActivity(input.id)),

  stats: publicQuery.query(() => getActivityStats()),
});
