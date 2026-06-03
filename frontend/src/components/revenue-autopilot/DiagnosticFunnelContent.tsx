"use client";

import Link from "next/link";
import { useState } from "react";
import { useTranslations } from "next-intl";
import { motion } from "framer-motion";
import { ArrowRight, CheckCircle2, Shield, Sparkles } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { cn } from "@/lib/utils";
import api from "@/lib/api";

interface Props {
  locale: string;
  title: string;
}

export function DiagnosticFunnelContent({ locale, title }: Props) {
  const tn = useTranslations("diagnosticPage");
  const isRTL = locale === "ar";

  const [riskPayload, setRiskPayload] = useState({
    role: "",
    company: "",
    country: locale === "ar" ? "Saudi Arabia" : "",
    ai_usage: "",
    budget_range: "",
    urgency: "",
    pain: "",
    notes: "",
    source: "dealix_diagnostic",
  });
  const [riskResult, setRiskResult] = useState<Record<string, unknown> | null>(null);
  const [leadForm, setLeadForm] = useState({
    name: "",
    email: "",
    phone: "",
    company: "",
    role: "",
    pain: "",
    consent_proof_pack: true,
    consent_marketing: false,
  });
  const [leadNotice, setLeadNotice] = useState("");
  const [chatQ, setChatQ] = useState("");
  const [chatAnswer, setChatAnswer] = useState<Record<string, unknown> | null>(null);

  async function computeRiskScore() {
    const res = await api.postPublicRiskScore(riskPayload);
    setRiskResult(res.data as Record<string, unknown>);
  }

  async function submitLead() {
    setLeadNotice("");
    const body = {
      ...leadForm,
      country: riskPayload.country,
      ai_usage: riskPayload.ai_usage,
      budget_range: riskPayload.budget_range,
      urgency: riskPayload.urgency,
      source: riskPayload.source,
    };
    const res = await api.postPublicLead(body);
    const data = res.data as Record<string, unknown>;
    setLeadNotice(
      `${locale === "ar" ? "تم الإنشاء" : "Captured"} • ${data.lead_id}`,
    );
  }

  async function fetchKbAnswer() {
    const res = await api.getPublicKnowledgeAnswer(chatQ);
    setChatAnswer(res.data as Record<string, unknown>);
  }

  return (
    <div className="relative overflow-hidden grid-pattern">
      <header className="border-b border-border/70 bg-sidebar/70 backdrop-blur-md">
        <div className="mx-auto flex max-w-5xl flex-col gap-4 px-6 py-4 md:flex-row md:items-center md:justify-between">
          <div
            className={cn(
              "flex flex-col gap-2",
              isRTL ? "items-end text-right" : "items-start text-left",
            )}
          >
            <div className="flex flex-wrap items-center gap-2">
              <Badge variant="outline" className="border-gold-500 text-gold-300">
                {title}
              </Badge>
              <Sparkles className="h-4 w-4 text-gold-400" aria-hidden />
            </div>
            <p className="font-display text-2xl font-bold text-foreground md:text-3xl">{tn("subtitle")}</p>
          </div>
          <Link href={`/${locale}/dashboard`}
            className="inline-flex items-center gap-2 text-xs text-muted-foreground underline-offset-2 hover:text-gold-400"
          >
            {locale === "ar" ? "العودة للوحة التشغيل" : "Return to cockpit"}
          </Link>
        </div>
      </header>

      <section className="mx-auto max-w-5xl space-y-6 px-6 pt-12">
        <motion.div initial={{ opacity: 0.85, y: 8 }} animate={{ opacity: 1, y: 0 }} className="space-y-5">
          <p className="text-lg leading-relaxed text-muted-foreground md:text-xl">{tn("heroLine")}</p>
          <p className="text-sm leading-relaxed text-muted-foreground/90 md:text-base">{tn("heroSub")}</p>
          <div className="flex flex-col gap-3 pt-4 sm:flex-row">
            <Button
              size="lg"
              className="bg-gradient-to-br from-gold-500 to-amber-600 font-semibold text-black"
              asChild
            >
              <a href="#lead-form">{tn("ctaProofPack")}</a>
            </Button>
            <Button variant="outline" size="lg" className="border-gold-500 text-gold-300" asChild>
              <Link href={`/${locale}/ops/founder`}>
                {tn("ctaBook")}
                <ArrowRight className={cn("h-4 w-4", isRTL ? "mr-2 rotate-180" : "ml-2")} aria-hidden />
              </Link>
            </Button>
          </div>
          <p className="flex gap-2 pt-4 text-xs text-muted-foreground">
            <Shield className="mt-1 h-4 w-4 shrink-0 text-emerald-400" aria-hidden />
            <span>{tn("sections.noAutoSendNotice")}</span>
          </p>
        </motion.div>
      </section>

      <section className="mx-auto mt-14 grid max-w-5xl gap-4 px-6 md:grid-cols-3">
        {[
          { title: tn("sections.problemTitle"), body: tn("sections.problemBody") },
          { title: tn("sections.forTitle"), body: tn("sections.forBody") },
          { title: tn("sections.getTitle"), body: tn("sections.getBullets") },
        ].map((block) => (
          <Card key={block.title} className="bg-card border-border">
            <CardHeader>
              <CardTitle className="text-base">{block.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm leading-relaxed text-muted-foreground">{block.body}</p>
            </CardContent>
          </Card>
        ))}
      </section>

      <section className="mx-auto mt-12 grid max-w-5xl items-start gap-6 px-6 lg:grid-cols-2">
        <Card id="risk-score-panel" className="border-border/80 bg-card">
          <CardHeader>
            <CardTitle>{tn("riskScoreTitle")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-xs text-muted-foreground">{tn("riskScoreHint")}</p>
            <div className="grid gap-3">
              <div className="space-y-2">
                <Label htmlFor="role">{locale === "ar" ? "الدور" : "Role"}</Label>
                <Input
                  id="role"
                  value={riskPayload.role}
                  onChange={(e) => setRiskPayload((p) => ({ ...p, role: e.target.value }))}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="country">{locale === "ar" ? "الدولة" : "Country"}</Label>
                <Input
                  id="country"
                  value={riskPayload.country}
                  onChange={(e) => setRiskPayload((p) => ({ ...p, country: e.target.value }))}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="pain">{locale === "ar" ? "السياق" : "Pain / context"}</Label>
                <textarea
                  id="pain"
                  className={cn(
                    "min-h-[88px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm",
                    isRTL ? "text-right" : "text-left",
                  )}
                  value={riskPayload.pain}
                  onChange={(e) => setRiskPayload((p) => ({ ...p, pain: e.target.value }))}
                />
              </div>
            </div>
            <Button
              variant="outline"
              onClick={() => void computeRiskScore()}
              className="border-gold-500 text-gold-300"
            >
              {locale === "ar" ? "احسب المؤشر" : "Compute score"}
            </Button>
            {riskResult?.score !== undefined ? (
              <div className="space-y-1 rounded-lg border border-gold-500/30 bg-gold-500/5 p-4 text-xs">
                <p className="font-semibold text-gold-200">{String(riskResult.score)} pts</p>
                <pre
                  className={cn(
                    "whitespace-pre-wrap break-all font-mono",
                    isRTL ? "text-right" : "",
                  )}
                >
                  {JSON.stringify(riskResult.breakdown as object, null, 2)}
                </pre>
              </div>
            ) : null}
          </CardContent>
        </Card>

        <Card id="lead-form" className="bg-card border-border">
          <CardHeader>
            <CardTitle>{tn("leadFormTitle")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-3">
              <div className="space-y-2">
                <Label htmlFor="lname">{locale === "ar" ? "الاسم" : "Name"}</Label>
                <Input
                  id="lname"
                  value={leadForm.name}
                  onChange={(e) => setLeadForm((p) => ({ ...p, name: e.target.value }))}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="lemail">{locale === "ar" ? "البريد" : "Email"}</Label>
                <Input
                  id="lemail"
                  type="email"
                  value={leadForm.email}
                  onChange={(e) => setLeadForm((p) => ({ ...p, email: e.target.value }))}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="lcompany">{locale === "ar" ? "الشركة" : "Company"}</Label>
                <Input
                  id="lcompany"
                  value={leadForm.company}
                  onChange={(e) => setLeadForm((p) => ({ ...p, company: e.target.value }))}
                />
              </div>
              <textarea
                className={cn(
                  "min-h-[100px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm",
                  isRTL ? "text-right" : "text-left",
                )}
                placeholder={locale === "ar" ? "ما الذي تعالجه؟" : "What do you need to unblock?"}
                value={leadForm.pain}
                onChange={(e) => setLeadForm((p) => ({ ...p, pain: e.target.value }))}
              />
            </div>
            <label className="flex cursor-pointer select-none gap-3 text-xs">
              <input
                type="checkbox"
                checked={leadForm.consent_proof_pack}
                onChange={(e) => setLeadForm((p) => ({ ...p, consent_proof_pack: e.target.checked }))}
              />
              <span>
                {locale === "ar"
                  ? "موافقتي لتسليم الهيكل التجريبي داخل المنظومة"
                  : "Consent to deliver proof scaffolding internally"}
              </span>
            </label>
            <Button
              onClick={() => void submitLead()}
              className="bg-gold-500 text-black hover:bg-gold-600"
            >
              {tn("leadFormSubmit")}
            </Button>
            {leadNotice ? <p className="text-xs text-emerald-300">{leadNotice}</p> : null}
          </CardContent>
        </Card>
      </section>

      <section className="mx-auto mt-14 grid max-w-5xl gap-4 px-6 lg:grid-cols-3">
        <Card className="border-border bg-card lg:col-span-2">
          <CardHeader>
            <CardTitle>{tn("proofPreviewTitle")}</CardTitle>
          </CardHeader>
          <CardContent className="text-sm leading-relaxed text-muted-foreground">
            {tn("proofPreviewBody")}
          </CardContent>
        </Card>

        <Card className="border-border bg-card">
          <CardHeader>
            <CardTitle>{tn("sections.pricingTitle")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {[4999, 9999, 15000].map((amt) => (
              <div
                key={amt}
                className="flex gap-3 rounded-lg border border-white/10 px-4 py-2 text-sm"
              >
                <CheckCircle2 className="mt-1 h-5 w-5 text-gold-400 shrink-0" aria-hidden />
                <div>
                  <p className="font-semibold">SAR {amt.toLocaleString()}</p>
                  <p className="text-xs text-muted-foreground">
                    {locale === "ar" ? "مضبوطة بعد المراجعة" : "Finalized post discovery"}
                  </p>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </section>

      <section className="mx-auto mt-14 max-w-5xl px-6">
        <Card className="bg-card border-border">
          <CardHeader>
            <CardTitle>{tn("chatTitle")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <textarea
              className={cn(
                "min-h-[90px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm",
                isRTL ? "text-right" : "text-left",
              )}
              placeholder={tn("chatPlaceholder")}
              value={chatQ}
              onChange={(e) => setChatQ(e.target.value)}
            />
            <Button variant="secondary" size="sm" onClick={() => void fetchKbAnswer()}>
              {tn("chatAsk")}
            </Button>
            {chatAnswer?.answer_ar ? (
              <div className="space-y-3 rounded-xl border border-gold-500/20 bg-gold-500/5 px-4 py-3 text-sm">
                <Badge variant="outline" className="text-xs capitalize">
                  {String(chatAnswer.risk_level ?? "")}
                </Badge>
                <p className="whitespace-pre-wrap leading-relaxed text-muted-foreground">
                  {(locale === "ar" ? chatAnswer.answer_ar : chatAnswer.answer_en ?? chatAnswer.answer_ar) as string}
                </p>
              </div>
            ) : null}
          </CardContent>
        </Card>
      </section>

      <section className="mx-auto mt-12 max-w-5xl px-6">
        <Card className="border-destructive/30 bg-card">
          <CardHeader>
            <CardTitle>{tn("sections.trustTitle")}</CardTitle>
          </CardHeader>
          <CardContent className="text-sm leading-relaxed text-muted-foreground whitespace-pre-wrap">
            {tn("sections.trustBullets")}
          </CardContent>
        </Card>
      </section>

      <section className="mx-auto mt-12 max-w-5xl px-6 pb-24">
        <Card className="bg-card border-border">
          <CardHeader>
            <CardTitle>{tn("sections.faqTitle")}</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6 text-sm text-muted-foreground">
            <div key="faqOutbound" className={cn(isRTL ? "text-right" : "")}>
              <p className="mb-2 font-semibold text-foreground">{tn("faqOutboundQ")}</p>
              <p>{tn("faqOutboundA")}</p>
            </div>
            <div key="faqCompliance" className={cn(isRTL ? "text-right" : "")}>
              <p className="mb-2 font-semibold text-foreground">{tn("faqComplianceQ")}</p>
              <p>{tn("faqComplianceA")}</p>
            </div>
            <div key="faqKickoff" className={cn(isRTL ? "text-right" : "")}>
              <p className="mb-2 font-semibold text-foreground">{tn("faqKickoffQ")}</p>
              <p>{tn("faqKickoffA")}</p>
            </div>
          </CardContent>
        </Card>
      </section>
    </div>
  );
}
