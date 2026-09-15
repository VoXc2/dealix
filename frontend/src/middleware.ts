import { NextResponse, type NextRequest } from "next/server";
import createMiddleware from "next-intl/middleware";
import { routing } from "./i18n/routing";
import { guardInternalSurface } from "./lib/internalSurfaces";

const intlMiddleware = createMiddleware(routing);

export default function middleware(req: NextRequest) {
  // Fail-closed server-side gate for founder/internal surfaces. This is the
  // enforcement point: client-side `localStorage` JWT state is NOT consulted
  // here (it is not server-verifiable authorization). Closed surface -> 404
  // without confirming the path exists; public routes pass through to intl.
  if (guardInternalSurface(req.nextUrl.pathname) === "deny") {
    return new NextResponse("Not Found", { status: 404 });
  }
  return intlMiddleware(req);
}

export const config = {
  matcher: [
    // Internal Next API routes must pass through this gate (fail-closed);
    // route-level operator checks (e.g. dealix-proxy Bearer/secret) apply after.
    "/api/:path*",
    // Operational endpoints must never be locale-redirected (uptime monitors
    // treat non-200 as down): api, healthz. Dotted static assets excluded below.
    "/((?!api|healthz|_next|_vercel|.*\\..*).*)",
    "/",
  ],
};
