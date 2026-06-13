import { authRouter } from "./auth-router";
import { prospectRouter } from "./prospect-router";
import { dealRouter } from "./deal-router";
import { activityRouter } from "./activity-router";
import { warRoomRouter } from "./warroom-router";
import { createRouter, publicQuery } from "./middleware";

export const appRouter = createRouter({
  ping: publicQuery.query(() => ({ ok: true, ts: Date.now() })),
  auth: authRouter,
  prospect: prospectRouter,
  deal: dealRouter,
  activity: activityRouter,
  warRoom: warRoomRouter,
});

export type AppRouter = typeof appRouter;
