import { NextResponse } from "next/server";
import { ceoBriefJson, ceoBriefMarkdown } from "@/lib/company-os/company-os";

export const dynamic = "force-dynamic";

function todayIso() {
  return new Date().toISOString().slice(0, 10);
}

export async function GET(request: Request) {
  const url = new URL(request.url);
  const format = (url.searchParams.get("format") || "json").toLowerCase();
  const mode = (url.searchParams.get("mode") || "demo").toLowerCase() === "production" ? "production" : "demo";
  const date = url.searchParams.get("date") || todayIso();

  if (format === "md" || format === "markdown" || format === "txt") {
    const body = ceoBriefMarkdown(date, mode);
    return new NextResponse(body, {
      status: 200,
      headers: {
        "content-type": format === "txt" ? "text/plain; charset=utf-8" : "text/markdown; charset=utf-8",
        "content-disposition": `attachment; filename="dealix-daily-ceo-brief-${date}.${format === "txt" ? "txt" : "md"}"`,
      },
    });
  }

  const payload = ceoBriefJson(date, mode);
  return NextResponse.json(
    { ...payload, generatedAt: new Date().toISOString() },
    {
      status: 200,
      headers: { "cache-control": "no-store" },
    },
  );
}
