// Workflow 4: Subscribe to the realtime SSE stream from a Node server.

import { EventSource } from "undici";

const BASE = process.env.DEALIX_API_BASE?.replace(/\/$/, "") ?? "https://api.dealix.me";
const TOKEN = process.env.DEALIX_BEARER_TOKEN ?? "";

const url = new URL(`${BASE}/api/v1/realtime/stream`);
if (TOKEN) url.searchParams.set("access_token", TOKEN);

const es = new EventSource(url.toString());

es.addEventListener("hello", (e: any) => console.log("hello:", e.data));
es.addEventListener("heartbeat", (e: any) => console.log("hb:", e.data));
es.addEventListener("update", (e: any) => console.log("update:", e.data));

process.on("SIGINT", () => {
  es.close();
  process.exit(0);
});
