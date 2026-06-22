import { authRouter } from "./auth-router";
import { prospectRouter } from "./prospect-router";
import { dealRouter } from "./deal-router";
import { activityRouter } from "./activity-router";
import { warRoomRouter } from "./warroom-router";
import { brainRouter } from "./brain-router";
import { commandRoomRouter } from "./command-room-router";
import { bookingRouter } from "./booking-router";
import { createRouter, publicQuery } from "./middleware";

export const appRouter = createRouter({
  ping: publicQuery.query(() => ({ ok: true, ts: Date.now() })),
  auth: authRouter,
  prospect: prospectRouter,
  deal: dealRouter,
  activity: activityRouter,
  warRoom: warRoomRouter,
  booking: bookingRouter,
  brain: brainRouter,
  commandRoom: commandRoomRouter,
});

export type AppRouter = typeof appRouter;
