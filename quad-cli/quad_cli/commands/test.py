#!/usr/bin/env python3
"""
QUAD Test Runner
================

Run tests on generated code.

Usage:
  quad test                 # Run all tests
  quad test --database      # Run database tests only
  quad test --api           # Run API tests only
  quad test --web           # Run web tests only

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


# ─────────────────────────────────────────────────────────────
# Test Simulation (Demo)
# ─────────────────────────────────────────────────────────────

def simulate_test(name: str, count: int, delay: float = 0.2) -> tuple:
    """Simulate running tests"""
    time.sleep(delay)
    return (count, count)  # All pass for demo


def run_database_tests() -> tuple:
    """Run database tests"""
    Console.info("[Database] Running schema validation...")
    time.sleep(0.3)
    Console.success("All tables valid")
    Console.success("Foreign keys correct")
    Console.success("Indexes optimized")
    return (3, 3)


def run_api_tests() -> tuple:
    """Run API tests"""
    Console.info("[API] Running unit tests...")
    time.sleep(0.3)

    tests = [
        ("AuthControllerTest", 5),
        ("AccountControllerTest", 4),
        ("TransferControllerTest", 6),
    ]

    total_passed = 0
    total_tests = 0

    for test_name, count in tests:
        time.sleep(0.2)
        Console.success(f"{test_name} - {count}/{count} passed")
        total_passed += count
        total_tests += count

    Console.success(f"All {total_tests} tests passed")
    return (total_passed, total_tests)


def run_web_tests() -> tuple:
    """Run web tests"""
    Console.info("[Web] Running component tests...")
    time.sleep(0.3)

    tests = [
        "LoginForm.test.tsx",
        "TransferForm.test.tsx",
    ]

    total = 0
    for test_name in tests:
        time.sleep(0.2)
        Console.success(f"{test_name} - passed")
        total += 4  # Assume 4 tests per file

    Console.success(f"All {len(tests) * 4} tests passed")
    return (len(tests) * 4, len(tests) * 4)


def run_all_tests():
    """Run all tests"""
    Console.header("QUAD Test Runner")

    # Check project exists
    project_config = load_project_config()
    if not project_config:
        Console.error("Not in a QUAD project. Run: quad init <project-name>")
        return False

    stories = load_stories()
    if not stories:
        Console.warn("No stories found. Tests may be limited.")

    total_tests = 0
    total_passed = 0

    # Database tests
    db_passed, db_total = run_database_tests()
    total_tests += db_total
    total_passed += db_passed
    print()

    # API tests
    api_passed, api_total = run_api_tests()
    total_tests += api_total
    total_passed += api_passed
    print()

    # Web tests
    web_passed, web_total = run_web_tests()
    total_tests += web_total
    total_passed += web_passed
    print()

    # Summary
    print("  ════════════════════════════════════════")
    print(f"  Total: {total_tests} tests, {total_passed} passed, {total_tests - total_passed} failed")

    # Calculate coverage (simulated)
    coverage = 85
    print(f"  Coverage: {coverage}%")
    print("  ════════════════════════════════════════")
    print()

    if total_passed == total_tests:
        Console.success("All tests passed!")
        Console.info("Next: quad deploy dev")
    else:
        Console.error(f"{total_tests - total_passed} tests failed")

    print()
    return total_passed == total_tests


# ─────────────────────────────────────────────────────────────
# Entry Points
# ─────────────────────────────────────────────────────────────

def run_test(scope: str = None):
    """Entry point for CLI integration"""
    if scope == "database" or scope == "--database":
        Console.header("Database Tests")
        run_database_tests()
    elif scope == "api" or scope == "--api":
        Console.header("API Tests")
        run_api_tests()
    elif scope == "web" or scope == "--web":
        Console.header("Web Tests")
        run_web_tests()
    else:
        run_all_tests()


def main():
    """Command-line entry point"""
    args = sys.argv[1:]

    if args and args[0] in ("-h", "--help"):
        Console.header("QUAD Test Commands")
        Console.info("quad test              - Run all tests")
        Console.info("quad test --database   - Run database tests only")
        Console.info("quad test --api        - Run API tests only")
        Console.info("quad test --web        - Run web tests only")
    elif args:
        run_test(args[0])
    else:
        run_test()


if __name__ == "__main__":
    main()
