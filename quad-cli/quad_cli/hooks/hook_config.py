"""
Hook Configuration Management
==============================

Manage Claude CLI hook configuration.

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


def get_config_path() -> Path:
    """Get path to hook configuration file"""
    claude_dir = Path.home() / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    return claude_dir / "quad-hooks.json"


def get_log_path() -> Path:
    """Get path to hook log file"""
    claude_dir = Path.home() / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    return claude_dir / "quad-hooks.log"


def load_hook_config() -> Dict:
    """
    Load QUAD hook configuration.

    Returns default config if file doesn't exist.
    """
    config_path = get_config_path()

    if not config_path.exists():
        return get_default_config()

    try:
        return json.loads(config_path.read_text())
    except Exception:
        # If config is corrupted, return default
        return get_default_config()


def save_hook_config(config: Dict):
    """Save hook configuration"""
    config_path = get_config_path()
    config_path.write_text(json.dumps(config, indent=2))


def get_default_config() -> Dict:
    """Get default hook configuration"""
    return {
        "enabled": False,
        "mode": "prefix",
        "prefixes": ["quad-", "quad "],
        "commands": ["init", "story", "code", "test", "doc"],
        "session_override": {},
        "logging": {
            "enabled": True,
            "path": str(get_log_path())
        },
        "auto_context": True,
        "fallback": "direct"
    }


def get_session_id() -> str:
    """
    Get current Claude CLI session ID.

    Tries multiple methods:
    1. Environment variable CLAUDE_SESSION_ID
    2. .claude/current-session file
    3. Process ID (fallback)
    """
    # Method 1: Environment variable
    session_id = os.environ.get("CLAUDE_SESSION_ID")
    if session_id:
        return session_id

    # Method 2: Session file
    session_file = Path.home() / ".claude" / "current-session"
    if session_file.exists():
        try:
            return session_file.read_text().strip()
        except Exception:
            pass

    # Method 3: Process ID (fallback)
    return f"pid-{os.getpid()}"


def set_session_override(session_id: str, enabled: bool):
    """Set session-specific override"""
    config = load_hook_config()

    if "session_override" not in config:
        config["session_override"] = {}

    config["session_override"][session_id] = enabled
    save_hook_config(config)


def get_session_override(session_id: str) -> Optional[bool]:
    """Get session-specific override"""
    config = load_hook_config()
    return config.get("session_override", {}).get(session_id)


def log_hook_execution(command: str, intercepted: bool, reason: str = ""):
    """Log hook execution for debugging"""
    config = load_hook_config()

    if not config.get("logging", {}).get("enabled", False):
        return

    log_path = Path(config["logging"]["path"]).expanduser()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().isoformat()
    status = "INTERCEPTED" if intercepted else "PASSED"
    log_line = f"[{timestamp}] {status}: {command}"

    if reason:
        log_line += f" ({reason})"

    log_line += "\n"

    with log_path.open("a") as f:
        f.write(log_line)


def clear_logs():
    """Clear hook execution logs"""
    log_path = get_log_path()
    if log_path.exists():
        log_path.unlink()


def get_logs(tail: int = 50) -> str:
    """Get recent log entries"""
    log_path = get_log_path()

    if not log_path.exists():
        return "No logs found"

    with log_path.open("r") as f:
        lines = f.readlines()

    if tail > 0:
        lines = lines[-tail:]

    return "".join(lines)


def add_prefix(prefix: str):
    """Add a prefix to the prefix list"""
    config = load_hook_config()

    if "prefixes" not in config:
        config["prefixes"] = []

    if prefix not in config["prefixes"]:
        config["prefixes"].append(prefix)
        save_hook_config(config)
        return True

    return False


def remove_prefix(prefix: str):
    """Remove a prefix from the prefix list"""
    config = load_hook_config()

    if "prefixes" in config and prefix in config["prefixes"]:
        config["prefixes"].remove(prefix)
        save_hook_config(config)
        return True

    return False


def add_whitelist_command(command: str):
    """Add a command to the whitelist"""
    config = load_hook_config()

    if "commands" not in config:
        config["commands"] = []

    if command not in config["commands"]:
        config["commands"].append(command)
        save_hook_config(config)
        return True

    return False


def remove_whitelist_command(command: str):
    """Remove a command from the whitelist"""
    config = load_hook_config()

    if "commands" in config and command in config["commands"]:
        config["commands"].remove(command)
        save_hook_config(config)
        return True

    return False
