"use client";

/**
 * React hook bridging the SSE endpoint at /api/v1/realtime/stream
 * to TanStack Query. On every `update` event with a matching `key`,
 * the corresponding query is invalidated.
 *
 * Usage:
 *   useRealtime([
 *     { event: "lead.created", invalidate: ["leads"] },
 *     { event: "deal.updated", invalidate: ["deals"] },
 *   ]);
 */

import { useEffect } from "react";
import { useQueryClient } from "@tanstack/react-query";

const API_BASE =
  (typeof window !== "undefined" && (window as any).__DEALIX_API_BASE__) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "";

export interface RealtimeBinding {
  event: string;
  invalidate: readonly (string | number)[];
}

export function useRealtime(bindings: RealtimeBinding[]): void {
  const qc = useQueryClient();

  useEffect(() => {
    if (typeof window === "undefined") return;
    const access = localStorage.getItem("dealix_access_token");
    if (!access) return;
    // EventSource doesn't allow custom headers; pass the token as a
    // query param. Backend reads it for tenant resolution alongside
    // the Authorization header path.
    const url = new URL(`${API_BASE}/api/v1/realtime/stream`, window.location.origin);
    url.searchParams.set("access_token", access);
    const es = new EventSource(url.toString());

    const handlers: Array<[string, EventListener]> = [];
    bindings.forEach((b) => {
      const fn = (evt: MessageEvent) => {
        try {
          const data = JSON.parse(evt.data || "{}");
          if (b.event === "*" || data?.kind === b.event) {
            qc.invalidateQueries({ queryKey: b.invalidate as unknown[] });
          }
        } catch {
          /* ignore parse errors on heartbeats */
        }
      };
      es.addEventListener("update", fn as EventListener);
      handlers.push(["update", fn as EventListener]);
    });

    return () => {
      handlers.forEach(([name, fn]) => es.removeEventListener(name, fn));
      es.close();
    };
  }, [bindings, qc]);
}
