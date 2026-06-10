"use client";

import { useState, useCallback, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";
import { cn } from "@/lib/utils";

interface BottomSheetProps {
  open: boolean;
  onClose: () => void;
  children: React.ReactNode;
  title?: string;
  titleAr?: string;
  snapPoints?: number[];
  defaultSnap?: number;
  locale?: string;
}

export function BottomSheet({
  open,
  onClose,
  children,
  title,
  titleAr,
  snapPoints = [0.5, 0.85],
  defaultSnap = 0,
  locale = "en",
}: BottomSheetProps) {
  const [snapIndex, setSnapIndex] = useState(defaultSnap);
  const sheetRef = useRef<HTMLDivElement>(null);
  const startYRef = useRef(0);
  const isRTL = locale === "ar";

  const height = snapPoints[snapIndex] * 100;

  const handleTouchStart = useCallback((e: React.TouchEvent) => {
    startYRef.current = e.touches[0].clientY;
  }, []);

  const handleTouchMove = useCallback(
    (e: React.TouchEvent) => {
      if (!sheetRef.current) return;
      const deltaY = e.touches[0].clientY - startYRef.current;
      if (deltaY > 50 && snapIndex < snapPoints.length - 1) {
        setSnapIndex((prev) => Math.min(prev + 1, snapPoints.length - 1));
      } else if (deltaY < -50 && snapIndex > 0) {
        setSnapIndex((prev) => Math.max(prev - 1, 0));
      }
    },
    [snapIndex, snapPoints.length],
  );

  useEffect(() => {
    if (!open) setSnapIndex(defaultSnap);
  }, [open, defaultSnap]);

  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-[110] md:hidden">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-black/50"
            onClick={onClose}
          />

          {/* Sheet */}
          <motion.div
            ref={sheetRef}
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "100%" }}
            transition={{ type: "spring", damping: 30, stiffness: 300 }}
            className="absolute bottom-0 left-0 right-0 rounded-t-2xl bg-background border border-border shadow-2xl"
            style={{ height: `${height}vh` }}
            onTouchStart={handleTouchStart}
            onTouchMove={handleTouchMove}
          >
            {/* Handle */}
            <div className="flex items-center justify-center pt-2 pb-1">
              <div className="h-1 w-10 rounded-full bg-muted-foreground/30" />
            </div>

            {/* Header */}
            {(title || titleAr) && (
              <div className="flex items-center justify-between px-5 py-3 border-b border-border">
                <h3 className="text-sm font-semibold text-foreground">
                  {isRTL ? titleAr : title}
                </h3>
                <button
                  onClick={onClose}
                  className="rounded-lg p-1 text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            )}

            {/* Content */}
            <div className="overflow-y-auto h-[calc(100%-48px)] p-4">
              {children}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
