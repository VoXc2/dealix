#!/usr/bin/env python3
"""Board Pack Generator — يُنشئ تقرير مجلس الإدارة الشهري"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.hermes.orchestrators.wave_orchestrator import WAVE_CONFIGS

BOARD_SECTIONS = [
    "executive_summary",
    "wave_progress",
    "revenue_metrics",
    "market_position",
    "key_initiatives",
    "risks_and_mitigations",
    "next_month_outlook",
]


class BoardPackGenerator:
    """يُولد تقرير مجلس الإدارة الشهري مع جميع المقاييس والتوصيات"""

    def __init__(self, output_dir: str | Path | None = None) -> None:
        self.output_dir = Path(output_dir) if output_dir else ROOT / "data" / "board_packs"

    async def generate(self, month: str) -> str:
        """Generate board pack for a given month (YYYY-MM)."""
        report = await self._compile_report(month)
        pdf_path = await self._render_report(report)
        return pdf_path

    async def _compile_report(self, month: str) -> dict[str, Any]:
        """Compile all sections of the board report."""
        waves_data = self._compile_wave_data()
        revenue_data = await self._compile_revenue_data(month)

        return {
            "title": f"Dealix Board Pack — {month}",
            "generated_at": datetime.now().isoformat(),
            "period": month,
            "executive_summary": self._executive_summary(month, waves_data, revenue_data),
            "wave_progress": waves_data,
            "revenue_metrics": revenue_data,
            "market_position": self._market_position(),
            "key_initiatives": self._key_initiatives(),
            "risks_and_mitigations": self._risks(),
            "next_month_outlook": self._outlook(month),
            "sections_included": BOARD_SECTIONS,
        }

    def _compile_wave_data(self) -> list[dict[str, Any]]:
        """Compile wave progress data for the board."""
        waves: list[dict[str, Any]] = []
        for wave_id, config in WAVE_CONFIGS.items():
            waves.append({
                "wave_id": wave_id,
                "name_ar": config.name_ar,
                "name_en": config.name_en,
                "agents": config.agents,
                "status": "pending",
                "progress_pct": 0.0,
                "sla_hours": config.sla_hours,
                "approval_required": config.approval_required,
            })
        return waves

    async def _compile_revenue_data(self, month: str) -> dict[str, Any]:
        """Compile revenue metrics for the board."""
        return {
            "month": month,
            "total_revenue_sar": 0,
            "new_customers": 0,
            "proofs_delivered": 0,
            "pipeline_value_sar": 0,
            "avg_deal_size_sar": 0,
            "conversion_rate_pct": 0.0,
        }

    def _executive_summary(
        self, month: str, waves: list[dict[str, Any]], revenue: dict[str, Any]
    ) -> dict[str, Any]:
        """Generate executive summary."""
        total_waves = len(waves)
        return {
            "month": month,
            "highlights": [
                f"{total_waves} waves in progress across all product areas",
                "Building autonomous AI operations layer",
                "Saudi market readiness in progress",
            ],
            "concerns": [
                "Revenue generation in early stage",
                "Customer acquisition funnel building",
            ],
            "verdict": "ON_TRACK",
        }

    def _market_position(self) -> dict[str, Any]:
        """Generate market position section."""
        return {
            "target_market": "Saudi Arabia B2B AI Operations",
            "market_size_sar": "5,000,000,000",
            "position": "Emerging Leader",
            "competitors": ["Traditional consultancies", "Freelance operators"],
            "moat": "AI-native autonomous operations platform",
        }

    def _key_initiatives(self) -> list[dict[str, Any]]:
        """Generate key initiatives for the board."""
        return [
            {
                "name": "9-Wave Execution",
                "status": "IN_PROGRESS",
                "completion_target": "Q3 2026",
            },
            {
                "name": "Revenue Generation",
                "status": "EARLY_STAGE",
                "completion_target": "Q2 2026",
            },
            {
                "name": "Saudi Market Entry",
                "status": "IN_PROGRESS",
                "completion_target": "Q2 2026",
            },
        ]

    def _risks(self) -> list[dict[str, Any]]:
        """Generate risks and mitigations section."""
        return [
            {
                "risk": "Revenue concentration risk",
                "likelihood": "MEDIUM",
                "impact": "HIGH",
                "mitigation": "Diversify pipeline across 4 distribution engines",
            },
            {
                "risk": "Execution velocity",
                "likelihood": "LOW",
                "impact": "MEDIUM",
                "mitigation": "9-wave parallel execution with SLA tracking",
            },
        ]

    def _outlook(self, month: str) -> dict[str, Any]:
        """Generate next month outlook."""
        return {
            "next_month": self._next_month(month),
            "focus_areas": [
                "Complete Waves 1-3 foundation",
                "First customer acquisition",
                "Proof pack delivery",
            ],
            "board_actions": [
                "Review wave progress and approve Wave 1",
                "Discuss go-to-market strategy",
                "Approve budget for Wave 3 distribution engines",
            ],
        }

    async def _render_report(self, report: dict[str, Any]) -> str:
        """Render the report to a JSON file (PDF-ready structure)."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"board_pack_{report['period']}.json"
        filepath = self.output_dir / filename
        filepath.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Board pack generated: {filepath}")
        return str(filepath)

    @staticmethod
    def _next_month(current: str) -> str:
        """Return the next month string (YYYY-MM)."""
        try:
            y, m = map(int, current.split("-"))
            m += 1
            if m > 12:
                m = 1
                y += 1
            return f"{y:04d}-{m:02d}"
        except (ValueError, IndexError):
            return current


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--month",
        default=date.today().strftime("%Y-%m"),
        help="Month in YYYY-MM format (default: current)",
    )
    p.add_argument("--json", action="store_true", help="Print report JSON to stdout")
    args = p.parse_args()

    import asyncio

    generator = BoardPackGenerator()
    report_data = asyncio.run(generator._compile_report(args.month))

    if args.json:
        print(json.dumps(report_data, ensure_ascii=False, indent=2))
    else:
        print(f"== Board Pack Generator — {args.month} ==")
        print(f"  Sections: {', '.join(BOARD_SECTIONS)}")
        print(f"  Waves tracked: {len(report_data['wave_progress'])}")
        print(f"  Verdict: {report_data['executive_summary']['verdict']}")
        print(f"  Output: {asyncio.run(generator._render_report(report_data))}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
