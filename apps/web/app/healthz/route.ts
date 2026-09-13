import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export function GET() {
  // Immutable platform-managed SHA first: Vercel sets VERCEL_GIT_COMMIT_SHA
  // automatically. A generic GIT_SHA may be stale, so it never overrides it.
  const gitSha =
    process.env.VERCEL_GIT_COMMIT_SHA?.trim() ||
    process.env.NEXT_PUBLIC_GIT_SHA?.trim() ||
    process.env.GIT_SHA?.trim() ||
    "unknown";

  return NextResponse.json(
    {
      status: "ok",
      service: "dealix-web",
      git_sha: gitSha,
    },
    {
      status: 200,
      headers: { "cache-control": "no-store" },
    },
  );
}
