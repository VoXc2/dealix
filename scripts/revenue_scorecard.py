#!/usr/bin/env python3
"""
Dealix Revenue Scorecard Generator
Calculates and displays key revenue metrics.
"""

import csv
import json
from datetime import datetime
from pathlib import Path


def load_scorecard(filepath: str) -> list[dict]:
    """Load scorecard CSV."""
    rows = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
    except FileNotFoundError:
        print(f"Warning: {filepath} not found.")
    return rows


def load_pipeline(filepath: str) -> dict:
    """Load pipeline JSON."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def calculate_metrics(scorecard: list[dict], pipeline: dict) -> dict:
    """Calculate key metrics."""
    metrics = {}
    
    for row in scorecard:
        metric_name = row.get('metric', '')
        week_target = row.get('week_target', '0')
        week_actual = row.get('week_actual', '0')
        month_target = row.get('month_target', '0')
        month_actual = row.get('month_actual', '0')
        
        try:
            week_target = float(week_target) if week_target else 0
            week_actual = float(week_actual) if week_actual else 0
            month_target = float(month_target) if month_target else 0
            month_actual = float(month_actual) if month_actual else 0
        except ValueError:
            week_target = week_actual = month_target = month_actual = 0
        
        week_progress = (week_actual / week_target * 100) if week_target > 0 else 0
        month_progress = (month_actual / month_target * 100) if month_target > 0 else 0
        
        metrics[metric_name] = {
            'week_target': week_target,
            'week_actual': week_actual,
            'week_progress': week_progress,
            'month_target': month_target,
            'month_actual': month_actual,
            'month_progress': month_progress,
            'status': row.get('status', 'unknown')
        }
    
    return metrics


def generate_scorecard_report(scorecard_path: str, pipeline_path: str, output_path: str = None):
    """Generate and display revenue scorecard."""
    
    scorecard = load_scorecard(scorecard_path)
    pipeline = load_pipeline(pipeline_path)
    metrics = calculate_metrics(scorecard, pipeline)
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Print scorecard
    print("=" * 80)
    print(f"  DEALIX REVENUE SCORECARD — {today}")
    print("=" * 80)
    print()
    
    print(f"  {'Metric':<30} {'Week Target':>12} {'Actual':>10} {'%':>8} | {'Month Target':>12} {'Actual':>10} {'%':>8}")
    print("  " + "-" * 96)
    
    for metric_name, data in metrics.items():
        week_pct = f"{data['week_progress']:.0f}%" if data['week_target'] > 0 else "N/A"
        month_pct = f"{data['month_progress']:.0f}%" if data['month_target'] > 0 else "N/A"
        
        # Status indicator
        status_icon = {
            'on_track': '✅',
            'behind': '🟡',
            'not_started': '🔴',
            'ahead': '🚀'
        }.get(data['status'], '⬜')
        
        print(f"  {status_icon} {metric_name:<28} {data['week_target']:>12.0f} {data['week_actual']:>10.0f} {week_pct:>8} | {data['month_target']:>12.0f} {data['month_actual']:>10.0f} {month_pct:>8}")
    
    print()
    
    # Pipeline summary
    counts = pipeline.get('counts', {})
    if counts:
        print("  PIPELINE HEALTH:")
        print("  " + "-" * 40)
        for stage, count in counts.items():
            bar = "█" * min(int(count), 50)
            print(f"  {stage:<20} {count:>4} {bar}")
        print()
    
    # Key alerts
    alerts = []
    for metric_name, data in metrics.items():
        if data['week_progress'] < 50 and data['week_target'] > 0 and data['status'] != 'not_started':
            alerts.append(f"  ⚠️  {metric_name}: Week progress at {data['week_progress']:.0f}%")
        if data['status'] == 'not_started' and data['week_target'] > 0:
            alerts.append(f"  🔴 {metric_name}: Not started (target: {data['week_target']:.0f})")
    
    if alerts:
        print("  ALERTS:")
        for alert in alerts:
            print(alert)
        print()
    
    # Summary
    revenue_metric = metrics.get('Revenue collected SAR', {})
    mrr_metric = metrics.get('MRR SAR', {})
    
    print("  " + "=" * 40)
    print(f"  Monthly Revenue Target: {revenue_metric.get('month_target', 0):,.0f} SAR")
    print(f"  Monthly Revenue Actual: {revenue_metric.get('month_actual', 0):,.0f} SAR")
    print(f"  MRR Target: {mrr_metric.get('month_target', 0):,.0f} SAR")
    print(f"  MRR Actual: {mrr_metric.get('month_actual', 0):,.0f} SAR")
    print("  " + "=" * 40)
    
    # Write to file if output path provided
    if output_path:
        report = f"""# Revenue Scorecard — {today}

## Weekly Performance

| Metric | Target | Actual | Progress | Status |
|--------|--------|--------|----------|--------|
"""
        for metric_name, data in metrics.items():
            week_pct = f"{data['week_progress']:.0f}%" if data['week_target'] > 0 else "N/A"
            status = data['status'].replace('_', ' ').title()
            report += f"| {metric_name} | {data['week_target']:.0f} | {data['week_actual']:.0f} | {week_pct} | {status} |\n"
        
        report += f"""
## Pipeline Counts

| Stage | Count |
|-------|-------|
"""
        for stage, count in counts.items():
            report += f"| {stage} | {count} |\n"
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n  ✅ Scorecard report saved: {output_path}")


if __name__ == '__main__':
    base_dir = Path(__file__).parent.parent
    
    generate_scorecard_report(
        scorecard_path=str(base_dir / 'company_os' / 'finance' / 'revenue_scorecard.csv'),
        pipeline_path=str(base_dir / 'company_os' / 'revenue' / 'pipeline.json'),
        output_path=str(base_dir / 'company_os' / 'war_room' / 'SCORECARD_REPORT.md')
    )
