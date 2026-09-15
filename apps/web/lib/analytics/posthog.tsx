"use client";

import posthog from "posthog-js";
import { PostHogProvider } from "posthog-js/react";
import type { ReactNode } from "react";
import { useEffect, useState } from "react";

const NEXT_PUBLIC_POSTHOG_KEY = process.env.NEXT_PUBLIC_POSTHOG_KEY;
const NEXT_PUBLIC_POSTHOG_HOST = process.env.NEXT_PUBLIC_POSTHOG_HOST || "https://app.posthog.com";
export const ANALYTICS_CONSENT_KEY = "dealix.analytics_consent.v1";
type AnalyticsConsent = "granted" | "denied";
type ConsentState = AnalyticsConsent | "loading";
let posthogInitialized = false;

function readConsent(): AnalyticsConsent | null {
  if (typeof window === "undefined") return null;
  try {
    const value = window.localStorage.getItem(ANALYTICS_CONSENT_KEY);
    return value === "granted" || value === "denied" ? value : null;
  } catch {
    return null;
  }
}

export function analyticsConsentGranted(): boolean {
  return readConsent() === "granted";
}

function persistConsent(value: AnalyticsConsent): boolean {
  try {
    window.localStorage.setItem(ANALYTICS_CONSENT_KEY, value);
    return true;
  } catch {
    return false;
  }
}

function initPostHog(onReady: () => void): void {
  if (!NEXT_PUBLIC_POSTHOG_KEY || typeof window === "undefined") return;
  if (posthogInitialized) {
    posthog.opt_in_capturing();
    onReady();
    return;
  }
  posthog.init(NEXT_PUBLIC_POSTHOG_KEY, {
    api_host: NEXT_PUBLIC_POSTHOG_HOST,
    person_profiles: "identified_only",
    autocapture: false,
    capture_pageview: false,
    capture_pageleave: false,
    disable_session_recording: true,
    loaded: () => onReady(),
  });
  posthogInitialized = true;
}

export function PostHogProviderWithInit({ children }: { children: ReactNode }) {
  const [consent, setConsent] = useState<ConsentState>("loading");
  const [ready, setReady] = useState(false);

  useEffect(() => {
    setConsent(readConsent() ?? "loading");
  }, []);

  useEffect(() => {
    if (consent !== "granted") return;
    initPostHog(() => setReady(true));
  }, [consent]);

  const choose = (value: AnalyticsConsent) => {
    const persisted = persistConsent(value);
    const effectiveConsent: AnalyticsConsent = value === "granted" && !persisted ? "denied" : value;
    setConsent(effectiveConsent);
    if (effectiveConsent === "denied") {
      setReady(false);
      if (posthogInitialized) {
        posthog.opt_out_capturing();
        posthog.reset();
      }
    }
  };

  const content = NEXT_PUBLIC_POSTHOG_KEY && consent === "granted" && ready
    ? <PostHogProvider client={posthog}>{children}</PostHogProvider>
    : <>{children}</>;

  return (
    <>
      {content}
      {NEXT_PUBLIC_POSTHOG_KEY && consent === "loading" ? (
        <aside
          aria-label="Analytics consent"
          style={{ position: "fixed", insetInline: 16, bottom: 16, zIndex: 1000, maxWidth: 720, marginInline: "auto", padding: 16, borderRadius: 16, background: "#071421", color: "white", border: "1px solid rgba(255,255,255,.18)", boxShadow: "0 18px 60px rgba(0,0,0,.28)" }}
        >
          <strong>التحليلات الاختيارية · Optional analytics</strong>
          <p style={{ margin: "8px 0 12px", lineHeight: 1.6 }}>
            نستخدم تحليلات غير ضرورية فقط بعد موافقتك لتحسين تجربة Dealix. لا نفعّل التسجيل المرئي أو الالتقاط التلقائي، ولا نرسل الاسم أو البريد أو الهاتف أو نصوص النماذج. · We use non-essential analytics only after your opt-in, with no session replay, autocapture, or direct identifiers.
          </p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            <button type="button" onClick={() => choose("granted")} style={{ padding: "10px 16px", borderRadius: 10, border: 0, fontWeight: 700, cursor: "pointer" }}>موافق · Allow</button>
            <button type="button" onClick={() => choose("denied")} style={{ padding: "10px 16px", borderRadius: 10, border: "1px solid rgba(255,255,255,.35)", background: "transparent", color: "white", fontWeight: 700, cursor: "pointer" }}>رفض · Decline</button>
          </div>
        </aside>
      ) : null}
    </>
  );
}
