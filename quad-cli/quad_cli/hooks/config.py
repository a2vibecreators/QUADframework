"""
Hook Configuration
==================

Configuration for pre/post hooks.

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

from pathlib import Path
import json
from typing import Dict, List

# Default hook configuration
DEFAULT_HOOK_CONFIG = {
    "enabled": True,
    "hooks": {
        "pre_hook": {
            "enabled": True,
            "capture_request": True,
            "enrich_context": True
        },
        "post_hook": {
            "enabled": True,
            "capture_response": True,
            "analyze_context": True,
            "store_context": True
        }
    },
    "context_analysis": {
        "enabled": True,
        "provider": "gemini",  # gemini or claude
        "model": "gemini-pro"
    },
    "exclude_topics": [
        "politics",
        "religion",
        "personal_secrets",
        "passwords",
        "api_keys",
        "private_keys"
    ],
    "retention_days": 365,
    "auto_cleanup": True,
    "encryption": False  # TODO: Enable when implemented
}


def get_hook_config_path() -> Path:
    """Get path to hook config file"""
    quad_dir = Path.home() / ".quad"
    quad_dir.mkdir(parents=True, exist_ok=True)
    return quad_dir / "hooks.json"


def load_hook_config() -> Dict:
    """Load hook configuration"""
    config_path = get_hook_config_path()
    if config_path.exists():
        try:
            return json.loads(config_path.read_text())
        except:
            return DEFAULT_HOOK_CONFIG
    return DEFAULT_HOOK_CONFIG


def save_hook_config(config: Dict):
    """Save hook configuration"""
    config_path = get_hook_config_path()
    config_path.write_text(json.dumps(config, indent=2))


def is_hooks_enabled() -> bool:
    """Check if hooks are enabled"""
    config = load_hook_config()
    return config.get("enabled", True)


def is_topic_excluded(topic: str) -> bool:
    """Check if topic should be excluded from context"""
    config = load_hook_config()
    excluded = config.get("exclude_topics", [])
    return topic.lower() in [t.lower() for t in excluded]


def get_context_analysis_config() -> Dict:
    """Get context analysis configuration"""
    config = load_hook_config()
    return config.get("context_analysis", {
        "enabled": True,
        "provider": "gemini",
        "model": "gemini-pro"
    })
