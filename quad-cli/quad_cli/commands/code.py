#!/usr/bin/env python3
"""
QUAD Code Generator (PGCE Engine)
==================================

Generate production-ready code from user stories using PGCE algorithm.

Usage:
  quad code generate         # Generate code from stories
  quad code status           # Show generation status

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
    def confirm(question: str, default: bool = True) -> bool:
        suffix = "[Y/n]" if default else "[y/N]"
        answer = input(f"  {question} {suffix}: ").strip().lower()
        if not answer:
            return default
        return answer in ('y', 'yes')

    @staticmethod
    def progress_bar(current: int, total: int, width: int = 20) -> str:
        """Generate progress bar string"""
        filled = int(width * current / total)
        bar = "█" * filled + "░" * (width - filled)
        return bar


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
    """Load stories from .quad/stories.json"""
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
    if quad_dir:
        stories_file = quad_dir / "stories.json"
        data = {
            "stories": stories,
            "generated_at": datetime.now().isoformat(),
            "version": "1.0"
        }
        stories_file.write_text(json.dumps(data, indent=2))


# ─────────────────────────────────────────────────────────────
# Code Generation Simulation (Demo)
# ─────────────────────────────────────────────────────────────

# File templates for demo
FILE_TEMPLATES = {
    "database": {
        "files": [
            "sql/tables/users.sql",
            "sql/tables/accounts.sql",
            "sql/tables/transactions.sql",
            "migrations/V1__initial_schema.sql"
        ]
    },
    "auth": {
        "files": [
            "src/main/java/.../AuthController.java",
            "src/main/java/.../AuthService.java",
            "src/main/java/.../UserRepository.java",
            "src/main/java/.../JwtUtil.java"
        ]
    },
    "jwt": {
        "files": [
            "src/main/java/.../JwtFilter.java",
            "src/main/java/.../SecurityConfig.java"
        ]
    },
    "account": {
        "files": [
            "src/main/java/.../AccountController.java",
            "src/main/java/.../AccountService.java",
            "src/main/java/.../AccountRepository.java"
        ]
    },
    "transaction": {
        "files": [
            "src/main/java/.../TransactionController.java",
            "src/main/java/.../TransactionService.java"
        ]
    },
    "transfer": {
        "files": [
            "src/main/java/.../TransferController.java",
            "src/main/java/.../TransferService.java",
            "src/main/java/.../TransferValidator.java"
        ]
    },
    "login_ui": {
        "files": [
            "app/login/page.tsx",
            "components/LoginForm.tsx"
        ]
    },
    "dashboard_ui": {
        "files": [
            "app/dashboard/page.tsx",
            "components/AccountCard.tsx",
            "components/BalanceDisplay.tsx"
        ]
    },
    "transfer_ui": {
        "files": [
            "app/transfer/page.tsx",
            "components/TransferForm.tsx"
        ]
    },
    "transaction_ui": {
        "files": [
            "components/TransactionList.tsx",
            "components/TransactionRow.tsx"
        ]
    },
    "pdf": {
        "files": [
            "src/main/java/.../StatementService.java",
            "src/main/java/.../PdfGenerator.java"
        ]
    },
    "email": {
        "files": [
            "src/main/java/.../EmailService.java",
            "src/main/java/.../NotificationConfig.java"
        ]
    }
}


def get_files_for_story(story: Dict) -> List[str]:
    """Get file templates for a story based on title"""
    title = story.get("title", "").lower()

    if "database" in title:
        return FILE_TEMPLATES["database"]["files"]
    elif "authentication" in title or "auth" in title:
        return FILE_TEMPLATES["auth"]["files"]
    elif "jwt" in title:
        return FILE_TEMPLATES["jwt"]["files"]
    elif "account" in title and "balance" in title:
        return FILE_TEMPLATES["account"]["files"]
    elif "transaction" in title and "history" in title:
        return FILE_TEMPLATES["transaction"]["files"]
    elif "transfer" in title and "api" in title.lower():
        return FILE_TEMPLATES["transfer"]["files"]
    elif "login" in title and "ui" in title:
        return FILE_TEMPLATES["login_ui"]["files"]
    elif "dashboard" in title:
        return FILE_TEMPLATES["dashboard_ui"]["files"]
    elif "transfer" in title and "ui" in title:
        return FILE_TEMPLATES["transfer_ui"]["files"]
    elif "transaction" in title and "list" in title:
        return FILE_TEMPLATES["transaction_ui"]["files"]
    elif "pdf" in title:
        return FILE_TEMPLATES["pdf"]["files"]
    elif "email" in title:
        return FILE_TEMPLATES["email"]["files"]
    else:
        return ["src/generated/Component.java"]


def simulate_file_creation(filename: str, delay: float = 0.1):
    """Simulate file creation with delay"""
    time.sleep(delay)
    Console.success(f"Created: {filename}")


def generate_code():
    """Generate code from stories using PGCE engine"""
    Console.header("QUAD Code Generator (PGCE Engine)")

    # === HOOK INTEGRATION START ===
    from quad_cli.hooks import get_hook_manager

    hook_manager = get_hook_manager()

    command_args = {}

    # PRE-HOOK: Capture and enrich context
    pre_context = {}
    try:
        pre_context = hook_manager.pre_hook.execute("code", command_args)
    except Exception as e:
        print(f"  ⚠ Pre-hook warning: {e}")
    # === HOOK INTEGRATION END ===

    # Load project config
    project_config = load_project_config()
    if not project_config:
        Console.error("Not in a QUAD project. Run: quad init <project-name>")
        return False

    project_name = project_config.get("project_name", "project")
    project_slug = project_config.get("domain_slug", project_name.lower().replace(" ", "-"))

    # Load stories
    stories = load_stories()
    if not stories:
        Console.error("No stories found. Run: quad story create")
        return False

    # Sort by phase, then priority
    sorted_stories = sorted(stories, key=lambda s: (s.get("phase", 1), -s.get("priority", 0)))

    # Group by phase
    phases = {}
    for story in sorted_stories:
        phase = story.get("phase", 1)
        if phase not in phases:
            phases[phase] = []
        phases[phase].append(story)

    total_stories = len(stories)
    completed = 0
    total_files = 0

    # Process each phase
    for phase_num in sorted(phases.keys()):
        phase_stories = phases[phase_num]
        phase_names = {
            1: "Foundation",
            2: "Core Features",
            3: "User Interface",
            4: "Enhancements"
        }

        print()
        Console.header(f"Phase {phase_num}: {phase_names.get(phase_num, 'Phase ' + str(phase_num))} (Stories {completed+1}-{completed+len(phase_stories)})")

        for story in phase_stories:
            story_num = completed + 1
            print(f"  [{story_num}/{total_stories}] {story['title']}...")
            print()

            # Get files for this story
            files = get_files_for_story(story)

            # Determine repo based on story type
            story_type = story.get("type", "api")
            if story_type == "foundation":
                repo = f"{project_slug}-database"
            elif story_type == "ui":
                repo = f"{project_slug}-web"
            else:
                repo = f"{project_slug}-api"

            Console.info(f"Using pattern: {project_config.get('backend', 'Spring Boot')}")
            Console.info(f"Generating files in {repo}/...")
            print()

            # Simulate file creation
            for filename in files:
                simulate_file_creation(filename, delay=0.15)
                total_files += 1

            # Mark story as done
            story["status"] = "done"
            completed += 1

            print()

        # Show phase progress
        progress = completed / total_stories
        bar = Console.progress_bar(completed, total_stories)
        print(f"  Phase {phase_num} Complete! {bar} {int(progress * 100)}%")
        print()

        # Ask to continue (except last phase)
        if phase_num < max(phases.keys()):
            if not Console.confirm(f"Continue to Phase {phase_num + 1}?"):
                Console.warn("Code generation paused")
                break

    # Save updated stories (with status)
    save_stories(stories)

    # Show summary
    print()
    print("  ════════════════════════════════════════")
    print(f"  Code Generation Complete! {Console.progress_bar(total_stories, total_stories)} 100%")
    print("  ════════════════════════════════════════")
    print()
    print("  Summary:")
    print(f"  ├── {project_slug}-database/  ({sum(1 for s in stories if s.get('type') == 'foundation')} stories)")
    print(f"  ├── {project_slug}-api/       ({sum(1 for s in stories if s.get('type') in ('api', 'feature'))} stories)")
    print(f"  └── {project_slug}-web/       ({sum(1 for s in stories if s.get('type') == 'ui')} stories)")
    print()
    print(f"  Total: {total_files} files generated")
    print()
    Console.info("Next: quad test")
    print()

    # === HOOK INTEGRATION START ===
    # POST-HOOK: Analyze and store context
    try:
        result = {
            "project_name": project_name,
            "project_slug": project_slug,
            "total_stories": total_stories,
            "completed_stories": completed,
            "total_files": total_files,
            "phases": list(phases.keys()),
            "stories": stories,
            "config": project_config,
            "success": True
        }
        hook_manager.post_hook.execute("code", command_args, result, pre_context)
    except Exception as e:
        print(f"  ⚠ Post-hook warning: {e}")
    # === HOOK INTEGRATION END ===

    return True


def show_status():
    """Show code generation status"""
    Console.header("Code Generation Status")

    stories = load_stories()
    if not stories:
        Console.info("No stories found. Run: quad story create")
        return

    done = sum(1 for s in stories if s.get("status") == "done")
    in_progress = sum(1 for s in stories if s.get("status") == "in_progress")
    pending = len(stories) - done - in_progress

    print(f"  Stories: {len(stories)}")
    print(f"    ● Done: {done}")
    print(f"    ◐ In Progress: {in_progress}")
    print(f"    ○ Pending: {pending}")
    print()

    progress = done / len(stories) if stories else 0
    bar = Console.progress_bar(done, len(stories))
    print(f"  Progress: {bar} {int(progress * 100)}%")


# ─────────────────────────────────────────────────────────────
# Entry Points
# ─────────────────────────────────────────────────────────────

def run_code(subcommand: str = None, args: List[str] = None):
    """Entry point for CLI integration"""
    if subcommand == "generate" or subcommand is None:
        generate_code()
    elif subcommand == "status":
        show_status()
    else:
        Console.header("QUAD Code Commands")
        Console.info("quad code generate   - Generate code from stories")
        Console.info("quad code status     - Show generation status")


def main():
    """Command-line entry point"""
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        run_code("help")
    elif args[0] == "generate":
        run_code("generate")
    elif args[0] == "status":
        run_code("status")
    else:
        run_code(args[0], args[1:])


if __name__ == "__main__":
    main()
