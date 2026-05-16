"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useTranslations, useLocale } from "next-intl";
import { motion } from "framer-motion";
import { Star, ShieldCheck, Activity, ArrowRight } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";
import { DEFAULT_CUSTOMER_ID } from "@/lib/commercial";

interface BoardSnapshot {
  northStar: number;
  gatesPassed: number;
  gatesTotal: number;
  engagements: number;
}

/**
 * Self-contained, additive dashboard tile showing the Board Decision OS
 * signal. Fails silently (renders zeros) so it can never break the dashboard.
 */
export function BoardSignalTile() {
  const t = useTranslations("boardTile");
  const locale = useLocale();
  const [snapshot, setSnapshot] = useState<BoardSnapshot | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const res = await api.getBoardDecisionOverview(DEFAULT_CUSTOMER_ID, false);
        if (cancelled) return;
        const data = res.data as {
          north_star?: { count?: number };
          gates_passed?: string[];
          cel_summary?: { engagements?: number };
        };
        setSnapshot({
          northStar: data.north_star?.count ?? 0,
          gatesPassed: Array.isArray(data.gates_passed)
            ? data.gates_passed.length
            : 0,
          gatesTotal: 7,
          engagements: data.cel_summary?.engagements ?? 0,
        });
      } catch {
        if (!cancelled)
          setSnapshot({
            northStar: 0,
            gatesPassed: 0,
            gatesTotal: 7,
            engagements: 0,
          });
      }
    }
    void load();
    return () => {
      cancelled = true;
    };
  }, []);

  const s = snapshot ?? {
    northStar: 0,
    gatesPassed: 0,
    gatesTotal: 7,
    engagements: 0,
  };

  const tiles = [
    {
      icon: <Star className="w-4 h-4 text-gold-400" />,
      label: t("northStar"),
      value: s.northStar,
    },
    {
      icon: <ShieldCheck className="w-4 h-4 text-emerald-400" />,
      label: t("gatesPassed"),
      value: `${s.gatesPassed} / ${s.gatesTotal}`,
    },
    {
      icon: <Activity className="w-4 h-4 text-blue-400" />,
      label: t("engagements"),
      value: s.engagements,
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.55 }}
    >
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-base font-semibold">
              {t("title")}
            </CardTitle>
            <Link
              href={`/${locale}/board-decision-os`}
              className="text-xs font-medium text-gold-400 hover:underline flex items-center gap-1"
            >
              {t("viewBoard")}
              <ArrowRight className="w-3 h-3" />
            </Link>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {tiles.map((tile) => (
              <div
                key={tile.label}
                className="rounded-xl border border-border bg-muted/30 p-4"
              >
                <div className="flex items-center gap-2 mb-2">{tile.icon}</div>
                <p className="text-2xl font-bold text-foreground">
                  {tile.value}
                </p>
                <p className="text-xs text-muted-foreground mt-1">
                  {tile.label}
                </p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
