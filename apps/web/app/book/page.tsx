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
        <p className="eyebrow">Execution Diagnostic</p>
        <h1 style={{ maxWidth: 860 }}>ابدأ بحالة تنفيذ واحدة قابلة للقياس والإثبات</h1>
        <p style={{ maxWidth: 720, fontSize: "1.15rem", lineHeight: 1.7 }}>
          نراجع workflow أو قرارًا تشغيليًا واحدًا ونحدد الإشارة، صاحب القرار، baseline، حدود البيانات،
          وما إذا كان يمكن تحويله إلى تنفيذ محكوم ونتيجة قابلة للإثبات. لا Checkout ولا التزام شراء.
        </p>

        <div className="divider-gold" />

        <h3>ماذا نحتاج منك؟</h3>
        <ul style={{ maxWidth: 720 }}>
          <li>الـworkflow أو القرار الذي تريد تحسينه الآن، بصياغة عملية وليست عامة.</li>
          <li>من يملك القرار والمتابعة داخل الشركة.</li>
          <li>ما البيانات أو الأدوات التي تعتمدون عليها اليوم.</li>
          <li>كيف تعرفون أن الوضع تحسن: وقت، conversion، cash، جودة، سرعة قرار أو KPI آخر.</li>
        </ul>

        <h3>ماذا يحدث بعده؟</h3>
        <ul style={{ maxWidth: 720 }}>
          <li>إذا لم توجد حالة تنفيذ مناسبة لـDealix، نتوقف بدون التزام.</li>
          <li>إذا كانت مناسبة، ننتقل إلى Qualified Discovery لتثبيت baseline والنطاق ومعايير الإثبات.</li>
          <li>لا يصدر سعر إلا في Customer-Specific Quote بعد Discovery.</li>
          <li>إذا اتفقنا على التنفيذ، يبدأ Outcome Sprint بعد قبول النطاق واستيفاء شروط البدء والدفع المناسبة.</li>
          <li>بعد Proof Review فقط نقرر Stop / Redesign / Expand إلى Dealix Runtime.</li>
        </ul>

        <h3>لمن هذا المسار؟</h3>
        <ul style={{ maxWidth: 720 }}>
          <li>شركات تعمل في السعودية ولديها workflow اقتصادي أو تشغيلي واضح وصاحب قرار معروف.</li>
          <li>فرق لديها AI وCRM/ERP/Email/WhatsApp وأدوات متعددة لكن القرار والتنفيذ والإثبات غير مترابطة.</li>
          <li>شركات تقبل human approvals وتستطيع توفير بيانات مشروعة وقابلة للقياس.</li>
        </ul>

        <h3>لمن ليس هذا المسار؟</h3>
        <ul style={{ maxWidth: 720 }}>
          <li>من يريد ضمان عائد أو نتيجة مالية أو مدة ثابتة قبل فهم النطاق.</li>
          <li>من يريد mass outreach أو cold WhatsApp أو صلاحيات خارجية بلا حوكمة.</li>
          <li>من لا يستطيع تحديد owner أو baseline أو طريق واضح للإثبات.</li>
        </ul>

        <CTA
          href="mailto:founder@dealix.sa?subject=طلب%20Execution%20Diagnostic"
          label="اطلب Execution Diagnostic عبر البريد"
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
