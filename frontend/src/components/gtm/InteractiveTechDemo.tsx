"use client";

import { useState } from "react";
import { useLocale } from "next-intl";

export function InteractiveTechDemo() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [sector, setSector] = useState("technology_saas_si");
  const [diagnostic, setDiagnostic] = useState("A01");
  const sectors = [
    { id: "technology_saas_si", ar: "تقنية", en: "Technology" },
    { id: "government_b2g", ar: "حكومي", en: "Government" },
    { id: "construction_epc", ar: "إنشاءات", en: "Construction" },
    { id: "finance_fintech_insurance", ar: "مالية", en: "Finance" },
    { id: "healthcare", ar: "صحة", en: "Healthcare" },
  ];
  const diagnostics = [
    { id: "A01", ar: "تنفيذي/استراتيجي", en: "Executive" },
    { id: "A12", ar: "أتمتة", en: "Automation" },
    { id: "A37", ar: "فاتورة", en: "Fatoora" },
    { id: "A05", ar: "تسرّب إيراد", en: "Revenue Leakage" },
  ];
  return (
    <div className="rounded-2xl border border-white/10 bg-white/5 p-6 backdrop-blur">
      <h3 className="font-bold text-gold-400">{isAr ? "جرب التقنية تفاعلياً" : "Try Tech Interactively"}</h3>
      <p className="text-xs text-white/50 mt-1">{isAr ? "اختر قطاعك وشاهد التشخيص التقني بدون شوائب" : "Pick sector, see technical diagnostic without impurities"}</p>
      <div className="grid gap-4 md:grid-cols-2 mt-4">
        <div>
          <label className="text-xs text-white/40">{isAr ? "القطاع" : "Sector"}</label>
          <select value={sector} onChange={(e) => setSector(e.target.value)} className="w-full mt-1 bg-navy-800 border border-white/10 rounded-lg px-3 py-2 text-sm text-white">
            {sectors.map((s) => <option key={s.id} value={s.id}>{isAr ? s.ar : s.en}</option>)}
          </select>
        </div>
        <div>
          <label className="text-xs text-white/40">{isAr ? "التشخيص" : "Diagnostic"}</label>
          <select value={diagnostic} onChange={(e) => setDiagnostic(e.target.value)} className="w-full mt-1 bg-navy-800 border border-white/10 rounded-lg px-3 py-2 text-sm text-white">
            {diagnostics.map((d) => <option key={d.id} value={d.id}>{isAr ? d.ar : d.en}</option>)}
          </select>
        </div>
      </div>
      <div className="mt-4 rounded-xl border border-emerald-500/20 bg-emerald-500/10 p-4">
        <p className="text-sm font-bold text-emerald-400">{isAr ? "النتيجة التقنية" : "Technical Result"}</p>
        <p className="text-xs text-white/70 mt-1">{isAr ? `قطاع \${sector} + تشخيص \${diagnostic} → 5 وكلاء، 44 ذراع، DeepWIP≤3، بدون شوائب` : `Sector \${sector} + Diagnostic \${diagnostic} → 5 agents, 44 arms, DeepWIP≤3, no impurities`}</p>
        <p className="text-xs text-white/40 mt-2">500 cells • 50 families • 12 channels • SaaS 20 tenants • Proof L0-L5</p>
      </div>
    </div>
  );
}
