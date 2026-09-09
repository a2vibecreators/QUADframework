# AI Router Matrix - All Operating Modes
**Date:** January 15, 2026

---

## The Matrix: All Possible Combinations

### Dimension 1: Available Providers

| Gemini | Claude | Scenario |
|--------|--------|----------|
| ✅ | ✅ | Both available (best) |
| ✅ | ❌ | Gemini only (free) |
| ❌ | ✅ | Claude only (quality) |
| ❌ | ❌ | None (error) |

### Dimension 2: Router Mode

| Mode | Behavior |
|------|----------|
| **Smart** | Keyword → Gemini → Confidence check → Claude fallback |
| **Single** | Always use configured provider (no routing) |
| **Gemini-only** | Always Gemini (never fallback) |
| **Claude-only** | Always Claude (skip Gemini) |

### Dimension 3: Task Complexity

| Complexity | Keywords | Default Route |
|------------|----------|---------------|
| **Simple** | list, show, explain | Gemini (sufficient) |
| **Complex** | generate, implement, refactor | Gemini first, Claude fallback |
| **Critical** | production, security, compliance | Claude (always) |

---

## Complete Matrix: All 12 Operating Modes

### Mode 1: Smart Router (Both Available)
```
Configuration:
- gemini_api_key: SET
- claude_api_key: SET
- router_mode: smart
- fallback_enabled: true

Flow:
User request
  ↓
Keyword classification
  ├─ Simple → Gemini → Done
  ├─ Complex → Gemini → Check confidence
  │              ↓
  │           If < 0.7 → Claude fallback
  │              ↓
  │           If >= 0.7 → Done
  └─ Critical → Claude (skip Gemini)

Cost: Minimal (mostly free Gemini)
Quality: Best (Claude when needed)
```

---

### Mode 2: Smart Router (Gemini Only)
```
Configuration:
- gemini_api_key: SET
- claude_api_key: NOT SET
- router_mode: smart
- fallback_enabled: true

Flow:
User request
  ↓
Keyword classification
  ├─ Simple → Gemini → Done
  ├─ Complex → Gemini → Warning (no fallback)
  └─ Critical → Gemini → Warning (Claude recommended)

Cost: FREE
Quality: Good (80-85%)
Limitation: No quality fallback
```

---

### Mode 3: Smart Router (Claude Only)
```
Configuration:
- gemini_api_key: NOT SET
- claude_api_key: SET
- router_mode: smart
- fallback_enabled: true

Flow:
User request
  ↓
Keyword classification
  ├─ Simple → Claude (no Gemini to try first)
  ├─ Complex → Claude
  └─ Critical → Claude

Cost: HIGH (always paid API)
Quality: Excellent (95%+)
Limitation: No cost optimization
```

---

### Mode 4: Single Provider - Gemini
```
Configuration:
- gemini_api_key: SET
- claude_api_key: SET or NOT SET
- router_mode: single
- default_provider: gemini

Flow:
User request
  ↓
Always Gemini (ignore keywords, ignore complexity)
  ↓
Done (no confidence check, no fallback)

Cost: FREE
Quality: Good (80-85%)
Use case: Learning, testing, cost-conscious
```

---

### Mode 5: Single Provider - Claude
```
Configuration:
- gemini_api_key: SET or NOT SET
- claude_api_key: SET
- router_mode: single
- default_provider: claude

Flow:
User request
  ↓
Always Claude (ignore keywords, ignore complexity)
  ↓
Done

Cost: HIGH
Quality: Excellent (95%+)
Use case: Production, critical apps
```

---

### Mode 6: Gemini-Only Mode (Force)
```
Configuration:
- gemini_api_key: SET
- claude_api_key: SET
- router_mode: gemini_only
- fallback_enabled: false

Flow:
User request
  ↓
Always Gemini (even if Claude available)
  ↓
Done (never fallback even if confidence low)

Cost: FREE
Quality: Good (80-85%)
Use case: Cost optimization, learning
```

---

### Mode 7: Claude-Only Mode (Force)
```
Configuration:
- gemini_api_key: SET
- claude_api_key: SET
- router_mode: claude_only
- fallback_enabled: false

Flow:
User request
  ↓
Always Claude (skip Gemini even for simple tasks)
  ↓
Done

Cost: HIGH
Quality: Excellent (95%+)
Use case: Production, quality-first
```

---

### Mode 8-12: Error States

**Mode 8: No API Keys**
```
Error: No AI providers configured
Action: Prompt user to set API keys
```

**Mode 9: Invalid Mode**
```
Error: Unknown router_mode
Action: Fall back to smart mode
```

**Mode 10: Gemini API Failure**
```
Error: Gemini API call failed
Action: If Claude available → fallback, else error
```

**Mode 11: Claude API Failure**
```
Error: Claude API call failed
Action: If fallback_enabled and Gemini available → use Gemini
```

**Mode 12: Both APIs Failure**
```
Error: All providers failed
Action: Return error to user
```

---

## Configuration Examples

### Example 1: Smart Router (Recommended)
```json
{
  "router_mode": "smart",
  "fallback_enabled": true,
  "confidence_threshold": 0.7,
  "gemini": {
    "api_key": "YOUR_GEMINI_KEY",
    "model": "gemini-1.5-flash"
  },
  "claude": {
    "api_key": "YOUR_CLAUDE_KEY",
    "model": "claude-sonnet-4"
  }
}
```

**CLI commands:**
```bash
quad config set router.mode smart
quad config set router.fallback true
quad config set router.confidence_threshold 0.7
quad config set gemini.api_key "YOUR_KEY"
quad config set claude.api_key "YOUR_KEY"
```

---

### Example 2: Gemini-Only (Free)
```json
{
  "router_mode": "single",
  "default_provider": "gemini",
  "gemini": {
    "api_key": "YOUR_GEMINI_KEY",
    "model": "gemini-1.5-flash"
  }
}
```

**CLI commands:**
```bash
quad config set router.mode single
quad config set router.provider gemini
quad config set gemini.api_key "YOUR_KEY"
```

---

### Example 3: Claude-Only (Quality)
```json
{
  "router_mode": "single",
  "default_provider": "claude",
  "claude": {
    "api_key": "YOUR_CLAUDE_KEY",
    "model": "claude-sonnet-4"
  }
}
```

**CLI commands:**
```bash
quad config set router.mode single
quad config set router.provider claude
quad config set claude.api_key "YOUR_KEY"
```

---

### Example 4: Cost-Optimized (Gemini + Claude fallback)
```json
{
  "router_mode": "smart",
  "fallback_enabled": true,
  "confidence_threshold": 0.8,  // Higher threshold = more fallbacks
  "gemini": {
    "api_key": "YOUR_GEMINI_KEY",
    "model": "gemini-1.5-flash"
  },
  "claude": {
    "api_key": "YOUR_CLAUDE_KEY",
    "model": "claude-sonnet-4"
  }
}
```

**Result:** Most tasks use Gemini (free), only complex/low-confidence use Claude

---

### Example 5: Quality-First (Claude + Gemini backup)
```json
{
  "router_mode": "single",
  "default_provider": "claude",
  "fallback_enabled": true,
  "gemini": {
    "api_key": "YOUR_GEMINI_KEY"
  },
  "claude": {
    "api_key": "YOUR_CLAUDE_KEY"
  }
}
```

**Result:** Always use Claude, but if Claude fails, use Gemini as backup

---

## Decision Tree

```
┌─────────────────────────────────────┐
│      User runs QUAD command         │
└──────────────┬──────────────────────┘
               ↓
      ┌────────────────┐
      │ Router Mode?   │
      └────────┬───────┘
               ↓
    ┌──────────┴──────────┐
    ↓                     ↓
┌─────────┐         ┌──────────┐
│  Smart  │         │  Single  │
└────┬────┘         └────┬─────┘
     ↓                   ↓
┌─────────────┐     ┌──────────────────┐
│ Classify    │     │ Use configured   │
│ task by     │     │ provider         │
│ keywords    │     │ (gemini/claude)  │
└──────┬──────┘     └────────┬─────────┘
       ↓                     ↓
  ┌────┴────┐               Done
  │ Simple? │
  └────┬────┘
       ↓
   ┌───┴───┐
   │ YES   │ NO
   ↓       ↓
Gemini   ┌──────────┐
  ↓      │ Complex? │
 Done    └────┬─────┘
              ↓
         ┌────┴────┐
         │ YES     │ NO (Critical)
         ↓         ↓
      Gemini    Claude
         ↓         ↓
   ┌──────────┐  Done
   │ Check    │
   │ confidence│
   └────┬─────┘
        ↓
   ┌────┴────┐
   │ >= 0.7? │
   └────┬────┘
        ↓
    ┌───┴───┐
    │ YES   │ NO
    ↓       ↓
   Done   Claude
          (fallback)
            ↓
           Done
```

---

## Usage Examples

### Example 1: Let Router Decide (Smart Mode)
```bash
# Configure smart mode
quad config set router.mode smart
quad config set gemini.api_key "..."
quad config set claude.api_key "..."

# Run command (router decides)
quad story create "Build banking app"

Output:
🎯 Task Classification:
   Complexity: complex
   Recommended: gemini
   Reason: Complex task, try Gemini first

⚡ Trying Gemini (free)...
   Confidence: 0.85

✓ Gemini confidence sufficient (0.85 >= 0.70)

Result: 6 stories generated
Provider: gemini (FREE!)
Cost: $0.00
```

---

### Example 2: Force Gemini (Cost-Conscious)
```bash
# Force Gemini
quad config set router.mode single
quad config set router.provider gemini

# Run command
quad story create "Build banking app"

Output:
🎯 Using Gemini (forced)

Result: 6 stories generated
Provider: gemini
Cost: $0.00
Quality: Good (estimated 85%)
```

---

### Example 3: Force Claude (Quality-First)
```bash
# Force Claude
quad config set router.mode single
quad config set router.provider claude

# Run command
quad story create "Build banking app"

Output:
🎯 Using Claude (forced)

Result: 6 stories generated
Provider: claude
Cost: $0.16
Quality: Excellent (95%+)
```

---

### Example 4: Per-Command Override
```bash
# Default: Smart mode
quad config set router.mode smart

# But override for specific command
quad story create --provider gemini  # Force Gemini
quad code generate --provider claude  # Force Claude
quad test --provider auto             # Use smart router
```

---

## Confidence Threshold Tuning

### Aggressive Cost Savings (threshold = 0.9)
```bash
quad config set router.confidence_threshold 0.9
```
**Result:** Only fallback to Claude if Gemini very uncertain
**Cost:** Minimal (~$0-5/month)
**Quality:** Good (80-85%)

---

### Balanced (threshold = 0.7) - **RECOMMENDED**
```bash
quad config set router.confidence_threshold 0.7
```
**Result:** Fallback to Claude when Gemini somewhat uncertain
**Cost:** Low (~$10-20/month)
**Quality:** Excellent (90%+)

---

### Quality-First (threshold = 0.5)
```bash
quad config set router.confidence_threshold 0.5
```
**Result:** Fallback to Claude for most complex tasks
**Cost:** Moderate (~$30-50/month)
**Quality:** Excellent (93%+)

---

### Always Fallback (threshold = 1.0)
```bash
quad config set router.confidence_threshold 1.0
```
**Result:** Always fallback to Claude (Gemini never confident enough)
**Cost:** HIGH (same as Claude-only)
**Quality:** Excellent (95%+)

---

## Summary

### The Matrix Dimensions

| Dimension | Options |
|-----------|---------|
| **Router Mode** | smart, single, gemini_only, claude_only |
| **Providers** | gemini, claude, both, neither |
| **Complexity** | simple, complex, critical |
| **Confidence** | 0.0-1.0 (threshold configurable) |
| **Fallback** | enabled/disabled |

### Total Combinations: **12 modes**

### Recommended Configurations

| Use Case | Mode | Config |
|----------|------|--------|
| **Learning/Testing** | Gemini-only | `router.mode=single, provider=gemini` |
| **Production** | Smart router | `router.mode=smart, fallback=true, threshold=0.7` |
| **Quality-First** | Claude-only | `router.mode=single, provider=claude` |
| **Cost-Optimized** | Smart router | `router.mode=smart, threshold=0.8` |
| **No Claude API** | Gemini-only | `router.mode=single, provider=gemini` |
| **No Gemini API** | Claude-only | `router.mode=single, provider=claude` |

---

**The router works in ALL scenarios with or without Claude!**

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
