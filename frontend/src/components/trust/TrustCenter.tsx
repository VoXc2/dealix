"use client";

import { useState } from "react";
import { useLocale } from "next-intl";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface CertCard {
  id: string;
  labelAr: string;
  labelEn: string;
  statusAr: string;
  statusEn: string;
  badgeVariant: "emerald" | "gold" | "secondary" | "blue";
  descAr: string;
  descEn: string;
  extraAr?: string;
  extraEn?: string;
}

interface PolicyCard {
  id: string;
  titleAr: string;
  titleEn: string;
  bodyAr: string;
  bodyEn: string;
}

interface MetricCard {
  id: string;
  valueAr: string;
  valueEn: string;
  labelAr: string;
  labelEn: string;
  descAr: string;
  descEn: string;
  icon: string;
  color: string;
}

interface TrustBadge {
  labelAr: string;
  labelEn: string;
  icon: string;
}

interface Document {
  id: string;
  titleAr: string;
  titleEn: string;
  sizeLabel: string;
  icon: string;
}

// ---------------------------------------------------------------------------
// Static data
// ---------------------------------------------------------------------------

const CERT_CARDS: CertCard[] = [
  {
    id: "pdpl",
    labelAr: "حماية البيانات الشخصية",
    labelEn: "PDPL",
    statusAr: "ممتثل",
    statusEn: "Compliant",
    badgeVariant: "emerald",
    descAr:
      "مستوفون لمتطلبات نظام حماية البيانات الشخصية الصادر بالمرسوم الملكي. تشمل الامتثال: موافقة المستخدم، حق الحذف، تعيين مسؤول الخصوصية، وإجراءات الإخطار بالاختراق.",
    descEn:
      "Fully aligned with the Personal Data Protection Law issued by Royal Decree. Coverage includes user consent, right-to-erasure, DPO appointment, and breach notification procedures.",
  },
  {
    id: "zatca",
    labelAr: "هيئة الزكاة والضريبة والجمارك",
    labelEn: "ZATCA",
    statusAr: "جاهز للموجة 24",
    statusEn: "Wave 24 Ready",
    badgeVariant: "emerald",
    descAr:
      "النظام مهيأ لمتطلبات الفاتورة الإلكترونية المرحلة الثانية (التكامل). دعم كامل لتنسيق UBL XML ومعيار SHA-256 وواجهات ZATCA API.",
    descEn:
      "System is prepared for Phase 2 (Integration) e-invoicing requirements. Full support for UBL XML format, SHA-256 signing, and ZATCA API endpoints.",
    extraAr: "الموجة التالية: Q3 2026",
    extraEn: "Next wave: Q3 2026",
  },
  {
    id: "nca",
    labelAr: "الهيئة الوطنية للأمن السيبراني",
    labelEn: "NCA",
    statusAr: "قيد المراجعة",
    statusEn: "Under Review",
    badgeVariant: "gold",
    descAr:
      "مراجعة داخلية جارية لمتطلبات الضوابط الأساسية للأمن السيبراني (ECC-1:2018). المرحلة الحالية: تقييم الفجوات وإعداد خطة المعالجة.",
    descEn:
      "Internal review in progress for Essential Cybersecurity Controls (ECC-1:2018) requirements. Current phase: gap assessment and remediation plan preparation.",
  },
  {
    id: "iso",
    labelAr: "ISO 27001",
    labelEn: "ISO 27001",
    statusAr: "مخطط له",
    statusEn: "Planned",
    badgeVariant: "secondary",
    descAr:
      "شهادة إدارة أمن المعلومات مدرجة في خارطة الطريق لعام 2026. التوثيق الأولي لنظام إدارة أمن المعلومات (ISMS) قيد الإعداد.",
    descEn:
      "Information Security Management System certification on the 2026 roadmap. Preliminary ISMS documentation currently being prepared.",
  },
];

const POLICY_CARDS: PolicyCard[] = [
  {
    id: "data-protection",
    titleAr: "سياسة حماية البيانات",
    titleEn: "Data Protection Policy",
    bodyAr:
      "نجمع البيانات الشخصية بموافقة صريحة مسبقة فقط. لا تُستخدم أي بيانات عميل لأغراض التدريب أو التحسين دون إذن كتابي. يتمتع كل عميل بحق الوصول الكامل لبياناته وطلب حذفها في أي وقت. نحتفظ بسجل معالجة البيانات وفق متطلبات النظام. البيانات مشفرة أثناء النقل (TLS 1.3) وفي حالة السكون (AES-256).",
    bodyEn:
      "Personal data is collected only with explicit prior consent. No client data is used for training or improvement purposes without written authorization. Every client has the right to full access to their data and may request deletion at any time. We maintain a data processing register in compliance with regulatory requirements. Data is encrypted in transit (TLS 1.3) and at rest (AES-256).",
  },
  {
    id: "cybersecurity",
    titleAr: "سياسة الأمن السيبراني",
    titleEn: "Cybersecurity Policy",
    bodyAr:
      "تطبيق مبدأ أقل الصلاحيات على جميع الأنظمة والموظفين. مراجعة أمنية ربع سنوية من طرف ثالث مستقل. تدريب إلزامي للفريق على الأمن السيبراني كل ستة أشهر. سياسة استجابة للحوادث محددة بوضوح بإشعار خلال 72 ساعة. لا وصول لبيانات الإنتاج بدون مراجعة ثنائية.",
    bodyEn:
      "Principle of least privilege applied across all systems and staff. Quarterly security review by an independent third party. Mandatory cybersecurity training every six months for all team members. Clearly defined incident response policy with 72-hour notification requirement. No production data access without dual-party review.",
  },
  {
    id: "privacy",
    titleAr: "سياسة الخصوصية",
    titleEn: "Privacy Policy",
    bodyAr:
      "لا نبيع أو نؤجر أو نشارك البيانات الشخصية مع أطراف ثالثة لأغراض تجارية. البيانات التشغيلية محلية بالكامل داخل المملكة العربية السعودية. مدة الاحتفاظ بالبيانات لا تتجاوز ما يحدده العقد أو ما يستلزمه النظام. نوفر سجلاً كاملاً لكل عملية وصول لبيانات العميل عند الطلب.",
    bodyEn:
      "We never sell, rent, or share personal data with third parties for commercial purposes. Operational data is hosted entirely within the Kingdom of Saudi Arabia. Data retention does not exceed what is specified in the contract or required by law. We provide a full audit log of every data access event upon request.",
  },
];

const METRIC_CARDS: MetricCard[] = [
  {
    id: "uptime",
    valueAr: "99.9%",
    valueEn: "99.9%",
    labelAr: "وقت التشغيل",
    labelEn: "Uptime",
    descAr: "على مدار 90 يوماً الماضية",
    descEn: "Over the past 90 days",
    icon: "S",
    color: "text-emerald-500",
  },
  {
    id: "encryption",
    valueAr: "AES-256",
    valueEn: "AES-256",
    labelAr: "تشفير البيانات",
    labelEn: "Data Encryption",
    descAr: "جميع البيانات مشفرة في السكون والنقل",
    descEn: "All data encrypted at rest and in transit",
    icon: "L",
    color: "text-gold-500",
  },
  {
    id: "audit",
    valueAr: "30 يوماً",
    valueEn: "30 Days",
    labelAr: "آخر مراجعة أمنية",
    labelEn: "Last Security Audit",
    descAr: "مراجعة ربع سنوية من طرف مستقل",
    descEn: "Quarterly review by independent third party",
    icon: "A",
    color: "text-blue-400",
  },
  {
    id: "incidents",
    valueAr: "0",
    valueEn: "0",
    labelAr: "حوادث أمنية",
    labelEn: "Security Incidents",
    descAr: "خلال 90 يوماً الماضية",
    descEn: "In the past 90 days",
    icon: "C",
    color: "text-emerald-500",
  },
];

const TRUST_BADGES: TrustBadge[] = [
  { labelAr: "متوافق مع PDPL", labelEn: "PDPL Native", icon: "P" },
  { labelAr: "جاهز لـ ZATCA", labelEn: "ZATCA Ready", icon: "Z" },
  { labelAr: "لا تواصل بارد", labelEn: "No Cold Outreach", icon: "N" },
  { labelAr: "عربي أولاً", labelEn: "Arabic First", icon: "A" },
  { labelAr: "الموافقة أولاً", labelEn: "Approval First", icon: "M" },
  { labelAr: "سعودي الملكية", labelEn: "Saudi Owned", icon: "S" },
];

const DOCUMENTS: Document[] = [
  {
    id: "security-policy",
    titleAr: "سياسة الأمان — PDF",
    titleEn: "Security Policy — PDF",
    sizeLabel: "312 KB",
    icon: "D",
  },
  {
    id: "pdpl-report",
    titleAr: "تقرير امتثال PDPL",
    titleEn: "PDPL Compliance Report",
    sizeLabel: "180 KB",
    icon: "D",
  },
  {
    id: "zatca-cert",
    titleAr: "شهادة جاهزية ZATCA",
    titleEn: "ZATCA Readiness Certificate",
    sizeLabel: "95 KB",
    icon: "D",
  },
];

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

const FADE_UP = {
  hidden: { opacity: 0, y: 20 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, delay: i * 0.08, ease: "easeOut" },
  }),
};

function ShieldIcon({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.5}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    </svg>
  );
}

function LockIcon({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.5}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
      <path d="M7 11V7a5 5 0 0 1 10 0v4" />
    </svg>
  );
}

function ActivityIcon({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.5}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
    </svg>
  );
}

function CheckCircleIcon({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.5}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
      <polyline points="22 4 12 14.01 9 11.01" />
    </svg>
  );
}

function DownloadIcon({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.5}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="7 10 12 15 17 10" />
      <line x1="12" y1="15" x2="12" y2="3" />
    </svg>
  );
}

function FileTextIcon({ className }: { className?: string }) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.5}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      aria-hidden="true"
    >
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="16" y1="13" x2="8" y2="13" />
      <line x1="16" y1="17" x2="8" y2="17" />
      <polyline points="10 9 9 9 8 9" />
    </svg>
  );
}

function MetricIcon({ id }: { id: string }) {
  if (id === "uptime") return <ActivityIcon className="w-6 h-6" />;
  if (id === "encryption") return <LockIcon className="w-6 h-6" />;
  if (id === "audit") return <ShieldIcon className="w-6 h-6" />;
  return <CheckCircleIcon className="w-6 h-6" />;
}

function StatusBadge({
  variant,
  ar,
  en,
  isAr,
}: {
  variant: CertCard["badgeVariant"];
  ar: string;
  en: string;
  isAr: boolean;
}) {
  const text = isAr ? ar : en;
  const icon =
    variant === "emerald"
      ? "+"
      : variant === "gold"
        ? "~"
        : "-";
  const cls =
    variant === "emerald"
      ? "bg-emerald-500/15 text-emerald-400 border border-emerald-500/30"
      : variant === "gold"
        ? "bg-gold-500/15 text-gold-400 border border-gold-500/30"
        : "bg-muted text-muted-foreground border border-border";

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-semibold ${cls}`}
    >
      <span aria-hidden="true">{icon === "+" ? "✓" : icon === "~" ? "~" : "-"}</span>
      {text}
    </span>
  );
}

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------

export function TrustCenter() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [openPolicies, setOpenPolicies] = useState<Record<string, boolean>>({});

  function togglePolicy(id: string) {
    setOpenPolicies((prev) => ({ ...prev, [id]: !prev[id] }));
  }

  return (
    <div
      className="space-y-16"
      dir={isAr ? "rtl" : "ltr"}
    >
      {/* ------------------------------------------------------------------ */}
      {/* Hero header                                                          */}
      {/* ------------------------------------------------------------------ */}
      <motion.header
        initial={{ opacity: 0, y: -16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-[#001F3F] to-[#002f5f] px-8 py-12 text-white shadow-xl"
      >
        <div
          className="pointer-events-none absolute inset-0 opacity-10"
          style={{
            backgroundImage:
              "radial-gradient(circle at 20% 50%, #D4AF37 0%, transparent 60%), radial-gradient(circle at 80% 20%, #10B981 0%, transparent 50%)",
          }}
        />
        <div className="relative z-10 flex flex-col items-start gap-4 sm:flex-row sm:items-center">
          <div className="flex h-16 w-16 flex-shrink-0 items-center justify-center rounded-2xl bg-white/10 ring-1 ring-white/20">
            <ShieldIcon className="h-9 w-9 text-gold-400" />
          </div>
          <div>
            <h1 className="text-3xl font-bold leading-tight font-display">
              {isAr ? "مركز الثقة والامتثال" : "Trust & Compliance Center"}
            </h1>
            <p className="mt-2 max-w-xl text-white/70 text-sm leading-relaxed">
              {isAr
                ? "الشفافية الكاملة في سياسات الأمان والامتثال التنظيمي — لأن الثقة تُبنى بالأدلة لا بالكلام."
                : "Full transparency in security policies and regulatory compliance — because trust is built on evidence, not words."}
            </p>
          </div>
        </div>
        <div className="relative z-10 mt-6 flex flex-wrap gap-2">
          <Badge variant="emerald">
            {isAr ? "PDPL ممتثل" : "PDPL Compliant"}
          </Badge>
          <Badge variant="emerald">
            {isAr ? "ZATCA جاهز" : "ZATCA Ready"}
          </Badge>
          <Badge variant="gold">
            {isAr ? "NCA قيد المراجعة" : "NCA Under Review"}
          </Badge>
        </div>
      </motion.header>

      {/* ------------------------------------------------------------------ */}
      {/* Section 1: Compliance Certifications                                */}
      {/* ------------------------------------------------------------------ */}
      <section>
        <motion.h2
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mb-6 text-xl font-bold"
        >
          {isAr ? "شهادات الامتثال" : "Compliance Certifications"}
        </motion.h2>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {CERT_CARDS.map((cert, i) => (
            <motion.div
              key={cert.id}
              custom={i}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={FADE_UP}
              whileHover={{ y: -4, transition: { duration: 0.2 } }}
            >
              <Card className="h-full border-border/60 bg-card/80 backdrop-blur-sm transition-shadow hover:shadow-md">
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between gap-2">
                    <CardTitle className="text-base leading-snug">
                      {isAr ? cert.labelAr : cert.labelEn}
                    </CardTitle>
                    <StatusBadge
                      variant={cert.badgeVariant}
                      ar={cert.statusAr}
                      en={cert.statusEn}
                      isAr={isAr}
                    />
                  </div>
                </CardHeader>
                <CardContent className="text-sm text-muted-foreground leading-relaxed space-y-2">
                  <p>{isAr ? cert.descAr : cert.descEn}</p>
                  {cert.extraAr && (
                    <p className="text-xs font-medium text-gold-500">
                      {isAr ? cert.extraAr : cert.extraEn}
                    </p>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* Section 2: Security Policies (accordion)                            */}
      {/* ------------------------------------------------------------------ */}
      <section>
        <motion.h2
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mb-6 text-xl font-bold"
        >
          {isAr ? "السياسات الأمنية" : "Security Policies"}
        </motion.h2>
        <div className="space-y-3">
          {POLICY_CARDS.map((policy, i) => {
            const open = openPolicies[policy.id] ?? false;
            return (
              <motion.div
                key={policy.id}
                custom={i}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                variants={FADE_UP}
              >
                <div className="rounded-2xl border border-border/60 bg-card/80 backdrop-blur-sm overflow-hidden">
                  <button
                    type="button"
                    onClick={() => togglePolicy(policy.id)}
                    className="flex w-full items-center justify-between px-6 py-4 text-start transition-colors hover:bg-muted/30"
                    aria-expanded={open}
                  >
                    <span className="font-semibold text-sm">
                      {isAr ? policy.titleAr : policy.titleEn}
                    </span>
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth={2}
                      className={`h-4 w-4 flex-shrink-0 text-muted-foreground transition-transform ${open ? "rotate-180" : ""}`}
                      aria-hidden="true"
                    >
                      <polyline points="6 9 12 15 18 9" />
                    </svg>
                  </button>
                  {open && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                      transition={{ duration: 0.25 }}
                      className="px-6 pb-5"
                    >
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        {isAr ? policy.bodyAr : policy.bodyEn}
                      </p>
                    </motion.div>
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* Section 3: Security Metrics                                         */}
      {/* ------------------------------------------------------------------ */}
      <section>
        <motion.h2
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mb-6 text-xl font-bold"
        >
          {isAr ? "مؤشرات الأمان" : "Security Metrics"}
        </motion.h2>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {METRIC_CARDS.map((m, i) => (
            <motion.div
              key={m.id}
              custom={i}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={FADE_UP}
              whileHover={{ scale: 1.02, transition: { duration: 0.2 } }}
            >
              <Card className="border-border/60 bg-card/80">
                <CardContent className="pt-6">
                  <div className={`mb-3 ${m.color}`}>
                    <MetricIcon id={m.id} />
                  </div>
                  <p className={`text-2xl font-bold ${m.color}`}>
                    {isAr ? m.valueAr : m.valueEn}
                  </p>
                  <p className="mt-1 text-sm font-semibold">
                    {isAr ? m.labelAr : m.labelEn}
                  </p>
                  <p className="mt-1 text-xs text-muted-foreground leading-snug">
                    {isAr ? m.descAr : m.descEn}
                  </p>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* Section 4: Trust Badges Row                                         */}
      {/* ------------------------------------------------------------------ */}
      <section>
        <motion.h2
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mb-4 text-xl font-bold"
        >
          {isAr ? "شارات الثقة" : "Trust Badges"}
        </motion.h2>
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4 }}
          className="flex flex-wrap gap-3"
        >
          {TRUST_BADGES.map((badge) => (
            <div
              key={badge.labelEn}
              className="flex items-center gap-2 rounded-full border border-gold-500/30 bg-gold-500/8 px-4 py-2 text-sm font-semibold text-gold-600 dark:text-gold-400"
            >
              <span className="h-4 w-4 rounded-full bg-gold-500/20 text-center text-[10px] leading-4 font-bold" aria-hidden="true">
                {badge.icon}
              </span>
              {isAr ? badge.labelAr : badge.labelEn}
            </div>
          ))}
        </motion.div>
      </section>

      {/* ------------------------------------------------------------------ */}
      {/* Download Center                                                     */}
      {/* ------------------------------------------------------------------ */}
      <section>
        <motion.h2
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mb-6 text-xl font-bold"
        >
          {isAr ? "مركز التحميل" : "Download Center"}
        </motion.h2>
        <div className="grid gap-4 sm:grid-cols-3">
          {DOCUMENTS.map((doc, i) => (
            <motion.div
              key={doc.id}
              custom={i}
              initial="hidden"
              whileInView="visible"
              viewport={{ once: true }}
              variants={FADE_UP}
            >
              <Card className="border-border/60 bg-card/80 hover:shadow-md transition-shadow">
                <CardContent className="flex items-center gap-4 pt-5 pb-5">
                  <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-xl bg-navy-500/10 text-navy-500 dark:bg-navy-400/10 dark:text-navy-300">
                    <FileTextIcon className="h-5 w-5" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-semibold truncate">
                      {isAr ? doc.titleAr : doc.titleEn}
                    </p>
                    <p className="text-xs text-muted-foreground">{doc.sizeLabel}</p>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    aria-label={isAr ? `تحميل ${doc.titleAr}` : `Download ${doc.titleEn}`}
                    onClick={() => {
                      // Mock download — replace with real presigned URL in production
                      alert(
                        isAr
                          ? `سيتم توفير الملف قريباً: ${doc.titleAr}`
                          : `File coming soon: ${doc.titleEn}`,
                      );
                    }}
                  >
                    <DownloadIcon className="h-4 w-4" />
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
        <p className="mt-3 text-xs text-muted-foreground">
          {isAr
            ? "* هذه وثائق تمثيلية. نسخ الإنتاج النهائية متاحة للعملاء الموقّعين فقط."
            : "* These are representative documents. Final production versions are available to signed clients only."}
        </p>
      </section>
    </div>
  );
}
