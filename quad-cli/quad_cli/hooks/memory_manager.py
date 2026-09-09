"""
Memory Manager Module
=====================

Manages conversation memories with shelf life and expiration.
Phase 1: Hard expiration
Phase 2 (Roadmap): Fading memory with Gemini summarization

Patent Pending: Hierarchical memory with token optimization

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, asdict
import uuid


@dataclass
class Memory:
    """Conversation memory"""
    id: str
    user_id: str
    project_name: str
    context_type: str  # 'ticket', 'project', 'user', 'global'
    context_id: Optional[str]

    # Memory content
    user_input: str
    topic_detected: str
    importance_score: int
    importance_suggested: int
    importance_manual_override: bool

    # Shelf life
    shelf_life_category: str  # 'high', 'medium', 'low'
    created_at: str
    expires_at: str
    is_expired: bool

    # Metadata
    last_accessed_at: str
    access_count: int


class MemoryManager:
    """
    Manages conversation memories with intelligent expiration.

    Phase 1: Hard expiration (delete after shelf life)
    Phase 2: Fading memory (summarize with Gemini, keep emotion/facts)
    """

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize memory manager.

        Args:
            config_path: Path to .quad/hook-config.json
        """
        self.config_path = config_path or Path.home() / ".quad" / "hook-config.json"
        self.config = self._load_config()

        # In-memory cache (TODO: load from database)
        self.memories: List[Memory] = []

    def _load_config(self) -> Dict[str, Any]:
        """Load memory shelf life configuration"""
        if not self.config_path.exists():
            return self._get_default_config()

        with open(self.config_path, 'r') as f:
            config = json.load(f)
            return config.get('memoryShelfLife', self._get_default_config())

    def _get_default_config(self) -> Dict[str, Any]:
        """Default memory shelf life configuration"""
        return {
            "strategy": "hard_expiration",
            "durations": {
                "high": 30,
                "medium": 7,
                "low": 1,
                "unit": "days"
            },
            "importanceMapping": {
                "high": [8, 9, 10],
                "medium": [5, 6, 7],
                "low": [1, 2, 3, 4]
            },
            "cleanup": {
                "enabled": True,
                "schedule": "0 2 * * *",
                "deleteExpired": True
            }
        }

    def save_memory(
        self,
        user_id: str,
        project_name: str,
        context_type: str,
        context_id: Optional[str],
        user_input: str,
        topic_detected: str,
        importance_score: int,
        importance_suggested: int,
        importance_manual_override: bool = False
    ) -> Memory:
        """
        Save conversation memory.

        Args:
            user_id: User UUID
            project_name: Project name
            context_type: Context type ('ticket', 'project', 'user', 'global')
            context_id: Context ID (ticket ID, project ID, etc.)
            user_input: User's input text
            topic_detected: Detected topic
            importance_score: Final importance score (1-10)
            importance_suggested: Gemini's suggested score
            importance_manual_override: Whether user manually adjusted score

        Returns:
            Created memory
        """
        # Get shelf life category
        shelf_life_category = self._get_shelf_life_category(importance_score)

        # Calculate expiration date
        created_at = datetime.now()
        expires_at = self._calculate_expiration(shelf_life_category, created_at)

        # Create memory
        memory = Memory(
            id=str(uuid.uuid4()),
            user_id=user_id,
            project_name=project_name,
            context_type=context_type,
            context_id=context_id,
            user_input=user_input,
            topic_detected=topic_detected,
            importance_score=importance_score,
            importance_suggested=importance_suggested,
            importance_manual_override=importance_manual_override,
            shelf_life_category=shelf_life_category,
            created_at=created_at.isoformat(),
            expires_at=expires_at.isoformat(),
            is_expired=False,
            last_accessed_at=created_at.isoformat(),
            access_count=0
        )

        # Save to database
        self._save_to_database(memory)

        # Add to cache
        self.memories.append(memory)

        print(f"[Memory] Saved: {topic_detected} (importance: {importance_score}, shelf life: {shelf_life_category}, expires: {expires_at.strftime('%Y-%m-%d')})")

        return memory

    def _get_shelf_life_category(self, importance_score: int) -> str:
        """Get shelf life category from importance score"""
        importance_mapping = self.config.get('importanceMapping', {})

        for category, scores in importance_mapping.items():
            if importance_score in scores:
                return category

        return 'low'  # Default to low

    def _calculate_expiration(self, category: str, created_at: datetime) -> datetime:
        """Calculate expiration date based on shelf life category"""
        durations = self.config.get('durations', {})
        days = durations.get(category, 1)

        return created_at + timedelta(days=days)

    def _save_to_database(self, memory: Memory):
        """Save memory to database (quad_hook_memories table)"""
        # TODO: Insert into PostgreSQL database
        pass

    def get_memories(
        self,
        user_id: str,
        project_name: Optional[str] = None,
        context_type: Optional[str] = None,
        context_id: Optional[str] = None,
        include_expired: bool = False
    ) -> List[Memory]:
        """
        Retrieve memories with filters.

        Args:
            user_id: User UUID
            project_name: Filter by project (optional)
            context_type: Filter by context type (optional)
            context_id: Filter by context ID (optional)
            include_expired: Include expired memories

        Returns:
            List of memories
        """
        # TODO: Load from database

        # Filter in-memory cache
        memories = self.memories

        # Filter by user
        memories = [m for m in memories if m.user_id == user_id]

        # Filter by project
        if project_name:
            memories = [m for m in memories if m.project_name == project_name]

        # Filter by context type
        if context_type:
            memories = [m for m in memories if m.context_type == context_type]

        # Filter by context ID
        if context_id:
            memories = [m for m in memories if m.context_id == context_id]

        # Filter expired
        if not include_expired:
            memories = [m for m in memories if not m.is_expired]

        # Update access stats
        for memory in memories:
            memory.last_accessed_at = datetime.now().isoformat()
            memory.access_count += 1

        return memories

    def mark_expired(self) -> int:
        """
        Mark memories as expired (called by cleanup job).

        Returns:
            Number of memories marked as expired
        """
        count = 0
        now = datetime.now()

        for memory in self.memories:
            if not memory.is_expired:
                expires_at = datetime.fromisoformat(memory.expires_at)
                if expires_at <= now:
                    memory.is_expired = True
                    count += 1

        # TODO: Update database
        # UPDATE quad_hook_memories SET is_expired = TRUE WHERE expires_at <= NOW()

        return count

    def delete_expired(self, grace_period_days: int = 7) -> int:
        """
        Delete expired memories after grace period.

        Args:
            grace_period_days: Days to keep expired memories before deletion

        Returns:
            Number of memories deleted
        """
        if not self.config.get('cleanup', {}).get('deleteExpired', True):
            return 0

        count = 0
        cutoff = datetime.now() - timedelta(days=grace_period_days)

        # Delete from cache
        memories_to_keep = []
        for memory in self.memories:
            if memory.is_expired:
                expires_at = datetime.fromisoformat(memory.expires_at)
                if expires_at < cutoff:
                    count += 1
                    continue
            memories_to_keep.append(memory)

        self.memories = memories_to_keep

        # TODO: Delete from database
        # DELETE FROM quad_hook_memories WHERE is_expired = TRUE AND expires_at < NOW() - INTERVAL '7 days'

        return count

    def get_context_summary(
        self,
        user_id: str,
        context_type: str,
        context_id: str
    ) -> str:
        """
        Get summary of memories for a context (for sending to Claude).

        Args:
            user_id: User UUID
            context_type: Context type
            context_id: Context ID

        Returns:
            Formatted memory summary
        """
        memories = self.get_memories(user_id, context_type=context_type, context_id=context_id)

        if not memories:
            return "No previous context available."

        # Sort by importance (highest first)
        memories.sort(key=lambda m: m.importance_score, reverse=True)

        # Format summary
        lines = ["Previous context:"]
        for i, memory in enumerate(memories[:5], 1):  # Top 5 memories
            lines.append(f"{i}. [{memory.topic_detected}] {memory.user_input[:100]}...")

        return "\n".join(lines)

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        total = len(self.memories)
        expired = sum(1 for m in self.memories if m.is_expired)
        by_category = {}

        for category in ['high', 'medium', 'low']:
            by_category[category] = sum(1 for m in self.memories if m.shelf_life_category == category)

        return {
            'total_memories': total,
            'expired_memories': expired,
            'active_memories': total - expired,
            'by_category': by_category,
            'config': self.config
        }


# Global memory manager instance
_memory_manager: Optional[MemoryManager] = None


def get_memory_manager(config_path: Optional[Path] = None) -> MemoryManager:
    """Get singleton memory manager instance"""
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = MemoryManager(config_path)
    return _memory_manager
