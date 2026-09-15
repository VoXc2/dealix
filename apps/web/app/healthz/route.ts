import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export function GET() {
  // Immutable release identity first. Self-host injects DEALIX_RELEASE_SHA;
  // Railway and Vercel expose platform-managed commit SHAs automatically.
  // Generic/public fallbacks are last because they may be stale or build-time only.
  const gitSha =
    process.env.DEALIX_RELEASE_SHA?.trim() ||
    process.env.RAILWAY_GIT_COMMIT_SHA?.trim() ||
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
