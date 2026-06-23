import { describe, it, expect, beforeAll, afterAll } from "vitest";
import type { Server } from "node:http";
import app from "../boot";
import { env } from "../lib/env";

// Prevent production boot from starting the real HTTP server during tests
env.isProduction = false;

let server: Server;
let baseUrl: string = "";

describe("health endpoints", () => {
  beforeAll(async () => {
    // @ts-expect-error app.fetch is Hono's fetch handler
    server = (await import("@hono/node-server")).serve({ fetch: app.fetch, port: 0 });
    const address = server.address();
    if (address && typeof address === "object") {
      baseUrl = `http://localhost:${address.port}`;
    }
  });

  afterAll(() => {
    server?.close();
  });

  it("GET /health returns healthy", async () => {
    const response = await fetch(`${baseUrl}/health`);
    expect(response.status).toBe(200);
    const body = (await response.json()) as { status: string; version: string; environment: string };
    expect(body.status).toBe("healthy");
    expect(body.version).toBeDefined();
    expect(body.environment).toBeDefined();
  });

  it("GET /ready returns structured response", async () => {
    const response = await fetch(`${baseUrl}/ready`);
    const body = (await response.json()) as {
      status: string;
      checks: { application: string; database: string };
      timestamp: string;
    };
    expect(body.status).toMatch(/^(ready|not_ready)$/);
    expect(body.checks).toBeDefined();
    expect(body.checks.application).toBe("running");
    expect(body.timestamp).toBeDefined();
  });
});
