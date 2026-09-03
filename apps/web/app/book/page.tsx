"use client";

import PageShell from "@/components/PageShell";
import CTA from "@/components/CTA";

export default function BookPage() {
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
        <p className="eyebrow">Free Mini Diagnostic</p>
        <h1 style={{ maxWidth: 860 }}>ابدأ بتشخيص مشكلة تشغيلية واحدة — مجانًا</h1>
        <p style={{ maxWidth: 720, fontSize: "1.15rem", lineHeight: 1.7 }}>
          نراجع مشكلة واحدة تؤثر على الإيراد أو المتابعة أو القرار اليومي، ونحدد هل تستحق Discovery أعمق.
          لا بطاقة، لا Checkout، ولا التزام بشراء Pilot.
        </p>

        <div className="divider-gold" />

        <h3>ماذا نحتاج منك؟</h3>
        <ul style={{ maxWidth: 720 }}>
          <li>المشكلة التي تريد حلها الآن، بصياغة عملية وليست عامة.</li>
          <li>من يملك القرار والمتابعة داخل الشركة.</li>
          <li>ما البيانات أو الأدوات التي تعتمدون عليها اليوم.</li>
          <li>كيف تعرفون أن المشكلة تحسنت: وقت، conversion، متابعة، cash أو KPI آخر.</li>
        </ul>

        <h3>ماذا يحدث بعده؟</h3>
        <ul style={{ maxWidth: 720 }}>
          <li>إذا لم تكن المشكلة مناسبة لـDealix، نتوقف بدون التزام.</li>
          <li>إذا كانت مؤهلة، ننتقل إلى Qualified Discovery لتثبيت baseline والنطاق.</li>
          <li>لا يصدر سعر إلا في Customer-Specific Quote بعد Discovery.</li>
          <li>الـRevenue Command Pilot مدته 30 يومًا ويبدأ فقط بعد قبول العرض وإثبات الدفع.</li>
        </ul>

        <h3>لمن هذا المسار؟</h3>
        <ul style={{ maxWidth: 720 }}>
          <li>شركات B2B في السعودية لديها ألم تشغيلي واضح وصاحب قرار معروف.</li>
          <li>فرق تحتاج Revenue + Proof + Command بدل إضافة أدوات جديدة.</li>
          <li>شركات تقبل human approvals وتستطيع توفير بيانات مشروعة وقابلة للقياس.</li>
        </ul>

        <h3>لمن ليس هذا المسار؟</h3>
        <ul style={{ maxWidth: 720 }}>
          <li>من يريد ضمان عائد أو نتيجة مالية محددة مسبقًا.</li>
          <li>من يريد mass outreach أو cold WhatsApp أو صلاحيات خارجية بلا حوكمة.</li>
          <li>من لا يستطيع تحديد owner أو baseline أو طريق واضح للإثبات.</li>
        </ul>

        <CTA
          href="mailto:founder@dealix.sa?subject=طلب%20Mini%20Diagnostic%20مجاني"
          label="اطلب Mini Diagnostic عبر البريد"
        />

        <p
          style={{
            fontSize: "0.82rem",
            color: "rgba(255,255,255,0.40)",
            marginTop: "var(--sp-4)",
          }}
        >
          الإرسال عبر البريد هنا هو طلب منك أنت؛ Dealix لا تحول بيانات عامة إلى موافقة تواصل ولا تبدأ مراسلات خارجية تلقائيًا.
        </p>
      </section>
    </PageShell>
  );
}
