"""
Hook Manager
============

Orchestrates pre and post hooks for QUAD commands.

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

from typing import Dict, Any, Optional, Callable
from pathlib import Path

from .pre_hook import PreHook
from .post_hook import PostHook
from .config import is_hooks_enabled


class HookManager:
    """Manages execution of pre and post hooks"""

    def __init__(self):
        self.pre_hook = PreHook()
        self.post_hook = PostHook()

    def execute_with_hooks(
        self,
        command: str,
        args: Dict[str, Any],
        command_func: Callable
    ) -> Any:
        """
        Execute command with pre and post hooks.

        Args:
            command: Command name
            args: Command arguments
            command_func: Function to execute

        Returns:
            Command result
        """
        if not is_hooks_enabled():
            # Hooks disabled, run command directly
            return command_func()

        # PRE-HOOK
        pre_context = self.pre_hook.execute(command, args)

        # MAIN COMMAND (with enriched context)
        try:
            result = command_func()
        except Exception as e:
            # Still run post-hook even on error
            self.post_hook.execute(command, args, {"error": str(e)}, pre_context)
            raise e

        # POST-HOOK
        self.post_hook.execute(command, args, result, pre_context)

        return result

    @staticmethod
    def wrap_command(command_name: str):
        """
        Decorator to wrap a command with hooks.

        Usage:
            @HookManager.wrap_command("story")
            def run_story():
                # command implementation
                pass
        """
        def decorator(func: Callable):
            def wrapper(*args, **kwargs):
                manager = HookManager()
                return manager.execute_with_hooks(
                    command_name,
                    {"args": args, "kwargs": kwargs},
                    lambda: func(*args, **kwargs)
                )
            return wrapper
        return decorator


# Singleton instance
_hook_manager = None


def get_hook_manager() -> HookManager:
    """Get singleton HookManager instance"""
    global _hook_manager
    if _hook_manager is None:
        _hook_manager = HookManager()
    return _hook_manager
