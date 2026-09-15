import { NextResponse, type NextRequest } from "next/server";

// Production authority: apps/web is the image built by deploy/selfhost/compose.yml.
// Until a server-verifiable founder session exists, operational/founder surfaces
// fail closed in production. Client localStorage/admin-key state is never auth.
const INTERNAL_PAGE_PREFIXES = [
  "/crm", "/operator", "/review-queue", "/outreach-lab", "/followups",
  "/command-center", "/war-room", "/pipeline", "/kpi-finance", "/deals",
  "/proof-vault", "/launch", "/approvals", "/founder", "/control-plane",
  "/dashboard", "/data-room", "/delivery-workspace", "/client-success", "/retention",
  "/growth-command-center",
  "/lead-engine", "/hubspot-os", "/automated-sales", "/persuasion-room", "/product-network", "/quotes", "/revenue",
  "/revenue-machine", "/sales-agent", "/sales-agent-lab", "/sales-assets",
  "/sales-machine", "/settings", "/client-portal",
  "/daily-draft", "/sandbox", "/app", "/cmd-v2", "/dx3", "/iv4",
  "/rcmax", "/s9", "/t10", "/x5", "/z8", "/a14",
] as const;

const PUBLIC_EXCEPTIONS = ["/client-portal/demo"] as const;
const INTERNAL_API_PREFIXES = [
  "/api/crm", "/api/command-center", "/api/company-os", "/api/hubspot-os",
  "/api/sales-machine", "/api/sales-agent", "/api/analytics",
] as const;const TENANT_OPERATIONAL_SEGMENTS = new Set([
  "dashboard", "hr", "inventory", "projects", "settings",
]);

function stripLocale(pathname: string): string {
  const parts = pathname.split("/");
  if (parts.length > 2 && (parts[1] === "ar" || parts[1] === "en")) {
    const rest = parts.slice(2).join("/");
    return rest ? `/${rest}` : "/";
  }
  return pathname || "/";
}

function matchesPrefix(path: string, prefixes: readonly string[]): boolean {
  return prefixes.some((prefix) => path === prefix || path.startsWith(`${prefix}/`));
}

function isTenantOperationalPath(path: string): boolean {
  const parts = path.split("/").filter(Boolean);
  return parts.length >= 2 && TENANT_OPERATIONAL_SEGMENTS.has(parts[1]);
}

function isInternalPath(pathname: string): boolean {
  const path = stripLocale(pathname);
  if (matchesPrefix(path, PUBLIC_EXCEPTIONS)) return false;
  return matchesPrefix(path, INTERNAL_PAGE_PREFIXES) ||
    matchesPrefix(pathname, INTERNAL_API_PREFIXES) || isTenantOperationalPath(path);
}function internalSurfaceOpen(): boolean {
  const mode = (process.env.DEALIX_INTERNAL_SURFACE_MODE || "").toLowerCase();
  if (mode === "open") return true;
  if (mode === "closed") return false;
  const environments = [
    process.env.NODE_ENV,
    process.env.APP_ENV,
    process.env.RAILWAY_ENVIRONMENT_NAME,
  ].map((value) => (value || "").toLowerCase());
  return !environments.includes("production");
}

export function middleware(request: NextRequest) {
  if (!isInternalPath(request.nextUrl.pathname) || internalSurfaceOpen()) {
    return NextResponse.next();
  }
  return new NextResponse("Not Found", {
    status: 404,
    headers: {
      "Cache-Control": "no-store, max-age=0",
      "X-Robots-Tag": "noindex, nofollow, noarchive",
    },
  });
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};