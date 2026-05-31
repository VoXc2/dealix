import { authRouter } from "./auth-router";
import { prospectRouter } from "./prospect-router";
import { proposalRouter } from "./proposal-router";
import { followupRouter } from "./followup-router";
import { governanceRouter } from "./governance-router";
import { warRoomRouter } from "./warroom-router";
import { financeRouter } from "./finance-router";
import { createRouter, publicQuery } from "./middleware";

export const appRouter = createRouter({
  ping: publicQuery.query(() => ({ ok: true, ts: Date.now() })),
  auth: authRouter,
  prospects: prospectRouter,
  proposals: proposalRouter,
  followups: followupRouter,
  governance: governanceRouter,
  warRoom: warRoomRouter,
  finance: financeRouter,
});

export type AppRouter = typeof appRouter;
