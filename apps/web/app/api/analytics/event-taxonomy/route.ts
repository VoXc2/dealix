import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function GET() {
  return NextResponse.json(
    {
      events: [
        { name: "page_view", props: ["path", "locale"] },
        { name: "cta_click", props: ["cta_id", "source_page"] },
        { name: "sales_pack_download", props: ["format"] },
        { name: "ceo_brief_download", props: ["format"] },
        { name: "proposal_generated", props: ["account_id", "offer"] },
        { name: "lead_imported", props: ["count"] },
        { name: "draft_reviewed", props: ["reviewer", "decision"] },
        { name: "proof_report_generated", props: ["account_id"] },
      ],
      noPii: true,
      consentRequired: false,
    },
    { status: 200 },
  );
}
