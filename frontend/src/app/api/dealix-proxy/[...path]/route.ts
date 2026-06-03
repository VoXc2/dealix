/**
 * Server-side proxy for founder ops APIs — keeps DEALIX_ADMIN_API_KEY off the browser.
 * Requires authenticated operator (Bearer /api/v1/auth/me) or DEALIX_OPS_PROXY_SECRET.
 */
import { NextRequest, NextResponse } from "next/server";

const API_BASE = (process.env.DEALIX_API_URL || process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000").replace(
  /\/$/,
  "",
);
const ADMIN_KEY = process.env.DEALIX_ADMIN_API_KEY || "";
const OPS_PROXY_SECRET = process.env.DEALIX_OPS_PROXY_SECRET || "";

const ALLOWED_PREFIXES = [
  "/api/v1/ops-autopilot",
  "/api/v1/evidence",
  "/api/v1/sales",
  "/api/v1/support",
  "/api/v1/knowledge",
  "/api/v1/invoices",
  "/api/v1/diagnostics",
];

function canonicalPath(segments: string[]): string | null {
  const parts: string[] = [];
  for (const seg of segments) {
    if (!seg || seg === "." || seg === ".." || seg.includes("\0")) {
      return null;
    }
    parts.push(seg);
  }
  return `/${parts.join("/")}`;
}

function isAllowed(path: string): boolean {
  return ALLOWED_PREFIXES.some((p) => path === p || path.startsWith(`${p}/`));
}

async function assertOperatorAccess(req: NextRequest): Promise<NextResponse | null> {
  const auth = req.headers.get("authorization");
  if (auth?.startsWith("Bearer ")) {
    try {
      const check = await fetch(`${API_BASE}/api/v1/auth/me`, {
        headers: { Authorization: auth },
        cache: "no-store",
      });
      if (check.ok) {
        return null;
      }
    } catch {
      /* fall through */
    }
  }

  if (OPS_PROXY_SECRET) {
    const provided = req.headers.get("x-dealix-ops-proxy-secret") || "";
    if (provided && provided === OPS_PROXY_SECRET) {
      return null;
    }
  }

  return NextResponse.json(
    { detail: "unauthorized — sign in or provide valid ops proxy credentials" },
    { status: 401 },
  );
}

async function proxy(req: NextRequest, pathSegments: string[]) {
  if (!ADMIN_KEY) {
    return NextResponse.json(
      { detail: "DEALIX_ADMIN_API_KEY not configured on server" },
      { status: 503 },
    );
  }

  const denied = await assertOperatorAccess(req);
  if (denied) {
    return denied;
  }

  const path = canonicalPath(pathSegments);
  if (!path) {
    return NextResponse.json({ detail: "invalid_path" }, { status: 400 });
  }
  if (!isAllowed(path)) {
    return NextResponse.json({ detail: "path_not_allowed" }, { status: 403 });
  }

  const url = new URL(`${API_BASE}${path}`);
  req.nextUrl.searchParams.forEach((v, k) => url.searchParams.set(k, v));

  const headers: Record<string, string> = {
    "X-Admin-API-Key": ADMIN_KEY,
    "Content-Type": req.headers.get("content-type") || "application/json",
  };

  const init: RequestInit = {
    method: req.method,
    headers,
  };
  if (req.method !== "GET" && req.method !== "HEAD") {
    init.body = await req.text();
  }

  const upstream = await fetch(url.toString(), init);
  const text = await upstream.text();
  return new NextResponse(text, {
    status: upstream.status,
    headers: {
      "Content-Type": upstream.headers.get("content-type") || "application/json",
    },
  });
}

export async function GET(
  req: NextRequest,
  ctx: { params: Promise<{ path: string[] }> },
) {
  const { path } = await ctx.params;
  return proxy(req, path);
}

export async function POST(
  req: NextRequest,
  ctx: { params: Promise<{ path: string[] }> },
) {
  const { path } = await ctx.params;
  return proxy(req, path);
}

export async function PATCH(
  req: NextRequest,
  ctx: { params: Promise<{ path: string[] }> },
) {
  const { path } = await ctx.params;
  return proxy(req, path);
}

export async function PUT(
  req: NextRequest,
  ctx: { params: Promise<{ path: string[] }> },
) {
  const { path } = await ctx.params;
  return proxy(req, path);
}

export async function DELETE(
  req: NextRequest,
  ctx: { params: Promise<{ path: string[] }> },
) {
  const { path } = await ctx.params;
  return proxy(req, path);
}
