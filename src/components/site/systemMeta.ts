import { TrendingUp, Compass, RefreshCw, MessageSquare, FileText, type LucideIcon } from 'lucide-react'

// UI-only metadata (icon + accent classes) keyed by system id. Kept separate
// from src/data/systems.ts so the data module stays free of React/Tailwind.
export interface SystemMeta {
  icon: LucideIcon
  iconBg: string
  accentText: string
  accentBorder: string
}

const DEFAULT: SystemMeta = {
  icon: TrendingUp,
  iconBg: 'bg-emerald-100 text-emerald-600',
  accentText: 'text-emerald-600',
  accentBorder: 'border-emerald-500',
}

export const SYSTEM_META: Record<string, SystemMeta> = {
  'revenue-operating-system': {
    icon: TrendingUp,
    iconBg: 'bg-emerald-100 text-emerald-600',
    accentText: 'text-emerald-600',
    accentBorder: 'border-emerald-500',
  },
  'executive-command-os': {
    icon: Compass,
    iconBg: 'bg-indigo-100 text-indigo-600',
    accentText: 'text-indigo-600',
    accentBorder: 'border-indigo-500',
  },
  'follow-up-recovery-os': {
    icon: RefreshCw,
    iconBg: 'bg-amber-100 text-amber-600',
    accentText: 'text-amber-600',
    accentBorder: 'border-amber-500',
  },
  'whatsapp-client-os': {
    icon: MessageSquare,
    iconBg: 'bg-green-100 text-green-600',
    accentText: 'text-green-600',
    accentBorder: 'border-green-500',
  },
  'proposal-proof-os': {
    icon: FileText,
    iconBg: 'bg-sky-100 text-sky-600',
    accentText: 'text-sky-600',
    accentBorder: 'border-sky-500',
  },
}

export function systemMeta(id: string): SystemMeta {
  return SYSTEM_META[id] ?? DEFAULT
}
