// Workflow 1: Lead → Booking — TypeScript example.
//
// Run via `tsx docs/api/examples/typescript/lead_to_booking.ts` or
// import from a Next.js server action.

const BASE = process.env.DEALIX_API_BASE?.replace(/\/$/, "") ?? "https://api.dealix.me";
const API_KEY = process.env.DEALIX_API_KEY ?? "";

const headers: Record<string, string> = {
  "Content-Type": "application/json",
  ...(API_KEY ? { "X-API-Key": API_KEY } : {}),
};

async function captureLead(lead: Record<string, unknown>): Promise<string> {
  const r = await fetch(`${BASE}/api/v1/leads`, {
    method: "POST",
    headers,
    body: JSON.stringify(lead),
  });
  if (!r.ok) throw new Error(`capture failed: ${r.status}`);
  const body = (await r.json()) as { id: string };
  return body.id;
}

async function fetchBookingUrl(): Promise<string | null> {
  const r = await fetch(`${BASE}/api/v1/public/demo-request`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      company: "Example Co.",
      name: "Ops",
      email: "ops@example.sa",
      phone: "+966500000000",
      sector: "real-estate",
      consent: true,
    }),
  });
  if (!r.ok) return null;
  const body = (await r.json()) as { calendly_url?: string };
  return body.calendly_url ?? null;
}

async function main() {
  const id = await captureLead({
    company_name: "Example Co.",
    contact_email: "ops@example.sa",
    contact_phone: "+966500000000",
    sector: "real-estate",
  });
  console.log("captured:", id);
  console.log("book:", await fetchBookingUrl());
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
