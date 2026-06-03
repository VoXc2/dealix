import type { LucideIcon } from "lucide-react";
import {
  TrendingUp,
  Gauge,
  RefreshCw,
  MessageCircle,
  FileCheck,
} from "lucide-react";
import type { SystemIconName } from "@/data/systems";

/** Resolve a system's icon name (stored as plain data) to a lucide icon. */
export const SYSTEM_ICONS: Record<SystemIconName, LucideIcon> = {
  TrendingUp,
  Gauge,
  RefreshCw,
  MessageCircle,
  FileCheck,
};
