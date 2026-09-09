#!/usr/bin/env python3
"""
QUAD Story Generator
====================

Generate user stories from plain English using PGCE algorithm.

Usage:
  quad story create         # Interactive story generation
  quad story list           # List existing stories
  quad story show <id>      # Show story details

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import sys
import os
import json
import time
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

    @staticmethod
    def ask(question: str, default: str = None) -> str:
        if default:
            prompt = f"  {question} [{default}]: "
        else:
            prompt = f"  {question}: "
        answer = input(prompt).strip()
        return answer if answer else default

    @staticmethod
    def ask_multiline(question: str) -> str:
        """Ask for multiline input"""
        print(f"  {question}")
        print("  (Enter blank line to finish)")
        lines = []
        while True:
            line = input("  > ").strip()
            if not line:
                break
            lines.append(line)
        return "\n".join(lines)


def find_project_quad_dir() -> Optional[Path]:
    """Find .quad/ folder by walking up from current directory"""
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        quad_dir = parent / ".quad"
        if quad_dir.exists() and (quad_dir / "config.json").exists():
            return quad_dir
    return None


def load_project_config() -> Optional[Dict]:
    """Load project config from .quad/"""
    quad_dir = find_project_quad_dir()
    if quad_dir:
        config_file = quad_dir / "config.json"
        if config_file.exists():
            return json.loads(config_file.read_text())
    return None


def load_stories() -> List[Dict]:
    """Load existing stories from .quad/stories.json"""
    quad_dir = find_project_quad_dir()
    if quad_dir:
        stories_file = quad_dir / "stories.json"
        if stories_file.exists():
            data = json.loads(stories_file.read_text())
            return data.get("stories", [])
    return []


def save_stories(stories: List[Dict]):
    """Save stories to .quad/stories.json"""
    quad_dir = find_project_quad_dir()
    if not quad_dir:
        Console.error("Not in a QUAD project. Run: quad init <project-name>")
        return False

    stories_file = quad_dir / "stories.json"
    data = {
        "stories": stories,
        "generated_at": datetime.now().isoformat(),
        "version": "1.0"
    }
    stories_file.write_text(json.dumps(data, indent=2))
    return True


# ─────────────────────────────────────────────────────────────
# PGCE Algorithm
# ─────────────────────────────────────────────────────────────

def calculate_pgce_priority(story: Dict, all_stories: List[Dict]) -> float:
    """
    Calculate PGCE priority score.

    Formula: P = (D × 0.5) + (I × 0.3) + (C' × 0.2)

    Where:
    - D = Dependency factor (how many stories depend on this)
    - I = Impact factor (business value)
    - C' = Inverse complexity (simpler = higher priority)
    """
    # Get story attributes
    dependencies = story.get("dependencies", [])
    impact = story.get("impact", 5)  # 1-10
    complexity = story.get("complexity", 5)  # 1-10

    # D: Count how many other stories depend on this one
    story_id = story.get("id")
    dependent_count = sum(
        1 for s in all_stories
        if story_id in s.get("dependencies", [])
    )
    # Normalize D to 0-1 (max 10 dependents = 1.0)
    D = min(dependent_count / 10, 1.0)

    # I: Normalize impact to 0-1
    I = impact / 10

    # C': Inverse complexity (10 - complexity, normalized)
    C_prime = (10 - complexity) / 10

    # Calculate priority
    P = (D * 0.5) + (I * 0.3) + (C_prime * 0.2)

    return round(P, 2)


def assign_phases(stories: List[Dict]) -> List[Dict]:
    """Assign stories to phases based on priority and dependencies"""
    # Sort by priority (descending)
    sorted_stories = sorted(stories, key=lambda s: s.get("priority", 0), reverse=True)

    # Assign phases
    phase_thresholds = [0.7, 0.5, 0.3, 0.0]  # Phase 1, 2, 3, 4

    for story in sorted_stories:
        priority = story.get("priority", 0)
        phase = 4  # Default to phase 4

        for i, threshold in enumerate(phase_thresholds):
            if priority >= threshold:
                phase = i + 1
                break

        story["phase"] = phase

    return sorted_stories


# ─────────────────────────────────────────────────────────────
# Story Generation (Demo - Hardcoded patterns)
# ─────────────────────────────────────────────────────────────

def generate_stories_from_description(description: str, project_config: Dict) -> List[Dict]:
    """
    Generate user stories from description.

    In Phase 1 (demo), this uses pattern matching.
    In Phase 2+, this will call AI API.
    """
    stories = []
    story_id = 1

    project_type = project_config.get("project_type", "fullstack")
    backend = project_config.get("backend", "springboot")
    frontend = project_config.get("frontend", "nextjs")
    database = project_config.get("database", "postgresql")

    # Always start with foundation stories
    stories.append({
        "id": f"STORY-{story_id}",
        "title": "Database schema setup",
        "description": f"Set up {database} database schema with initial tables",
        "type": "foundation",
        "impact": 10,
        "complexity": 3,
        "dependencies": [],
    })
    story_id += 1

    # Auth stories
    if "login" in description.lower() or "auth" in description.lower() or "user" in description.lower():
        stories.append({
            "id": f"STORY-{story_id}",
            "title": "User authentication API",
            "description": "Implement user authentication endpoints (login, register, logout)",
            "type": "api",
            "impact": 9,
            "complexity": 4,
            "dependencies": ["STORY-1"],
        })
        story_id += 1

        stories.append({
            "id": f"STORY-{story_id}",
            "title": "JWT token management",
            "description": "Implement JWT token generation, validation, and refresh",
            "type": "api",
            "impact": 8,
            "complexity": 4,
            "dependencies": ["STORY-1", "STORY-2"],
        })
        story_id += 1

    # Account/balance stories
    if "account" in description.lower() or "balance" in description.lower():
        stories.append({
            "id": f"STORY-{story_id}",
            "title": "Account balance API",
            "description": "Implement account balance retrieval endpoint",
            "type": "api",
            "impact": 7,
            "complexity": 3,
            "dependencies": ["STORY-1"],
        })
        story_id += 1

    # Transaction stories
    if "transaction" in description.lower() or "history" in description.lower():
        stories.append({
            "id": f"STORY-{story_id}",
            "title": "Transaction history API",
            "description": "Implement transaction history endpoint with pagination",
            "type": "api",
            "impact": 7,
            "complexity": 4,
            "dependencies": ["STORY-1"],
        })
        story_id += 1

    # Transfer stories
    if "transfer" in description.lower() or "send" in description.lower() or "payment" in description.lower():
        stories.append({
            "id": f"STORY-{story_id}",
            "title": "Money transfer API",
            "description": "Implement money transfer endpoint with validation",
            "type": "api",
            "impact": 8,
            "complexity": 5,
            "dependencies": ["STORY-1"],
        })
        story_id += 1

    # UI stories (if fullstack or web)
    if project_type in ("fullstack", "web"):
        login_dep = [s["id"] for s in stories if "auth" in s["title"].lower()]

        stories.append({
            "id": f"STORY-{story_id}",
            "title": "Login page UI",
            "description": f"Create login page with {frontend} and form validation",
            "type": "ui",
            "impact": 6,
            "complexity": 3,
            "dependencies": login_dep if login_dep else ["STORY-1"],
        })
        story_id += 1

        stories.append({
            "id": f"STORY-{story_id}",
            "title": "Dashboard UI",
            "description": "Create main dashboard with account summary",
            "type": "ui",
            "impact": 6,
            "complexity": 4,
            "dependencies": [f"STORY-{story_id-1}"],
        })
        story_id += 1

        if "transfer" in description.lower():
            stories.append({
                "id": f"STORY-{story_id}",
                "title": "Transfer form UI",
                "description": "Create money transfer form with validation",
                "type": "ui",
                "impact": 5,
                "complexity": 4,
                "dependencies": [f"STORY-{story_id-1}"],
            })
            story_id += 1

        if "transaction" in description.lower():
            stories.append({
                "id": f"STORY-{story_id}",
                "title": "Transaction list UI",
                "description": "Create transaction history list component",
                "type": "ui",
                "impact": 5,
                "complexity": 3,
                "dependencies": [f"STORY-{story_id-2}"],
            })
            story_id += 1

    # PDF/report stories
    if "pdf" in description.lower() or "statement" in description.lower() or "report" in description.lower():
        stories.append({
            "id": f"STORY-{story_id}",
            "title": "PDF statement generation",
            "description": "Implement PDF statement generation service",
            "type": "feature",
            "impact": 4,
            "complexity": 5,
            "dependencies": ["STORY-1"],
        })
        story_id += 1

    # Email/notification stories
    if "email" in description.lower() or "notification" in description.lower():
        stories.append({
            "id": f"STORY-{story_id}",
            "title": "Email notifications",
            "description": "Implement email notification service",
            "type": "feature",
            "impact": 4,
            "complexity": 4,
            "dependencies": ["STORY-1"],
        })
        story_id += 1

    # Calculate priorities for all stories
    for story in stories:
        story["priority"] = calculate_pgce_priority(story, stories)

    # Assign phases
    stories = assign_phases(stories)

    return stories


# ─────────────────────────────────────────────────────────────
# Commands
# ─────────────────────────────────────────────────────────────

def create_stories():
    """Create stories from user description"""
    Console.header("QUAD Story Generator")

    # Check project exists
    project_config = load_project_config()
    if not project_config:
        Console.error("Not in a QUAD project. Run: quad init <project-name>")
        return False

    Console.info(f"Project: {project_config.get('project_name', 'Unknown')}")
    print()

    # Get description
    print("  Describe what you want to build:")
    description = Console.ask_multiline("Features")

    if not description:
        Console.error("Description required")
        return False

    # === HOOK INTEGRATION START ===
    from quad_cli.hooks import get_hook_manager

    hook_manager = get_hook_manager()

    # Prepare command args for hooks
    command_args = {
        "description": description,
        "project_config": project_config
    }

    # PRE-HOOK: Capture and enrich context
    pre_context = {}
    try:
        pre_context = hook_manager.pre_hook.execute("story", command_args)
    except Exception as e:
        # Don't fail if hooks have issues
        print(f"  ⚠ Pre-hook warning: {e}")

    # === HOOK INTEGRATION END ===

    print()
    Console.info("Generating user stories using PGCE algorithm...")
    time.sleep(0.5)  # Dramatic pause for demo

    Console.info("Analyzing requirements...")
    time.sleep(0.3)

    Console.info("Calculating dependencies...")
    time.sleep(0.3)

    Console.info("Prioritizing by PGCE formula: P = (D × 0.5) + (I × 0.3) + (C' × 0.2)")
    time.sleep(0.3)

    # Generate stories
    stories = generate_stories_from_description(description, project_config)

    print()
    Console.success(f"Generated {len(stories)} stories in priority order:")
    print()

    # Display as table
    print("  ┌────┬─────────────────────────────────┬──────────┬───────┐")
    print("  │ #  │ Story                           │ Priority │ Phase │")
    print("  ├────┼─────────────────────────────────┼──────────┼───────┤")

    for i, story in enumerate(sorted(stories, key=lambda s: s["priority"], reverse=True)):
        title = story["title"][:33].ljust(33)
        priority = f"{story['priority']:.2f}".center(8)
        phase = str(story["phase"]).center(5)
        print(f"  │ {i+1:<2} │ {title} │ {priority} │ {phase} │")

    print("  └────┴─────────────────────────────────┴──────────┴───────┘")

    # Save stories
    save_stories(stories)
    print()
    Console.success(f"Saved {len(stories)} stories to database")

    quad_dir = find_project_quad_dir()
    Console.success(f"Created: {quad_dir}/stories.json")
    print()

    # === HOOK INTEGRATION START ===
    # POST-HOOK: Analyze and store context
    try:
        result = {
            "stories": stories,
            "count": len(stories),
            "success": True
        }
        hook_manager.post_hook.execute("story", command_args, result, pre_context)
    except Exception as e:
        # Don't fail if hooks have issues
        print(f"  ⚠ Post-hook warning: {e}")
    # === HOOK INTEGRATION END ===

    Console.info("Ready to generate code? Run: quad code")
    print()

    return True


def list_stories():
    """List existing stories"""
    Console.header("User Stories")

    stories = load_stories()
    if not stories:
        Console.info("No stories found. Run: quad story create")
        return

    # Group by phase
    phases = {}
    for story in stories:
        phase = story.get("phase", 1)
        if phase not in phases:
            phases[phase] = []
        phases[phase].append(story)

    for phase_num in sorted(phases.keys()):
        print(f"\n  Phase {phase_num}")
        print("  " + "─" * 40)
        for story in phases[phase_num]:
            status_icon = "○"  # pending
            if story.get("status") == "done":
                status_icon = "●"
            elif story.get("status") == "in_progress":
                status_icon = "◐"

            print(f"  {status_icon} [{story['id']}] {story['title']}")
            print(f"      Priority: {story.get('priority', 0):.2f} | Type: {story.get('type', 'unknown')}")


def show_story(story_id: str):
    """Show story details"""
    stories = load_stories()
    story = next((s for s in stories if s["id"] == story_id), None)

    if not story:
        Console.error(f"Story not found: {story_id}")
        return

    Console.header(f"Story: {story['title']}")

    print(f"  ID: {story['id']}")
    print(f"  Type: {story.get('type', 'unknown')}")
    print(f"  Phase: {story.get('phase', 1)}")
    print(f"  Priority: {story.get('priority', 0):.2f}")
    print(f"  Impact: {story.get('impact', 5)}/10")
    print(f"  Complexity: {story.get('complexity', 5)}/10")
    print(f"  Dependencies: {', '.join(story.get('dependencies', [])) or 'None'}")
    print()
    print(f"  Description:")
    print(f"    {story.get('description', '')}")


# ─────────────────────────────────────────────────────────────
# Entry Points
# ─────────────────────────────────────────────────────────────

def run_story(subcommand: str = None, args: List[str] = None):
    """Entry point for CLI integration"""
    args = args or []

    if subcommand == "create" or subcommand is None:
        create_stories()
    elif subcommand == "list":
        list_stories()
    elif subcommand == "show" and args:
        show_story(args[0])
    else:
        Console.header("QUAD Story Commands")
        Console.info("quad story create    - Generate stories from description")
        Console.info("quad story list      - List existing stories")
        Console.info("quad story show <id> - Show story details")


def main():
    """Command-line entry point"""
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        run_story("help")
    elif args[0] == "create":
        run_story("create")
    elif args[0] == "list":
        run_story("list")
    elif args[0] == "show" and len(args) > 1:
        run_story("show", args[1:])
    else:
        run_story(args[0], args[1:])


if __name__ == "__main__":
    main()
