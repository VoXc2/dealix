#!/usr/bin/env python3
"""CEO Master Plan Status — تتبع Waves الـ 9 في لوحة واحدة"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.hermes.orchestrators.wave_orchestrator import WAVE_CONFIGS, WaveStatus


class CEOMasterPlanStatus:
    WAVES: dict[str, dict] = {
        "wave_1_brand": {"name_ar": "الهوية البصرية والعلامة التجارية", "progress": 0, "total_tasks": 17},
        "wave_2_quality": {"name_ar": "تناسق المشروع وجودة الكود", "progress": 0, "total_tasks": 20},
        "wave_3_distribution": {"name_ar": "مكاين التصريف الأربعة الكبرى", "progress": 0, "total_tasks": 45},
        "wave_4_intelligence": {"name_ar": "الذكاء الصناعي الأصيل", "progress": 0, "total_tasks": 30},
        "wave_5_enterprise": {"name_ar": "جاهزية المؤسسات الكبرى", "progress": 0, "total_tasks": 25},
        "wave_6_ux": {"name_ar": "واجهة المستخدم العالمية", "progress": 0, "total_tasks": 35},
        "wave_7_saudi": {"name_ar": "السعودية العميقة", "progress": 0, "total_tasks": 40},
        "wave_8_gulf": {"name_ar": "التوسع الخليجي", "progress": 0, "total_tasks": 15},
        "wave_9_ops": {"name_ar": "التميز التنفيذي والتشغيلي", "progress": 0, "total_tasks": 15},
    }

    async def get_status(self) -> dict:
        return self.WAVES

    def print_dashboard(self) -> None:
        """Print CEO dashboard to console with progress bars."""
        overall_total = sum(w["total_tasks"] for w in self.WAVES.values())
        overall_progress = sum(w["progress"] for w in self.WAVES.values())
        overall_pct = (overall_progress / overall_total * 100) if overall_total else 0

        print("=" * 62)
        print("   DEALIX CEO MASTER PLAN — EXECUTIVE DASHBOARD")
        print(f"   {'Overall Progress':20s} {overall_progress}/{overall_total} ({overall_pct:.1f}%)")
        print("=" * 62)
        for wave_id, info in self.WAVES.items():
            pct = (info["progress"] / info["total_tasks"]) * 100 if info["total_tasks"] else 0
            filled = int(pct / 5)
            bar = "█" * filled + "░" * (20 - filled)
            status = "●" if pct >= 100 else "○" if pct > 0 else "◌"
            print(f"  {status} {info['name_ar']:25s} [{bar}] {pct:5.1f}%  ({info['progress']}/{info['total_tasks']})")

        print("=" * 62)
        waves_complete = sum(1 for w in self.WAVES.values() if w["progress"] >= w["total_tasks"])
        print(f"   Waves complete: {waves_complete}/{len(self.WAVES)}")
        print(f"   CEO_MASTER_PLAN_VERDICT={'PASS' if overall_pct >= 100 else 'IN_PROGRESS'}")

    def to_json(self) -> dict:
        return {
            "waves": self.WAVES,
            "overall": {
                "total_tasks": sum(w["total_tasks"] for w in self.WAVES.values()),
                "completed_tasks": sum(w["progress"] for w in self.WAVES.values()),
                "pct": (sum(w["progress"] for w in self.WAVES.values()) / sum(w["total_tasks"] for w in self.WAVES.values()) * 100)
                if sum(w["total_tasks"] for w in self.WAVES.values())
                else 0,
            },
            "verdict": "PASS"
            if all(w["progress"] >= w["total_tasks"] for w in self.WAVES.values())
            else "IN_PROGRESS",
        }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true", help="Output as JSON")
    p.add_argument("--set", nargs=2, metavar=("WAVE_ID", "PROGRESS"), help="Set progress for a wave")
    args = p.parse_args()

    status = CEOMasterPlanStatus()

    if args.set:
        wave_id, progress_str = args.set
        if wave_id in status.WAVES:
            try:
                status.WAVES[wave_id]["progress"] = int(progress_str)
            except ValueError:
                print(f"Error: progress must be an integer, got {progress_str!r}", file=sys.stderr)
                return 1
        else:
            print(f"Error: unknown wave_id {wave_id!r}. Available: {list(status.WAVES.keys())}", file=sys.stderr)
            return 1

    if args.json:
        print(json.dumps(status.to_json(), ensure_ascii=False, indent=2))
    else:
        status.print_dashboard()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
