import createMiddleware from "next-intl/middleware";
import { routing } from "./i18n/routing";

export default createMiddleware(routing);

export const config = {
  matcher: [
    // Operational endpoints must never be locale-redirected (uptime monitors
    // treat non-200 as down): api, healthz. Dotted static assets excluded below.
    "/((?!api|healthz|_next|_vercel|.*\\..*).*)",
    "/",
  ],
};
