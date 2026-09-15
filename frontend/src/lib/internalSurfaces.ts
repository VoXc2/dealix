/**
 * Canonical internal-surface classification — SOURCE ONLY fail-closed gate.
 *
 * Doctrine: `docs/auth/V11_ADMIN_ACCESS_BOUNDARY.md` classifies founder/internal
 * pages as internal/founder-only. `robots.txt`/noindex is crawl hygiene, NOT
 * access control — the server-side middleware gate in `src/middleware.ts` is
 * the enforcement point and the sole authority consulted by tests.
 *
 * Auth model honesty: no authenticated server-side web session exists today.
 * Frontend auth state lives in client `localStorage` JWTs (`useAuth`), which
 * the server cannot verify and therefore MUST NOT treat as authorization.
 * This module deliberately never reads `localStorage`, cookies, or tokens.
 * Production denies internal surfaces outright (404, no existence signal);
 * documented internal/dev mode (`DEALIX_INTERNAL_SURFACE_MODE=open`, the
 * default outside production) keeps them testable until a real server-side
 * session (httpOnly cookie + backend verify) is wired.
 *
 * Public site/diagnostic routes are preserved by default: anything NOT listed
 * here passes through. Keep this list to operational/founder surfaces only.
 */

/** Page prefixes treated as internal (locale-agnostic, see stripLocalePrefix). */
export const INTERNAL_PAGE_PREFIXES: readonly string[] = [
  "/crm",
  "/deals",
  "/approvals",
  "/founder",
  "/command-room",
  "/war-room",
  "/ops",
  "/operator",
  "/admin",
  "/dashboard",
  "/pipeline",
  "/analytics",
  "/clients",
  "/settings",
  "/market-control",
  "/proposal-queue",
  "/auto-distribution",
  "/delivery",
  "/brain",
  "/review-queue",
  "/outreach-lab",
  "/outreach-review",
  "/followups",
  "/kpi-finance",
  "/proof-vault",
  "/quotes",
  "/revenue",
  "/launch",
  "/client-portal",
];

/** Public exceptions inside internal prefixes (doctrine: demo stays public). */
export const INTERNAL_PAGE_PUBLIC_EXCEPTIONS: readonly string[] = [
  "/client-portal/demo",
];

/**
 * Next API route prefixes treated as internal. `/api/dealix-proxy` is the
 * operator-gated proxy (Bearer /api/v1/auth/me or ops secret at route level);
 * the middleware gate applies first so a closed surface never reaches it.
 */
export const INTERNAL_API_PREFIXES: readonly string[] = [
  "/api/crm",
  "/api/deals",
  "/api/founder",
  "/api/ops",
  "/api/internal",
  "/api/admin",
  "/api/command-room",
  "/api/approvals",
  "/api/dealix-proxy",
];

/** Documented public site/diagnostic routes — must NEVER be classified internal. */
export const DOCUMENTED_PUBLIC_ROUTES: readonly string[] = [
  "/",
  "/dealix-diagnostic",
  "/risk-score",
  "/proof-pack",
  "/learn",
  "/partners",
  "/pricing",
  "/login",
  "/register",
  "/about",
  "/services",
  "/book-call",
  "/demo",
  "/privacy",
  "/trust",
  "/sectors",
  "/solutions",
];

const SUPPORTED_LOCALES = new Set(["ar", "en"]);

/** Strip a leading `/ar` or `/en` locale segment; `/` is returned unchanged. */
export function stripLocalePrefix(pathname: string): string {
  const parts = pathname.split("/");
  // ["", "ar", "crm", ...]
  if (parts.length > 2 && SUPPORTED_LOCALES.has(parts[1])) {
    const rest = parts.slice(2).join("/");
    return rest ? `/${rest}` : "/";
  }
  return pathname || "/";
}

function matchesPrefix(path: string, prefixes: readonly string[]): boolean {
  return prefixes.some((p) => path === p || path.startsWith(`${p}/`));
}

function matchesException(path: string): boolean {
  return INTERNAL_PAGE_PUBLIC_EXCEPTIONS.some(
    (p) => path === p || path.startsWith(`${p}/`),
  );
}

/** True when the (locale-stripped) page path is an internal surface. */
export function isInternalPage(pathname: string): boolean {
  const path = stripLocalePrefix(pathname);
  if (matchesException(path)) return false;
  return matchesPrefix(path, INTERNAL_PAGE_PREFIXES);
}

/** True when the request path targets an internal Next API route. */
export function isInternalApi(pathname: string): boolean {
  return matchesPrefix(pathname, INTERNAL_API_PREFIXES);
}

function isProductionEnv(env: NodeJS.ProcessEnv = process.env): boolean {
  const values = [env.NODE_ENV, env.APP_ENV, env.VERCEL_ENV].map((v) =>
    (v || "").toLowerCase(),
  );
  return values.includes("production");
}

/**
 * True only when internal surfaces may be served. Explicit
 * `DEALIX_INTERNAL_SURFACE_MODE=open|closed` wins; otherwise closed in
 * production, open elsewhere (dev/test/documented internal mode).
 */
export function isInternalSurfaceOpen(env: NodeJS.ProcessEnv = process.env): boolean {
  const mode = (env.DEALIX_INTERNAL_SURFACE_MODE || "").toLowerCase();
  if (mode === "open") return true;
  if (mode === "closed") return false;
  return !isProductionEnv(env);
}

/**
 * Fail-closed decision for middleware/API routes: returns `"deny"` when the
 * path is internal and the surface gate is closed, `"allow"` otherwise.
 * Public routes always allow here (backend JWT/RBAC still applies per API).
 */
export function guardInternalSurface(
  pathname: string,
  env: NodeJS.ProcessEnv = process.env,
): "allow" | "deny" {
  if (!isInternalPage(pathname) && !isInternalApi(pathname)) return "allow";
  return isInternalSurfaceOpen(env) ? "allow" : "deny";
}
