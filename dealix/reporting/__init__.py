"""Dealix Reporting OS — executive reports, proof packs, weekly summaries.

نظام التقارير — تقارير تنفيذية، حِزم إثبات الأثر، ملخصات أسبوعية.
"""
from dealix.reporting.executive_report import ExecutiveReport, build_executive_report
from dealix.reporting.proof_pack import ProofPack, build_proof_pack
from dealix.reporting.weekly_summary import WeeklySummary, build_weekly_summary

__all__ = [
    "ExecutiveReport",
    "ProofPack",
    "WeeklySummary",
    "build_executive_report",
    "build_proof_pack",
    "build_weekly_summary",
]
