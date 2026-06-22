"use client";

import { useEffect, useRef, useCallback, useState } from "react";
import { tokenStorage } from "@/lib/api/client";

interface SSEOptions<T> {
  url: string;
  onMessage: (data: T) => void;
  onError?: (error: Event) => void;
  enabled?: boolean;
}

interface SSEState {
  isConnected: boolean;
  lastEventId: string | null;
  error: string | null;
}

export function useSSE<T = unknown>({
  url,
  onMessage,
  onError,
  enabled = true,
}: SSEOptions<T>): SSEState & { reconnect: () => void } {
  const eventSourceRef = useRef<EventSource | null>(null);
  const [state, setState] = useState<SSEState>({
    isConnected: false,
    lastEventId: null,
    error: null,
  });

  const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

  const connect = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    const token = tokenStorage.getAccessToken();
    const fullUrl = `${API_BASE}${url}${token ? `?token=${token}` : ""}`;

    const es = new EventSource(fullUrl, { withCredentials: false });

    es.onopen = () => {
      setState((s) => ({ ...s, isConnected: true, error: null }));
    };

    es.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data) as T;
        setState((s) => ({ ...s, lastEventId: event.lastEventId }));
        onMessage(data);
      } catch {
        // non-JSON message, ignore
      }
    };

    es.onerror = (event) => {
      setState((s) => ({ ...s, isConnected: false, error: "Connection error" }));
      onError?.(event);
      // Auto-reconnect after 5s
      setTimeout(connect, 5000);
    };

    eventSourceRef.current = es;
  }, [url, onMessage, onError, API_BASE]);

  useEffect(() => {
    if (!enabled) return;
    connect();
    return () => {
      eventSourceRef.current?.close();
    };
  }, [connect, enabled]);

  return {
    ...state,
    reconnect: connect,
  };
}
