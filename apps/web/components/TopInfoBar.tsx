import Link from "next/link";

// Slim premium explanation strip above navigation.
// Static strip (no scrolling, no animation of the strip itself) — zero CLS,
// minimal vertical footprint.
// AR-first inline bilingual: Arabic primary, English secondary on desktop.
export default function TopInfoBar() {
  return (
    <div className="bg-[#001F3F] text-white text-[11px] sm:text-xs leading-none border-b border-white/10">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 min-h-[32px] py-2 flex items-center justify-between gap-3">
        <p className="truncate font-medium tracking-wide">
          <span className="font-semibold">Dealix — نظام تشغيل أعمال بالذكاء الاصطناعي للشركات في السعودية</span>
          <span className="opacity-70 hidden md:inline"> · من الإشارة إلى التنفيذ والنتائج الموثقة</span>
          <span className="opacity-50 hidden lg:inline" dir="ltr"> · Saudi-first AI Business Operating System — from signal to governed execution and verified outcomes</span>
        </p>
        <Link
          href="/book"
          className="hidden sm:inline-flex flex-shrink-0 items-center gap-1.5 rounded-full bg-[#06B6D4] px-3 py-1 font-semibold text-[#001F3F] hover:bg-[#22D3EE] transition-colors"
        >
          <span className="w-1.5 h-1.5 rounded-full bg-[#001F3F] animate-pulse" aria-hidden="true" />
          تشخيص مجاني · Free Diagnostic
        </Link>
      </div>
    </div>
  );
}
