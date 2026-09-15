// Client-side convenience redirect only — NOT access control. The fail-closed
// server-side gate in `src/middleware.ts` (backed by
// `src/lib/internalSurfaces.ts`) is the enforcement point; client
// `localStorage` JWT state is not server-verifiable authorization.
"use client";

import { useEffect } from "react";
import { useLocale } from "next-intl";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/hooks/useAuth";

export default function OpsLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();
  const locale = useLocale();

  useEffect(() => {
    if (isLoading) return;
    if (!isAuthenticated && process.env.NODE_ENV === "production") {
      router.replace(`/${locale}/login?next=/${locale}/ops/founder`);
    }
  }, [isAuthenticated, isLoading, locale, router]);

  if (isLoading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center text-sm text-muted-foreground">
        Loading…
      </div>
    );
  }

  return <>{children}</>;
}
