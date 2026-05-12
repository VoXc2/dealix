/**
 * T6 example — discover Skills, pick a Vertical, register a custom Agent.
 *
 * Mirrors docs/api/examples/python/t6_skills_and_verticals.py.
 * Runs against a live deployment when DEALIX_API_BASE + DEALIX_API_KEY
 * are set. TypeScript ≥ 4.7, Node ≥ 20.
 */

const BASE = (process.env.DEALIX_API_BASE || "https://api.dealix.me").replace(/\/$/, "");
const API_KEY = process.env.DEALIX_API_KEY || "";

const HEADERS = {
  "X-API-Key": API_KEY,
  "Content-Type": "application/json",
  accept: "application/json",
};

async function api<T = unknown>(method: string, path: string, body?: unknown): Promise<T> {
  const r = await fetch(`${BASE}${path}`, {
    method,
    headers: HEADERS,
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!r.ok) throw new Error(`HTTP ${r.status}: ${await r.text()}`);
  return (await r.json()) as T;
}

interface Skill {
  id: string;
  description: string;
}
interface Vertical {
  id: string;
  pricing_default_plan: string;
}

async function main() {
  const skills = await api<{ skills: Skill[] }>("GET", "/api/v1/skills");
  console.log(`Catalogue: ${skills.skills.length} skills`);
  for (const s of skills.skills) console.log(`  - ${s.id}: ${s.description}`);

  const verts = await api<{ verticals: Vertical[] }>("GET", "/api/v1/verticals");
  console.log(`\n${verts.verticals.length} verticals`);
  for (const v of verts.verticals) console.log(`  - ${v.id} (plan ${v.pricing_default_plan})`);

  console.log("\nApplying 'real-estate' bundle…");
  console.log(await api("POST", "/api/v1/verticals/apply", { vertical_id: "real-estate" }));

  const manifest = {
    id: "real-estate-qualifier",
    name: "Real-estate Saudi qualifier",
    model: "claude-haiku-4-5",
    tools: ["sales_qualifier", "compliance_reviewer"],
    prompt_override:
      "You are an Arabic-Khaliji real-estate sales qualifier. " +
      "Score the lead 0..1 using BANT and the PDPL contactability gate.",
    max_usd_per_request: 0.5,
    locale: "ar",
  };
  console.log("\nRegistering custom agent…");
  console.log(await api("POST", "/api/v1/agents", manifest));

  console.log("\nInstalling lead_to_booking workflow template…");
  console.log(await api("POST", "/api/v1/workflows/install", { template_id: "lead_to_booking" }));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
