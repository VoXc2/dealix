"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { LEARN_ARTICLES } from "@/content/learn/articles";

/* ─── Data ──────────────────────────────────────────── */

type Category = {
  id: string;
  ar: string;
  en: string;
  color: string;
  slugs: string[];
};

const CATEGORIES: Category[] = [
  {
    id: "all",
    ar: "الكل",
    en: "All",
    color: "bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300",
    slugs: [],
  },
  {
    id: "pdpl",
    ar: "PDPL",
    en: "PDPL",
    color: "bg-blue-100 dark:bg-blue-950/30 text-blue-700 dark:text-blue-300",
    slugs: ["pdpl-guide-saudi-b2b-2026", "no-cold-whatsapp-policy"],
  },
  {
    id: "zatca",
    ar: "ZATCA",
    en: "ZATCA",
    color: "bg-amber-100 dark:bg-amber-950/30 text-amber-700 dark:text-amber-300",
    slugs: ["zatca-wave-24-guide"],
  },
  {
    id: "ai",
    ar: "حوكمة AI",
    en: "AI Governance",
    color: "bg-purple-100 dark:bg-purple-950/30 text-purple-700 dark:text-purple-300",
    slugs: ["ai-governance-saudi-b2b"],
  },
  {
    id: "revenue",
    ar: "تشغيل الإيرادات",
    en: "Revenue Ops",
    color: "bg-emerald-100 dark:bg-emerald-950/30 text-emerald-700 dark:text-emerald-300",
    slugs: ["revenue-leakage-detection", "post-lead-revenue-ops", "crm-vs-revenue-ops"],
  },
  {
    id: "sprint",
    ar: "Sprint",
    en: "Sprint",
    color: "bg-orange-100 dark:bg-orange-950/30 text-orange-700 dark:text-orange-300",
    slugs: ["10-lead-audit", "audit-lead-follow-up", "what-is-proof-pack"],
  },
];

const SLUG_TO_CATEGORY: Record<string, Category> = {};
for (const cat of CATEGORIES) {
  for (const slug of cat.slugs) {
    SLUG_TO_CATEGORY[slug] = cat;
  }
}

const FEATURED_SLUGS = [
  "pdpl-guide-saudi-b2b-2026",
  "zatca-wave-24-guide",
  "ai-governance-saudi-b2b",
  "revenue-leakage-detection",
];

/* ─── Component ─────────────────────────────────────── */

interface LearnHubProps {
  className?: string;
}

export function LearnHub({ className = "" }: LearnHubProps) {
  const locale = useLocale();
  const isAr = locale === "ar";
  const base = `/${locale}`;
  const [activeCategory, setActiveCategory] = useState("all");
  const [email, setEmail] = useState("");
  const [subscribed, setSubscribed] = useState(false);

  const filteredArticles =
    activeCategory === "all"
      ? LEARN_ARTICLES
      : LEARN_ARTICLES.filter((a) => {
          const cat = CATEGORIES.find((c) => c.id === activeCategory);
          return cat ? cat.slugs.includes(a.slug) : true;
        });

  const featuredArticles = LEARN_ARTICLES.filter((a) => FEATURED_SLUGS.includes(a.slug));

  const handleSubscribe = (e: React.FormEvent) => {
    e.preventDefault();
    if (email) setSubscribed(true);
  };

  return (
    <div
      className={`space-y-14 ${className}`}
      dir={isAr ? "rtl" : "ltr"}
    >

      {/* ── Header ── */}
      <header className={isAr ? "text-right" : "text-left"}>
        <p className="text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-2">
          {isAr ? "مكتبة المعرفة" : "Knowledge Library"}
        </p>
        <h1 className="text-4xl font-bold">
          {isAr ? "تعلّم Revenue Ops بالعربية" : "Learn Revenue Ops"}
        </h1>
        <p className="mt-4 text-muted-foreground leading-relaxed max-w-2xl">
          {isAr
            ? "محتوى متخصص لشركات B2B السعودية — PDPL، ZATCA، حوكمة AI، تشغيل الإيرادات. كل مقالة عملية وقابلة للتطبيق فوراً."
            : "Specialized content for Saudi B2B companies — PDPL, ZATCA, AI governance, revenue operations. Every article is practical and immediately applicable."}
        </p>
      </header>

      {/* ── Category Filter ── */}
      <div className="flex flex-wrap gap-2">
        {CATEGORIES.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setActiveCategory(cat.id)}
            className={`rounded-full px-3 py-1.5 text-xs font-medium transition-all border ${
              activeCategory === cat.id
                ? `${cat.color} border-transparent`
                : "border-border/60 bg-card/50 text-muted-foreground hover:bg-muted/30"
            }`}
          >
            {isAr ? cat.ar : cat.en}
          </button>
        ))}
      </div>

      {/* ── Featured Articles (only when 'all' is active) ── */}
      {activeCategory === "all" && (
        <div>
          <p className="text-xs text-muted-foreground uppercase tracking-wide font-semibold mb-4">
            {isAr ? "مقالات مميزة" : "Featured Articles"}
          </p>
          <div className="grid gap-4 sm:grid-cols-2">
            {featuredArticles.map((a) => {
              const cat = SLUG_TO_CATEGORY[a.slug];
              return (
                <Link
                  key={a.slug}
                  href={`${base}/learn/${a.slug}`}
                  className="group rounded-xl border border-border/60 bg-card/50 p-5 hover:border-border hover:shadow-sm transition-all"
                >
                  {cat && (
                    <span className={`inline-block rounded-full px-2.5 py-0.5 text-xs font-medium mb-3 ${cat.color}`}>
                      {isAr ? cat.ar : cat.en}
                    </span>
                  )}
                  <h2 className="font-semibold text-base group-hover:text-primary transition-colors">
                    {isAr ? a.titleAr : a.titleEn}
                  </h2>
                  <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
                    {isAr ? a.descriptionAr : a.descriptionEn}
                  </p>
                  {a.readTimeMinAr && (
                    <p className="text-xs text-muted-foreground mt-3">
                      T {isAr ? a.readTimeMinAr : a.readTimeMinEn}
                    </p>
                  )}
                </Link>
              );
            })}
          </div>
        </div>
      )}

      {/* ── All / Filtered Articles ── */}
      <div>
        <p className="text-xs text-muted-foreground uppercase tracking-wide font-semibold mb-4">
          {activeCategory === "all"
            ? (isAr ? "جميع المقالات" : "All Articles")
            : (isAr
                ? `${CATEGORIES.find((c) => c.id === activeCategory)?.ar ?? ""} — المقالات`
                : `${CATEGORIES.find((c) => c.id === activeCategory)?.en ?? ""} — Articles`)}
        </p>
        {filteredArticles.length === 0 ? (
          <p className="text-muted-foreground text-sm">
            {isAr ? "لا توجد مقالات في هذا التصنيف حالياً." : "No articles in this category yet."}
          </p>
        ) : (
          <ul className="space-y-3">
            {filteredArticles.map((a) => {
              const cat = SLUG_TO_CATEGORY[a.slug];
              return (
                <li key={a.slug}>
                  <Link
                    href={`${base}/learn/${a.slug}`}
                    className="group flex items-center justify-between rounded-xl border border-border/40 bg-card/30 px-5 py-3 hover:border-border hover:bg-card/60 transition-all"
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      {cat && (
                        <span className={`hidden sm:inline-block flex-shrink-0 rounded-full px-2 py-0.5 text-xs font-medium ${cat.color}`}>
                          {isAr ? cat.ar : cat.en}
                        </span>
                      )}
                      <span className="font-medium group-hover:text-primary transition-colors text-sm truncate">
                        {isAr ? a.titleAr : a.titleEn}
                      </span>
                    </div>
                    {a.readTimeMinAr && (
                      <span className="text-xs text-muted-foreground flex-shrink-0 ms-3">
                        {isAr ? a.readTimeMinAr : a.readTimeMinEn}
                      </span>
                    )}
                  </Link>
                </li>
              );
            })}
          </ul>
        )}
      </div>

      {/* ── Request a Topic ── */}
      <Card className="border-border/60 bg-card/50 p-6">
        <p className="font-semibold text-sm mb-1">
          {isAr ? "اطلب موضوعاً" : "Request a Topic"}
        </p>
        <p className="text-sm text-muted-foreground mb-4">
          {isAr
            ? "لديك موضوع تريد معرفة المزيد عنه؟ نرحّب باقتراحاتك."
            : "Have a topic you want to learn more about? We welcome your suggestions."}
        </p>
        <Button asChild size="sm" variant="outline">
          <Link href={`${base}/dealix-diagnostic`}>
            {isAr ? "اقترح موضوعاً" : "Suggest a Topic"}
          </Link>
        </Button>
      </Card>

      {/* ── Newsletter Signup ── */}
      <div className="rounded-xl bg-gradient-to-br from-[#0A1628] to-[#0a2040] text-white p-6">
        <p className="font-semibold text-lg mb-1">
          {isAr ? "ملخص أسبوعي لـ Revenue Ops" : "Weekly Revenue Ops Digest"}
        </p>
        <p className="text-white/70 text-sm mb-5">
          {isAr
            ? "مقالة جديدة كل أسبوع — PDPL، ZATCA، حوكمة AI، وتشغيل الإيرادات للسوق السعودي."
            : "New article every week — PDPL, ZATCA, AI governance, and revenue ops for the Saudi market."}
        </p>
        {subscribed ? (
          <p className="text-emerald-400 text-sm font-medium">
            {isAr ? "شكراً! سنتواصل معك قريباً." : "Thank you! We'll be in touch soon."}
          </p>
        ) : (
          <form onSubmit={handleSubscribe} className="flex flex-col sm:flex-row gap-3">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder={isAr ? "بريدك الإلكتروني" : "Your email address"}
              className="flex-1 rounded-lg border border-white/20 bg-white/10 px-4 py-2 text-sm text-white placeholder:text-white/40 focus:outline-none focus:ring-1 focus:ring-[#C9974B]"
              required
            />
            <button
              type="submit"
              className="rounded-lg bg-[#C9974B] text-[#0A1628] px-5 py-2 text-sm font-semibold hover:bg-[#b8863a] transition-colors whitespace-nowrap"
            >
              {isAr ? "اشترك" : "Subscribe"}
            </button>
          </form>
        )}
        <p className="mt-3 text-xs text-white/40">
          {isAr
            ? "لا spam. إلغاء الاشتراك في أي وقت. PDPL أصيل."
            : "No spam. Unsubscribe at any time. PDPL native."}
        </p>
      </div>

      {/* ── CTA ── */}
      <div className="rounded-xl border border-border/60 bg-card/50 p-6 flex flex-wrap gap-4 items-center justify-between">
        <div>
          <p className="font-semibold">{isAr ? "جاهز للتطبيق؟" : "Ready to apply?"}</p>
          <p className="text-sm text-muted-foreground mt-1">
            {isAr ? "ابدأ بـ Risk Score مجاني أو تشخيص محكوم." : "Start with a free Risk Score or a governed diagnostic."}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button asChild size="sm" className="bg-[#C9974B] text-[#0A1628] hover:bg-[#b8863a] font-semibold">
            <Link href={`${base}/risk-score`}>
              {isAr ? "Risk Score مجاني" : "Free Risk Score"}
            </Link>
          </Button>
          <Button asChild size="sm" variant="outline">
            <Link href={`${base}/dealix-diagnostic`}>
              {isAr ? "تشخيص محكوم" : "Governed Diagnostic"}
            </Link>
          </Button>
        </div>
      </div>

    </div>
  );
}
