"""
Hook Detection Logic
====================

Determine if a command should be intercepted by QUAD hooks.

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

from typing import Tuple, Dict
from .hook_config import load_hook_config, get_session_id, log_hook_execution


def should_invoke_hook(command: str) -> Tuple[bool, str]:
    """
    Determine if hook should intercept this command.

    Args:
        command: User input string

    Returns:
        Tuple of (should_intercept, reason)
    """
    config = load_hook_config()
    session_id = get_session_id()

    # Check 1: Global enable
    if not config.get("enabled", False):
        reason = "Hooks globally disabled"
        log_hook_execution(command, False, reason)
        return False, reason

    # Check 2: Session override
    session_override = config.get("session_override", {}).get(session_id)
    if session_override is not None:
        if not session_override:
            reason = f"Session {session_id} disabled"
            log_hook_execution(command, False, reason)
            return False, reason
        else:
            # Session explicitly enabled, continue to mode check
            pass

    # Check 3: Mode-based logic
    mode = config.get("mode", "prefix")

    if mode == "disabled":
        reason = "Mode set to disabled"
        log_hook_execution(command, False, reason)
        return False, reason

    elif mode == "prefix":
        prefixes = config.get("prefixes", ["quad-", "quad "])
        cmd_stripped = command.strip()

        for prefix in prefixes:
            if cmd_stripped.startswith(prefix):
                reason = f"Matches prefix '{prefix}'"
                log_hook_execution(command, True, reason)
                return True, reason

        reason = "No prefix match"
        log_hook_execution(command, False, reason)
        return False, reason

    elif mode == "whitelist":
        commands = config.get("commands", [])
        cmd_name = command.strip().split()[0] if command.strip() else ""

        if cmd_name in commands:
            reason = f"Command '{cmd_name}' in whitelist"
            log_hook_execution(command, True, reason)
            return True, reason

        reason = f"Command '{cmd_name}' not in whitelist"
        log_hook_execution(command, False, reason)
        return False, reason

    elif mode == "all":
        reason = "Mode set to all"
        log_hook_execution(command, True, reason)
        return True, reason

    # Unknown mode, default to no intercept
    reason = f"Unknown mode: {mode}"
    log_hook_execution(command, False, reason)
    return False, reason


def test_hook(command: str) -> Dict:
    """
    Test if a command would be intercepted (dry-run).

    Returns detailed information about the decision.
    """
    config = load_hook_config()
    session_id = get_session_id()
    should_intercept, reason = should_invoke_hook(command)

    return {
        "command": command,
        "would_intercept": should_intercept,
        "reason": reason,
        "config": {
            "enabled": config.get("enabled"),
            "mode": config.get("mode"),
            "session_id": session_id,
            "session_override": config.get("session_override", {}).get(session_id)
        }
    }
