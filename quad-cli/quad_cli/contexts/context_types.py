"""
Context Types
=============

Define different types of contexts that can be stored.

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

from enum import Enum
from pathlib import Path
from typing import Dict


class ContextType(Enum):
    """Context type enumeration"""
    PROJECT = "project"
    HEALTH = "health"
    FINANCE = "finance"
    PREFERENCES = "preferences"
    MEMORY = "memory"


# Context type configurations
CONTEXT_TYPES: Dict[ContextType, Dict] = {
    ContextType.PROJECT: {
        "description": "Technical decisions, architecture, patterns",
        "storage": ".quad/project-memory.json",  # Project-local
        "enabled": True,
        "keywords": [
            "architecture", "framework", "library", "api",
            "database", "schema", "deployment", "ci/cd",
            "testing", "security", "performance"
        ]
    },
    ContextType.HEALTH: {
        "description": "Health-related discussions and information",
        "storage": "~/.quad/contexts/health.json",  # User-global
        "enabled": True,
        "keywords": [
            "health", "medical", "doctor", "medicine",
            "allergy", "condition", "symptom", "treatment",
            "nutrition", "exercise", "wellness"
        ]
    },
    ContextType.FINANCE: {
        "description": "Finance, banking, payment discussions",
        "storage": "~/.quad/contexts/finance.json",  # User-global
        "enabled": True,
        "keywords": [
            "finance", "banking", "payment", "transaction",
            "account", "balance", "transfer", "budget",
            "investment", "loan", "credit", "debit"
        ]
    },
    ContextType.PREFERENCES: {
        "description": "User preferences and coding style",
        "storage": "~/.quad/contexts/preferences.json",  # User-global
        "enabled": True,
        "keywords": [
            "prefer", "like", "dislike", "always", "never",
            "usually", "style", "convention", "format"
        ]
    },
    ContextType.MEMORY: {
        "description": "General conversation memory",
        "storage": "~/.quad/contexts/memory.json",  # User-global
        "enabled": True,
        "keywords": []  # Catch-all
    }
}


def get_context_storage_path(context_type: ContextType) -> Path:
    """Get storage path for context type"""
    config = CONTEXT_TYPES[context_type]
    storage_path = config["storage"]

    # Expand home directory
    if storage_path.startswith("~/"):
        return Path.home() / storage_path[2:]
    else:
        # Project-local path (relative to current directory)
        return Path.cwd() / storage_path


def is_context_enabled(context_type: ContextType) -> bool:
    """Check if context type is enabled"""
    return CONTEXT_TYPES[context_type]["enabled"]


def get_context_keywords(context_type: ContextType) -> list:
    """Get keywords for context type"""
    return CONTEXT_TYPES[context_type]["keywords"]


def classify_context(text: str) -> ContextType:
    """
    Classify text into a context type based on keywords.

    Args:
        text: Text to classify

    Returns:
        Most relevant context type
    """
    text_lower = text.lower()

    # Count keyword matches for each context type
    scores = {}
    for context_type, config in CONTEXT_TYPES.items():
        keywords = config["keywords"]
        if not keywords:  # Skip memory (catch-all)
            continue

        score = sum(1 for keyword in keywords if keyword in text_lower)
        scores[context_type] = score

    # Return context type with highest score
    if scores:
        max_score = max(scores.values())
        if max_score > 0:
            for context_type, score in scores.items():
                if score == max_score:
                    return context_type

    # Default to MEMORY if no matches
    return ContextType.MEMORY
