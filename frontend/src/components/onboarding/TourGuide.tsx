"use client";

import { useState, useCallback, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, ChevronLeft, ChevronRight, Compass } from "lucide-react";
import { useLocale } from "next-intl";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

interface TourStep {
  id: string;
  targetSelector: string;
  title: string;
  titleAr: string;
  description: string;
  descriptionAr: string;
  position: "top" | "bottom" | "left" | "right";
}

interface TourGuideProps {
  steps: TourStep[];
  isActive: boolean;
  onComplete: () => void;
  onDismiss: () => void;
}

export function TourGuide({ steps, isActive, onComplete, onDismiss }: TourGuideProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [targetRect, setTargetRect] = useState<DOMRect | null>(null);
  const locale = useLocale();
  const isRTL = locale === "ar";

  const step = steps[currentStep];

  const updatePosition = useCallback(() => {
    if (!step) return;
    const el = document.querySelector(step.targetSelector);
    if (el) {
      setTargetRect(el.getBoundingClientRect());
    }
  }, [step]);

  useEffect(() => {
    if (isActive) updatePosition();
    window.addEventListener("scroll", updatePosition);
    window.addEventListener("resize", updatePosition);
    return () => {
      window.removeEventListener("scroll", updatePosition);
      window.removeEventListener("resize", updatePosition);
    };
  }, [isActive, updatePosition]);

  useEffect(() => {
    if (!isActive) {
      setCurrentStep(0);
      setTargetRect(null);
    }
  }, [isActive]);

  const handleNext = useCallback(() => {
    if (currentStep < steps.length - 1) {
      setCurrentStep((prev) => prev + 1);
    } else {
      onComplete();
    }
  }, [currentStep, steps.length, onComplete]);

  const handlePrev = useCallback(() => {
    if (currentStep > 0) setCurrentStep((prev) => prev - 1);
  }, [currentStep]);

  if (!isActive || !step || !targetRect) return null;

  const getTooltipPosition = () => {
    const gap = 12;
    switch (step.position) {
      case "top":
        return {
          left: targetRect.left + targetRect.width / 2,
          top: targetRect.top - gap,
          transform: "translate(-50%, -100%)",
        };
      case "bottom":
        return {
          left: targetRect.left + targetRect.width / 2,
          top: targetRect.bottom + gap,
          transform: "translate(-50%, 0)",
        };
      case "left":
        return {
          left: targetRect.left - gap,
          top: targetRect.top + targetRect.height / 2,
          transform: "translate(-100%, -50%)",
        };
      case "right":
        return {
          left: targetRect.right + gap,
          top: targetRect.top + targetRect.height / 2,
          transform: "translate(0, -50%)",
        };
    }
  };

  const pos = getTooltipPosition();

  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 z-[200] bg-black/40" onClick={onDismiss} />

      {/* Highlight ring */}
      <div
        className="fixed z-[201] rounded-lg border-2 border-gold-500 pointer-events-none"
        style={{
          left: targetRect.left - 4,
          top: targetRect.top - 4,
          width: targetRect.width + 8,
          height: targetRect.height + 8,
        }}
      />

      {/* Tooltip */}
      <AnimatePresence mode="wait">
        <motion.div
          key={step.id}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          className="fixed z-[202] w-72 rounded-2xl border border-border bg-card shadow-2xl p-5"
          style={{ left: pos.left, top: pos.top, transform: pos.transform }}
        >
          {/* Header */}
          <div className="flex items-start justify-between mb-3">
            <div className="flex items-center gap-2">
              <Compass className="w-4 h-4 text-gold-500" />
              <span className="text-[11px] font-semibold uppercase tracking-wider text-muted-foreground">
                {isRTL
                  ? `خطوة ${currentStep + 1} من ${steps.length}`
                  : `Step ${currentStep + 1} of ${steps.length}`}
              </span>
            </div>
            <button
              onClick={onDismiss}
              className="rounded-lg p-0.5 text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <h3 className="text-sm font-semibold text-foreground mb-1">
            {isRTL ? step.titleAr : step.title}
          </h3>
          <p className="text-xs text-muted-foreground mb-4">
            {isRTL ? step.descriptionAr : step.description}
          </p>

          {/* Navigation */}
          <div className="flex items-center justify-between">
            <div className="flex gap-1">
              {steps.map((s, i) => (
                <div
                  key={s.id}
                  className={cn(
                    "h-1.5 w-1.5 rounded-full",
                    i === currentStep ? "bg-gold-500" : "bg-border",
                  )}
                />
              ))}
            </div>
            <div className="flex items-center gap-1">
              {currentStep > 0 && (
                <Button variant="ghost" size="sm" onClick={handlePrev}>
                  <ChevronLeft className="w-3.5 h-3.5" />
                </Button>
              )}
              <Button size="sm" onClick={handleNext}>
                {currentStep < steps.length - 1 ? (
                  <>
                    {isRTL ? "التالي" : "Next"}
                    <ChevronRight className="w-3.5 h-3.5 ml-0.5" />
                  </>
                ) : (
                  isRTL ? "إنهاء" : "Finish"
                )}
              </Button>
            </div>
          </div>
        </motion.div>
      </AnimatePresence>
    </>
  );
}
