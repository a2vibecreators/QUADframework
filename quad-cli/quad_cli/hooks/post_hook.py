"""
Post-Hook
=========

Executes after QUAD command completes.
Captures response, analyzes context, and stores in appropriate context trees.

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from .config import (
    is_hooks_enabled,
    load_hook_config,
    is_topic_excluded,
    get_context_analysis_config
)


class PostHook:
    """Post-hook for capturing and analyzing response context"""

    def __init__(self):
        self.config = load_hook_config()

    def execute(
        self,
        command: str,
        args: Dict[str, Any],
        result: Any,
        pre_context: Optional[Dict] = None
    ):
        """
        Execute post-hook after command completes.

        Args:
            command: Command name
            args: Command arguments
            result: Command result
            pre_context: Context from pre-hook
        """
        if not is_hooks_enabled():
            return

        post_config = self.config.get("hooks", {}).get("post_hook", {})
        if not post_config.get("enabled", True):
            return

        context = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "captured_at": "post_hook"
        }

        # Capture response
        if post_config.get("capture_response", True):
            context["response"] = self._capture_response(command, result)

        # Analyze context
        if post_config.get("analyze_context", True):
            analysis = self._analyze_context(command, args, result, pre_context)
            context["analysis"] = analysis

            # Store context in appropriate trees
            if post_config.get("store_context", True):
                self._store_context(analysis)

        # Log post-hook execution
        self._log_execution(context)

    def _capture_response(self, command: str, result: Any) -> Dict:
        """Capture response details"""
        return {
            "command": command,
            "result_type": str(type(result)),
            "timestamp": datetime.now().isoformat(),
            # Don't store full result (could be huge), just metadata
            "success": self._is_success(result)
        }

    def _is_success(self, result: Any) -> bool:
        """Determine if command was successful"""
        if isinstance(result, dict):
            return result.get("success", True)
        if isinstance(result, bool):
            return result
        return True  # Default to success

    def _analyze_context(
        self,
        command: str,
        args: Dict,
        result: Any,
        pre_context: Optional[Dict]
    ) -> Dict:
        """
        Analyze context using AI.

        This will extract:
        - Topics discussed
        - Decisions made
        - Preferences expressed
        - Information to remember
        """
        analysis_config = get_context_analysis_config()

        if not analysis_config.get("enabled", True):
            return {}

        # Try AI-powered analysis first
        try:
            from quad_cli.ai import get_ai_router

            router = get_ai_router()

            # Use AI to analyze context
            # This uses smart routing (Gemini first, Claude fallback)
            ai_result = router.generate(
                prompt=f"""
Analyze this QUAD command execution and extract context.

Command: {command}
Arguments: {json.dumps(args, indent=2)}
Result: {json.dumps(str(result)[:1000], indent=2)}

Extract and return JSON:
{{
  "topics": ["project", "finance", "health", "preferences", "memory"],
  "decisions": [{{"type": "tech_stack", "value": "Spring Boot"}}],
  "preferences": [{{"type": "framework", "value": "React"}}],
  "memory": {{"key": "value"}}
}}
                """,
                task_hint="analyze context"  # Hints it's a simple analysis task
            )

            # Parse AI result
            if ai_result.get("result"):
                # If result is string, try to parse as JSON
                result_text = ai_result["result"]
                if isinstance(result_text, str):
                    try:
                        return json.loads(result_text)
                    except:
                        pass

            # If AI failed or returned non-JSON, fallback to rule-based
            return self._rule_based_analysis(command, args, result)

        except Exception as e:
            # AI analysis failed, use rule-based fallback
            print(f"  ⚠ AI analysis failed: {e}, using rule-based")
            return self._rule_based_analysis(command, args, result)

    def _rule_based_analysis(self, command: str, args: Dict, result: Any) -> Dict:
        """
        Rule-based context extraction.
        TODO: Replace with AI analysis using Gemini.
        """
        analysis = {
            "topics": [],
            "decisions": [],
            "preferences": [],
            "memory": {}
        }

        # Extract based on command type
        if command == "init":
            analysis["topics"].append("project")
            analysis["decisions"].append({
                "type": "tech_stack",
                "project_type": args.get("project_type"),
                "frontend": args.get("frontend"),
                "backend": args.get("backend"),
                "database": args.get("database")
            })

        elif command == "story":
            analysis["topics"].append("project")
            if isinstance(result, dict) and "stories" in result:
                analysis["memory"]["story_patterns"] = {
                    "count": len(result.get("stories", [])),
                    "generated_at": datetime.now().isoformat()
                }

        elif command == "code":
            analysis["topics"].append("project")
            analysis["memory"]["code_generation"] = {
                "timestamp": datetime.now().isoformat()
            }

        return analysis

    def _store_context(self, analysis: Dict):
        """
        Store analyzed context in appropriate context trees.

        Context trees:
        - project: .quad/project-memory.json
        - health: ~/.quad/contexts/health.json
        - finance: ~/.quad/contexts/finance.json
        - preferences: ~/.quad/contexts/preferences.json
        - memory: ~/.quad/contexts/memory.json
        """
        for topic in analysis.get("topics", []):
            if is_topic_excluded(topic):
                continue

            # TODO: Implement actual context storage
            # For now, just log what would be stored
            self._log_context_storage(topic, analysis)

    def _log_context_storage(self, topic: str, analysis: Dict):
        """Log what context would be stored (for debugging)"""
        log_dir = Path.home() / ".quad" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / "context_storage.log"

        with log_file.open("a") as f:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "topic": topic,
                "analysis": analysis
            }
            f.write(f"{json.dumps(entry)}\n")

    def _log_execution(self, context: Dict):
        """Log post-hook execution for debugging"""
        log_dir = Path.home() / ".quad" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / "post_hook.log"

        # Keep log file size manageable
        if log_file.exists():
            lines = log_file.read_text().split("\n")
            if len(lines) > 1000:
                lines = lines[-1000:]
                log_file.write_text("\n".join(lines))

        # Append new log entry
        with log_file.open("a") as f:
            f.write(f"{datetime.now().isoformat()} - {json.dumps(context)}\n")
