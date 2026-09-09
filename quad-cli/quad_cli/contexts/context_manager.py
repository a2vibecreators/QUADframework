"""
Context Manager
===============

High-level context management operations.

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

from typing import Dict, List, Optional
from datetime import datetime

from .context_types import ContextType, CONTEXT_TYPES, classify_context
from .context_store import ContextStore


class ContextManager:
    """Manage context operations across all context types"""

    def __init__(self):
        self.stores = {
            context_type: ContextStore(context_type)
            for context_type in ContextType
        }

    def store_context(
        self,
        text: str,
        metadata: Optional[Dict] = None,
        context_type: Optional[ContextType] = None
    ):
        """
        Store context in appropriate context tree.

        Args:
            text: Context text to store
            metadata: Additional metadata
            context_type: Explicit context type (auto-classify if None)
        """
        # Auto-classify if not specified
        if context_type is None:
            context_type = classify_context(text)

        # Create entry
        entry = {
            "text": text,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        # Store in appropriate context
        store = self.stores[context_type]
        store.append_entry(entry)

    def search_all(self, query: str, limit: int = 10) -> Dict[ContextType, List]:
        """
        Search across all context types.

        Args:
            query: Search query
            limit: Max results per context type

        Returns:
            Dict mapping context types to matching entries
        """
        results = {}

        for context_type, store in self.stores.items():
            matches = store.search(query, limit)
            if matches:
                results[context_type] = matches

        return results

    def search_context(
        self,
        context_type: ContextType,
        query: str,
        limit: int = 10
    ) -> List[Dict]:
        """
        Search specific context type.

        Args:
            context_type: Context type to search
            query: Search query
            limit: Max results

        Returns:
            List of matching entries
        """
        store = self.stores[context_type]
        return store.search(query, limit)

    def get_all_summaries(self) -> Dict[str, Dict]:
        """Get summaries of all context types"""
        summaries = {}

        for context_type, store in self.stores.items():
            summaries[context_type.value] = store.get_summary()

        return summaries

    def get_context_summary(self, context_type: ContextType) -> Dict:
        """Get summary of specific context type"""
        store = self.stores[context_type]
        return store.get_summary()

    def clear_context(self, context_type: ContextType):
        """Clear specific context type"""
        store = self.stores[context_type]
        store.clear()

    def clear_all(self):
        """Clear all contexts"""
        for store in self.stores.values():
            store.clear()

    def export_context(self, context_type: ContextType, output_path: str):
        """Export context to JSON file"""
        from pathlib import Path
        store = self.stores[context_type]
        store.export_json(Path(output_path))

    def import_context(self, context_type: ContextType, input_path: str):
        """Import context from JSON file"""
        from pathlib import Path
        store = self.stores[context_type]
        store.import_json(Path(input_path))

    def enable_context(self, context_type: ContextType):
        """Enable specific context type"""
        CONTEXT_TYPES[context_type]["enabled"] = True
        # TODO: Persist to config

    def disable_context(self, context_type: ContextType):
        """Disable specific context type"""
        CONTEXT_TYPES[context_type]["enabled"] = False
        # TODO: Persist to config

    def get_enabled_contexts(self) -> List[ContextType]:
        """Get list of enabled context types"""
        return [
            context_type
            for context_type, config in CONTEXT_TYPES.items()
            if config["enabled"]
        ]


# Singleton instance
_context_manager = None


def get_context_manager() -> ContextManager:
    """Get singleton ContextManager instance"""
    global _context_manager
    if _context_manager is None:
        _context_manager = ContextManager()
    return _context_manager
