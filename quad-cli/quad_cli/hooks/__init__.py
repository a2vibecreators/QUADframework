"""
QUAD Hooks System
==================

Pre/post hooks for Claude CLI integration.
Future: QUAD VS Code Plugin will use same architecture.

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

from .hook_manager import HookManager, get_hook_manager
from .pre_hook import PreHook
from .post_hook import PostHook
from .hook_config import (
    load_hook_config,
    save_hook_config,
    get_session_id,
    set_session_override,
    get_session_override,
    log_hook_execution
)
from .hook_detector import should_invoke_hook, test_hook
from .claude_integration import intercept_command, load_quad_context

__all__ = [
    # Existing
    "HookManager",
    "PreHook",
    "PostHook",
    "get_hook_manager",
    # New - Config
    "load_hook_config",
    "save_hook_config",
    "get_session_id",
    "set_session_override",
    "get_session_override",
    "log_hook_execution",
    # New - Detection
    "should_invoke_hook",
    "test_hook",
    # New - Integration
    "intercept_command",
    "load_quad_context"
]
