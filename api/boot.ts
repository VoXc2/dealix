import { Hono } from "hono";
import { bodyLimit } from "hono/body-limit";
import type { HttpBindings } from "@hono/node-server";
import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { appRouter } from "./router";
import { createContext } from "./context";
import { env } from "./lib/env";
import { createOAuthCallbackHandler } from "./kimi/auth";
import { Paths } from "@contracts/constants";
import { getDb } from "./queries/connection";
import { eq } from "drizzle-orm";
import {
  whatsappConversations,
  whatsappMessages,
} from "@db/schema";
import health from "./health";

const app = new Hono<{ Bindings: HttpBindings }>();

// Health check endpoints
app.route('/', health);

app.use(bodyLimit({ maxSize: 50 * 1024 * 1024 }));
app.get(Paths.oauthCallback, createOAuthCallbackHandler());

app.get("/api/whatsapp/webhook", async (c) => {
  const mode = c.req.query("hub.mode");
  const token = c.req.query("hub.verify_token");
  const challenge = c.req.query("hub.challenge");
  const verifyToken = process.env.WHATSAPP_WEBHOOK_VERIFY_TOKEN || "";

  if (mode === "subscribe" && token && token === verifyToken && challenge) {
    return c.text(challenge, 200);
  }

  return c.text("Forbidden", 403);
});

app.post("/api/whatsapp/webhook", async (c) => {
  const payload = await c.req.json();
  const db = getDb();
  const value = payload?.entry?.[0]?.changes?.[0]?.value;
  const messages = value?.messages;
  const statuses = value?.statuses;

  if (Array.isArray(messages)) {
    for (const message of messages) {
      const waId = String(message?.from || "");
      const body =
        String(message?.text?.body || message?.button?.text || "") || "";

      const existingConversation = await db
        .select()
        .from(whatsappConversations)
        .where(eq(whatsappConversations.waId, waId));

      let conversationId = existingConversation[0]?.id;

      if (!conversationId) {
        const created = await db.insert(whatsappConversations).values({
          waId,
          name: waId,
          lastMessageAt: new Date(),
          lastMessageDirection: "inbound",
          lastMessageBody: body,
          status: "open",
        });
        conversationId = Number(created[0].insertId);
      } else {
        await db
          .update(whatsappConversations)
          .set({
            lastMessageAt: new Date(),
            lastMessageDirection: "inbound",
            lastMessageBody: body,
          })
          .where(eq(whatsappConversations.id, conversationId));
      }

      await db.insert(whatsappMessages).values({
        conversationId,
        waMessageId: String(message?.id || ""),
        direction: "inbound",
        type: "text",
        body,
        status: "delivered",
        sentAt: new Date(),
      });
    }
  }

  if (Array.isArray(statuses)) {
    for (const statusEntry of statuses) {
      const waMessageId = String(statusEntry?.id || "");
      const status = String(statusEntry?.status || "");
      if (!waMessageId) {
        continue;
      }

      if (
        status === "sent" ||
        status === "delivered" ||
        status === "read" ||
        status === "failed"
      ) {
        await db
          .update(whatsappMessages)
          .set({
            status,
            ...(status === "delivered" ? { deliveredAt: new Date() } : {}),
            ...(status === "read" ? { readAt: new Date() } : {}),
            ...(status === "failed"
              ? {
                  errorCode: "WEBHOOK_FAILURE",
                  errorMessage: "Failed delivery reported by webhook",
                }
              : {}),
          })
          .where(eq(whatsappMessages.waMessageId, waMessageId));
      }
    }
  }

  return c.json({ ok: true });
});

app.use("/api/trpc/*", async (c) => {
  return fetchRequestHandler({
    endpoint: "/api/trpc",
    req: c.req.raw,
    router: appRouter,
    createContext,
  });
});
app.all("/api/*", (c) => c.json({ error: "Not Found" }, 404));

export default app;

if (env.isProduction) {
  const { serve } = await import("@hono/node-server");
  const { serveStaticFiles } = await import("./lib/vite");
  serveStaticFiles(app);

  const port = parseInt(process.env.PORT || "3000");
  serve({ fetch: app.fetch, port }, () => {
    console.log(`Server running on http://localhost:${port}/`);
  });
}
