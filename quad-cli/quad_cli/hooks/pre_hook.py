"""
Pre-Hook
========

Executes before QUAD command runs.
Captures request context and enriches with historical context.

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from .config import is_hooks_enabled, load_hook_config


class PreHook:
    """Pre-hook for capturing and enriching request context"""

    def __init__(self):
        self.config = load_hook_config()

    def execute(self, command: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute pre-hook before command runs.

        Args:
            command: Command name (e.g., 'story', 'code', 'init')
            args: Command arguments

        Returns:
            Enriched context to be used by command
        """
        if not is_hooks_enabled():
            return {}

        pre_config = self.config.get("hooks", {}).get("pre_hook", {})
        if not pre_config.get("enabled", True):
            return {}

        context = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "args": args,
            "captured_at": "pre_hook"
        }

        # Capture request
        if pre_config.get("capture_request", True):
            context["request"] = self._capture_request(command, args)

        # Enrich with historical context
        if pre_config.get("enrich_context", True):
            context["enriched"] = self._enrich_context(command, args)

        # Log pre-hook execution
        self._log_execution(context)

        return context

    def _capture_request(self, command: str, args: Dict) -> Dict:
        """Capture request details"""
        return {
            "command": command,
            "args": self._sanitize_args(args),
            "timestamp": datetime.now().isoformat()
        }

    def _enrich_context(self, command: str, args: Dict) -> Dict:
        """
        Enrich request with historical context.

        For example:
        - If 'story' command, load past project patterns
        - If 'code' command, load architectural decisions
        - If 'test' command, load past test patterns
        """
        enrichment = {}

        # Load relevant historical context based on command
        if command == "story":
            enrichment["past_projects"] = self._load_past_project_patterns()
        elif command == "code":
            enrichment["architecture_decisions"] = self._load_architecture_context()
        elif command == "init":
            enrichment["preferences"] = self._load_user_preferences()

        return enrichment

    def _load_past_project_patterns(self) -> Dict:
        """Load patterns from past projects"""
        # TODO: Implement context loading from storage
        return {}

    def _load_architecture_context(self) -> Dict:
        """Load architectural decisions from memory"""
        # TODO: Implement context loading from storage
        return {}

    def _load_user_preferences(self) -> Dict:
        """Load user preferences"""
        # TODO: Implement context loading from storage
        return {}

    def _sanitize_args(self, args: Dict) -> Dict:
        """Remove sensitive data from args before logging"""
        sanitized = args.copy()

        # Remove sensitive keys
        sensitive_keys = ["password", "api_key", "secret", "token", "key"]
        for key in sensitive_keys:
            if key in sanitized:
                sanitized[key] = "***REDACTED***"

        return sanitized

    def _log_execution(self, context: Dict):
        """Log pre-hook execution for debugging"""
        log_dir = Path.home() / ".quad" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / "pre_hook.log"

        # Keep log file size manageable (last 1000 lines)
        if log_file.exists():
            lines = log_file.read_text().split("\n")
            if len(lines) > 1000:
                lines = lines[-1000:]
                log_file.write_text("\n".join(lines))

        # Append new log entry
        with log_file.open("a") as f:
            f.write(f"{datetime.now().isoformat()} - {json.dumps(context)}\n")
