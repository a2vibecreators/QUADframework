"""
Importance Scoring Module
=========================

AI-powered importance scoring with pattern learning.
Uses Gemini to rate input importance, learns from user adjustments.

Patent Pending: Adaptive importance scoring with user feedback learning

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict

# TODO: Add Gemini API client import
# from google.generativeai import GenerativeModel


@dataclass
class ImportanceAdjustment:
    """Historical importance adjustment"""
    gemini_suggested: int
    user_adjusted: int
    topic: str
    context: str
    timestamp: str
    adjustment_diff: int  # positive = user scored higher, negative = user scored lower


class ImportanceScorer:
    """
    AI-powered importance scoring system.

    Uses Gemini to rate input importance, learns from user patterns.
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize importance scorer.

        Args:
            config_path: Path to .quad/hook-config.json
        """
        self.config_path = config_path or Path.home() / ".quad" / "hook-config.json"
        self.config = self._load_config()
        self.adjustment_history: List[ImportanceAdjustment] = []

        # TODO: Initialize Gemini client
        # self.gemini_model = self._init_gemini()

    def _load_config(self) -> Dict[str, Any]:
        """Load importance scoring configuration"""
        if not self.config_path.exists():
            return self._get_default_config()

        with open(self.config_path, 'r') as f:
            config = json.load(f)
            return config.get('importanceScoring', self._get_default_config())

    def _get_default_config(self) -> Dict[str, Any]:
        """Default importance scoring configuration"""
        return {
            "enabled": True,
            "threshold": 5,
            "scale": {"min": 1, "max": 10},
            "geminiConfig": {
                "model": "gemini-2.0-flash-thinking-exp-1219",
                "promptTemplate": """Rate importance (1-10) of this user input based on current work context.

Current Project: {{project}}
Current Work: {{currentWork}}
User Input: {{userInput}}

Consider:
- Relevance to current task
- Decision-making impact
- Long-term value
- Technical complexity

Respond with just a number 1-10."""
            },
            "allowManualOverride": True,
            "learnFromAdjustments": True
        }

    def _init_gemini(self):
        """Initialize Gemini API client"""
        # TODO: Initialize Gemini client
        # api_key = os.getenv('GEMINI_API_KEY')
        # return GenerativeModel(self.config['geminiConfig']['model'])
        pass

    async def score_importance(
        self,
        user_input: str,
        project: str,
        current_work: str,
        context: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Score input importance using Gemini + pattern learning.

        Args:
            user_input: User's input text
            project: Current project name
            current_work: Description of current work
            context: Additional context

        Returns:
            Importance score (1-10)
        """
        if not self.config.get('enabled', True):
            return self.config.get('threshold', 5)  # Default to threshold

        # Get Gemini's suggestion
        gemini_score = await self._get_gemini_score(user_input, project, current_work)

        # Check if we have learned patterns
        if self.config.get('learnFromAdjustments', True):
            adjusted_score = self._apply_learned_patterns(gemini_score, user_input, context)
            if adjusted_score is not None:
                return adjusted_score

        return gemini_score

    async def _get_gemini_score(
        self,
        user_input: str,
        project: str,
        current_work: str
    ) -> int:
        """
        Get importance score from Gemini.

        Args:
            user_input: User's input text
            project: Current project name
            current_work: Description of current work

        Returns:
            Gemini's suggested score (1-10)
        """
        # TODO: Call Gemini API
        # For now, return mock score based on input length and keywords
        return self._mock_gemini_score(user_input)

    def _mock_gemini_score(self, user_input: str) -> int:
        """Mock Gemini scoring for testing (REMOVE in production)"""
        # Simple heuristic based on input characteristics
        score = 5  # Default medium importance

        # Adjust based on input length
        if len(user_input) > 200:
            score += 1  # Longer input = more important

        # Adjust based on keywords
        high_importance_keywords = [
            'bug', 'error', 'fix', 'critical', 'urgent', 'important',
            'production', 'deploy', 'security', 'performance'
        ]
        medium_importance_keywords = [
            'feature', 'implement', 'add', 'update', 'refactor', 'improve'
        ]
        low_importance_keywords = [
            'question', 'what is', 'how do', 'explain', 'tell me'
        ]

        user_input_lower = user_input.lower()

        if any(keyword in user_input_lower for keyword in high_importance_keywords):
            score += 2
        elif any(keyword in user_input_lower for keyword in medium_importance_keywords):
            score += 1
        elif any(keyword in user_input_lower for keyword in low_importance_keywords):
            score -= 1

        # Constrain to 1-10
        return max(1, min(10, score))

    def _apply_learned_patterns(
        self,
        gemini_score: int,
        user_input: str,
        context: Optional[Dict[str, Any]]
    ) -> Optional[int]:
        """
        Apply learned patterns from historical adjustments.

        Args:
            gemini_score: Gemini's suggested score
            user_input: User's input text
            context: Additional context

        Returns:
            Adjusted score if pattern found, None otherwise
        """
        if not self.adjustment_history:
            return None

        # TODO: Load adjustment history from database (quad_hook_importance_patterns table)

        # Find similar past adjustments
        topic = self._detect_topic(user_input)
        similar_adjustments = [
            adj for adj in self.adjustment_history
            if adj.topic == topic
        ]

        if not similar_adjustments:
            return None

        # Calculate average adjustment difference
        avg_diff = sum(adj.adjustment_diff for adj in similar_adjustments) / len(similar_adjustments)

        # Calculate confidence (more samples = higher confidence)
        confidence = min(1.0, len(similar_adjustments) / 3.0)

        # Only apply if confidence is high enough
        if confidence < 0.7:
            return None

        # Apply learned adjustment
        adjusted_score = gemini_score + int(avg_diff)

        return max(1, min(10, adjusted_score))

    def _detect_topic(self, user_input: str) -> str:
        """
        Detect topic from user input.

        Args:
            user_input: User's input text

        Returns:
            Detected topic
        """
        # Simple keyword-based topic detection
        # TODO: Use more sophisticated NLP/AI for topic detection

        topics = {
            'bug_fix': ['bug', 'error', 'fix', 'issue', 'problem'],
            'feature': ['feature', 'add', 'implement', 'create'],
            'refactor': ['refactor', 'improve', 'optimize', 'clean'],
            'documentation': ['doc', 'documentation', 'readme', 'comment'],
            'testing': ['test', 'testing', 'spec', 'unit test'],
            'deployment': ['deploy', 'production', 'release'],
            'question': ['what', 'how', 'why', 'explain', 'tell me']
        }

        user_input_lower = user_input.lower()

        for topic, keywords in topics.items():
            if any(keyword in user_input_lower for keyword in keywords):
                return topic

        return 'general'

    def record_adjustment(
        self,
        gemini_score: int,
        user_score: int,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Record user's manual adjustment for learning.

        Args:
            gemini_score: Gemini's suggested score
            user_score: User's adjusted score
            user_input: User's input text
            context: Additional context
        """
        topic = self._detect_topic(user_input)
        adjustment = ImportanceAdjustment(
            gemini_suggested=gemini_score,
            user_adjusted=user_score,
            topic=topic,
            context=str(context) if context else "",
            timestamp=datetime.now().isoformat(),
            adjustment_diff=user_score - gemini_score
        )

        self.adjustment_history.append(adjustment)

        # TODO: Save to database (quad_hook_importance_patterns table)

        print(f"[Learning] User adjusted {topic} importance: {gemini_score} → {user_score} (diff: {adjustment.adjustment_diff:+d})")

    def get_shelf_life_category(self, importance_score: int) -> str:
        """
        Get shelf life category based on importance score.

        Args:
            importance_score: Importance score (1-10)

        Returns:
            'high', 'medium', or 'low'
        """
        if importance_score >= 8:
            return 'high'  # 30 days
        elif importance_score >= 5:
            return 'medium'  # 7 days
        else:
            return 'low'  # 1 day

    def should_save_to_memory(self, importance_score: int) -> bool:
        """
        Check if input should be saved to memory.

        Args:
            importance_score: Importance score (1-10)

        Returns:
            True if should save, False otherwise
        """
        threshold = self.config.get('threshold', 5)
        return importance_score >= threshold

    def get_stats(self) -> Dict[str, Any]:
        """Get scoring statistics for debugging"""
        return {
            'config': self.config,
            'adjustment_history_count': len(self.adjustment_history),
            'topics_learned': list(set(adj.topic for adj in self.adjustment_history))
        }


# Global importance scorer instance
_importance_scorer: Optional[ImportanceScorer] = None


def get_importance_scorer(config_path: Optional[Path] = None) -> ImportanceScorer:
    """Get singleton importance scorer instance"""
    global _importance_scorer
    if _importance_scorer is None:
        _importance_scorer = ImportanceScorer(config_path)
    return _importance_scorer
