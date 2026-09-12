import { TrackedLink } from "@/components/analytics/TrackedLink";

export const metadata = {
  title: "AI Governance Readiness Saudi Arabia | Dealix",
  description: "Free evidence-led diagnostic for Saudi AI governance, AI provider accreditation readiness, controls, ownership and proof packs.",
};

const checks = [
  "هل الجهة والمنتج/الخدمة المراد تقييمها محددان بوضوح؟",
  "هل يوجد AI owner مسؤول عن المتطلبات والقرارات؟",
  "هل data flows وmodel/provider inventory وaccess boundaries موثقة؟",
  "هل approval gates والhuman oversight والincident path قابلة للإثبات؟",
  "هل الملفات والأدلة المطلوبة منظمة في proof pack يمكن مراجعته؟",
];

export default function AiGovernanceReadinessPage() {
  return (
    <main className="dx-corporate-page">
      <section className="card dot-pattern" style={{ textAlign: "center" }}>
        <p className="eyebrow">FREE · AI GOVERNANCE READINESS</p>
        <h1>حوكمة AI تبدأ من evidence وownership — لا من claims.</h1>
        <p style={{ maxWidth: 860, margin: "0 auto" }}>
          منصة حوكمة البيانات الوطنية لدى SDAIA تعرض مسار اعتماد مقدمي خدمات الذكاء الاصطناعي
          الذي يتضمن تسجيل الجهة، تعيين مسؤول للذكاء الاصطناعي، استكمال الاستبيان وإرفاق الملفات
          المطلوبة قبل مراجعة الطلب. Dealix يساعدك في readiness، evidence architecture وoperating
          controls؛ الاعتماد نفسه يبقى بيد الجهة المختصة.
        </p>
        <div className="actions" style={{ justifyContent: "center" }}>
          <TrackedLink href="/book" ctaId="ai_governance_free_diagnostic" surface="ai_governance">ابدأ التشخيص المجاني</TrackedLink>
          <a href="https://dgp.sdaia.gov.sa/wps/portal/pdp/services/aiserviceprovideraccreditation" target="_blank" rel="noreferrer">المصدر الرسمي — SDAIA ↗</a>
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
        <p className="eyebrow">DELIVERABLES</p>
        <h2>من الوثائق المتفرقة إلى governance operating pack</h2>
        <ul>
          <li>AI system/provider inventory وdata-flow map.</li>
          <li>Ownership وapproval matrix مع material-action boundaries.</li>
          <li>Evidence gap register وخطة إغلاق مرتبة حسب المخاطر.</li>
          <li>Readiness pack قابل للمراجعة، مع فصل واضح بين self-assessment وبين أي اعتماد رسمي.</li>
        </ul>
      </section>

      <section className="card card-gold">
        <p className="eyebrow">TRUTH BOUNDARY</p>
        <h2>Readiness ≠ Accreditation.</h2>
        <p>
          Dealix لا تمنح اعتماد SDAIA ولا badge تنظيميًا، ولا تدّعي compliance غير مثبت. مهمتنا هي
          تنظيم الأدلة، الضوابط، المسؤوليات ومسار التنفيذ بحيث تعرف الشركة ما هو مثبت وما يزال gap.
        </p>
        <TrackedLink href="/book" ctaId="ai_governance_bottom_diagnostic" surface="ai_governance">ابدأ من نظام AI واحد</TrackedLink>
      </section>
    </main>
  );
}
