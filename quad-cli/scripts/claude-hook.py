#!/usr/bin/env python3
"""
Claude CLI Hook Entry Point
============================

This script is called by Claude CLI's user-prompt-submit hook.
It intercepts commands and routes QUAD commands to QUAD CLI.

Usage:
  Called automatically by Claude CLI via:
  ~/.claude/settings.json:
  {
    "hooks": {
      "user-prompt-submit": {
        "command": "python3 ~/.quad/hooks/claude-hook.py",
        "stdin": true,
        "action": "passthrough"
      }
    }
  }

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import sys
import os

# Add QUAD CLI to path
sys.path.insert(0, os.path.expanduser("~/.quad"))

try:
    from quad_cli.hooks import intercept_command

    # Read user input from stdin
    user_input = sys.stdin.read().strip()

    # Try to intercept
    result = intercept_command(user_input)

    if result:
        # QUAD handled it - return result
        print(result)
    else:
        # Pass through to Claude unchanged
        print(user_input)

    sys.exit(0)

except Exception as e:
    # Error - pass through to Claude
    # Log error for debugging
    error_log = os.path.expanduser("~/.claude/quad-hook-error.log")
    with open(error_log, "a") as f:
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] ERROR: {str(e)}\n")

    # Pass input through unchanged
    user_input = sys.stdin.read().strip()
    print(user_input)
    sys.exit(0)
