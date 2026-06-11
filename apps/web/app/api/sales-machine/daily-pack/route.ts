import { NextResponse } from "next/server";
import { dailyPackMarkdown } from "@/lib/sales-automation/lead-sources";

export const dynamic = "force-dynamic";

function todayIso() {
  return new Date().toISOString().slice(0, 10);
}

export async function GET(request: Request) {
  const url = new URL(request.url);
  const date = url.searchParams.get("date") || todayIso();
  const format = (url.searchParams.get("format") || "md").toLowerCase();
  const body = dailyPackMarkdown(date);
  if (format === "json") {
    return NextResponse.json({
      date,
      generatedAt: new Date().toISOString(),
      body,
      safety: { autoSend: false, humanReview: true },
    });
  }
  return new NextResponse(body, {
    status: 200,
    headers: {
      "content-type": format === "txt" ? "text/plain; charset=utf-8" : "text/markdown; charset=utf-8",
      "content-disposition": `attachment; filename="dealix-sales-machine-daily-pack-${date}.${format === "txt" ? "txt" : "md"}"`,
    },
  });
}
