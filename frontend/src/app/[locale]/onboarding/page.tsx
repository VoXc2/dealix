"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { useRouter, useSearchParams } from "next/navigation";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type Step = "start" | "integrations" | "dpa" | "finalize" | "done";

const STEPS: Step[] = ["start", "integrations", "dpa", "finalize", "done"];

const INTEGRATION_OPTIONS = [
  { id: "hubspot", label_ar: "HubSpot CRM", label_en: "HubSpot CRM" },
  { id: "whatsapp", label_ar: "واتساب الأعمال", label_en: "WhatsApp Business" },
  { id: "calendly", label_ar: "Calendly", label_en: "Calendly" },
  { id: "resend", label_ar: "Resend (بريد المعاملات)", label_en: "Resend (transactional email)" },
  { id: "moyasar", label_ar: "Moyasar (الدفع)", label_en: "Moyasar (payments)" },
  { id: "stripe", label_ar: "Stripe (دولي)", label_en: "Stripe (international)" },
];

const API_BASE =
  (typeof window !== "undefined" && (window as any).__DEALIX_API_BASE__) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "";

async function api<T>(path: string, body?: unknown): Promise<T> {
  const r = await fetch(`${API_BASE}${path}`, {
    method: body ? "POST" : "GET",
    headers: { "content-type": "application/json", accept: "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!r.ok) {
    let detail: any = {};
    try {
      detail = await r.json();
    } catch {}
    throw new Error(detail?.detail || `request_failed_${r.status}`);
  }
  return (await r.json()) as T;
}

export default function OnboardingPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const router = useRouter();
  const params = useSearchParams();
  const [step, setStep] = useState<Step>("start");
  const [onboardingId, setOnboardingId] = useState<string | null>(
    params.get("id")
  );
  const [busy, setBusy] = useState(false);
  // Step 1 inputs
  const [company, setCompany] = useState("");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  // Step 2
  const [picked, setPicked] = useState<Set<string>>(new Set());
  // Step 3
  const [signer, setSigner] = useState("");
  const [accepted, setAccepted] = useState(false);
  // Step 4 output
  const [apiKey, setApiKey] = useState<string | null>(null);

  // Resume support.
  useEffect(() => {
    if (!onboardingId) return;
    (async () => {
      try {
        const state = await api<any>(`/api/v1/onboarding/${onboardingId}`);
        if (state?.step && STEPS.includes(state.step as Step)) {
          setStep(state.step === "finalized" ? "done" : (state.step as Step));
        }
      } catch {
        /* ignore resume failure; user can restart */
      }
    })();
  }, [onboardingId]);

  const t = (ar: string, en: string) => (isAr ? ar : en);

  async function submitStart(e: React.FormEvent) {
    e.preventDefault();
    if (!company || !email || !name) return;
    setBusy(true);
    try {
      const res = await api<any>("/api/v1/onboarding/start", {
        company,
        email,
        name,
        locale,
      });
      setOnboardingId(res.tenant_id);
      router.replace(`/${locale}/onboarding?id=${res.tenant_id}`);
      setStep("integrations");
    } catch (err: any) {
      toast.error(t("تعذّر البدء", "Could not start") + ": " + err.message);
    } finally {
      setBusy(false);
    }
  }

  async function submitIntegrations() {
    if (!onboardingId) return;
    setBusy(true);
    try {
      await api("/api/v1/onboarding/integrations", {
        onboarding_id: onboardingId,
        integrations: Array.from(picked),
      });
      setStep("dpa");
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function submitDPA() {
    if (!onboardingId) return;
    if (!accepted || !signer) {
      toast.error(t("الموافقة والاسم مطلوبان", "Acceptance + signer required"));
      return;
    }
    setBusy(true);
    try {
      await api("/api/v1/onboarding/dpa", {
        onboarding_id: onboardingId,
        accept: true,
        signer_name: signer,
      });
      setStep("finalize");
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setBusy(false);
    }
  }

  async function submitFinalize() {
    if (!onboardingId) return;
    setBusy(true);
    try {
      const res = await api<any>("/api/v1/onboarding/finalize", {
        onboarding_id: onboardingId,
        plan: "starter",
      });
      setApiKey(res.api_key);
      setStep("done");
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setBusy(false);
    }
  }

  const progress = STEPS.indexOf(step) + 1;

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4 py-8">
      <div className="max-w-xl w-full bg-card border border-border rounded-xl p-8 shadow-xl">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-2xl font-bold">
            {t("ابدأ مع Dealix", "Get started with Dealix")}
          </h1>
          <span className="text-sm text-muted-foreground">
            {progress} / {STEPS.length}
          </span>
        </div>
        <div className="h-2 bg-muted rounded-full mb-8 overflow-hidden">
          <div
            className="h-full bg-emerald-500 transition-all"
            style={{ width: `${(progress / STEPS.length) * 100}%` }}
          />
        </div>

        {step === "start" && (
          <form onSubmit={submitStart} className="space-y-4">
            <div>
              <Label>{t("اسم الشركة", "Company name")}</Label>
              <Input value={company} onChange={(e) => setCompany(e.target.value)} required />
            </div>
            <div>
              <Label>{t("اسمك", "Your name")}</Label>
              <Input value={name} onChange={(e) => setName(e.target.value)} required />
            </div>
            <div>
              <Label>{t("البريد الإلكتروني للعمل", "Work email")}</Label>
              <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            </div>
            <Button type="submit" disabled={busy} className="w-full">
              {busy ? t("جاري الإنشاء…", "Creating…") : t("متابعة", "Continue")}
            </Button>
          </form>
        )}

        {step === "integrations" && (
          <div className="space-y-4">
            <p className="text-muted-foreground text-sm">
              {t(
                "اختر التكاملات التي تريد تفعيلها. يمكن تعديلها لاحقاً.",
                "Pick the integrations you want enabled. You can edit later."
              )}
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {INTEGRATION_OPTIONS.map((opt) => {
                const on = picked.has(opt.id);
                return (
                  <label
                    key={opt.id}
                    className={`p-3 rounded-lg border cursor-pointer transition ${
                      on ? "border-emerald-500 bg-emerald-500/10" : "border-border"
                    }`}
                  >
                    <input
                      type="checkbox"
                      checked={on}
                      onChange={() => {
                        const n = new Set(picked);
                        if (on) n.delete(opt.id);
                        else n.add(opt.id);
                        setPicked(n);
                      }}
                      className="mr-2 align-middle"
                    />
                    {isAr ? opt.label_ar : opt.label_en}
                  </label>
                );
              })}
            </div>
            <Button onClick={submitIntegrations} disabled={busy} className="w-full">
              {busy ? "…" : t("متابعة", "Continue")}
            </Button>
          </div>
        )}

        {step === "dpa" && (
          <div className="space-y-4">
            <p>
              {t(
                "للمتابعة وفق نظام PDPL السعودي، نحتاج موافقتك على اتفاقية معالجة البيانات.",
                "To proceed under Saudi PDPL, we need your acceptance of the Data Processing Agreement."
              )}
            </p>
            <a
              href="/docs/legal/DPA.md"
              target="_blank"
              className="text-emerald-500 underline text-sm"
              rel="noreferrer"
            >
              {t("اقرأ الـ DPA", "Read the DPA")}
            </a>
            <div>
              <Label>{t("اسم الموقّع", "Signer name")}</Label>
              <Input value={signer} onChange={(e) => setSigner(e.target.value)} />
            </div>
            <label className="flex items-center gap-2 text-sm">
              <input
                type="checkbox"
                checked={accepted}
                onChange={(e) => setAccepted(e.target.checked)}
              />
              {t("أوافق على اتفاقية معالجة البيانات", "I accept the DPA")}
            </label>
            <Button onClick={submitDPA} disabled={busy} className="w-full">
              {busy ? "…" : t("متابعة", "Continue")}
            </Button>
          </div>
        )}

        {step === "finalize" && (
          <div className="space-y-4">
            <p>
              {t(
                "خطوة أخيرة — سننشئ مفتاح API الأول لشركتك.",
                "Final step — we will create your first API key."
              )}
            </p>
            <Button onClick={submitFinalize} disabled={busy} className="w-full">
              {busy ? t("جاري الإنشاء…", "Creating…") : t("إنهاء وإنشاء المفتاح", "Finalize & issue key")}
            </Button>
          </div>
        )}

        {step === "done" && (
          <div className="space-y-4 text-center">
            <h2 className="text-xl font-semibold">
              {t("تم! حسابك جاهز", "Done! Your account is ready")}
            </h2>
            {apiKey && (
              <div className="bg-muted p-4 rounded-lg font-mono text-sm break-all border border-emerald-500/40">
                {apiKey}
              </div>
            )}
            <p className="text-xs text-muted-foreground">
              {t(
                "احفظ هذا المفتاح الآن — لن يُعرض مرة أخرى.",
                "Save this key now — it will not be shown again."
              )}
            </p>
            <Button onClick={() => router.push(`/${locale}/dashboard`)} className="w-full">
              {t("افتح اللوحة", "Open dashboard")}
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}
