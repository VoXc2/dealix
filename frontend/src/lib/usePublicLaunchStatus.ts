"use client";
import { useEffect, useState } from "react";

export function isMoyasarLive(mode?: string) {
  return (mode || "").toLowerCase() === "live";
}

export function usePublicLaunchStatus() {
  const [status, setStatus] = useState<{ healthcheck_ok?: boolean; moyasar_mode?: string } | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${base}/api/v1/founder/launch-status/public`)
      .then((r) => (r.ok ? r.json() : null))
      .then(setStatus)
      .catch(() => setStatus(null))
      .finally(() => setLoading(false));
  }, []);
  const mode = process.env.NEXT_PUBLIC_DEALIX_MOYASAR_MODE || status?.moyasar_mode;
  return { status, loading, moyasarLive: isMoyasarLive(mode) };
}
