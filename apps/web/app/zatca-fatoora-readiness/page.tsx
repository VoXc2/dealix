import { TrackedLink } from "@/components/analytics/TrackedLink";

export const metadata = {
  title: "ZATCA Fatoora Readiness | Dealix",
  description: "Free Saudi B2B diagnostic for Fatoora integration readiness, workflow gaps, evidence, owners and execution planning.",
};

const checks = [
  "هل تم إشعار المنشأة ضمن موجة الربط والتكامل؟",
  "هل نظام الفوترة الحالي قادر على التكامل مع Fatoora ومتطلبات المرحلة الثانية؟",
  "هل owners بين Finance وERP/IT وOperations واضحون؟",
  "هل توجد بيئة اختبار، mapping للحقول، ومعالجة واضحة للأخطاء والاستثناءات؟",
  "هل توجد receipts وevidence تثبت الجاهزية بدل الاعتماد على الانطباع؟",
];

export default function ZatcaFatooraReadinessPage() {
  return (
    <main className="dx-corporate-page">
      <section className="card dot-pattern" style={{ textAlign: "center" }}>
        <p className="eyebrow">FREE · SAUDI EXECUTION DIAGNOSTIC</p>
        <h1>ZATCA / Fatoora Integration Readiness</h1>
        <p style={{ maxWidth: 860, margin: "0 auto" }}>
          في 24 يوليو 2026 أعلنت زاتكا أن المجموعة الخامسة والعشرين تشمل المنشآت التي تجاوزت
          إيراداتها الخاضعة لضريبة القيمة المضافة 187,500 ريال في أي من 2022–2025، مع موعد
          ربط وتكامل للمستهدفين لا يتجاوز 1 فبراير 2027. Dealix يحوّل الإشارة التنظيمية إلى
          readiness map وowners وevidence وخطة تنفيذ — وليس إلى ادعاء امتثال.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <TrackedLink href="/book" ctaId="zatca_free_diagnostic" surface="zatca_readiness">ابدأ التشخيص المجاني</TrackedLink>
          <a href="https://zatca.gov.sa/ar/MediaCenter/News/Pages/Wave25-E-invoicing.aspx" target="_blank" rel="noreferrer">المصدر الرسمي — ZATCA ↗</a>
        </div>
      </section>

      <section className="card">
        <p className="eyebrow">READINESS MAP</p>
        <h2>ما الذي نفحصه؟</h2>
        <div className="cards">
          {checks.map((item) => <article className="card" key={item}><p>{item}</p></article>)}
        </div>
      </section>

      <section className="card">
        <p className="eyebrow">OUTPUT</p>
        <h2>مخرجات قابلة للتنفيذ قبل أي عرض مدفوع</h2>
        <ul>
          <li>Evidence-backed gap map للفوترة والتكامل والـowners.</li>
          <li>قائمة مخاطر واعتماديات واختبارات acceptance ذات أولوية.</li>
          <li>أصغر implementation path مناسب للـERP أو المزود الحالي بدل استبدال stack بلا داعٍ.</li>
          <li>Customer-specific scope فقط بعد Qualified Discovery؛ لا يوجد سعر عام ثابت.</li>
        </ul>
      </section>

      <section className="card card-gold">
        <p className="eyebrow">TRUTH BOUNDARY</p>
        <h2>Dealix ليست جهة ضريبية ولا جهة اعتماد.</h2>
        <p>
          هذا المسار تشخيص جاهزية وتنفيذ تقني/تشغيلي. إشعار زاتكا الخاص بالمنشأة والمتطلبات الرسمية
          هما المرجع؛ Dealix لا تصدر حكمًا ضريبيًا ولا شهادة امتثال ولا ترفع readiness إلى compliance
          أو Customer Proof بدون دليل وقبول مناسب.
        </p>
        <TrackedLink href="/book" ctaId="zatca_bottom_diagnostic" surface="zatca_readiness">ابدأ من مشكلة التكامل الحالية</TrackedLink>
      </section>
    </main>
  );
}
