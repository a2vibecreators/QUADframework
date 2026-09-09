"""
Claude CLI Integration
======================

Intercept commands in Claude CLI and route to QUAD.

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import subprocess
from pathlib import Path
from typing import Optional, Dict
from .hook_detector import should_invoke_hook
from .hook_config import load_hook_config


def execute_quad_command(command: str) -> Dict:
    """
    Execute QUAD CLI command.

    Args:
        command: QUAD command (e.g., "quad init banking-app")

    Returns:
        Dict with stdout, stderr, exit_code, success
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "success": result.returncode == 0
        }

    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Command timed out after 5 minutes",
            "exit_code": 124,
            "success": False
        }

    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Error executing command: {str(e)}",
            "exit_code": 1,
            "success": False
        }


def load_quad_context() -> str:
    """
    Load QUAD context for Claude.

    Returns formatted context summary.
    """
    try:
        from quad_cli.contexts import ContextManager, ContextType

        context_mgr = ContextManager()

        # Get recent entries from all contexts
        contexts = []

        for context_type in [ContextType.PROJECT, ContextType.PREFERENCES]:
            store = context_mgr.get_store(context_type)
            data = store.load()
            entries = data.get("entries", [])

            if entries:
                # Get last 3 entries
                recent = entries[-3:]
                contexts.append({
                    "type": context_type.value,
                    "count": len(entries),
                    "recent": recent
                })

        if not contexts:
            return "[QUAD Context: No context available]"

        # Format context
        lines = ["[QUAD Context]"]

        for ctx in contexts:
            lines.append(f"  {ctx['type'].title()}: {ctx['count']} entries")

            for entry in ctx["recent"]:
                topics = entry.get("topics", [])
                if topics:
                    lines.append(f"    - Topics: {', '.join(topics[:3])}")

        return "\n".join(lines)

    except Exception as e:
        return f"[QUAD Context: Error loading context - {str(e)}]"


def intercept_command(user_input: str) -> Optional[str]:
    """
    Main hook function called by Claude CLI.

    Args:
        user_input: User's input string

    Returns:
        QUAD result if intercepted, None if pass-through
    """
    # Check if should intercept
    should_intercept, reason = should_invoke_hook(user_input)

    if not should_intercept:
        return None

    # Execute QUAD command
    result = execute_quad_command(user_input)

    if result["success"]:
        # Success - return output
        output = result["stdout"]

        # Load context if enabled
        config = load_hook_config()
        if config.get("auto_context", True):
            context = load_quad_context()
            output = f"{output}\n\n{context}"

        return output

    else:
        # Error - check fallback behavior
        config = load_hook_config()
        fallback = config.get("fallback", "direct")

        if fallback == "direct":
            # Pass through to Claude
            return None
        else:
            # Show error
            return f"QUAD Error: {result['stderr']}"


def format_context_for_claude(context_data: Dict) -> str:
    """
    Format QUAD context in a way Claude can understand.

    Args:
        context_data: Context data from QUAD

    Returns:
        Formatted markdown string
    """
    lines = ["## QUAD Context"]
    lines.append("")

    # Project info
    if "project" in context_data:
        lines.append("### Project")
        project = context_data["project"]
        if "name" in project:
            lines.append(f"- **Name:** {project['name']}")
        if "type" in project:
            lines.append(f"- **Type:** {project['type']}")
        if "stack" in project:
            lines.append(f"- **Stack:** {', '.join(project['stack'])}")
        lines.append("")

    # Recent activity
    if "recent" in context_data:
        lines.append("### Recent Activity")
        for activity in context_data["recent"]:
            lines.append(f"- {activity}")
        lines.append("")

    return "\n".join(lines)
