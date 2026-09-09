"""
Pause Detection Module
======================

Adaptive pause detection with pattern learning.
Learns user typing patterns and adjusts timeout dynamically.

Patent Pending: Adaptive timeout based on user behavior analysis

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import time
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class UserTypingPattern:
    """User typing behavior patterns"""
    avg_typing_speed_wpm: float = 40.0
    avg_message_length: int = 100
    avg_pause_between_messages_ms: int = 3000

    # Burst patterns
    detects_short_bursts: bool = False
    short_burst_avg_messages: int = 2
    short_burst_timeout_ms: int = 1500

    # Long thought patterns
    detects_long_thoughts: bool = False
    long_thought_avg_length: int = 200
    long_thought_timeout_ms: int = 5000

    # Learning stats
    total_messages_analyzed: int = 0
    last_pattern_update: str = ""
    confidence_score: float = 0.0  # 0.0 to 1.0


class PauseDetector:
    """
    Adaptive pause detection system.

    Learns user typing patterns and adjusts pause timeout dynamically.
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize pause detector.

        Args:
            config_path: Path to .quad/hook-config.json
        """
        self.config_path = config_path or Path.home() / ".quad" / "hook-config.json"
        self.config = self._load_config()
        self.user_pattern = self._load_user_pattern()

        # Message buffer for pause detection
        self.message_buffer: List[Dict[str, Any]] = []
        self.last_message_time: Optional[datetime] = None

    def _load_config(self) -> Dict[str, Any]:
        """Load hook configuration"""
        if not self.config_path.exists():
            return self._get_default_config()

        with open(self.config_path, 'r') as f:
            config = json.load(f)
            return config.get('pauseDetection', self._get_default_config())

    def _get_default_config(self) -> Dict[str, Any]:
        """Default pause detection configuration"""
        return {
            "enabled": True,
            "baseTimeout": 3000,
            "adaptiveMode": True,
            "learnFromPatterns": True,
            "timeoutRange": {
                "min": 1500,
                "max": 5000
            }
        }

    def _load_user_pattern(self) -> UserTypingPattern:
        """Load user typing pattern from database or cache"""
        # TODO: Load from database (quad_hook_user_patterns table)
        # For now, return default pattern
        return UserTypingPattern()

    def _save_user_pattern(self):
        """Save user pattern to database"""
        # TODO: Save to database (quad_hook_user_patterns table)
        pass

    def calculate_timeout(self) -> int:
        """
        Calculate adaptive timeout based on user patterns.

        Returns:
            Timeout in milliseconds
        """
        if not self.config.get('adaptiveMode', True):
            return self.config.get('baseTimeout', 3000)

        # Check for short burst pattern
        if self.user_pattern.detects_short_bursts:
            if self._is_in_burst_mode():
                return self.user_pattern.short_burst_timeout_ms

        # Check for long thought pattern
        if self.user_pattern.detects_long_thoughts:
            if self._is_in_long_thought_mode():
                return self.user_pattern.long_thought_timeout_ms

        # Default timeout
        base_timeout = self.config.get('baseTimeout', 3000)

        # Constrain to min/max range
        timeout_range = self.config.get('timeoutRange', {})
        min_timeout = timeout_range.get('min', 1500)
        max_timeout = timeout_range.get('max', 5000)

        return max(min_timeout, min(base_timeout, max_timeout))

    def _is_in_burst_mode(self) -> bool:
        """Check if user is in short burst typing mode"""
        if len(self.message_buffer) < 2:
            return False

        recent_messages = self.message_buffer[-3:]  # Last 3 messages

        # Check if messages are short and quick
        avg_length = sum(len(msg.get('text', '')) for msg in recent_messages) / len(recent_messages)

        if avg_length < self.user_pattern.short_burst_avg_messages * 50:  # Short messages
            return True

        return False

    def _is_in_long_thought_mode(self) -> bool:
        """Check if user is in long thought typing mode"""
        if not self.message_buffer:
            return False

        last_message = self.message_buffer[-1]
        message_length = len(last_message.get('text', ''))

        return message_length >= self.user_pattern.long_thought_avg_length

    def add_message(self, text: str, timestamp: Optional[datetime] = None):
        """
        Add message to buffer and analyze patterns.

        Args:
            text: Message text
            timestamp: Message timestamp (default: now)
        """
        if timestamp is None:
            timestamp = datetime.now()

        message = {
            'text': text,
            'timestamp': timestamp,
            'length': len(text)
        }

        self.message_buffer.append(message)
        self.last_message_time = timestamp

        # Keep buffer size manageable (last 10 messages)
        if len(self.message_buffer) > 10:
            self.message_buffer.pop(0)

        # Learn from patterns
        if self.config.get('learnFromPatterns', True):
            self._update_patterns()

    def _update_patterns(self):
        """Update user typing patterns based on recent messages"""
        if len(self.message_buffer) < 3:
            return  # Need at least 3 messages to detect patterns

        # Analyze burst patterns
        self._detect_burst_pattern()

        # Analyze long thought patterns
        self._detect_long_thought_pattern()

        # Update stats
        self.user_pattern.total_messages_analyzed += 1
        self.user_pattern.last_pattern_update = datetime.now().isoformat()

        # Calculate confidence (more messages = higher confidence, up to 1.0)
        self.user_pattern.confidence_score = min(
            1.0,
            self.user_pattern.total_messages_analyzed / 50.0
        )

        # Save updated pattern
        self._save_user_pattern()

    def _detect_burst_pattern(self):
        """Detect if user types in short bursts"""
        if len(self.message_buffer) < 3:
            return

        recent = self.message_buffer[-5:]  # Last 5 messages

        # Calculate average message length
        avg_length = sum(m['length'] for m in recent) / len(recent)

        # Calculate time between messages
        time_deltas = []
        for i in range(1, len(recent)):
            delta = (recent[i]['timestamp'] - recent[i-1]['timestamp']).total_seconds() * 1000
            time_deltas.append(delta)

        avg_time_delta = sum(time_deltas) / len(time_deltas) if time_deltas else 3000

        # Detect burst: short messages sent quickly
        if avg_length < 100 and avg_time_delta < 5000:
            self.user_pattern.detects_short_bursts = True
            self.user_pattern.short_burst_timeout_ms = int(avg_time_delta * 0.7)  # 70% of avg time

    def _detect_long_thought_pattern(self):
        """Detect if user types long, thoughtful messages"""
        if len(self.message_buffer) < 2:
            return

        recent = self.message_buffer[-3:]  # Last 3 messages

        # Calculate average message length
        avg_length = sum(m['length'] for m in recent) / len(recent)

        # Detect long thoughts: messages over 200 characters
        if avg_length >= 200:
            self.user_pattern.detects_long_thoughts = True
            self.user_pattern.long_thought_avg_length = int(avg_length)
            self.user_pattern.long_thought_timeout_ms = 5000  # 5 seconds for long thoughts

    def should_process_now(self) -> bool:
        """
        Check if enough time has passed since last message to process.

        Returns:
            True if should process, False if should wait
        """
        if not self.last_message_time:
            return False

        timeout_ms = self.calculate_timeout()
        time_since_last = (datetime.now() - self.last_message_time).total_seconds() * 1000

        return time_since_last >= timeout_ms

    def get_merged_input(self) -> str:
        """
        Get all messages in buffer merged into single input.

        Returns:
            Merged input text
        """
        return "\n".join(msg['text'] for msg in self.message_buffer)

    def clear_buffer(self):
        """Clear message buffer after processing"""
        self.message_buffer.clear()
        self.last_message_time = None

    def get_pattern_info(self) -> Dict[str, Any]:
        """Get current pattern information for debugging"""
        return {
            'pattern': asdict(self.user_pattern),
            'current_timeout': self.calculate_timeout(),
            'is_burst_mode': self._is_in_burst_mode(),
            'is_long_thought_mode': self._is_in_long_thought_mode(),
            'buffer_size': len(self.message_buffer)
        }


# Global pause detector instance
_pause_detector: Optional[PauseDetector] = None


def get_pause_detector(config_path: Optional[Path] = None) -> PauseDetector:
    """Get singleton pause detector instance"""
    global _pause_detector
    if _pause_detector is None:
        _pause_detector = PauseDetector(config_path)
    return _pause_detector
