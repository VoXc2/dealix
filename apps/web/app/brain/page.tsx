import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Company Brain — Dashboard | Dealix",
  description:
    "لوحة عقل الشركة: قرارات حديثة، سياسات نشطة، فجوات معرفية، سياق محفوظ.",
};

interface BrainEntry {
  id: string;
  type: "decision" | "policy" | "context" | "gap";
  labelAr: string;
  labelEn: string;
  detail: string;
  updatedAt: string;
}

const RECENT_ENTRIES: BrainEntry[] = [
  {
    id: "dec-001",
    type: "decision",
    labelAr: "قرار: اعتماد draft_only كوضع افتراضي لكل الإرسال",
    labelEn: "Decision: adopt draft_only as default for all outbound",
    detail: "لا إرسال تلقائي حتى يُفعّل صراحة. يقلل خطر الامتثال والخطأ.",
    updatedAt: "2026-06-22",
  },
  {
    id: "pol-001",
    type: "policy",
    labelAr: "سياسة: موافقة بشرية على كل فاتورة قبل الإرسال",
    labelEn: "Policy: human approval on every invoice before send",
    detail: "كل فاتورة تمر ببوابة موافقة. سجل التدقيق يُحفظ لكل موافقة.",
    updatedAt: "2026-06-20",
  },
  {
    id: "ctx-001",
    type: "context",
    labelAr: "سياق: ملف عميل B2B في قطاع الخدمات",
    labelEn: "Context: B2B client profile in services sector",
    detail: "SLA رد 24 ساعة. قناة التواصل المفضلة واتساب. القرار لدى المؤسس.",
    updatedAt: "2026-06-19",
  },
  {
    id: "gap-001",
    type: "gap",
    labelAr: "فجوة: لا يوجد playbook لتسليم Enterprise بعد",
    labelEn: "Gap: no Enterprise delivery playbook yet",
    detail: "التسليم الحالي يغطي SMB/Mid. Enterprise يحتاج playbook مخصص.",
    updatedAt: "2026-06-18",
  },
];

const TYPE_STYLES: Record<BrainEntry["type"], { ar: string; color: string }> = {
  decision: { ar: "قرار", color: "text-amber-300" },
  policy: { ar: "سياسة", color: "text-sky-300" },
  context: { ar: "سياق", color: "text-emerald-300" },
  gap: { ar: "فجوة", color: "text-rose-300" },
};

const stats = [
  { labelAr: "قرارات محفوظة", labelEn: "Decisions", value: "—" },
  { labelAr: "سياسات نشطة", labelEn: "Active policies", value: "—" },
  { labelAr: "سياق محفوظ", labelEn: "Context records", value: "—" },
  { labelAr: "فجوات معرفية", labelEn: "Knowledge gaps", value: "—" },
];

export default function BrainDashboardPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">
            Company Brain OS
          </p>
          <h1 className="mt-3 text-4xl font-semibold">عقل الشركة</h1>
          <p className="mt-2 text-sm text-white/60">
            Company Brain — unified memory for decisions, policies, and context
          </p>
          <p className="mt-4 max-w-2xl text-sm text-white/70">
            ذاكرة موحّدة للشركة. بدلاً من أن تكون المعرفة في رؤوس الأفراد،
            أصبحت قابلة للبحث والتسليم. كل قرار له سبب، وكل سياسة لها تاريخ،
            وكل سياق محفوظ.
          </p>
        </header>

        {/* Stats */}
        <section className="mt-10 grid gap-4 md:grid-cols-4">
          {stats.map((s) => (
            <div
              key={s.labelEn}
              className="rounded-2xl border border-white/10 bg-white/5 p-5"
            >
              <p className="text-xs uppercase tracking-widest text-white/50">
                {s.labelEn}
              </p>
              <p className="mt-2 text-2xl font-semibold text-amber-200">
                {s.value}
              </p>
              <p className="mt-1 text-xs text-white/60">{s.labelAr}</p>
            </div>
          ))}
        </section>

        {/* Recent entries */}
        <section className="mt-10">
          <h2 className="text-lg font-semibold text-amber-300">
            أحدث المدخلات
          </h2>
          <ul className="mt-4 space-y-3">
            {RECENT_ENTRIES.map((e) => {
              const style = TYPE_STYLES[e.type];
              return (
                <li
                  key={e.id}
                  className="rounded-2xl border border-white/10 bg-white/5 p-5"
                >
                  <div className="flex flex-wrap items-baseline justify-between gap-2">
                    <p className={`text-xs uppercase tracking-widest ${style.color}`}>
                      {style.ar} · {e.labelEn}
                    </p>
                    <p className="text-xs text-white/40">{e.updatedAt}</p>
                  </div>
                  <p className="mt-2 text-sm font-medium text-white">
                    {e.labelAr}
                  </p>
                  <p className="mt-1 text-xs text-white/60">{e.detail}</p>
                </li>
              );
            })}
          </ul>
        </section>

        {/* Quick links */}
        <section className="mt-10 grid gap-4 md:grid-cols-2">
          <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <p className="text-xs uppercase tracking-widest text-amber-300/80">
              منتجات مرتبطة
            </p>
            <ul className="mt-3 space-y-2 text-sm">
              <li>
                <Link
                  href="/products/company-brain-os"
                  className="text-white/80 hover:text-amber-200 hover:underline"
                >
                  نظام عقل الشركة ←
                </Link>
              </li>
              <li>
                <Link
                  href="/products/revenue-command-room-os"
                  className="text-white/80 hover:text-amber-200 hover:underline"
                >
                  نظام غرفة قيادة الإيراد ←
                </Link>
              </li>
            </ul>
          </div>
          <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <p className="text-xs uppercase tracking-widest text-amber-300/80">
              أسطح تشغيلية
            </p>
            <ul className="mt-3 space-y-2 text-sm">
              <li>
                <Link
                  href="/war-room"
                  className="text-white/80 hover:text-amber-200 hover:underline"
                >
                  غرفة الحرب ←
                </Link>
              </li>
              <li>
                <Link
                  href="/settings/outbound-safety"
                  className="text-white/80 hover:text-amber-200 hover:underline"
                >
                  إعدادات السلامة الصادرة ←
                </Link>
              </li>
            </ul>
          </div>
        </section>

        <section className="mt-10 flex flex-wrap gap-3">
          <Link
            href="/book"
            className="rounded-full bg-amber-300 px-6 py-3 text-sm font-semibold text-black transition hover:bg-amber-200"
          >
            احجز تشخيص
          </Link>
          <Link
            href="/products/company-brain-os"
            className="rounded-full border border-white/20 px-6 py-3 text-sm font-medium text-white transition hover:border-white/40"
          >
            تعرّف على Company Brain OS
          </Link>
        </section>

        <p className="mt-8 text-xs text-white/40">
          الأرقام في البطاقات تُعرض كـ — حتى ربط مصدر بيانات فعلي. لا أرقام
          افتراضية أو محاكاة.
        </p>
      </div>
    </main>
  );
}