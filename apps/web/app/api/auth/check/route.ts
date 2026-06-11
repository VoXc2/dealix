import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  const demoMode = process.env.NEXT_PUBLIC_DEMO_MODE !== "false";
  let body: { token?: string } = {};
  try {
    body = (await request.json()) as { token?: string };
  } catch {
    // form-encoded fallback
    try {
      const text = await request.text();
      const params = new URLSearchParams(text);
      body = { token: params.get("token") || undefined };
    } catch {
      // ignore
    }
  }

  const expected = process.env.DEALIX_ADMIN_TOKEN || "";
  if (demoMode) {
    return NextResponse.json({ ok: true, mode: "demo" });
  }
  if (!expected) {
    return NextResponse.json({ ok: false, error: "admin token not configured" }, { status: 500 });
  }
  if (body.token !== expected) {
    return NextResponse.json({ ok: false, error: "invalid token" }, { status: 401 });
  }
  return NextResponse.json({ ok: true, mode: "production" });
}

export async function GET() {
  return NextResponse.json({
    ok: true,
    mode: process.env.NEXT_PUBLIC_DEMO_MODE === "false" ? "production" : "demo",
  });
}
