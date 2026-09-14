import Link from "next/link";

export default function LocaleNotFound() {
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center px-6 text-center py-16">
      <p className="text-sm font-semibold tracking-widest uppercase text-[var(--dealix-gold)] mb-3">404 — Not Found</p>
      <h1 className="text-3xl font-bold mb-3">الصفحة غير موجودة — Page not found</h1>
      <p className="text-muted-foreground max-w-md mb-8">الرابط قد يكون معطوباً أو الصفحة انتقلت. / The link may be broken or the page has moved.</p>
      <div className="flex flex-wrap gap-3 justify-center">
        <Link href="/ar" className="px-6 py-3 rounded-xl bg-[var(--dealix-navy)] text-white font-semibold hover:bg-[#000a1e] transition-colors">
          الرئيسية — Home
        </Link>
        <Link href="/ar/dealix-diagnostic" className="px-6 py-3 rounded-xl border border-border hover:bg-muted transition-colors">
          التشخيص المجاني
        </Link>
      </div>
    </div>
  );
}
