import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export function GET() {
  // Immutable release identity is injected by the self-hosted release plane.
  const gitSha =
    process.env.DEALIX_RELEASE_SHA?.trim() ||
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
