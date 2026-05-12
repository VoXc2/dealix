"use client";

import { QueryClient } from "@tanstack/react-query";
import { isAxiosError } from "axios";

// One shared client per browser session. Wrap the app in a QueryClientProvider
// at app/layout.tsx and import this singleton.
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (failureCount, error) => {
        // Don't retry on 4xx (auth, validation, not-found).
        if (isAxiosError(error)) {
          const status = error.response?.status ?? 0;
          if (status >= 400 && status < 500) return false;
        }
        return failureCount < 2;
      },
      staleTime: 30_000,
      refetchOnWindowFocus: false,
    },
  },
});
