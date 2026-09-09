"""
QUAD AI Integration
===================

Smart AI routing with confidence-based fallback.

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

from .router import AIRouter, get_ai_router
from .gemini import GeminiAPI
from .claude import ClaudeAPI

__all__ = ["AIRouter", "get_ai_router", "GeminiAPI", "ClaudeAPI"]
