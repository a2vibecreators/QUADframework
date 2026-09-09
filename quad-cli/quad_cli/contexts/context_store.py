"""
Context Store
=============

Storage layer for context data (JSON-based).

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

from .context_types import (
    ContextType,
    get_context_storage_path,
    is_context_enabled
)


class ContextStore:
    """Store and retrieve context data"""

    def __init__(self, context_type: ContextType):
        self.context_type = context_type
        self.storage_path = get_context_storage_path(context_type)

    def load(self) -> Dict:
        """Load context from storage"""
        if not self.storage_path.exists():
            return self._create_empty_context()

        try:
            data = json.loads(self.storage_path.read_text())
            return data
        except:
            return self._create_empty_context()

    def save(self, context: Dict):
        """Save context to storage"""
        # Ensure parent directory exists
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        # Add metadata
        context["last_updated"] = datetime.now().isoformat()
        context["context_type"] = self.context_type.value

        # Write to file
        self.storage_path.write_text(json.dumps(context, indent=2))

    def append_entry(self, entry: Dict):
        """Append entry to context with smart metadata"""
        context = self.load()

        # Add timestamp if not present
        if "timestamp" not in entry:
            entry["timestamp"] = datetime.now().isoformat()

        # Add metadata for smart cleanup
        if "metadata" not in entry:
            entry["metadata"] = {}

        # Initialize smart metadata
        entry["metadata"]["last_accessed"] = datetime.now().isoformat()
        entry["metadata"]["access_count"] = 1
        entry["metadata"]["age_days"] = 0
        entry["metadata"]["tags"] = entry["metadata"].get("tags", [])
        entry["metadata"]["pinned"] = entry["metadata"].get("pinned", False)
        entry["metadata"]["retention_policy"] = self._calculate_retention_policy(entry)

        # Append to entries list
        if "entries" not in context:
            context["entries"] = []

        context["entries"].append(entry)

        # Clean up old entries (smart cleanup)
        context["entries"] = self._smart_cleanup(context["entries"])

        # Save updated context
        self.save(context)

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search context for entries matching query.
        Updates last_accessed and access_count for found entries.

        Args:
            query: Search query
            limit: Max results to return

        Returns:
            List of matching entries
        """
        context = self.load()
        entries = context.get("entries", [])

        query_lower = query.lower()
        matches = []
        updated = False

        for entry in entries:
            # Simple keyword search in entry text
            entry_text = json.dumps(entry).lower()
            if query_lower in entry_text:
                # Update access tracking
                if "metadata" in entry:
                    entry["metadata"]["last_accessed"] = datetime.now().isoformat()
                    entry["metadata"]["access_count"] = entry["metadata"].get("access_count", 0) + 1

                    # Auto-promote to important if accessed 5+ times
                    if entry["metadata"]["access_count"] >= 5:
                        entry["metadata"]["retention_policy"] = "important"

                    updated = True

                matches.append(entry)

            if len(matches) >= limit:
                break

        # Save updated access tracking
        if updated:
            self.save(context)

        return matches

    def clear(self):
        """Clear all context data"""
        if self.storage_path.exists():
            self.storage_path.unlink()

    def get_summary(self) -> Dict:
        """Get summary statistics of context"""
        context = self.load()
        entries = context.get("entries", [])

        return {
            "context_type": self.context_type.value,
            "total_entries": len(entries),
            "storage_path": str(self.storage_path),
            "last_updated": context.get("last_updated"),
            "created_at": context.get("created_at")
        }

    def _create_empty_context(self) -> Dict:
        """Create empty context structure"""
        return {
            "context_type": self.context_type.value,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "entries": []
        }

    def _cleanup_old_entries(self, entries: List[Dict]) -> List[Dict]:
        """
        Remove entries older than retention period.

        Default retention: 365 days
        """
        from quad_cli.hooks.config import load_hook_config

        config = load_hook_config()
        retention_days = config.get("retention_days", 365)

        cutoff_date = datetime.now() - timedelta(days=retention_days)

        cleaned_entries = []
        for entry in entries:
            timestamp_str = entry.get("timestamp")
            if not timestamp_str:
                # No timestamp, keep entry
                cleaned_entries.append(entry)
                continue

            try:
                entry_date = datetime.fromisoformat(timestamp_str)
                if entry_date >= cutoff_date:
                    cleaned_entries.append(entry)
            except:
                # Invalid timestamp, keep entry
                cleaned_entries.append(entry)

        return cleaned_entries

    def _smart_cleanup(self, entries: List[Dict]) -> List[Dict]:
        """
        Smart cleanup based on retention policy and age.

        Retention policies:
        - auto: Context-specific max age (30-365 days)
        - important: 2 years (accessed 5+ times)
        - permanent: Never delete (user pinned)
        """
        now = datetime.now()

        # Get context-specific max age
        max_age_map = {
            ContextType.MEMORY: 30,
            ContextType.PROJECT: 90,
            ContextType.PREFERENCES: 180,
            ContextType.FINANCE: 365,
            ContextType.HEALTH: 365
        }
        default_max_age = max_age_map.get(self.context_type, 90)

        cleaned_entries = []
        archived_entries = []

        for entry in entries:
            # Update age_days
            if "metadata" in entry:
                last_accessed = entry["metadata"].get("last_accessed", entry.get("timestamp"))
                if last_accessed:
                    try:
                        last_accessed_date = datetime.fromisoformat(last_accessed)
                        age_days = (now - last_accessed_date).days
                        entry["metadata"]["age_days"] = age_days
                    except:
                        entry["metadata"]["age_days"] = 0

            # Get retention policy
            metadata = entry.get("metadata", {})
            retention_policy = metadata.get("retention_policy", "auto")
            age_days = metadata.get("age_days", 0)
            pinned = metadata.get("pinned", False)

            # Decide whether to keep
            should_keep = False

            if pinned or retention_policy == "permanent":
                should_keep = True
            elif retention_policy == "important":
                # Keep for 2 years
                should_keep = age_days < 730
            elif retention_policy == "auto":
                # Keep based on context-specific max age
                should_keep = age_days < default_max_age
            else:
                # Unknown policy, keep
                should_keep = True

            if should_keep:
                cleaned_entries.append(entry)
            else:
                archived_entries.append(entry)

        # Archive deleted entries
        if archived_entries:
            self._archive_entries(archived_entries)

        return cleaned_entries

    def _calculate_retention_policy(self, entry: Dict) -> str:
        """Calculate initial retention policy for entry"""
        metadata = entry.get("metadata", {})

        # Check if pinned
        if metadata.get("pinned", False):
            return "permanent"

        # Check if has "important" tag
        tags = metadata.get("tags", [])
        if "important" in tags:
            return "important"

        # Default to auto
        return "auto"

    def _archive_entries(self, entries: List[Dict]):
        """Archive entries before deletion"""
        archive_path = self.storage_path.parent / f"{self.storage_path.stem}-archive.json"

        # Load existing archive
        if archive_path.exists():
            try:
                archive = json.loads(archive_path.read_text())
            except:
                archive = {"archived_at": datetime.now().isoformat(), "entries": []}
        else:
            archive = {"archived_at": datetime.now().isoformat(), "entries": []}

        # Append new entries
        for entry in entries:
            entry["archived_at"] = datetime.now().isoformat()
            archive["entries"].append(entry)

        # Save archive
        archive["last_updated"] = datetime.now().isoformat()
        archive_path.write_text(json.dumps(archive, indent=2))

    def export_json(self, output_path: Path):
        """Export context to JSON file"""
        context = self.load()
        output_path.write_text(json.dumps(context, indent=2))

    def import_json(self, input_path: Path):
        """Import context from JSON file"""
        if not input_path.exists():
            raise FileNotFoundError(f"File not found: {input_path}")

        data = json.loads(input_path.read_text())
        self.save(data)
