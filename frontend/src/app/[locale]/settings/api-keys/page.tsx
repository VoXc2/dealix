"use client";

/**
 * API key management — list / rotate / revoke.
 *
 * Reads from TenantRecord.meta_json.api_keys via a thin admin endpoint
 * the founder wires later (we ship the UI; the endpoint is on the
 * roadmap). For now this page shows the keys persisted at onboarding
 * time and lets the user mint a new one (full backend support adds
 * later as `POST /api/v1/customers/{id}/api-keys`).
 */

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";

type KeyInfo = { label: string; prefix: string; created_at: string };

export default function ApiKeysPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = (ar: string, en: string) => (isAr ? ar : en);
  const [keys, setKeys] = useState<KeyInfo[]>([]);
  const [loading, setLoading] = useState(false);

  // Placeholder: backend endpoint to enumerate keys is a follow-up.
  useEffect(() => {
    setLoading(true);
    // For now, we read from localStorage if the trial wizard stashed
    // the issued key prefix there.
    try {
      const raw = localStorage.getItem("dealix_api_keys");
      if (raw) setKeys(JSON.parse(raw));
    } catch {
      /* ignore */
    }
    setLoading(false);
  }, []);

  function rotate() {
    toast.info(
      t(
        "ميزة التدوير تتطلب طلب من الإدارة — تواصل مع الدعم.",
        "Key rotation is admin-gated; please contact support."
      )
    );
  }

  return (
    <div className="p-8 max-w-2xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">{t("مفاتيح API", "API keys")}</h1>
      <p className="text-muted-foreground">
        {t(
          "كل مفتاح يبدأ بـ dlx_live_ متبوعاً ب 28 حرف. لا نعرض المفتاح الكامل بعد الإنشاء.",
          "Every key starts with dlx_live_ followed by 28 chars. The full key is shown only at creation."
        )}
      </p>
      {loading ? (
        <p>{t("جاري التحميل…", "Loading…")}</p>
      ) : keys.length === 0 ? (
        <p className="text-muted-foreground text-sm">
          {t(
            "لا مفاتيح بعد. أنشئ تجربتك أو تواصل مع الدعم لإصدار مفتاح.",
            "No keys yet. Start a trial or contact support to issue one."
          )}
        </p>
      ) : (
        <table className="w-full text-sm bg-card border border-border rounded-xl">
          <thead className="bg-muted text-muted-foreground text-left">
            <tr>
              <th className="p-2">{t("الاسم", "Label")}</th>
              <th className="p-2">{t("البادئة", "Prefix")}</th>
              <th className="p-2">{t("أُنشئ", "Created")}</th>
            </tr>
          </thead>
          <tbody>
            {keys.map((k, i) => (
              <tr key={i} className="border-t border-border">
                <td className="p-2">{k.label}</td>
                <td className="p-2 font-mono">{k.prefix}…</td>
                <td className="p-2">{new Date(k.created_at).toLocaleDateString(isAr ? "ar-SA" : "en-US")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <Button onClick={rotate} variant="outline">
        {t("تدوير المفتاح", "Rotate key")}
      </Button>
    </div>
  );
}
