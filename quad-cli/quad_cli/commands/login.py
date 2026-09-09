#!/usr/bin/env python3
"""
QUAD Login Command
==================

Simple login for QUAD CLI.

Usage:
  quad login                  # Interactive login
  quad login --status         # Show current login
  quad login --logout         # Logout

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict

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


def save_config(config: Dict):
    """Save config to ~/.quad/config.json"""
    QUAD_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    QUAD_CONFIG_FILE.write_text(json.dumps(config, indent=2))


def load_config() -> Optional[Dict]:
    """Load config from ~/.quad/config.json"""
    if QUAD_CONFIG_FILE.exists():
        try:
            return json.loads(QUAD_CONFIG_FILE.read_text())
        except:
            return None
    return None


def login_simple():
    """Simple login - just ask for name"""
    Console.header("QUAD Login")

    name = Console.ask("Your name")
    if not name:
        Console.error("Name required")
        return False

    config = {
        "user_name": name,
        "logged_in_at": datetime.now().isoformat(),
    }
    save_config(config)

    print()
    Console.success(f"Welcome, {name}!")
    Console.info(f"Config saved to: {QUAD_CONFIG_FILE}")
    return True


def show_current_login():
    """Show current login status"""
    config = load_config()

    Console.header("Current Login")

    if not config:
        Console.warn("Not logged in")
        Console.info("Run: quad login")
        return

    if config.get("user_name"):
        Console.info(f"User: {config['user_name']}")
    if config.get("logged_in_at"):
        Console.info(f"Since: {config['logged_in_at'][:10]}")


def logout():
    """Logout - remove config"""
    Console.header("QUAD Logout")

    if QUAD_CONFIG_FILE.exists():
        QUAD_CONFIG_FILE.unlink()
        Console.success("Logged out successfully")
    else:
        Console.info("Not logged in")


def run_login(status: bool = False, do_logout: bool = False, **kwargs):
    """Entry point for CLI integration"""

    if do_logout:
        logout()
    elif status:
        show_current_login()
    else:
        login_simple()


def main():
    """Command-line entry point"""
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ("-s", "--status", "status"):
            run_login(status=True)
        elif arg in ("logout", "--logout"):
            run_login(do_logout=True)
        elif arg in ("-h", "--help"):
            print(__doc__)
        else:
            run_login()
    else:
        run_login()


if __name__ == "__main__":
    main()
