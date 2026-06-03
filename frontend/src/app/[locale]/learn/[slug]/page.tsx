import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { allSlugs, getArticle } from "@/content/learn/articles";
import { buildArticleMetadata } from "@/lib/gtmMetadata";

type PageProps = {
  params: Promise<{ locale: string; slug: string }>;
};

export async function generateStaticParams() {
  const locales = ["ar", "en"];
  return locales.flatMap((locale) => allSlugs().map((slug) => ({ locale, slug })));
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale, slug } = await params;
  const article = getArticle(slug);
  if (!article) return { title: "Dealix Learn" };
  return buildArticleMetadata(locale, article.titleAr, article.titleEn, article.descriptionAr, article.descriptionEn, slug);
}

export default async function LearnArticlePage({ params }: PageProps) {
  const { locale, slug } = await params;
  const article = getArticle(slug);
  if (!article) notFound();

  const isAr = locale === "ar";
  const base = `/${locale}`;
  const sections = isAr ? article.sections.ar : article.sections.en;
  const allArticles = (await import("@/content/learn/articles")).LEARN_ARTICLES;
  const otherArticles = allArticles.filter((a) => a.slug !== slug).slice(0, 3);

  return (
    <div className="min-h-screen bg-background" dir={isAr ? "rtl" : "ltr"}>

      {/* Top nav */}
      <header className="border-b border-border/60 sticky top-0 bg-background/95 backdrop-blur z-10">
        <div className="mx-auto max-w-3xl px-6 py-3 flex items-center justify-between text-sm">
          <div className="flex gap-4">
            <Link href={base} className="text-muted-foreground hover:text-foreground transition-colors">
              {isAr ? "← الرئيسية" : "← Home"}
            </Link>
            <Link href={`${base}/learn`} className="text-muted-foreground hover:text-foreground transition-colors">
              {isAr ? "المكتبة" : "Library"}
            </Link>
          </div>
          <Link href={`${base}/dealix-diagnostic`} className="rounded-lg bg-primary text-primary-foreground px-3 py-1.5 text-xs font-medium hover:bg-primary/90 transition-colors">
            {isAr ? "ابدأ التشخيص" : "Start Diagnostic"}
          </Link>
        </div>
      </header>

      <article className={`mx-auto max-w-3xl px-6 py-12 ${isAr ? "text-right" : "text-left"}`}>

        {/* Article header */}
        <header className="mb-10">
          {article.readTimeMinAr && (
            <p className="text-xs text-muted-foreground mb-3">
              ⏱ {isAr ? article.readTimeMinAr : article.readTimeMinEn}
            </p>
          )}
          <h1 className="text-3xl font-bold leading-tight md:text-4xl">
            {isAr ? article.titleAr : article.titleEn}
          </h1>
          <p className="mt-4 text-lg text-muted-foreground leading-relaxed">
            {isAr ? article.descriptionAr : article.descriptionEn}
          </p>

          {/* Divider */}
          <div className="mt-6 h-px bg-gradient-to-r from-transparent via-border to-transparent" />
        </header>

        {/* Article content */}
        <div className="space-y-10">
          {sections.map((s, i) => (
            <section key={s.heading}>
              <h2 className="text-xl font-semibold mb-3 flex items-baseline gap-2">
                <span className="text-xs text-muted-foreground font-normal">{isAr ? `${toArabicNumeral(i + 1)}.` : `${i + 1}.`}</span>
                {s.heading}
              </h2>
              <p className="text-muted-foreground leading-relaxed text-base">{s.body}</p>
            </section>
          ))}
        </div>

        {/* CTA block */}
        <div className="mt-14 rounded-2xl bg-gradient-to-br from-[#001F3F] to-[#0a2040] text-white p-8">
          <h2 className="text-2xl font-bold">
            {isAr ? "جاهز للتطبيق؟" : "Ready to apply this?"}
          </h2>
          <p className="mt-2 text-white/70">
            {isAr
              ? "ابدأ بـ Risk Score مجاني أو تشخيص 7 أيام كامل."
              : "Start with a free Risk Score or a full 7-day diagnostic."}
          </p>
          <div className="mt-5 flex flex-wrap gap-3">
            <Link href={`${base}/risk-score`} className="inline-flex items-center gap-2 rounded-lg bg-amber-500 text-white px-5 py-2.5 text-sm font-semibold hover:bg-amber-600 transition-colors">
              {isAr ? "Risk Score مجاني" : "Free Risk Score"}
            </Link>
            <Link href={`${base}/proof-pack`} className="inline-flex items-center gap-2 rounded-lg bg-white/10 border border-white/20 text-white px-5 py-2.5 text-sm font-semibold hover:bg-white/20 transition-colors">
              {isAr ? "عيّنة Proof Pack" : "Proof Pack Sample"}
            </Link>
            <Link href={`${base}/dealix-diagnostic`} className="inline-flex items-center gap-2 rounded-lg bg-white/10 border border-white/20 text-white px-5 py-2.5 text-sm font-semibold hover:bg-white/20 transition-colors">
              {isAr ? "تشخيص 7 أيام" : "7-Day Diagnostic"}
            </Link>
          </div>
        </div>

        {/* More articles */}
        {otherArticles.length > 0 && (
          <div className="mt-12">
            <h2 className="text-lg font-semibold mb-4">
              {isAr ? "مقالات ذات صلة" : "Related Articles"}
            </h2>
            <div className="grid gap-3 sm:grid-cols-3">
              {otherArticles.map((a) => (
                <Link
                  key={a.slug}
                  href={`${base}/learn/${a.slug}`}
                  className="rounded-xl border border-border/50 bg-card/50 p-4 hover:border-border hover:bg-card transition-all"
                >
                  <p className="font-medium text-sm line-clamp-2">{isAr ? a.titleAr : a.titleEn}</p>
                  {a.readTimeMinAr && (
                    <p className="text-xs text-muted-foreground mt-1">
                      {isAr ? a.readTimeMinAr : a.readTimeMinEn}
                    </p>
                  )}
                </Link>
              ))}
            </div>
          </div>
        )}

      </article>
    </div>
  );
}

function toArabicNumeral(n: number): string {
  return n.toString().replace(/\d/g, (d) => "٠١٢٣٤٥٦٧٨٩"[parseInt(d)]);
}
