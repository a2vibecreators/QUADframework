# Discussion 6: Claude CLI Hook Integration

**Date:** January 15, 2026
**Topic:** Enabling QUAD commands through Claude CLI with selective hook control
**Key Question:** How to intercept and route QUAD commands in Claude CLI sessions?

---

## The Problem

**Current State:**
- QUAD CLI runs independently: `quad story create`
- Claude CLI runs independently: `claude-code`
- No integration between them

**Desired State:**
User types in Claude CLI:
```
quad init banking-app
```

Claude CLI should:
1. Detect this is a QUAD command
2. Route to QUAD CLI
3. Execute `quad init banking-app`
4. Capture context (pre-hook + post-hook)
5. Return result to Claude CLI

---

## Use Cases

### Use Case 1: Developer Mode (Hooks ON)
**Scenario:** Working on a QUAD project in VS Code

```
User in Claude CLI:
> "Create a new banking project"
Claude: [Suggests using QUAD]
> "quad init banking-portal"
[Hook intercepts, routes to QUAD]
QUAD: [Creates project, captures context]
Claude: [Shows result]
```

**Requirements:**
- Hooks enabled
- All QUAD commands intercepted
- Context captured automatically
- Seamless experience

---

### Use Case 2: Direct Mode (Hooks OFF)
**Scenario:** Discussing QUAD architecture with Claude

```
User in Claude CLI:
> "How should I implement the AI router?"
Claude: [Responds directly, no hooks]
> "Show me examples from the codebase"
Claude: [Reads files, no QUAD interception]
```

**Requirements:**
- Hooks disabled for this session
- Direct Claude access
- No QUAD interception
- Can still use QUAD explicitly if needed

---

### Use Case 3: Selective Mode (Prefix-based)
**Scenario:** Mixed workflow

```
User in Claude CLI:
> "quad story create"       ← Hook intercepts (starts with "quad")
> "ls -la"                  ← No interception (doesn't start with "quad")
> "git status"              ← No interception
> "quad code generate"      ← Hook intercepts
```

**Requirements:**
- Only intercept commands with "quad" prefix
- Everything else passes through normally
- Best of both worlds

---

## Architecture

### Components

```
┌──────────────────────────────────────────────────────┐
│                   User Input                         │
│         "quad init banking-portal"                   │
└──────────────┬───────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────┐
│            Claude CLI (with hooks)                   │
│                                                      │
│  1. Pre-prompt hook checks:                          │
│     should_invoke_quad_hook(input)                   │
│                                                      │
│     ┌─────────────────┐                             │
│     │ Hook Config     │                             │
│     │ enabled: true   │                             │
│     │ mode: prefix    │                             │
│     │ session: xyz    │                             │
│     └─────────────────┘                             │
└──────────────┬───────────────────────────────────────┘
               │
               ├─ YES (is QUAD command)
               │  │
               │  ▼
               │  ┌────────────────────────────────────┐
               │  │     Execute QUAD CLI              │
               │  │                                    │
               │  │  quad init banking-portal          │
               │  │         │                          │
               │  │         ▼                          │
               │  │  [Pre-hook: Load context]          │
               │  │         │                          │
               │  │         ▼                          │
               │  │  [Main command execution]          │
               │  │         │                          │
               │  │         ▼                          │
               │  │  [Post-hook: Store context]        │
               │  └────────────────────────────────────┘
               │                  │
               │                  ▼
               │  ┌────────────────────────────────────┐
               │  │  Return result to Claude CLI       │
               │  └────────────────────────────────────┘
               │
               └─ NO (not QUAD command)
                  │
                  ▼
               ┌────────────────────────────────────┐
               │  Pass to Claude directly           │
               └────────────────────────────────────┘
```

---

## Configuration System

### File: `~/.claude/quad-hooks.json`

```json
{
  "enabled": true,
  "mode": "prefix",
  "prefixes": ["quad-", "quad "],
  "commands": ["init", "story", "code", "test", "doc"],
  "session_override": {
    "session_abc123": false,
    "session_xyz789": true
  },
  "logging": {
    "enabled": true,
    "path": "~/.claude/quad-hooks.log"
  },
  "auto_context": true,
  "fallback": "direct"
}
```

**Fields:**
- `enabled`: Global enable/disable
- `mode`: "prefix" | "whitelist" | "all" | "disabled"
- `prefixes`: List of command prefixes to intercept (for "prefix" mode)
- `commands`: Whitelist of commands (for "whitelist" mode)
- `session_override`: Per-session enable/disable
- `logging`: Hook execution logs
- `auto_context`: Automatically load context in Claude
- `fallback`: What to do if QUAD CLI fails ("direct" | "error")

---

## Hook Detection Logic

### Python Implementation

```python
import json
from pathlib import Path
from typing import Optional, Dict

def load_hook_config() -> Dict:
    """Load QUAD hook configuration"""
    config_path = Path.home() / ".claude" / "quad-hooks.json"

    if not config_path.exists():
        return {
            "enabled": False,
            "mode": "prefix",
            "prefixes": ["quad-", "quad "],
            "commands": ["init", "story", "code", "test", "doc"]
        }

    return json.loads(config_path.read_text())


def get_session_id() -> str:
    """Get current Claude CLI session ID"""
    # TODO: How does Claude CLI track sessions?
    # Option 1: Environment variable
    # Option 2: .claude/current-session file
    # Option 3: Process ID
    return os.environ.get("CLAUDE_SESSION_ID", "default")


def should_invoke_hook(command: str) -> bool:
    """
    Determine if hook should intercept this command.

    Args:
        command: User input string

    Returns:
        True if should route to QUAD CLI
    """
    config = load_hook_config()
    session_id = get_session_id()

    # Check 1: Global enable
    if not config.get("enabled", False):
        return False

    # Check 2: Session override
    session_override = config.get("session_override", {}).get(session_id)
    if session_override is not None:
        return session_override

    # Check 3: Mode-based logic
    mode = config.get("mode", "prefix")

    if mode == "disabled":
        return False

    elif mode == "prefix":
        prefixes = config.get("prefixes", ["quad-", "quad "])
        return any(command.strip().startswith(prefix) for prefix in prefixes)

    elif mode == "whitelist":
        commands = config.get("commands", [])
        cmd_name = command.strip().split()[0]
        return cmd_name in commands

    elif mode == "all":
        return True

    return False


def execute_quad_command(command: str) -> Dict:
    """
    Execute QUAD CLI command and capture result.

    Args:
        command: QUAD command (e.g., "quad init banking-app")

    Returns:
        Dict with stdout, stderr, exit_code
    """
    import subprocess

    # Execute QUAD command
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.returncode,
        "success": result.returncode == 0
    }


def intercept_command(user_input: str) -> Optional[str]:
    """
    Main hook function called by Claude CLI.

    Args:
        user_input: User's input string

    Returns:
        QUAD result if intercepted, None if pass-through
    """
    # Check if should intercept
    if not should_invoke_hook(user_input):
        return None

    # Log interception
    log_hook_execution(user_input)

    # Execute QUAD command
    result = execute_quad_command(user_input)

    if result["success"]:
        # Load context if enabled
        if load_hook_config().get("auto_context", True):
            context = load_quad_context()
            return f"{result['stdout']}\n\n[Context loaded: {context}]"
        return result["stdout"]
    else:
        # Fallback handling
        fallback = load_hook_config().get("fallback", "direct")
        if fallback == "direct":
            return None  # Pass to Claude
        else:
            return f"QUAD Error: {result['stderr']}"


def log_hook_execution(command: str):
    """Log hook execution for debugging"""
    config = load_hook_config()
    if not config.get("logging", {}).get("enabled", False):
        return

    log_path = Path(config["logging"]["path"]).expanduser()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with log_path.open("a") as f:
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] Intercepted: {command}\n")
```

---

## Integration with Claude CLI

### Option 1: User Prompt Submit Hook

Claude CLI supports `<user-prompt-submit-hook>` in settings:

```json
{
  "hooks": {
    "user-prompt-submit": {
      "command": "python3 ~/.quad/hooks/claude-hook.py",
      "stdin": true,
      "action": "passthrough"
    }
  }
}
```

**Hook Script: `~/.quad/hooks/claude-hook.py`**
```python
#!/usr/bin/env python3
import sys
from quad_cli.hooks.claude_integration import intercept_command

# Read user input from stdin
user_input = sys.stdin.read().strip()

# Try to intercept
result = intercept_command(user_input)

if result:
    # QUAD handled it
    print(result)
    sys.exit(0)
else:
    # Pass through to Claude
    print(user_input)
    sys.exit(0)
```

---

### Option 2: Alias-based Routing

Simpler alternative without hooks:

```bash
# ~/.bashrc or ~/.zshrc

# Function to detect QUAD commands
quad-or-claude() {
    if [[ "$1" == quad* ]]; then
        # Route to QUAD
        command "$@"
    else
        # Route to Claude
        claude-code "$@"
    fi
}

# Alias
alias quad="quad-or-claude"
```

**Usage:**
```bash
quad init banking-app    # Goes to QUAD CLI
help me debug           # Goes to Claude
```

---

## QUAD CLI Commands for Hook Control

### New Commands: `quad hooks`

```bash
# Enable/disable hooks globally
quad hooks enable
quad hooks disable

# Check status
quad hooks status
# Output:
#   QUAD Hooks Status
#   ─────────────────
#   Global: Enabled
#   Mode: prefix
#   Session: abc123
#   Session Override: Not set
#   Commands intercepted: quad*, quad *

# Per-session control
quad hooks session enable
quad hooks session disable
quad hooks session status

# Configure mode
quad hooks config set mode prefix
quad hooks config set mode whitelist
quad hooks config set mode all
quad hooks config set mode disabled

# Add/remove prefixes
quad hooks prefix add "q-"
quad hooks prefix remove "quad-"
quad hooks prefix list

# Add/remove whitelisted commands
quad hooks whitelist add "test"
quad hooks whitelist remove "init"
quad hooks whitelist list

# View logs
quad hooks logs
quad hooks logs --tail 50
quad hooks logs --clear

# Test hook
quad hooks test "quad init banking-app"
# Output:
#   Hook would intercept: YES
#   Reason: Matches prefix "quad "
```

---

## Implementation Files

### File Structure

```
quad-cli/
├── quad_cli/
│   ├── hooks/
│   │   ├── claude_integration.py    ← NEW: Claude CLI integration
│   │   ├── hook_detector.py         ← NEW: Detection logic
│   │   └── hook_config.py           ← NEW: Config management
│   └── commands/
│       └── hooks.py                 ← NEW: quad hooks commands
└── scripts/
    └── claude-hook.py               ← NEW: Hook entry point for Claude CLI
```

### `quad_cli/hooks/claude_integration.py`

```python
"""
Claude CLI Integration
======================

Intercept commands in Claude CLI and route to QUAD.

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import subprocess
from pathlib import Path
from typing import Optional, Dict
from .hook_detector import should_invoke_hook
from .hook_config import load_hook_config, log_hook_execution


def execute_quad_command(command: str) -> Dict:
    """Execute QUAD CLI command"""
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "exit_code": result.returncode,
        "success": result.returncode == 0
    }


def load_quad_context() -> str:
    """Load QUAD context for Claude"""
    from quad_cli.contexts import ContextManager

    context_mgr = ContextManager()
    # Get recent context entries
    # Format for Claude to understand
    # Return formatted string
    return "[Context loaded from QUAD]"


def intercept_command(user_input: str) -> Optional[str]:
    """
    Main hook function called by Claude CLI.

    Returns QUAD result if intercepted, None if pass-through.
    """
    if not should_invoke_hook(user_input):
        return None

    log_hook_execution(user_input)

    result = execute_quad_command(user_input)

    if result["success"]:
        config = load_hook_config()
        if config.get("auto_context", True):
            context = load_quad_context()
            return f"{result['stdout']}\n\n{context}"
        return result["stdout"]
    else:
        fallback = load_hook_config().get("fallback", "direct")
        if fallback == "direct":
            return None
        else:
            return f"Error: {result['stderr']}"
```

### `quad_cli/commands/hooks.py`

```python
"""
QUAD Hooks Commands
===================

Manage Claude CLI hook integration.

Commands:
  quad hooks enable/disable
  quad hooks status
  quad hooks config set mode prefix

Copyright (c) 2026 Gopi Suman Addanke. All Rights Reserved.
"""

import click
from quad_cli.hooks.hook_config import (
    load_hook_config,
    save_hook_config,
    get_session_id
)


@click.group()
def hooks():
    """Manage Claude CLI hooks"""
    pass


@hooks.command()
def enable():
    """Enable QUAD hooks globally"""
    config = load_hook_config()
    config["enabled"] = True
    save_hook_config(config)
    click.echo("✓ QUAD hooks enabled")


@hooks.command()
def disable():
    """Disable QUAD hooks globally"""
    config = load_hook_config()
    config["enabled"] = False
    save_hook_config(config)
    click.echo("✓ QUAD hooks disabled")


@hooks.command()
def status():
    """Show hook status"""
    config = load_hook_config()
    session_id = get_session_id()

    click.echo("\nQUAD Hooks Status")
    click.echo("─" * 40)
    click.echo(f"Global: {'Enabled' if config.get('enabled') else 'Disabled'}")
    click.echo(f"Mode: {config.get('mode', 'prefix')}")
    click.echo(f"Session: {session_id}")

    override = config.get("session_override", {}).get(session_id)
    if override is not None:
        click.echo(f"Session Override: {override}")

    if config.get("mode") == "prefix":
        prefixes = config.get("prefixes", [])
        click.echo(f"Prefixes: {', '.join(prefixes)}")

    click.echo()


# ... more commands ...
```

---

## Testing Plan

### Test 1: Hook Interception
```bash
# Setup
quad hooks enable
quad hooks config set mode prefix

# Test
echo "quad init test-app" | python3 ~/.quad/hooks/claude-hook.py

# Expected: QUAD init executes, returns result
```

### Test 2: Pass-Through
```bash
# Setup
quad hooks enable
quad hooks config set mode prefix

# Test
echo "ls -la" | python3 ~/.quad/hooks/claude-hook.py

# Expected: "ls -la" passed through unchanged
```

### Test 3: Session Override
```bash
# Setup
quad hooks enable
quad hooks session disable

# Test
echo "quad story create" | python3 ~/.quad/hooks/claude-hook.py

# Expected: Passed through (session override)
```

### Test 4: Whitelist Mode
```bash
# Setup
quad hooks config set mode whitelist
quad hooks whitelist add "init"

# Test 1
echo "quad init app" | python3 ~/.quad/hooks/claude-hook.py
# Expected: Intercepted

# Test 2
echo "quad story create" | python3 ~/.quad/hooks/claude-hook.py
# Expected: Passed through (not in whitelist)
```

---

## Open Questions

### Q1: How does Claude CLI track sessions?
**Options:**
- Environment variable (`CLAUDE_SESSION_ID`)
- File in `.claude/` folder
- Process ID
- Need to investigate Claude CLI internals

### Q2: Where to store session overrides?
**Options:**
- In `quad-hooks.json` (current approach)
- Separate file per session (`.claude/sessions/abc123.json`)
- In-memory only (lost on restart)

### Q3: Context auto-loading format?
**Question:** How to format QUAD context for Claude to understand?

**Options:**
```
Option A: Markdown summary
─────────────────────────
[QUAD Context]
- Project: banking-portal
- Tech Stack: React, Node.js, PostgreSQL
- Recent: Created 5 stories for account management

Option B: Structured data
─────────────────────────
<quad_context>
  <project>banking-portal</project>
  <stack>React, Node.js, PostgreSQL</stack>
  <recent>5 stories created</recent>
</quad_context>

Option C: JSON
─────────────────────────
{
  "quad_context": {
    "project": "banking-portal",
    "stack": ["React", "Node.js", "PostgreSQL"],
    "recent": "5 stories created"
  }
}
```

**Recommendation:** Option A (Markdown) - Most readable for Claude

### Q4: Error handling?
**Question:** What if QUAD CLI is not installed?

**Options:**
- Fallback to direct Claude
- Show error message
- Offer to install QUAD

---

## Recommendations

### Phase 1: Basic Hook (This Week) ✅
- Implement hook detection logic
- Create `quad hooks` commands
- Test with simple script

### Phase 2: Claude Integration (Next Week)
- Integrate with Claude CLI hooks
- Test in real Claude CLI sessions
- Add session tracking

### Phase 3: Context Auto-Loading (Week 3)
- Format context for Claude
- Auto-inject on hook execution
- Test with real workflows

### Phase 4: Polish (Week 4)
- Logging system
- Error handling
- Documentation
- User testing with Pradeep

---

## User Workflow Examples

### Example 1: New Project Setup

```
User in Claude CLI (Hooks ON):
> "I need to create a banking app"

Claude: "I can help you set up a QUAD project. Would you like to initialize it?"

User: "Yes"

Claude: "I'll run: quad init banking-portal"

[Hook intercepts]
[QUAD executes]
[Context captured]

Claude: "Project initialized! Tech stack saved to context."

User: "Now create user stories for accounts"

Claude: "Running: quad story create"

[Hook intercepts]
[Loads tech stack from context]
[Generates stories]

Claude: "Created 8 stories. Want to review?"
```

---

### Example 2: Mixed Workflow

```
User in Claude CLI (Hooks: Prefix mode):
> "quad init banking-app"       ← Intercepted
> "git status"                  ← Passed through to Claude
> "quad story create"           ← Intercepted
> "help me understand PGCE"     ← Passed through to Claude
> "quad code generate"          ← Intercepted
```

---

## Success Criteria

✅ **Functional:**
- Hook intercepts QUAD commands correctly
- Pass-through works for non-QUAD commands
- Session overrides work independently
- No impact on Claude performance

✅ **User Experience:**
- Seamless integration (feels native)
- Clear status messages
- Easy enable/disable
- Good error messages

✅ **Reliability:**
- No false positives (wrong interception)
- No false negatives (missed interception)
- Graceful failure (if QUAD not installed)
- No data loss

---

## Next Steps

1. ✅ Update BACKLOG.md (Done)
2. ✅ Create this discussion document (Done)
3. Implement hook detection logic
4. Implement `quad hooks` commands
5. Create Claude CLI hook script
6. Test with real Claude CLI sessions
7. Document for users
8. Get Pradeep to test

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
