"use client";

import posthog from "posthog-js";
import { PostHogProvider } from "posthog-js/react";
import type { ReactNode } from "react";
import { useEffect, useState } from "react";

const NEXT_PUBLIC_POSTHOG_KEY = process.env.NEXT_PUBLIC_POSTHOG_KEY;
const NEXT_PUBLIC_POSTHOG_HOST = process.env.NEXT_PUBLIC_POSTHOG_HOST || "https://us.i.posthog.com";
export const ANALYTICS_CONSENT_KEY = "dealix.analytics_consent.v1";
type AnalyticsConsent = "granted" | "denied";
type ConsentState = AnalyticsConsent | "loading";
let posthogInitialized = false;
let runtimeConsentOverride: AnalyticsConsent | null = null;

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
  if (runtimeConsentOverride !== null) return runtimeConsentOverride === "granted";
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
  const [preferencesOpen, setPreferencesOpen] = useState(false);

  useEffect(() => {
    const storedConsent = readConsent();
    runtimeConsentOverride = storedConsent;
    setConsent(storedConsent ?? "loading");
  }, []);

  useEffect(() => {
    if (consent !== "granted") return;
    initPostHog(() => setReady(true));
  }, [consent]);

  const choose = (value: AnalyticsConsent) => {
    const persisted = persistConsent(value);
    const effectiveConsent: AnalyticsConsent = value === "granted" && !persisted ? "denied" : value;
    runtimeConsentOverride = effectiveConsent;
    setConsent(effectiveConsent);
    setPreferencesOpen(false);
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
      {NEXT_PUBLIC_POSTHOG_KEY && (consent === "loading" || preferencesOpen) ? (
        <aside
          aria-label="Analytics preferences"
          style={{ position: "fixed", insetInline: 16, bottom: 16, zIndex: 1000, maxWidth: 720, marginInline: "auto", padding: 16, borderRadius: 16, background: "#071421", color: "white", border: "1px solid rgba(255,255,255,.18)", boxShadow: "0 18px 60px rgba(0,0,0,.28)" }}
        >
          <strong>التحليلات الاختيارية · Optional analytics</strong>
          <p style={{ margin: "8px 0 12px", lineHeight: 1.6 }}>
            نستخدم تحليلات غير ضرورية فقط بعد موافقتك لتحسين تجربة Dealix. يمكنك تغيير اختيارك أو سحب الموافقة في أي وقت. لا نفعّل التسجيل المرئي أو الالتقاط التلقائي، ولا نرسل الاسم أو البريد أو الهاتف أو نصوص النماذج. · We use non-essential analytics only after your opt-in. You can change or revoke consent at any time, with no session replay, autocapture, or direct identifiers.
          </p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            <button type="button" onClick={() => choose("granted")} style={{ padding: "10px 16px", borderRadius: 10, border: 0, fontWeight: 700, cursor: "pointer" }}>موافق · Allow</button>
            <button type="button" onClick={() => choose("denied")} style={{ padding: "10px 16px", borderRadius: 10, border: "1px solid rgba(255,255,255,.35)", background: "transparent", color: "white", fontWeight: 700, cursor: "pointer" }}>رفض / سحب الموافقة · Decline / Revoke</button>
            {consent !== "loading" ? (
              <button type="button" onClick={() => setPreferencesOpen(false)} style={{ padding: "10px 16px", borderRadius: 10, border: "1px solid rgba(255,255,255,.22)", background: "transparent", color: "white", cursor: "pointer" }}>إغلاق · Close</button>
            ) : null}
          </div>
        </aside>
      ) : null}
      {NEXT_PUBLIC_POSTHOG_KEY && consent !== "loading" && !preferencesOpen ? (
        <button
          type="button"
          aria-label="Analytics privacy preferences"
          onClick={() => setPreferencesOpen(true)}
          style={{ position: "fixed", insetInlineEnd: 16, bottom: 16, zIndex: 999, padding: "8px 12px", borderRadius: 999, border: "1px solid rgba(7,20,33,.22)", background: "white", color: "#071421", fontWeight: 700, cursor: "pointer", boxShadow: "0 8px 28px rgba(0,0,0,.16)" }}
        >
          الخصوصية · Privacy
        </button>
      ) : null}
    </>
  );
}
