// V6 Middleware — admin gate for internal routes
// In demo mode, allows access. In production, requires DEALIX_ADMIN_TOKEN.

import { NextRequest, NextResponse } from "next/server";

const INTERNAL_PREFIXES = [
  "/crm",
  "/command-center",
  "/war-room",
  "/pipeline",
  "/review-queue",
  "/proof-vault",
  "/operator",
  "/launch",
  "/kpi-finance",
  "/data-room",
  "/client-portal",
  "/deals",
  "/outreach-lab",
];

export function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname;
  const isInternal = INTERNAL_PREFIXES.some((p) => path === p || path.startsWith(p + "/"));
  if (!isInternal) {
    return NextResponse.next();
  }

  const demoMode = process.env.NEXT_PUBLIC_DEMO_MODE !== "false";
  if (demoMode) {
    const res = NextResponse.next();
    res.headers.set("x-dealix-demo", "true");
    return res;
  }

  // Production: require token
  const expected = process.env.DEALIX_ADMIN_TOKEN || "";
  const got = request.headers.get("authorization")?.replace(/^Bearer\s+/i, "") || "";
  if (!expected || got !== expected) {
    return NextResponse.json(
      { error: "admin token required", demoMode: false },
      { status: 401 },
    );
  }
  return NextResponse.next();
}

export const config = {
  matcher: [
    "/crm/:path*",
    "/command-center/:path*",
    "/war-room/:path*",
    "/pipeline/:path*",
    "/review-queue/:path*",
    "/proof-vault/:path*",
    "/operator/:path*",
    "/launch/:path*",
    "/kpi-finance/:path*",
    "/data-room/:path*",
    "/client-portal/:path*",
    "/deals/:path*",
    "/outreach-lab/:path*",
  ],
};
