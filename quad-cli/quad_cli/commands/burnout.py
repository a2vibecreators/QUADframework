#!/usr/bin/env python3
"""
QUAD Team Analytics
===================

Team burnout analysis and sprint charts.

Usage:
  quad burnout              # Show team burnout analysis
  quad chart velocity       # Show sprint velocity chart
  quad chart tickets        # Show ticket status chart

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List

# Config paths
QUAD_CONFIG_DIR = Path.home() / ".quad"
QUAD_CONFIG_FILE = QUAD_CONFIG_DIR / "config.json"


class Console:
    """Simple console utilities"""

    @staticmethod
    def header(text: str):
        print(f"\n  {text}")
        print(f"  {'─' * len(text)}\n")

    @staticmethod
    def success(text: str):
        print(f"  ✓ {text}")

    @staticmethod
    def info(text: str):
        print(f"  → {text}")

    @staticmethod
    def error(text: str):
        print(f"  ✗ {text}")

    @staticmethod
    def warn(text: str):
        print(f"  ⚠ {text}")


def load_global_config() -> Optional[Dict]:
    """Load global config"""
    if QUAD_CONFIG_FILE.exists():
        return json.loads(QUAD_CONFIG_FILE.read_text())
    return None


# ─────────────────────────────────────────────────────────────
# Demo Data
# ─────────────────────────────────────────────────────────────

DEMO_TEAM = [
    {"name": "Pradeep Kumar", "workload": 80, "tickets": 8, "status": "High"},
    {"name": "Manju Singh", "workload": 60, "tickets": 5, "status": "OK"},
    {"name": "Suman Addanki", "workload": 50, "tickets": 4, "status": "OK"},
]

DEMO_SPRINTS = [
    {"sprint": "Sprint 1", "points": 42},
    {"sprint": "Sprint 2", "points": 38},
    {"sprint": "Sprint 3", "points": 35},
    {"sprint": "Sprint 4", "points": 45},
]


# ─────────────────────────────────────────────────────────────
# Burnout Analysis
# ─────────────────────────────────────────────────────────────

def show_burnout():
    """Show team burnout analysis"""
    Console.header("Team Burnout Analysis")

    config = load_global_config()
    org_name = config.get("org_name", "Organization") if config else "Organization"

    Console.info(f"Organization: {org_name}")
    print()

    # Table header
    print("  ┌─────────────────┬───────────┬────────────┐")
    print("  │ Team Member     │ Workload  │ Status     │")
    print("  ├─────────────────┼───────────┼────────────┤")

    # Team data
    for member in DEMO_TEAM:
        name = member["name"][:15].ljust(15)
        workload = member["workload"]

        # Create bar
        filled = int(workload / 10)
        bar = "█" * filled + "░" * (10 - filled)

        # Status with color hint
        status = member["status"]
        if status == "High":
            status_str = f"{workload}% - High"
        else:
            status_str = f"{workload}% - OK"

        print(f"  │ {name} │ {bar}│ {status_str.ljust(10)} │")

    print("  └─────────────────┴───────────┴────────────┘")
    print()

    # Alerts
    high_risk = [m for m in DEMO_TEAM if m["workload"] >= 75]
    if high_risk:
        for member in high_risk:
            Console.warn(f"Alert: {member['name']} is at risk of burnout")
            Console.info(f"  Suggestion: Reassign {member['tickets'] - 4} tickets to others")
            print()


def show_velocity_chart():
    """Show sprint velocity chart"""
    Console.header("Sprint Velocity (Last 4 Sprints)")

    max_points = max(s["points"] for s in DEMO_SPRINTS)

    for sprint in DEMO_SPRINTS:
        name = sprint["sprint"]
        points = sprint["points"]

        # Scale bar to fit
        bar_length = int(points / max_points * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)

        print(f"  {name}: {bar} {points} pts")

    # Stats
    avg = sum(s["points"] for s in DEMO_SPRINTS) / len(DEMO_SPRINTS)
    print()
    print(f"  Average: {avg:.0f} pts/sprint")

    # Trend
    if DEMO_SPRINTS[-1]["points"] > DEMO_SPRINTS[-2]["points"]:
        print("  Trend: ↑ Improving")
    elif DEMO_SPRINTS[-1]["points"] < DEMO_SPRINTS[-2]["points"]:
        print("  Trend: ↓ Declining")
    else:
        print("  Trend: → Stable")

    print()


def show_tickets_chart():
    """Show ticket status pie chart (ASCII)"""
    Console.header("Ticket Status Distribution")

    # Demo data
    statuses = {
        "Done": 45,
        "In Progress": 12,
        "To Do": 23,
        "Blocked": 3
    }

    total = sum(statuses.values())

    for status, count in statuses.items():
        pct = count / total * 100
        bar_len = int(pct / 5)  # 5% = 1 char
        bar = "█" * bar_len

        # Status icons
        icons = {
            "Done": "●",
            "In Progress": "◐",
            "To Do": "○",
            "Blocked": "✗"
        }
        icon = icons.get(status, "○")

        print(f"  {icon} {status.ljust(12)} {bar.ljust(20)} {count} ({pct:.0f}%)")

    print()
    print(f"  Total: {total} tickets")
    print()


def show_workload():
    """Show workload distribution"""
    Console.header("Team Workload Distribution")

    for member in DEMO_TEAM:
        name = member["name"][:20].ljust(20)
        tickets = member["tickets"]
        workload = member["workload"]

        bar_len = tickets
        bar = "▓" * bar_len + "░" * (10 - bar_len)

        print(f"  {name} {bar} {tickets} tickets ({workload}%)")

    print()

    # Suggestions
    Console.info("Recommendations:")
    print("    • Move 2 tickets from Pradeep to Manju")
    print("    • Suman has capacity for 2 more tickets")
    print()


# ─────────────────────────────────────────────────────────────
# Entry Points
# ─────────────────────────────────────────────────────────────

def run_burnout():
    """Entry point for quad burnout"""
    show_burnout()


def run_chart(chart_type: str = None):
    """Entry point for quad chart"""
    if chart_type == "velocity":
        show_velocity_chart()
    elif chart_type == "tickets":
        show_tickets_chart()
    elif chart_type == "workload":
        show_workload()
    else:
        Console.header("QUAD Charts")
        Console.info("quad chart velocity   - Sprint velocity over time")
        Console.info("quad chart tickets    - Ticket status distribution")
        Console.info("quad chart workload   - Team workload distribution")


def main():
    """Command-line entry point"""
    args = sys.argv[1:] if len(sys.argv) > 1 else []

    if not args or args[0] in ("-h", "--help"):
        Console.header("QUAD Analytics")
        Console.info("quad burnout          - Team burnout analysis")
        Console.info("quad chart velocity   - Sprint velocity chart")
        Console.info("quad chart tickets    - Ticket status chart")
        Console.info("quad chart workload   - Workload distribution")
    elif args[0] == "burnout" or (len(args) == 0):
        run_burnout()
    elif args[0] == "chart" and len(args) > 1:
        run_chart(args[1])
    elif args[0] == "velocity":
        show_velocity_chart()
    elif args[0] == "tickets":
        show_tickets_chart()
    elif args[0] == "workload":
        show_workload()
    else:
        run_chart(args[0])


if __name__ == "__main__":
    main()
