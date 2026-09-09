#!/usr/bin/env python3
"""
QUAD Configuration Management
==============================

Manage QUAD AI configuration.

Usage:
  quad config list                        # List all config
  quad config get <key>                   # Get specific value
  quad config set <key> <value>           # Set value
  quad config set gemini.api_key "KEY"    # Set Gemini API key
  quad config set claude.api_key "KEY"    # Set Claude API key
  quad config set router.mode smart       # Set router mode
  quad config status                      # Show AI status

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import sys
import json
from typing import Optional

from quad_cli.ai.config import (
    load_ai_config,
    save_ai_config,
    get_config_value,
    set_config_value,
    print_ai_status
)


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


def list_config():
    """List all configuration"""
    Console.header("QUAD AI Configuration")

    config = load_ai_config()

    def print_dict(d, indent=0):
        for key, value in d.items():
            if isinstance(value, dict):
                print(f"{'  ' * indent}{key}:")
                print_dict(value, indent + 1)
            else:
                # Mask API keys
                if "api_key" in key.lower() and value:
                    value = f"{value[:10]}...{value[-4:]}" if len(str(value)) > 14 else "***"
                print(f"{'  ' * indent}{key}: {value}")

    print_dict(config)
    print()


def get_value(key: str):
    """Get configuration value"""
    value = get_config_value(key)

    if value is None:
        Console.error(f"Key not found: {key}")
        return

    # Mask API keys
    if "api_key" in key.lower() and value:
        display_value = f"{value[:10]}...{value[-4:]}" if len(str(value)) > 14 else "***"
    else:
        display_value = value

    Console.info(f"{key} = {display_value}")


def set_value(key: str, value: str):
    """Set configuration value"""
    # Try to parse as JSON for booleans/numbers
    try:
        if value.lower() == "true":
            parsed_value = True
        elif value.lower() == "false":
            parsed_value = False
        elif value.lower() == "null":
            parsed_value = None
        elif value.replace(".", "").replace("-", "").isdigit():
            parsed_value = float(value) if "." in value else int(value)
        else:
            parsed_value = value
    except:
        parsed_value = value

    set_config_value(key, parsed_value)
    Console.success(f"Set {key} = {parsed_value}")


def show_status():
    """Show AI configuration status"""
    Console.header("QUAD AI Status")
    print_ai_status()


def show_examples():
    """Show configuration examples"""
    Console.header("QUAD Config Examples")

    examples = [
        ("Set Gemini API key", "quad config set gemini.api_key YOUR_KEY"),
        ("Set Claude API key", "quad config set claude.api_key YOUR_KEY"),
        ("", ""),
        ("Router Modes:", ""),
        ("  Smart routing", "quad config set router.mode smart"),
        ("  Single provider", "quad config set router.mode single"),
        ("  Gemini only", "quad config set router.mode gemini_only"),
        ("  Claude only", "quad config set router.mode claude_only"),
        ("", ""),
        ("Set confidence threshold", "quad config set router.confidence_threshold 0.7"),
        ("Enable/disable fallback", "quad config set router.fallback_enabled true"),
        ("", ""),
        ("Set default provider", "quad config set router.default_provider gemini"),
        ("Change models", "quad config set gemini.model gemini-1.5-pro"),
    ]

    for desc, cmd in examples:
        if desc:
            Console.info(desc)
        if cmd:
            print(f"    {cmd}")
        if not desc and not cmd:
            print()

    print()


def run_config(subcommand: str = None, args: list = None):
    """Entry point for CLI integration"""
    args = args or []

    if subcommand == "list":
        list_config()
    elif subcommand == "get" and args:
        get_value(args[0])
    elif subcommand == "set" and len(args) >= 2:
        key = args[0]
        value = " ".join(args[1:])  # Join in case value has spaces
        set_value(key, value)
    elif subcommand == "status":
        show_status()
    elif subcommand == "examples":
        show_examples()
    else:
        Console.header("QUAD Config Commands")
        Console.info("quad config list                  - List all configuration")
        Console.info("quad config get <key>             - Get specific value")
        Console.info("quad config set <key> <value>     - Set value")
        Console.info("quad config status                - Show AI status")
        Console.info("quad config examples              - Show examples")
        print()
        Console.info("Common keys:")
        Console.info("  router.mode                     - smart, single, gemini_only, claude_only")
        Console.info("  router.confidence_threshold     - 0.0-1.0 (default: 0.7)")
        Console.info("  router.fallback_enabled         - true/false")
        Console.info("  gemini.api_key                  - Your Gemini API key")
        Console.info("  claude.api_key                  - Your Claude API key")
        Console.info("  gemini.model                    - gemini-1.5-flash or gemini-1.5-pro")
        Console.info("  claude.model                    - claude-sonnet-4 or claude-opus-4")
        print()


def main():
    """Command-line entry point"""
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        run_config("help")
    else:
        run_config(args[0], args[1:])


if __name__ == "__main__":
    main()
