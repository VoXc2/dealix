import Link from "next/link";

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6 text-center bg-[#001F3F] text-white">
      <p className="text-sm font-semibold tracking-widest uppercase text-cyan-400 mb-3">404 — Not Found</p>
      <h1 className="text-4xl font-bold mb-3">الصفحة غير موجودة</h1>
      <p className="text-white/60 max-w-md mb-8">
        Page not found. The link may be broken or the page has moved. / الرابط قد يكون معطوباً أو الصفحة انتقلت.
      </p>
      <div className="flex flex-wrap gap-3 justify-center">
        <Link href="/ar" className="px-6 py-3 rounded-xl bg-cyan-500 text-navy-500 font-bold hover:bg-cyan-400 transition-colors">
          الرئيسية — Home
        </Link>
        <Link href="/ar/dealix-diagnostic" className="px-6 py-3 rounded-xl border border-white/20 text-white hover:bg-white/10 transition-colors">
          التشخيص المجاني — Free Diagnostic
        </Link>
      </div>
    </div>
  );
}
