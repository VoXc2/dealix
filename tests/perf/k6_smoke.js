// k6 smoke + budget test for Dealix.
// Run: `k6 run tests/perf/k6_smoke.js`
//
// Budgets (failing thresholds match docs/sla.md):
//   p95 < 500 ms on /api/v1/public/health
//   error rate < 1% over the test window
//
// Override base URL: K6_BASE_URL=https://api.dealix.me k6 run ...

import http from "k6/http";
import { check, sleep } from "k6";

const BASE = __ENV.K6_BASE_URL || "http://localhost:8000";

export const options = {
  scenarios: {
    smoke: {
      executor: "constant-vus",
      vus: 5,
      duration: "60s",
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(95)<500"],
    // Critical-path budget for the status endpoint that BetterStack pings.
    "http_req_duration{endpoint:status}": ["p(95)<300"],
  },
};

export default function () {
  const health = http.get(`${BASE}/api/v1/public/health`);
  check(health, { "public health 200": (r) => r.status === 200 });

  const status = http.get(`${BASE}/api/v1/status`, {
    tags: { endpoint: "status" },
  });
  check(status, { "status 200 or 503": (r) => r.status === 200 || r.status === 503 });

  sleep(1);
}
