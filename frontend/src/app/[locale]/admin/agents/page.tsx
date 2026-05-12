"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { toast } from "sonner";

const API_BASE =
  (typeof window !== "undefined" && (window as any).__DEALIX_API_BASE__) ||
  process.env.NEXT_PUBLIC_API_BASE ||
  "";

function authHeader(): Record<string, string> {
  const t = typeof window !== "undefined" ? localStorage.getItem("dealix_access_token") : null;
  return t ? { Authorization: `Bearer ${t}` } : {};
}

type Agent = {
  id: string;
  name: string;
  model: string;
  tools: string[];
  max_usd_per_request: number;
  locale: string;
};

type WorkflowTemplate = {
  id: string;
  description: string;
};

const SAMPLE_AGENT = `{
  "id": "lead-qualifier-ksa",
  "name": "KSA lead qualifier",
  "description": "BANT + PDPL gate for Saudi inbound.",
  "model": "claude-haiku-4-5",
  "tools": ["sales_qualifier", "compliance_reviewer"],
  "prompt_override": "You are an Arabic-Khaliji sales qualifier.",
  "max_usd_per_request": 0.5,
  "locale": "ar"
}`;

export default function AgentsBuilderPage() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const t = (ar: string, en: string) => (isAr ? ar : en);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [marketplace, setMarketplace] = useState<WorkflowTemplate[]>([]);
  const [draft, setDraft] = useState(SAMPLE_AGENT);
  const [submitting, setSubmitting] = useState(false);

  async function reload() {
    try {
      const [a, m] = await Promise.all([
        fetch(`${API_BASE}/api/v1/agents`, { headers: { ...authHeader() } }).then((r) =>
          r.ok ? r.json() : { agents: [] }
        ),
        fetch(`${API_BASE}/api/v1/workflows/marketplace`, {
          headers: { ...authHeader() },
        }).then((r) => (r.ok ? r.json() : { templates: [] })),
      ]);
      setAgents(a.agents || []);
      setMarketplace(m.templates || []);
    } catch (e: any) {
      toast.error(e.message);
    }
  }

  useEffect(() => {
    reload();
  }, []);

  async function submit() {
    setSubmitting(true);
    try {
      const parsed = JSON.parse(draft);
      const r = await fetch(`${API_BASE}/api/v1/agents`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...authHeader(),
        },
        body: JSON.stringify(parsed),
      });
      const body = await r.json();
      if (!r.ok) throw new Error(body.detail || `HTTP ${r.status}`);
      toast.success(t("تم تسجيل الوكيل", "Agent registered"));
      reload();
    } catch (e: any) {
      toast.error(`${e.message}`);
    } finally {
      setSubmitting(false);
    }
  }

  async function install(template_id: string) {
    try {
      const r = await fetch(`${API_BASE}/api/v1/workflows/install`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...authHeader(),
        },
        body: JSON.stringify({ template_id }),
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      toast.success(t("تم تثبيت المسار", "Workflow installed"));
    } catch (e: any) {
      toast.error(e.message);
    }
  }

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-8">
      <header>
        <h1 className="text-3xl font-bold">
          {t("صانع الوكلاء + متجر المسارات", "Agent builder + workflow marketplace")}
        </h1>
      </header>

      <section className="space-y-3">
        <h2 className="text-xl font-semibold">{t("وكلاؤك", "Your agents")}</h2>
        {agents.length === 0 ? (
          <p className="text-muted-foreground text-sm">
            {t("لا وكلاء بعد. أنشئ واحد بالأسفل.", "No agents yet. Create one below.")}
          </p>
        ) : (
          <ul className="space-y-2">
            {agents.map((a) => (
              <li
                key={a.id}
                className="border border-border bg-card rounded-lg p-3 flex justify-between items-center"
              >
                <div>
                  <strong>{a.name}</strong>{" "}
                  <code className="text-xs text-muted-foreground">{a.id}</code>
                  <div className="text-xs text-muted-foreground">
                    {a.model} · ${a.max_usd_per_request} · {a.tools.join(", ")}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-semibold">{t("سجّل وكيل", "Register agent")}</h2>
        <p className="text-sm text-muted-foreground">
          {t(
            "ألصق agent.yaml كـ JSON. التحقق يتم خادمياً.",
            "Paste an agent.yaml as JSON. Validation runs server-side."
          )}
        </p>
        <textarea
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          rows={14}
          className="w-full font-mono text-sm p-3 border border-border rounded-lg bg-card"
          spellCheck={false}
        />
        <button
          onClick={submit}
          disabled={submitting}
          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-300 text-white rounded-lg font-medium"
        >
          {submitting ? t("جاري التسجيل…", "Registering…") : t("تسجيل", "Register")}
        </button>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-semibold">
          {t("متجر المسارات", "Workflow marketplace")}
        </h2>
        <ul className="space-y-2">
          {marketplace.map((m) => (
            <li
              key={m.id}
              className="border border-border bg-card rounded-lg p-3 flex justify-between items-center"
            >
              <div>
                <code className="font-semibold">{m.id}</code>
                <p className="text-sm text-muted-foreground">{m.description}</p>
              </div>
              <button
                onClick={() => install(m.id)}
                className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded text-sm"
              >
                {t("تثبيت", "Install")}
              </button>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
