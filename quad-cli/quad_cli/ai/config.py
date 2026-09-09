"""
AI Configuration
================

Manage AI provider configuration (Gemini, Claude, Router).

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


# Default configuration
DEFAULT_AI_CONFIG = {
    "router": {
        "mode": "smart",  # smart, single, gemini_only, claude_only
        "default_provider": "gemini",
        "fallback_enabled": True,
        "confidence_threshold": 0.7
    },
    "gemini": {
        "api_key": None,
        "model": "gemini-1.5-flash",  # or gemini-1.5-pro
        "enabled": True
    },
    "claude": {
        "api_key": None,
        "model": "claude-sonnet-4",  # or claude-opus-4
        "enabled": True
    }
}


def get_config_path() -> Path:
    """Get path to AI config file"""
    quad_dir = Path.home() / ".quad"
    quad_dir.mkdir(parents=True, exist_ok=True)
    return quad_dir / "ai_config.json"


def load_ai_config() -> Dict[str, Any]:
    """Load AI configuration"""
    config_path = get_config_path()

    if config_path.exists():
        try:
            config = json.loads(config_path.read_text())
            # Merge with defaults (in case new keys added)
            return merge_configs(DEFAULT_AI_CONFIG, config)
        except:
            return DEFAULT_AI_CONFIG.copy()

    return DEFAULT_AI_CONFIG.copy()


def save_ai_config(config: Dict[str, Any]):
    """Save AI configuration"""
    config_path = get_config_path()
    config_path.write_text(json.dumps(config, indent=2))


def merge_configs(default: Dict, user: Dict) -> Dict:
    """Merge user config with defaults (recursive)"""
    result = default.copy()

    for key, value in user.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value

    return result


def get_config_value(key: str) -> Any:
    """
    Get configuration value by dot notation.

    Examples:
        get_config_value("router.mode") → "smart"
        get_config_value("gemini.api_key") → "..."
    """
    config = load_ai_config()

    keys = key.split(".")
    value = config

    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return None

    return value


def set_config_value(key: str, value: Any):
    """
    Set configuration value by dot notation.

    Examples:
        set_config_value("router.mode", "single")
        set_config_value("gemini.api_key", "YOUR_KEY")
    """
    config = load_ai_config()

    keys = key.split(".")
    current = config

    # Navigate to parent
    for k in keys[:-1]:
        if k not in current:
            current[k] = {}
        current = current[k]

    # Set value
    current[keys[-1]] = value

    save_ai_config(config)


def get_router_mode() -> str:
    """Get current router mode"""
    return get_config_value("router.mode") or "smart"


def get_default_provider() -> str:
    """Get default AI provider"""
    return get_config_value("router.default_provider") or "gemini"


def is_fallback_enabled() -> bool:
    """Check if fallback is enabled"""
    return get_config_value("router.fallback_enabled") != False  # Default to True


def get_confidence_threshold() -> float:
    """Get confidence threshold for fallback"""
    threshold = get_config_value("router.confidence_threshold")
    return float(threshold) if threshold is not None else 0.7


def get_gemini_api_key() -> Optional[str]:
    """Get Gemini API key"""
    return get_config_value("gemini.api_key")


def get_claude_api_key() -> Optional[str]:
    """Get Claude API key"""
    return get_config_value("claude.api_key")


def is_gemini_enabled() -> bool:
    """Check if Gemini is enabled"""
    enabled = get_config_value("gemini.enabled")
    return enabled != False  # Default to True


def is_claude_enabled() -> bool:
    """Check if Claude is enabled"""
    enabled = get_config_value("claude.enabled")
    return enabled != False  # Default to True


def has_gemini() -> bool:
    """Check if Gemini is available (enabled + has API key)"""
    return is_gemini_enabled() and get_gemini_api_key() is not None


def has_claude() -> bool:
    """Check if Claude is available (enabled + has API key)"""
    return is_claude_enabled() and get_claude_api_key() is not None


def print_ai_status():
    """Print AI configuration status (for debugging)"""
    config = load_ai_config()

    print("AI Configuration Status:")
    print("=" * 50)

    # Router
    print(f"\nRouter Mode: {get_router_mode()}")
    print(f"Default Provider: {get_default_provider()}")
    print(f"Fallback Enabled: {is_fallback_enabled()}")
    print(f"Confidence Threshold: {get_confidence_threshold()}")

    # Gemini
    print(f"\nGemini:")
    print(f"  Enabled: {is_gemini_enabled()}")
    print(f"  API Key: {'✓ Set' if get_gemini_api_key() else '✗ Not Set'}")
    print(f"  Model: {get_config_value('gemini.model')}")
    print(f"  Available: {'✓ Yes' if has_gemini() else '✗ No'}")

    # Claude
    print(f"\nClaude:")
    print(f"  Enabled: {is_claude_enabled()}")
    print(f"  API Key: {'✓ Set' if get_claude_api_key() else '✗ Not Set'}")
    print(f"  Model: {get_config_value('claude.model')}")
    print(f"  Available: {'✓ Yes' if has_claude() else '✗ No'}")

    print()


if __name__ == "__main__":
    # Test configuration
    print_ai_status()
