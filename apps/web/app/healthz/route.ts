import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export function GET() {
  const gitSha = process.env.GIT_SHA?.trim() || "unknown";

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
