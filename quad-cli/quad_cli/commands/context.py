#!/usr/bin/env python3
"""
QUAD Context Management
=======================

Manage context memory system.

Usage:
  quad context list               # List all contexts
  quad context show health        # Show specific context
  quad context enable health      # Enable context
  quad context disable health     # Disable context
  quad context clear health       # Clear specific context
  quad context clear --all        # Clear all contexts
  quad context search "banking"   # Search all contexts
  quad context export health.json # Export context
  quad context import health.json # Import context

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import sys
import json
from pathlib import Path
from typing import Optional

from quad_cli.contexts import ContextManager, ContextType, CONTEXT_TYPES
from quad_cli.hooks.config import load_hook_config, save_hook_config


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


def list_contexts():
    """List all context types and their status"""
    Console.header("QUAD Contexts")

    manager = ContextManager()
    summaries = manager.get_all_summaries()

    print("  ┌─────────────┬──────────┬──────────┬────────────────────────┐")
    print("  │ Context     │ Enabled  │ Entries  │ Last Updated           │")
    print("  ├─────────────┼──────────┼──────────┼────────────────────────┤")

    for context_type, summary in summaries.items():
        enabled = "✓" if CONTEXT_TYPES[ContextType(context_type)]["enabled"] else "✗"
        entries = str(summary["total_entries"]).center(8)
        last_updated = summary.get("last_updated", "Never")[:19] if summary.get("last_updated") else "Never"

        print(f"  │ {context_type.ljust(11)} │ {enabled.center(8)} │ {entries} │ {last_updated.ljust(22)} │")

    print("  └─────────────┴──────────┴──────────┴────────────────────────┘")
    print()
    Console.info("Use 'quad context show <name>' to view details")
    print()


def show_context(context_name: str):
    """Show details of specific context"""
    try:
        context_type = ContextType(context_name.lower())
    except ValueError:
        Console.error(f"Unknown context: {context_name}")
        Console.info("Available contexts: project, health, finance, preferences, memory")
        return

    Console.header(f"Context: {context_name}")

    manager = ContextManager()
    summary = manager.get_context_summary(context_type)

    Console.info(f"Type: {summary['context_type']}")
    Console.info(f"Entries: {summary['total_entries']}")
    Console.info(f"Storage: {summary['storage_path']}")
    Console.info(f"Created: {summary.get('created_at', 'Unknown')}")
    Console.info(f"Updated: {summary.get('last_updated', 'Unknown')}")

    # Show recent entries
    if summary['total_entries'] > 0:
        print()
        Console.info("Recent entries:")
        store = manager.stores[context_type]
        context = store.load()
        entries = context.get("entries", [])[-5:]  # Last 5 entries

        for i, entry in enumerate(entries, 1):
            timestamp = entry.get("timestamp", "Unknown")[:19]
            text = entry.get("text", "")[:50]
            print(f"\n  {i}. [{timestamp}]")
            print(f"     {text}...")

    print()


def enable_context(context_name: str):
    """Enable specific context"""
    try:
        context_type = ContextType(context_name.lower())
    except ValueError:
        Console.error(f"Unknown context: {context_name}")
        return

    CONTEXT_TYPES[context_type]["enabled"] = True

    # Persist to config
    config = load_hook_config()
    if "enabled_contexts" not in config:
        config["enabled_contexts"] = []
    if context_name.lower() not in config["enabled_contexts"]:
        config["enabled_contexts"].append(context_name.lower())
    save_hook_config(config)

    Console.success(f"Enabled context: {context_name}")


def disable_context(context_name: str):
    """Disable specific context"""
    try:
        context_type = ContextType(context_name.lower())
    except ValueError:
        Console.error(f"Unknown context: {context_name}")
        return

    CONTEXT_TYPES[context_type]["enabled"] = False

    # Persist to config
    config = load_hook_config()
    if "enabled_contexts" in config and context_name.lower() in config["enabled_contexts"]:
        config["enabled_contexts"].remove(context_name.lower())
    save_hook_config(config)

    Console.success(f"Disabled context: {context_name}")


def clear_context(context_name: Optional[str] = None, clear_all: bool = False):
    """Clear context data"""
    manager = ContextManager()

    if clear_all:
        Console.warn("This will clear ALL contexts!")
        confirm = input("  Type 'yes' to confirm: ")
        if confirm.lower() != "yes":
            Console.info("Cancelled")
            return

        manager.clear_all()
        Console.success("Cleared all contexts")
        return

    if not context_name:
        Console.error("Specify context name or use --all")
        return

    try:
        context_type = ContextType(context_name.lower())
    except ValueError:
        Console.error(f"Unknown context: {context_name}")
        return

    manager.clear_context(context_type)
    Console.success(f"Cleared context: {context_name}")


def search_contexts(query: str):
    """Search all contexts"""
    Console.header(f"Search: {query}")

    manager = ContextManager()
    results = manager.search_all(query, limit=5)

    if not results:
        Console.info("No results found")
        return

    for context_type, matches in results.items():
        print(f"\n  {context_type.value.upper()}")
        print(f"  {'-' * 40}")

        for i, entry in enumerate(matches, 1):
            timestamp = entry.get("timestamp", "Unknown")[:19]
            text = entry.get("text", "")[:100]
            print(f"\n  {i}. [{timestamp}]")
            print(f"     {text}...")

    print()


def export_context(context_name: str, output_path: str):
    """Export context to JSON"""
    try:
        context_type = ContextType(context_name.lower())
    except ValueError:
        Console.error(f"Unknown context: {context_name}")
        return

    manager = ContextManager()
    manager.export_context(context_type, output_path)
    Console.success(f"Exported {context_name} to {output_path}")


def import_context(context_name: str, input_path: str):
    """Import context from JSON"""
    try:
        context_type = ContextType(context_name.lower())
    except ValueError:
        Console.error(f"Unknown context: {context_name}")
        return

    if not Path(input_path).exists():
        Console.error(f"File not found: {input_path}")
        return

    manager = ContextManager()
    manager.import_context(context_type, input_path)
    Console.success(f"Imported {input_path} to {context_name}")


def run_context(subcommand: str = None, args: list = None):
    """Entry point for CLI integration"""
    args = args or []

    if subcommand == "list":
        list_contexts()
    elif subcommand == "show" and args:
        show_context(args[0])
    elif subcommand == "enable" and args:
        enable_context(args[0])
    elif subcommand == "disable" and args:
        disable_context(args[0])
    elif subcommand == "clear":
        if args and args[0] == "--all":
            clear_context(clear_all=True)
        elif args:
            clear_context(args[0])
        else:
            Console.error("Specify context name or use --all")
    elif subcommand == "search" and args:
        search_contexts(" ".join(args))
    elif subcommand == "export" and len(args) >= 2:
        export_context(args[0], args[1])
    elif subcommand == "import" and len(args) >= 2:
        import_context(args[0], args[1])
    else:
        Console.header("QUAD Context Commands")
        Console.info("quad context list               - List all contexts")
        Console.info("quad context show <name>        - Show context details")
        Console.info("quad context enable <name>      - Enable context")
        Console.info("quad context disable <name>     - Disable context")
        Console.info("quad context clear <name>       - Clear specific context")
        Console.info("quad context clear --all        - Clear all contexts")
        Console.info("quad context search <query>     - Search contexts")
        Console.info("quad context export <name> <file> - Export context")
        Console.info("quad context import <name> <file> - Import context")
        print()
        Console.info("Available contexts: project, health, finance, preferences, memory")
        print()


def main():
    """Command-line entry point"""
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        run_context("help")
    else:
        run_context(args[0], args[1:])


if __name__ == "__main__":
    main()
