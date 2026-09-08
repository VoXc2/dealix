"use client";

import PageShell from "@/components/PageShell";
import CTA from "@/components/CTA";

const founderEmail = process.env.NEXT_PUBLIC_FOUNDER_EMAIL ?? "sami.assiri11@gmail.com";
const whatsappUrl = process.env.NEXT_PUBLIC_WHATSAPP_URL?.trim();

export default function BookPage() {
  const emailHref = `mailto:${founderEmail}?subject=${encodeURIComponent("طلب Free Execution Diagnostic — Dealix")}`;

  return (
    <PageShell>
      <section
        className="card dot-pattern"
        style={{
          position: "relative",
          overflow: "hidden",
          paddingTop: "clamp(40px,6vw,72px)",
          paddingBottom: "clamp(40px,6vw,72px)",
        }}
      >
        <p className="eyebrow">Free Execution Diagnostic</p>
        <h1 style={{ maxWidth: 860 }}>ابدأ بمشكلة تنفيذ واحدة — والتشخيص الأولي علينا</h1>
        <p style={{ maxWidth: 760, fontSize: "1.15rem", lineHeight: 1.7 }}>
          اشرح لنا workflow أو قرارًا تشغيليًا مهمًا. نراجع السياق المتاح، نفصل الحقائق عن الفرضيات،
          ونحدد أين يستحق التدخل وما الذي يجب إثباته قبل أي عرض أو التزام شراء.
        </p>

        <div className="divider-gold" />

        <h3>أرسل لنا أربع نقاط فقط</h3>
        <ul style={{ maxWidth: 760 }}>
          <li>ما الـworkflow أو القرار الذي تريد تحسينه الآن؟</li>
          <li>من يملك القرار والمتابعة داخل الشركة؟</li>
          <li>ما الأدوات أو البيانات التي يعتمد عليها العمل اليوم؟</li>
          <li>كيف تعرف أن الوضع تحسن: وقت، conversion، cash، جودة، سرعة قرار أو KPI آخر؟</li>
        </ul>

        <h3>ماذا تستلم؟</h3>
        <ul style={{ maxWidth: 760 }}>
          <li>Mini Diagnostic أولي يفصل ما نعرفه عمّا نحتاج التحقق منه.</li>
          <li>Problem / execution hypothesis واضحة بدل ادعاء مشكلة غير مثبتة.</li>
          <li>أسئلة تحقق عملية، وأصغر تدخل قابل للقياس إذا كانت الحالة مناسبة.</li>
          <li>إذا لم توجد حالة تنفيذ مناسبة لـDealix، نقول ذلك بوضوح ولا يوجد التزام شراء.</li>
        </ul>

        <h3>إذا كانت الحالة مناسبة</h3>
        <ul style={{ maxWidth: 760 }}>
          <li>Qualified Discovery لتثبيت baseline والنطاق ومعايير الإثبات.</li>
          <li>Customer-Specific Quote فقط بعد فهم الحالة؛ لا أسعار عامة مضللة ولا Checkout مباشر.</li>
          <li>Outcome Sprint محكوم، ثم Proof Review قبل أي توسع إلى Dealix Runtime.</li>
        </ul>

        <div className="actions" style={{ marginTop: "var(--sp-6)", flexWrap: "wrap" }}>
          <CTA href={emailHref} label="اطلب التشخيص المجاني عبر البريد" />
          {whatsappUrl ? (
            <CTA href={whatsappUrl} label="تواصل مع Founder Office على WhatsApp" />
          ) : null}
        </div>

        <p
          style={{
            fontSize: "0.82rem",
            color: "rgba(255,255,255,0.44)",
            marginTop: "var(--sp-4)",
            maxWidth: 760,
          }}
        >
          هذه الصفحة قناة inbound: أنت تبدأ التواصل. Dealix لا تعتبر رقمًا أو بريدًا عامًا موافقة على مراسلات تسويقية،
          ولا تحول Research أو Draft إلى علاقة أو إرسال فعلي بدون أساس مناسب.
        </p>
      </section>
    </PageShell>
  );
}
