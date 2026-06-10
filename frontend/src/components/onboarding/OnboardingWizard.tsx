"use client";

import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ChevronLeft,
  ChevronRight,
  Check,
  Rocket,
  Building2,
  Users,
  Puzzle,
  PartyPopper,
  Loader2,
} from "lucide-react";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import {
  ONBOARDING_STEPS,
  getStepProgress,
  type OnboardingData,
} from "@/lib/onboarding/steps";

const stepIcons = [Rocket, Building2, Users, Puzzle, PartyPopper];

interface OnboardingWizardProps {
  onComplete: (data: Partial<OnboardingData>) => Promise<void>;
  onSkip?: () => void;
  initialData?: Partial<OnboardingData>;
}

export function OnboardingWizard({ onComplete, onSkip, initialData }: OnboardingWizardProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState<Partial<OnboardingData>>(initialData ?? {});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const locale = useLocale();
  const isRTL = locale === "ar";

  const step = ONBOARDING_STEPS[currentStep];
  const progress = getStepProgress(currentStep);

  const handleNext = useCallback(async () => {
    if (step.schema) {
      try {
        const stepData = formData[step.id as keyof OnboardingData] || {};
        step.schema.parse(stepData);
        setErrors({});
      } catch (err: any) {
        const fieldErrors: Record<string, string> = {};
        if (err.errors) {
          err.errors.forEach((e: any) => {
            fieldErrors[e.path.join(".")] = e.message;
          });
        }
        setErrors(fieldErrors);
        return;
      }
    }

    if (currentStep < ONBOARDING_STEPS.length - 1) {
      setCurrentStep((prev) => prev + 1);
    } else {
      setIsSubmitting(true);
      try {
        await onComplete(formData);
      } finally {
        setIsSubmitting(false);
      }
    }
  }, [currentStep, step, formData, onComplete]);

  const handleBack = useCallback(() => {
    if (currentStep > 0) setCurrentStep((prev) => prev - 1);
  }, [currentStep]);

  const updateField = useCallback(
    (field: string, value: unknown) => {
      setFormData((prev) => ({
        ...prev,
        [step.id]: { ...((prev as any)[step.id] || {}), [field]: value },
      }));
      setErrors((prev) => {
        const next = { ...prev };
        delete next[field];
        return next;
      });
    },
    [step.id],
  );

  const StepIcon = stepIcons[currentStep] || Rocket;

  return (
    <div className="mx-auto max-w-2xl">
      {/* Progress */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs text-muted-foreground">
            {isRTL
              ? `الخطوة ${currentStep + 1} من ${ONBOARDING_STEPS.length}`
              : `Step ${currentStep + 1} of ${ONBOARDING_STEPS.length}`}
          </span>
          {step.isSkippable && (
            <button
              onClick={handleNext}
              className="text-xs text-muted-foreground hover:text-foreground transition-colors"
            >
              {isRTL ? "تخطي" : "Skip"}
            </button>
          )}
        </div>
        <Progress value={progress} className="h-2" />
      </div>

      {/* Step indicator dots */}
      <div className="flex items-center justify-center gap-2 mb-8">
        {ONBOARDING_STEPS.map((s, idx) => (
          <button
            key={s.id}
            onClick={() => idx < currentStep && setCurrentStep(idx)}
            disabled={idx > currentStep}
            className={cn(
              "flex h-8 w-8 items-center justify-center rounded-full border text-xs font-medium transition-all",
              idx === currentStep
                ? "border-gold-500 bg-gold-500/10 text-gold-500"
                : idx < currentStep
                  ? "border-emerald-500 bg-emerald-500/10 text-emerald-500 cursor-pointer"
                  : "border-border text-muted-foreground",
            )}
          >
            {idx < currentStep ? (
              <Check className="w-4 h-4" />
            ) : (
              <StepIcon className="w-3.5 h-3.5" />
            )}
          </button>
        ))}
      </div>

      {/* Step content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={step.id}
          initial={{ opacity: 0, x: isRTL ? -20 : 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: isRTL ? 20 : -20 }}
          transition={{ duration: 0.2 }}
          className="rounded-2xl border border-border bg-card p-8"
        >
          <div className="flex flex-col items-center text-center mb-8">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gold-500/10 mb-4">
              <StepIcon className="w-8 h-8 text-gold-500" />
            </div>
            <h2 className="text-2xl font-bold text-foreground mb-2">
              {isRTL ? step.title : step.titleEn}
            </h2>
            <p className="text-sm text-muted-foreground max-w-md">
              {isRTL ? step.description : step.descriptionEn}
            </p>
          </div>

          {/* Welcome step */}
          {step.id === "welcome" && (
            <div className="space-y-4 text-center">
              <p className="text-sm text-muted-foreground">
                {isRTL
                  ? "سنرشدك خلال الإعداد الأولي لمنصة ديليكس"
                  : "We'll guide you through the initial Dealix platform setup"}
              </p>
              <ul className="space-y-2 text-sm text-left max-w-sm mx-auto">
                {[
                  { ar: "إعداد ملف الشركة", en: "Company profile setup" },
                  { ar: "تحديد العميل المثالي", en: "Ideal customer profile" },
                  { ar: "ربط الأدوات والتكاملات", en: "Tool integrations" },
                  { ar: "جاهزية كاملة للانطلاق", en: "Full launch readiness" },
                ].map((item, i) => (
                  <li key={i} className="flex items-center gap-2">
                    <Check className="w-4 h-4 text-emerald-500 shrink-0" />
                    <span>{isRTL ? item.ar : item.en}</span>
                  </li>
                ))}
              </ul>
              <label className="flex items-center gap-2 justify-center mt-4 cursor-pointer">
                <input
                  type="checkbox"
                  checked={(formData.welcome as any)?.agreed ?? false}
                  onChange={(e) => updateField("agreed", e.target.checked)}
                  className="rounded border-border"
                />
                <span className="text-sm text-muted-foreground">
                  {isRTL ? "أوافق على البدء" : "I agree to get started"}
                </span>
              </label>
              {errors.agreed && (
                <p className="text-xs text-red-500">{errors.agreed}</p>
              )}
            </div>
          )}

          {/* Company step */}
          {step.id === "company" && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">
                  {isRTL ? "اسم الشركة" : "Company Name"} *
                </label>
                <input
                  type="text"
                  value={(formData.company as any)?.companyName ?? ""}
                  onChange={(e) => updateField("companyName", e.target.value)}
                  className="w-full rounded-lg border border-border bg-background px-4 py-2.5 text-sm"
                  placeholder={isRTL ? "اسم شركتك" : "Your company name"}
                  dir={isRTL ? "rtl" : "ltr"}
                />
                {errors.companyName && (
                  <p className="text-xs text-red-500 mt-1">{errors.companyName}</p>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  {isRTL ? "المجال" : "Industry"} *
                </label>
                <select
                  value={(formData.company as any)?.industry ?? ""}
                  onChange={(e) => updateField("industry", e.target.value)}
                  className="w-full rounded-lg border border-border bg-background px-4 py-2.5 text-sm"
                >
                  <option value="">{isRTL ? "اختر المجال" : "Select industry"}</option>
                  {[
                    { ar: "تقنية", en: "Technology" },
                    { ar: "مالية", en: "Finance" },
                    { ar: "صحة", en: "Healthcare" },
                    { ar: "تعليم", en: "Education" },
                    { ar: "عقارات", en: "Real Estate" },
                    { ar: "تجارة إلكترونية", en: "E-commerce" },
                    { ar: "استشارات", en: "Consulting" },
                    { ar: "أخرى", en: "Other" },
                  ].map((opt) => (
                    <option key={opt.en} value={opt.en}>
                      {isRTL ? opt.ar : opt.en}
                    </option>
                  ))}
                </select>
                {errors.industry && (
                  <p className="text-xs text-red-500 mt-1">{errors.industry}</p>
                )}
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  {isRTL ? "حجم الشركة" : "Company Size"}
                </label>
                <select
                  value={(formData.company as any)?.companySize ?? ""}
                  onChange={(e) => updateField("companySize", e.target.value)}
                  className="w-full rounded-lg border border-border bg-background px-4 py-2.5 text-sm"
                >
                  <option value="">{isRTL ? "اختر الحجم" : "Select size"}</option>
                  {["1-10", "11-50", "51-200", "201-1000", "1000+"].map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  {isRTL ? "الموقع الإلكتروني" : "Website"}
                </label>
                <input
                  type="url"
                  value={(formData.company as any)?.website ?? ""}
                  onChange={(e) => updateField("website", e.target.value)}
                  className="w-full rounded-lg border border-border bg-background px-4 py-2.5 text-sm"
                  placeholder="https://example.com"
                  dir="ltr"
                />
              </div>
            </div>
          )}

          {/* ICP step */}
          {step.id === "icp" && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">
                  {isRTL ? "المجال المستهدف" : "Target Industry"}
                </label>
                <select
                  value={(formData.icp as any)?.targetIndustry ?? ""}
                  onChange={(e) => updateField("targetIndustry", e.target.value)}
                  className="w-full rounded-lg border border-border bg-background px-4 py-2.5 text-sm"
                >
                  <option value="">{isRTL ? "اختر المجال" : "Select industry"}</option>
                  {["Technology", "Finance", "Healthcare", "Education", "Real Estate", "E-commerce", "Consulting"].map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  {isRTL ? "نقاط الألم" : "Pain Points"}
                </label>
                <div className="flex flex-wrap gap-2">
                  {[
                    { ar: "نمو الإيرادات", en: "Revenue Growth" },
                    { ar: "كفاءة المبيعات", en: "Sales Efficiency" },
                    { ar: "تسويق", en: "Marketing" },
                    { ar: "خدمة العملاء", en: "Customer Service" },
                    { ar: "الامتثال", en: "Compliance" },
                    { ar: "تقنية", en: "Technology" },
                  ].map((point) => {
                    const selected = ((formData.icp as any)?.painPoints ?? []) as string[];
                    const isSelected = selected.includes(point.en);
                    return (
                      <button
                        key={point.en}
                        type="button"
                        onClick={() => {
                          const current = ((formData.icp as any)?.painPoints ?? []) as string[];
                          const updated = isSelected
                            ? current.filter((p) => p !== point.en)
                            : [...current, point.en];
                          updateField("painPoints", updated);
                        }}
                        className={cn(
                          "rounded-lg border px-3 py-1.5 text-xs font-medium transition-colors",
                          isSelected
                            ? "border-gold-500 bg-gold-500/10 text-gold-500"
                            : "border-border text-muted-foreground hover:border-foreground/30",
                        )}
                      >
                        {isRTL ? point.ar : point.en}
                      </button>
                    );
                  })}
                </div>
                {errors.painPoints && (
                  <p className="text-xs text-red-500 mt-1">{errors.painPoints}</p>
                )}
              </div>
            </div>
          )}

          {/* Integrations step */}
          {step.id === "integrations" && (
            <div className="space-y-4">
              {[
                { id: "hubspot", label: "HubSpot", labelAr: "هب سبوت" },
                { id: "calenderly", label: "Calendly", labelAr: "كاليندلي" },
                { id: "googleWorkspace", label: "Google Workspace", labelAr: "قوقل ورك سبيس" },
                { id: "slack", label: "Slack", labelAr: "سلاك" },
              ].map((integration) => (
                <label
                  key={integration.id}
                  className="flex items-center justify-between rounded-lg border border-border p-4 cursor-pointer hover:bg-accent/50 transition-colors"
                >
                  <span className="text-sm font-medium">
                    {isRTL ? integration.labelAr : integration.label}
                  </span>
                  <input
                    type="checkbox"
                    checked={(formData.integrations as any)?.[integration.id] ?? false}
                    onChange={(e) => updateField(integration.id, e.target.checked)}
                    className="rounded border-border"
                  />
                </label>
              ))}
            </div>
          )}

          {/* Ready step */}
          {step.id === "ready" && (
            <div className="text-center space-y-4">
              <p className="text-sm text-muted-foreground">
                {isRTL
                  ? "كل شيء جاهز! يمكنك الآن البدء في استخدام ديليكس"
                  : "Everything is ready! You can now start using Dealix"}
              </p>
              <div className="grid grid-cols-2 gap-3 max-w-xs mx-auto">
                {[
                  { ar: "لوحة التحكم", en: "Dashboard" },
                  { ar: "الصفقات", en: "Deals" },
                  { ar: "العملاء", en: "Clients" },
                  { ar: "التقارير", en: "Reports" },
                ].map((item, i) => (
                  <div
                    key={i}
                    className="rounded-lg border border-border bg-accent/30 p-3 text-center text-xs font-medium"
                  >
                    {isRTL ? item.ar : item.en}
                  </div>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      </AnimatePresence>

      {/* Navigation */}
      <div className="flex items-center justify-between mt-6">
        <div>
          {currentStep > 0 ? (
            <Button variant="ghost" onClick={handleBack}>
              <ChevronLeft className="w-4 h-4 mr-1" />
              {isRTL ? "السابق" : "Back"}
            </Button>
          ) : onSkip ? (
            <Button variant="ghost" onClick={onSkip}>
              {isRTL ? "تخطي الإعداد" : "Skip setup"}
            </Button>
          ) : (
            <div />
          )}
        </div>
        <Button onClick={handleNext} disabled={isSubmitting}>
          {isSubmitting ? (
            <Loader2 className="w-4 h-4 animate-spin mr-1" />
          ) : currentStep === ONBOARDING_STEPS.length - 1 ? (
            <>
              {isRTL ? "ابدأ الآن" : "Get Started"}
              <Rocket className="w-4 h-4 ml-1" />
            </>
          ) : (
            <>
              {isRTL ? "التالي" : "Next"}
              <ChevronRight className="w-4 h-4 ml-1" />
            </>
          )}
        </Button>
      </div>
    </div>
  );
}
