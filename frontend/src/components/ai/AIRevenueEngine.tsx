"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useLocale } from "next-intl";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, Send, TrendingUp, AlertCircle, Zap } from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { apiClient } from "@/lib/api";

// ── Types ────────────────────────────────────────────────────────────────────

type MessageRole = "user" | "ai";

interface ChatMessage {
  id: string;
  role: MessageRole;
  text: string;
  recommendation?: RecommendationPayload;
  timestamp: number;
}

interface RecommendationPayload {
  recommendation_ar: string;
  recommendation_en: string;
  impact_estimate: string;
  confidence_score: number;
  category: "growth" | "retention" | "pipeline" | "pricing";
}

type ImpactLevel = "high" | "medium" | "low";

interface Opportunity {
  id: string;
  title_ar: string;
  title_en: string;
  impact: ImpactLevel;
  potential_sar: number;
}

// ── Constants ─────────────────────────────────────────────────────────────────

const QUICK_QUESTIONS_AR = [
  "كيف أزيد إيراداتي 20%؟",
  "أين أخسر العملاء؟",
  "ما فرص التوسع؟",
  "تحليل pipeline الحالي",
];

const QUICK_QUESTIONS_EN = [
  "How do I grow revenue 20%?",
  "Where am I losing clients?",
  "What expansion opportunities exist?",
  "Analyze current pipeline",
];

const MOCK_RESPONSES: Record<string, RecommendationPayload> = {
  default_ar_0: {
    recommendation_ar:
      "بناءً على تحليل بياناتك، يمكنك زيادة إيراداتك 20% خلال 90 يوماً عبر ثلاث مسارات: أولاً، تفعيل برنامج upsell للعملاء الحاليين في المرحلة B (التأثير المقدر: +8%). ثانياً، تقليص دورة المبيعات من 45 يوماً إلى 28 يوماً عبر أتمتة متابعة العملاء المحتملين (+7%). ثالثاً، إطلاق حزمة تسعير جديدة للقطاع المتوسط بسعر 12,000 ريال (+5%).",
    recommendation_en:
      "Based on your data, a 20% revenue increase within 90 days is achievable via three tracks: upsell activation for tier-B clients (+8%), sales-cycle compression from 45 to 28 days through lead follow-up automation (+7%), and a new mid-market pricing bundle at SAR 12,000 (+5%).",
    impact_estimate: "+20% خلال 90 يوماً",
    confidence_score: 82,
    category: "growth",
  },
  default_ar_1: {
    recommendation_ar:
      "التحليل يظهر أن 38% من خسارة العملاء تحدث بين التجربة المجانية ومرحلة القرار. السبب الرئيسي: غياب لمسة إنسانية بعد اليوم السابع. التوصية: تفعيل تسلسل بريد إلكتروني شخصي في اليوم 7 و14 مع دراسة حالة من القطاع المماثل. التأثير المتوقع: تقليل معدل الإلغاء 18%.",
    recommendation_en:
      "Analysis shows 38% of client loss occurs between free trial and decision stage. Root cause: absence of a human touchpoint after day 7. Recommendation: activate a personalised email sequence on day 7 and day 14 with a sector-matched case study. Expected impact: 18% reduction in churn.",
    impact_estimate: "-18% معدل الإلغاء",
    confidence_score: 75,
    category: "retention",
  },
  default_ar_2: {
    recommendation_ar:
      "ثلاث فرص توسع غير مستغلة في بياناتك: (1) قطاع اللوجستيات — 12 شركة في pool الاستهداف لم يتم التواصل معها. (2) العملاء الحاليون ذوو aiScore أعلى من 85 — 6 منهم مؤهلون لباقة enterprise. (3) الشراكات: 3 شركاء محتملون في قطاع المحاسبة يمكنهم تحويل 8–12 عميل شهرياً.",
    recommendation_en:
      "Three untapped expansion signals: (1) Logistics sector — 12 companies in your targeting pool not yet contacted. (2) Existing clients with aiScore above 85 — 6 qualify for an enterprise upgrade. (3) Partnerships: 3 accounting-sector partners could refer 8–12 clients per month.",
    impact_estimate: "+SAR 340,000 سنوياً",
    confidence_score: 78,
    category: "growth",
  },
  default_ar_3: {
    recommendation_ar:
      "تحليل pipeline الحالي: لديك 24 فرصة نشطة بقيمة إجمالية 1.2 مليون ريال. 8 منها في مرحلة التفاوض منذ أكثر من 21 يوماً (خطر الركود). توصية فورية: جدول اجتماعات مراجعة لهذه الفرص الثمانية خلال 48 ساعة. النقاط الساخنة الثلاث التي تستحق الأولوية: شركة العقارات السعودية (92 نقطة ICP)، مجموعة الرياض الطبية (88 نقطة)، مؤسسة التقنية المتقدمة (95 نقطة).",
    recommendation_en:
      "Pipeline analysis: 24 active opportunities totalling SAR 1.2 million. 8 have been in negotiation for more than 21 days (stagnation risk). Immediate recommendation: schedule review calls for these 8 within 48 hours. Top-three hot spots: Saudi Real Estate (ICP 92), Riyadh Medical Group (ICP 88), Advanced Technology Est. (ICP 95).",
    impact_estimate: "SAR 480,000 في خطر",
    confidence_score: 88,
    category: "pipeline",
  },
};

const OPPORTUNITIES: Opportunity[] = [
  {
    id: "opp-1",
    title_ar: "تفعيل upsell للعملاء الحاليين",
    title_en: "Activate upsell for existing clients",
    impact: "high",
    potential_sar: 185000,
  },
  {
    id: "opp-2",
    title_ar: "استعادة العملاء الغائبين 60+ يوم",
    title_en: "Re-engage clients silent 60+ days",
    impact: "medium",
    potential_sar: 96000,
  },
  {
    id: "opp-3",
    title_ar: "إطلاق باقة القطاع المتوسط",
    title_en: "Launch mid-market bundle",
    impact: "high",
    potential_sar: 240000,
  },
];

const NEXT_BEST_ACTION = {
  ar: "أرسل دراسة حالة للعملاء في مرحلة التفاوض خلال 24 ساعة القادمة",
  en: "Send a case study to clients in negotiation stage within the next 24 hours",
};

// ── Helpers ────────────────────────────────────────────────────────────────────

function impactLabel(impact: ImpactLevel, isAr: boolean): string {
  const map: Record<ImpactLevel, { ar: string; en: string }> = {
    high: { ar: "تأثير عالٍ", en: "High Impact" },
    medium: { ar: "تأثير متوسط", en: "Medium Impact" },
    low: { ar: "تأثير منخفض", en: "Low Impact" },
  };
  return isAr ? map[impact].ar : map[impact].en;
}

function impactVariant(impact: ImpactLevel): "emerald" | "gold" | "secondary" {
  if (impact === "high") return "emerald";
  if (impact === "medium") return "gold";
  return "secondary";
}

function formatSar(value: number): string {
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1)}M`;
  if (value >= 1_000) return `${(value / 1_000).toFixed(0)}K`;
  return String(value);
}

function getMockResponse(questionIndex: number): RecommendationPayload {
  const key = `default_ar_${questionIndex}`;
  return MOCK_RESPONSES[key] ?? MOCK_RESPONSES["default_ar_0"];
}

function uid(): string {
  return Math.random().toString(36).slice(2, 10);
}

// ── Sub-components ─────────────────────────────────────────────────────────────

function TypingIndicator() {
  return (
    <div className="flex items-center gap-1 px-4 py-3">
      {[0, 1, 2].map((i) => (
        <motion.span
          key={i}
          className="w-2 h-2 rounded-full bg-gold-400"
          animate={{ y: [0, -6, 0] }}
          transition={{
            duration: 0.7,
            repeat: Infinity,
            delay: i * 0.15,
            ease: "easeInOut",
          }}
        />
      ))}
    </div>
  );
}

interface RecommendationCardProps {
  payload: RecommendationPayload;
  isAr: boolean;
}

function RecommendationCard({ payload, isAr }: RecommendationCardProps) {
  const categoryLabel: Record<RecommendationPayload["category"], { ar: string; en: string }> = {
    growth: { ar: "نمو", en: "Growth" },
    retention: { ar: "احتفاظ", en: "Retention" },
    pipeline: { ar: "pipeline", en: "Pipeline" },
    pricing: { ar: "تسعير", en: "Pricing" },
  };

  return (
    <div className="mt-3 rounded-xl border border-gold-500/20 bg-gold-500/5 p-4 space-y-3">
      <div className="flex items-center justify-between flex-wrap gap-2">
        <Badge variant="gold">
          {isAr
            ? categoryLabel[payload.category].ar
            : categoryLabel[payload.category].en}
        </Badge>
        <span className="text-xs text-muted-foreground">
          {isAr ? "الثقة:" : "Confidence:"}{" "}
          <span className="text-gold-400 font-semibold">{payload.confidence_score}%</span>
        </span>
      </div>

      <p className="text-sm text-foreground leading-relaxed">
        {isAr ? payload.recommendation_ar : payload.recommendation_en}
      </p>

      <div className="flex items-center gap-2 pt-1 border-t border-border">
        <TrendingUp className="w-4 h-4 text-emerald-400 shrink-0" />
        <span className="text-xs font-semibold text-emerald-400">
          {payload.impact_estimate}
        </span>
      </div>
    </div>
  );
}

interface MessageBubbleProps {
  message: ChatMessage;
  isAr: boolean;
}

function MessageBubble({ message, isAr }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.28, ease: "easeOut" }}
      className={cn(
        "flex w-full",
        isUser ? "justify-end" : "justify-start",
      )}
    >
      <div
        className={cn(
          "max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed",
          isUser
            ? "bg-gold-500/20 border border-gold-500/30 text-foreground"
            : "bg-card border border-border text-foreground",
        )}
      >
        {message.text}
        {message.recommendation && (
          <RecommendationCard
            payload={message.recommendation}
            isAr={isAr}
          />
        )}
      </div>
    </motion.div>
  );
}

// ── Revenue Score circle ───────────────────────────────────────────────────────

const SCORE_VALUE = 73;
const CIRCLE_RADIUS = 38;
const CIRCLE_CIRCUMFERENCE = 2 * Math.PI * CIRCLE_RADIUS;

function RevenueScoreCard({ isAr }: { isAr: boolean }) {
  const [displayed, setDisplayed] = useState(0);

  useEffect(() => {
    let frame: ReturnType<typeof requestAnimationFrame>;
    const duration = 1200;
    const start = performance.now();

    function tick(now: number) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplayed(Math.round(eased * SCORE_VALUE));
      if (progress < 1) frame = requestAnimationFrame(tick);
    }

    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, []);

  const strokeDashoffset =
    CIRCLE_CIRCUMFERENCE - (displayed / 100) * CIRCLE_CIRCUMFERENCE;

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-semibold text-muted-foreground">
          {isAr ? "نقاط الإيرادات" : "Revenue Score"}
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col items-center gap-3 pb-5">
        <div className="relative w-24 h-24">
          <svg className="w-24 h-24 -rotate-90" viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r={CIRCLE_RADIUS}
              stroke="currentColor"
              strokeWidth="8"
              fill="none"
              className="text-muted/20"
            />
            <motion.circle
              cx="50"
              cy="50"
              r={CIRCLE_RADIUS}
              stroke="#D4AF37"
              strokeWidth="8"
              fill="none"
              strokeLinecap="round"
              strokeDasharray={CIRCLE_CIRCUMFERENCE}
              strokeDashoffset={strokeDashoffset}
            />
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-2xl font-bold text-gold-400">{displayed}</span>
          </div>
        </div>
        <p className="text-xs text-center text-muted-foreground">
          {isAr
            ? "أداء قوي — فرص تحسين قائمة"
            : "Strong performance — improvement opportunities exist"}
        </p>
      </CardContent>
    </Card>
  );
}

// ── Opportunities panel ────────────────────────────────────────────────────────

function OpportunitiesPanel({ isAr }: { isAr: boolean }) {
  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-semibold text-muted-foreground">
          {isAr ? "أبرز الفرص" : "Top Opportunities"}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-3 pb-4">
        {OPPORTUNITIES.map((opp, idx) => (
          <motion.div
            key={opp.id}
            initial={{ opacity: 0, x: isAr ? 12 : -12 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.1 + idx * 0.08, duration: 0.25 }}
            className="flex items-start justify-between gap-2"
          >
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium leading-snug truncate">
                {isAr ? opp.title_ar : opp.title_en}
              </p>
              <p className="text-xs text-emerald-400 font-semibold mt-0.5">
                SAR {formatSar(opp.potential_sar)}
              </p>
            </div>
            <Badge variant={impactVariant(opp.impact)} className="shrink-0 text-[10px]">
              {impactLabel(opp.impact, isAr)}
            </Badge>
          </motion.div>
        ))}
      </CardContent>
    </Card>
  );
}

// ── Next best action ───────────────────────────────────────────────────────────

function NextBestActionCard({ isAr }: { isAr: boolean }) {
  return (
    <Card className="border-emerald-500/30 bg-emerald-500/5">
      <CardContent className="flex items-start gap-3 pt-5 pb-5">
        <div className="mt-0.5 rounded-lg bg-emerald-500/10 p-2 shrink-0">
          <Zap className="w-4 h-4 text-emerald-400" />
        </div>
        <div>
          <p className="text-xs font-semibold text-emerald-400 mb-1">
            {isAr ? "الإجراء الأمثل التالي" : "Next Best Action"}
          </p>
          <p className="text-sm text-foreground leading-relaxed">
            {isAr ? NEXT_BEST_ACTION.ar : NEXT_BEST_ACTION.en}
          </p>
        </div>
      </CardContent>
    </Card>
  );
}

// ── Main component ─────────────────────────────────────────────────────────────

export function AIRevenueEngine() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading, scrollToBottom]);

  const sendQuestion = useCallback(
    async (question: string) => {
      if (!question.trim() || isLoading) return;

      const userMsg: ChatMessage = {
        id: uid(),
        role: "user",
        text: question.trim(),
        timestamp: Date.now(),
      };

      setMessages((prev) => [...prev, userMsg]);
      setInputValue("");
      setIsLoading(true);

      // Determine which mock index maps to this quick question
      const qList = isAr ? QUICK_QUESTIONS_AR : QUICK_QUESTIONS_EN;
      const qIndex = qList.indexOf(question.trim());
      const mockIndex = qIndex >= 0 ? qIndex : 0;

      try {
        const res = await apiClient.post<{
          recommendation: RecommendationPayload;
          message?: string;
        }>("/api/v1/value-engine/recommend", {
          query: question.trim(),
          context: { locale },
        });

        const payload = res.data.recommendation ?? getMockResponse(mockIndex);
        const aiText = isAr ? payload.recommendation_ar : payload.recommendation_en;

        setMessages((prev) => [
          ...prev,
          {
            id: uid(),
            role: "ai",
            text: aiText,
            recommendation: payload,
            timestamp: Date.now(),
          },
        ]);
      } catch {
        // API not available — use mock response
        const payload = getMockResponse(mockIndex);
        const aiText = isAr ? payload.recommendation_ar : payload.recommendation_en;

        setMessages((prev) => [
          ...prev,
          {
            id: uid(),
            role: "ai",
            text: aiText,
            recommendation: payload,
            timestamp: Date.now(),
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [isAr, isLoading, locale],
  );

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendQuestion(inputValue);
      }
    },
    [inputValue, sendQuestion],
  );

  const quickQuestions = isAr ? QUICK_QUESTIONS_AR : QUICK_QUESTIONS_EN;

  return (
    <div className="space-y-5">
      {/* Page header */}
      <div className="flex items-center gap-3">
        <div className="rounded-xl bg-gold-500/10 p-2.5 border border-gold-500/20">
          <Sparkles className="w-5 h-5 text-gold-400" />
        </div>
        <div>
          <h1 className="text-xl font-bold">
            {isAr ? "محرك الإيرادات بالذكاء الاصطناعي" : "AI Revenue Engine"}
          </h1>
          <p className="text-sm text-muted-foreground">
            {isAr
              ? "توصيات ذكية لزيادة إيراداتك"
              : "Smart recommendations to grow your revenue"}
          </p>
        </div>
      </div>

      {/* Main layout */}
      <div className="flex flex-col lg:flex-row gap-5">
        {/* Chat panel — 2/3 width on large screens */}
        <div className="flex-1 lg:w-0 min-w-0 flex flex-col gap-4">
          {/* Quick question chips */}
          <div className="flex flex-wrap gap-2">
            {quickQuestions.map((q) => (
              <button
                key={q}
                onClick={() => sendQuestion(q)}
                disabled={isLoading}
                className={cn(
                  "rounded-full border border-border bg-card px-3 py-1.5 text-xs font-medium",
                  "text-muted-foreground hover:border-gold-500/40 hover:text-gold-400",
                  "transition-colors disabled:opacity-50 disabled:cursor-not-allowed",
                )}
              >
                {q}
              </button>
            ))}
          </div>

          {/* Messages area */}
          <Card className="flex flex-col min-h-[420px] max-h-[560px]">
            <CardContent className="flex-1 overflow-y-auto p-4 space-y-4 pt-4">
              <AnimatePresence initial={false}>
                {messages.length === 0 && (
                  <motion.div
                    key="empty"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="flex flex-col items-center justify-center h-full min-h-[300px] gap-3 text-center"
                  >
                    <div className="rounded-2xl bg-gold-500/10 p-4 border border-gold-500/15">
                      <Sparkles className="w-8 h-8 text-gold-400" />
                    </div>
                    <p className="text-sm text-muted-foreground max-w-xs">
                      {isAr
                        ? "اطرح سؤالاً عن إيراداتك أو اختر من الأسئلة السريعة أعلاه"
                        : "Ask a question about your revenue or choose from the quick questions above"}
                    </p>
                  </motion.div>
                )}

                {messages.map((msg) => (
                  <MessageBubble key={msg.id} message={msg} isAr={isAr} />
                ))}

                {isLoading && (
                  <motion.div
                    key="typing"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 10 }}
                    className="flex justify-start"
                  >
                    <div className="rounded-2xl border border-border bg-card">
                      <TypingIndicator />
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
              <div ref={messagesEndRef} />
            </CardContent>

            {/* Input area */}
            <div className="border-t border-border p-4">
              <div className="flex items-end gap-2">
                <textarea
                  ref={textareaRef}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder={
                    isAr
                      ? "اسألني عن إيراداتك..."
                      : "Ask me about your revenue..."
                  }
                  rows={2}
                  disabled={isLoading}
                  className={cn(
                    "flex-1 min-w-0 resize-none rounded-xl border border-input bg-background",
                    "px-4 py-2.5 text-sm ring-offset-background placeholder:text-muted-foreground",
                    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
                    "focus-visible:ring-offset-0 disabled:cursor-not-allowed disabled:opacity-50",
                    "transition-colors",
                  )}
                />
                <Button
                  variant="gold"
                  size="icon"
                  onClick={() => sendQuestion(inputValue)}
                  disabled={isLoading || !inputValue.trim()}
                  className="shrink-0 h-10 w-10 rounded-xl"
                  aria-label={isAr ? "إرسال" : "Send"}
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
              <p className="mt-2 text-[10px] text-muted-foreground">
                {isAr
                  ? "Shift + Enter لسطر جديد · Enter للإرسال"
                  : "Shift + Enter for new line · Enter to send"}
              </p>
            </div>
          </Card>
        </div>

        {/* Right insights panel — 1/3 width on large screens */}
        <div className="w-full lg:w-80 shrink-0 space-y-4">
          <RevenueScoreCard isAr={isAr} />
          <OpportunitiesPanel isAr={isAr} />
          <NextBestActionCard isAr={isAr} />

          {/* Disclaimer */}
          <div className="flex items-start gap-2 rounded-xl border border-border bg-card p-3">
            <AlertCircle className="w-4 h-4 text-muted-foreground shrink-0 mt-0.5" />
            <p className="text-[11px] text-muted-foreground leading-relaxed">
              {isAr
                ? "التوصيات مبنية على البيانات المتاحة. راجع مديرك قبل اتخاذ قرارات مالية."
                : "Recommendations are based on available data. Consult your manager before making financial decisions."}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
