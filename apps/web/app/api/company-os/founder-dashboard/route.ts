import { NextResponse } from "next/server";
import { FOUNDER_DASHBOARD_DEMO } from "@/lib/generated/founder-dashboard";

export const dynamic = "force-dynamic";

export async function GET() {
  return NextResponse.json(
    { ...FOUNDER_DASHBOARD_DEMO, generatedAt: new Date().toISOString() },
    { status: 200, headers: { "cache-control": "no-store" } },
  );
}
