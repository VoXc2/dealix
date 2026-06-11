import { NextResponse } from "next/server";
import { ultimatePackJson } from "@/lib/sales-machine/ultimate-sales-os";

export const dynamic = "force-dynamic";

function todayIso() {
  return new Date().toISOString().slice(0, 10);
}

export async function GET(request: Request) {
  const url = new URL(request.url);
  const date = url.searchParams.get("date") || todayIso();
  const format = (url.searchParams.get("format") || "json").toLowerCase();
  const data = ultimatePackJson(date);

  if (format === "md") {
    const lines: string[] = [];
    lines.push(`# Dealix Ultimate Sales OS Pack — ${date}`);
    lines.push("");
    lines.push("## Top offers");
    for (const o of data.offers) lines.push(`- **${o.name}** — ${o.setup} setup · ${o.monthly} monthly`);
    lines.push("");
    lines.push("## Industry plays");
    for (const p of data.industries) lines.push(`- **${p.industry}** → ${p.bestOffer} — ${p.first7DayWin}`);
    lines.push("");
    lines.push("## Pillars");
    for (const p of data.pillars) lines.push(`- **${p.title}** (${p.titleAr}) — ${p.solution}`);
    lines.push("");
    lines.push("---");
    lines.push("Safety: no auto-send, human review required, no fake ROI, no fake testimonials.");
    return new NextResponse(lines.join("\n"), {
      status: 200,
      headers: { "content-type": "text/markdown; charset=utf-8" },
    });
  }

  return NextResponse.json(data, {
    status: 200,
    headers: { "cache-control": "no-store" },
  });
}
