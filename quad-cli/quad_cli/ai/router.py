"""
AI Router
=========

Smart routing between AI providers with confidence-based fallback.

Algorithm:
1. Keyword-based task classification
2. Try Gemini first (free)
3. Check confidence score
4. Fallback to Claude if confidence < threshold
5. Return best result

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import json
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

from .gemini import GeminiAPI
from .claude import ClaudeAPI


class TaskClassifier:
    """Classify tasks by complexity using keywords"""

    # Simple tasks: Gemini can handle well
    SIMPLE_KEYWORDS = [
        "list", "show", "explain", "describe", "what is",
        "how does", "define", "summarize", "analyze",
        "classify", "categorize", "extract", "parse"
    ]

    # Complex tasks: Might need Claude
    COMPLEX_KEYWORDS = [
        "generate code", "implement", "refactor", "optimize",
        "architecture", "design pattern", "algorithm",
        "microservices", "distributed", "scale", "security"
    ]

    # Critical tasks: Always use Claude
    CRITICAL_KEYWORDS = [
        "production", "deploy", "critical", "security audit",
        "compliance", "pci-dss", "hipaa", "gdpr"
    ]

    @classmethod
    def classify(cls, task: str) -> Dict[str, Any]:
        """
        Classify task complexity.

        Returns:
            {
                "complexity": "simple" | "complex" | "critical",
                "confidence": 0.0-1.0,
                "recommended_provider": "gemini" | "claude",
                "keywords_matched": [...]
            }
        """
        task_lower = task.lower()

        # Check critical first
        critical_matches = [kw for kw in cls.CRITICAL_KEYWORDS if kw in task_lower]
        if critical_matches:
            return {
                "complexity": "critical",
                "confidence": 1.0,
                "recommended_provider": "claude",
                "keywords_matched": critical_matches,
                "reason": "Critical task requires highest quality"
            }

        # Check complex
        complex_matches = [kw for kw in cls.COMPLEX_KEYWORDS if kw in task_lower]
        if complex_matches:
            return {
                "complexity": "complex",
                "confidence": 0.7,
                "recommended_provider": "gemini",  # Try Gemini first
                "fallback_provider": "claude",
                "keywords_matched": complex_matches,
                "reason": "Complex task, try Gemini first, fallback to Claude"
            }

        # Check simple
        simple_matches = [kw for kw in cls.SIMPLE_KEYWORDS if kw in task_lower]
        if simple_matches:
            return {
                "complexity": "simple",
                "confidence": 0.9,
                "recommended_provider": "gemini",
                "keywords_matched": simple_matches,
                "reason": "Simple task, Gemini sufficient"
            }

        # Default: complex (unknown)
        return {
            "complexity": "complex",
            "confidence": 0.5,
            "recommended_provider": "gemini",
            "fallback_provider": "claude",
            "keywords_matched": [],
            "reason": "Unknown task type, try Gemini first"
        }


class AIRouter:
    """
    Smart AI router with confidence-based fallback.

    Flow:
    1. Classify task (simple/complex/critical)
    2. Route to Gemini or Claude based on classification
    3. Check confidence score in response
    4. Fallback to Claude if confidence < threshold
    """

    def __init__(self, config: Optional[Dict] = None):
        # Load configuration
        if config:
            self.config = config
        else:
            from .config import load_ai_config
            self.config = load_ai_config()

        # Initialize providers
        self.gemini = None
        self.claude = None

        # Confidence threshold for fallback
        self.confidence_threshold = self.config.get("router", {}).get("confidence_threshold", 0.7)

        # Initialize providers based on availability
        self._init_providers()

    def _init_providers(self):
        """Initialize AI providers"""
        # Initialize Gemini
        gemini_key = self.config.get("gemini", {}).get("api_key")
        if gemini_key:
            try:
                self.gemini = GeminiAPI(gemini_key)
            except Exception as e:
                print(f"Warning: Could not initialize Gemini: {e}")

        # Initialize Claude
        claude_key = self.config.get("claude", {}).get("api_key")
        if claude_key:
            try:
                self.claude = ClaudeAPI(claude_key)
            except Exception as e:
                print(f"Warning: Could not initialize Claude: {e}")

    def generate(
        self,
        prompt: str,
        context: Optional[Dict] = None,
        task_hint: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate response with smart routing.

        Args:
            prompt: The prompt to send
            context: Optional context to include
            task_hint: Optional task description for classification

        Returns:
            {
                "result": "...",
                "provider": "gemini" | "claude",
                "confidence": 0.0-1.0,
                "classification": {...},
                "fallback_used": True/False,
                "metadata": {...}
            }
        """

        # Step 1: Classify task
        classification = TaskClassifier.classify(task_hint or prompt)

        print(f"  🎯 Task Classification:")
        print(f"     Complexity: {classification['complexity']}")
        print(f"     Recommended: {classification['recommended_provider']}")
        print(f"     Reason: {classification['reason']}")

        # Step 2: Critical task? Go straight to Claude
        if classification["complexity"] == "critical":
            return self._generate_with_claude(
                prompt, context, classification, fallback_used=False
            )

        # Step 3: Try Gemini first
        if self.gemini:
            print(f"  ⚡ Trying Gemini (free)...")
            gemini_result = self._generate_with_gemini(
                prompt, context, classification, fallback_used=False
            )

            # Step 4: Check confidence
            confidence = gemini_result.get("confidence", 0.0)
            print(f"     Confidence: {confidence:.2f}")

            if confidence >= self.confidence_threshold:
                print(f"  ✓ Gemini confidence sufficient ({confidence:.2f} >= {self.confidence_threshold})")
                return gemini_result

            # Step 5: Confidence too low, fallback to Claude
            if self.claude and self.config.get("fallback_enabled", True):
                print(f"  ⚠ Gemini confidence low ({confidence:.2f} < {self.confidence_threshold})")
                print(f"  🔄 Falling back to Claude...")
                return self._generate_with_claude(
                    prompt, context, classification, fallback_used=True
                )
            else:
                print(f"  ⚠ Gemini confidence low, but no Claude fallback available")
                return gemini_result

        # Step 6: No Gemini? Use Claude directly
        elif self.claude:
            print(f"  🚀 Using Claude (Gemini not available)...")
            return self._generate_with_claude(
                prompt, context, classification, fallback_used=False
            )

        # Step 7: No providers available
        else:
            return {
                "result": None,
                "error": "No AI providers configured. Set API keys for Gemini or Claude.",
                "provider": None,
                "confidence": 0.0,
                "classification": classification
            }

    def _generate_with_gemini(
        self,
        prompt: str,
        context: Optional[Dict],
        classification: Dict,
        fallback_used: bool
    ) -> Dict[str, Any]:
        """Generate with Gemini"""
        try:
            # Add context to prompt if provided
            full_prompt = self._build_prompt(prompt, context)

            # Generate
            result = self.gemini.generate(full_prompt)

            # Extract confidence (Gemini provides this in some responses)
            confidence = self._extract_confidence(result)

            return {
                "result": result,
                "provider": "gemini",
                "confidence": confidence,
                "classification": classification,
                "fallback_used": fallback_used,
                "metadata": {
                    "model": self.config.get("gemini", {}).get("model"),
                    "cost": 0.0  # Free tier
                }
            }

        except Exception as e:
            print(f"  ✗ Gemini error: {e}")
            # If Gemini fails, try Claude
            if self.claude and self.config.get("fallback_enabled", True):
                print(f"  🔄 Falling back to Claude due to error...")
                return self._generate_with_claude(
                    prompt, context, classification, fallback_used=True
                )
            else:
                return {
                    "result": None,
                    "error": str(e),
                    "provider": "gemini",
                    "confidence": 0.0,
                    "classification": classification
                }

    def _generate_with_claude(
        self,
        prompt: str,
        context: Optional[Dict],
        classification: Dict,
        fallback_used: bool
    ) -> Dict[str, Any]:
        """Generate with Claude"""
        try:
            # Add context to prompt if provided
            full_prompt = self._build_prompt(prompt, context)

            # Generate
            result = self.claude.generate(full_prompt)

            # Claude always high confidence
            confidence = 0.95

            return {
                "result": result,
                "provider": "claude",
                "confidence": confidence,
                "classification": classification,
                "fallback_used": fallback_used,
                "metadata": {
                    "model": self.config.get("claude", {}).get("model"),
                    "cost_estimate": self._estimate_cost(full_prompt, result)
                }
            }

        except Exception as e:
            return {
                "result": None,
                "error": str(e),
                "provider": "claude",
                "confidence": 0.0,
                "classification": classification,
                "fallback_used": fallback_used
            }

    def _build_prompt(self, prompt: str, context: Optional[Dict]) -> str:
        """Build full prompt with context"""
        if not context:
            return prompt

        context_str = json.dumps(context, indent=2)
        return f"{prompt}\n\nContext:\n{context_str}"

    def _extract_confidence(self, result: str) -> float:
        """
        Extract confidence from result.

        Gemini sometimes includes confidence markers.
        For now, use heuristics.
        """
        # Heuristic: Check for uncertainty markers
        uncertainty_markers = [
            "i'm not sure",
            "i think",
            "maybe",
            "possibly",
            "might be",
            "could be",
            "uncertain"
        ]

        result_lower = str(result).lower()

        # If uncertainty markers present, lower confidence
        for marker in uncertainty_markers:
            if marker in result_lower:
                return 0.6  # Low confidence

        # Check length (very short responses might be uncertain)
        if len(str(result)) < 50:
            return 0.7

        # Default: high confidence
        return 0.85

    def _estimate_cost(self, prompt: str, result: str) -> float:
        """Estimate Claude API cost"""
        # Rough token estimation (4 chars = 1 token)
        input_tokens = len(prompt) / 4
        output_tokens = len(str(result)) / 4

        # Claude pricing (approximate)
        input_cost = (input_tokens / 1000) * 0.015
        output_cost = (output_tokens / 1000) * 0.075

        return round(input_cost + output_cost, 4)


# Singleton instance
_ai_router = None


def get_ai_router() -> AIRouter:
    """Get singleton AIRouter instance"""
    global _ai_router
    if _ai_router is None:
        _ai_router = AIRouter()
    return _ai_router
