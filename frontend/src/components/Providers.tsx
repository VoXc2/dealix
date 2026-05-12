"use client";

import { QueryClientProvider } from "@tanstack/react-query";
import { ReactNode } from "react";

import { queryClient } from "@/lib/query-client";

/**
 * Single React-context boundary for app-wide providers. Drop into
 * `[locale]/layout.tsx` (or the authed shell only — pick one) and
 * everything below gets TanStack Query, future Knock/PostHog/Sentry
 * providers, etc.
 */
export function Providers({ children }: { children: ReactNode }) {
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
}
