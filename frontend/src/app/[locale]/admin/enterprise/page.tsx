"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { toast } from "sonner";

const API_BASE =
  (typeof window !== "undefined" && (window as any).__DEALIX_API_BASE__) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "";

function adminHeader(): Record<string, string> {
  const k =
    typeof window !== "undefined"
      ? localStorage.getItem("dealix_admin_key") || ""
      : "";
  return k ? { "x-api-key": k } : {};
}

type ByokStatus = { configured: boolean; provider: string | null; key_id_present: boolean };
type AuditFwdStatus = { datadog: boolean; splunk: boolean; s3: boolean };

export default function EnterpriseAdminPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = (ar: string, en: string) => (isAr ? ar : en);
  const [byok, setByok] = useState<ByokStatus | null>(null);
  const [fwd, setFwd] = useState<AuditFwdStatus | null>(null);
  const [tenant, setTenant] = useState("");
  const [adminKey, setAdminKey] = useState("");
  const [rotating, setRotating] = useState(false);
  const [newSecret, setNewSecret] = useState<string | null>(null);
  const [sandbox, setSandbox] = useState<string | null>(null);

  useEffect(() => {
    setAdminKey(localStorage.getItem("dealix_admin_key") || "");
  }, []);

  function saveAdminKey() {
    localStorage.setItem("dealix_admin_key", adminKey);
    toast.success(t("تم الحفظ", "Saved"));
  }

  async function loadStatus() {
    try {
      const [b, f] = await Promise.all([
        fetch(`${API_BASE}/api/v1/admin/byok/status`, { headers: { ...adminHeader() } }).then(
          (r) => (r.ok ? r.json() : null)
        ),
        fetch(`${API_BASE}/api/v1/admin/audit-forward/status`, {
          headers: { ...adminHeader() },
        }).then((r) => (r.ok ? r.json() : null)),
      ]);
      setByok(b);
      setFwd(f);
      if (!b || !f) toast.error(t("غير مصرّح", "Unauthorized"));
    } catch (e: any) {
      toast.error(e.message);
    }
  }

  async function rotateWebhook() {
    if (!tenant) return;
    setRotating(true);
    setNewSecret(null);
    try {
      const r = await fetch(
        `${API_BASE}/api/v1/admin/tenant/${tenant}/webhook-keys/rotate`,
        { method: "POST", headers: { ...adminHeader() } }
      );
      const body = await r.json();
      if (!r.ok) throw new Error(body.detail || `HTTP ${r.status}`);
      setNewSecret(body.webhook_secret);
      toast.success(t("تم التدوير", "Rotated"));
    } catch (e: any) {
      toast.error(e.message);
    } finally {
      setRotating(false);
    }
  }

  async function spinUpSandbox() {
    if (!tenant) return;
    try {
      const r = await fetch(`${API_BASE}/api/v1/admin/sandbox/spin-up`, {
        method: "POST",
        headers: { "Content-Type": "application/json", ...adminHeader() },
        body: JSON.stringify({ tenant_id: tenant, label: "ops-spin-up" }),
      });
      const body = await r.json();
      if (!r.ok) throw new Error(body.detail || `HTTP ${r.status}`);
      setSandbox(body.tenant_id);
      toast.success(t("تم إنشاء البيئة", "Sandbox created"));
    } catch (e: any) {
      toast.error(e.message);
    }
  }

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-8">
      <header>
        <h1 className="text-3xl font-bold">{t("إدارة المؤسسة", "Enterprise admin")}</h1>
        <p className="text-muted-foreground mt-2">
          {t(
            "BYOK، تدوير مفاتيح Webhooks، إنشاء بيئات تجريبية، فحص حالة التشفير وإعادة توجيه السجلات.",
            "BYOK status, webhook key rotation, sandbox spin-up, encryption + audit-forward telemetry."
          )}
        </p>
      </header>

      <section className="bg-card border border-border rounded-xl p-4 space-y-3">
        <h2 className="font-semibold">{t("مفتاح المسؤول", "Admin API key")}</h2>
        <p className="text-sm text-muted-foreground">
          {t(
            "هذا المفتاح يُحفظ محلياً في المتصفح ولا يُرسل لأي طرف ثالث.",
            "Stored in localStorage only; sent solely to your Dealix API."
          )}
        </p>
        <div className="flex gap-2">
          <input
            type="password"
            value={adminKey}
            onChange={(e) => setAdminKey(e.target.value)}
            className="flex-1 px-3 py-2 border border-border rounded-lg bg-background"
            placeholder="ADMIN_API_KEYS value"
          />
          <button
            onClick={saveAdminKey}
            className="px-3 py-2 bg-slate-700 hover:bg-slate-800 text-white rounded-lg text-sm"
          >
            {t("حفظ", "Save")}
          </button>
        </div>
        <button
          onClick={loadStatus}
          className="px-3 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-sm"
        >
          {t("جلب الحالة", "Load status")}
        </button>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-card border border-border rounded-xl p-4">
          <h2 className="font-semibold">{t("BYOK", "BYOK")}</h2>
          {byok ? (
            <ul className="text-sm space-y-1 mt-2">
              <li>configured: {byok.configured ? "✓" : "—"}</li>
              <li>provider: {byok.provider ?? "—"}</li>
              <li>key id present: {byok.key_id_present ? "✓" : "—"}</li>
            </ul>
          ) : (
            <p className="text-sm text-muted-foreground">{t("اضغط جلب الحالة", "Click load status")}</p>
          )}
        </div>
        <div className="bg-card border border-border rounded-xl p-4">
          <h2 className="font-semibold">{t("إعادة توجيه السجلات", "Audit forwarding")}</h2>
          {fwd ? (
            <ul className="text-sm space-y-1 mt-2">
              <li>datadog: {fwd.datadog ? "✓" : "—"}</li>
              <li>splunk: {fwd.splunk ? "✓" : "—"}</li>
              <li>s3: {fwd.s3 ? "✓" : "—"}</li>
            </ul>
          ) : (
            <p className="text-sm text-muted-foreground">{t("اضغط جلب الحالة", "Click load status")}</p>
          )}
        </div>
      </section>

      <section className="bg-card border border-border rounded-xl p-4 space-y-3">
        <h2 className="font-semibold">
          {t("عمليات لكل مستأجر", "Per-tenant operations")}
        </h2>
        <input
          value={tenant}
          onChange={(e) => setTenant(e.target.value)}
          placeholder="tenant_id"
          className="w-full px-3 py-2 border border-border rounded-lg bg-background"
        />
        <div className="flex gap-2">
          <button
            onClick={rotateWebhook}
            disabled={!tenant || rotating}
            className="px-3 py-2 bg-amber-600 hover:bg-amber-700 disabled:bg-amber-300 text-white rounded-lg text-sm"
          >
            {rotating
              ? t("جاري التدوير…", "Rotating…")
              : t("تدوير مفتاح Webhook", "Rotate webhook key")}
          </button>
          <button
            onClick={spinUpSandbox}
            disabled={!tenant}
            className="px-3 py-2 bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-300 text-white rounded-lg text-sm"
          >
            {t("إنشاء بيئة تجريبية", "Spin up sandbox")}
          </button>
        </div>
        {newSecret && (
          <div className="bg-amber-50 border border-amber-200 rounded p-3 text-xs">
            <strong>{t("احفظ هذا المفتاح الآن:", "Save this secret now:")}</strong>
            <code className="block break-all mt-1">{newSecret}</code>
          </div>
        )}
        {sandbox && (
          <div className="bg-emerald-50 border border-emerald-200 rounded p-3 text-xs">
            <strong>{t("بيئة جديدة:", "New sandbox tenant:")}</strong>
            <code className="block break-all mt-1">{sandbox}</code>
          </div>
        )}
      </section>
    </div>
  );
}
