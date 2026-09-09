# QUAD Demo - Step 1: Installation

**Document:** Installing QUAD CLI Commands
**Version:** 1.0
**Last Updated:** January 2026
**Author:** Suman Addanke

---

## Overview

This document covers installing the QUAD CLI tool.

**Prerequisites:** Complete [00-PREREQUISITES.md](./00-PREREQUISITES.md) first.
**Time Required:** ~5 minutes

---

## STEP 1.1: Install QUAD CLI

### Option A: From Downloads (Recommended)

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1.1.1 | Run: `curl -fsSL https://downloads.quadframe.work/install.sh \| bash` | Script runs | [ ] |
| 1.1.2 | Wait for completion | "Installation complete" | [ ] |
| 1.1.3 | Run: `quad --version` | Version shown | [ ] |

### Option B: From Source (Development)

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1.1.1 | `cd ~/git` | In git folder | [ ] |
| 1.1.2 | `git clone https://github.com/a2vibes/a2vibes.git` | Repo cloned | [ ] |
| 1.1.3 | `cd a2vibes/QUAD/quad-cli` | In quad-cli folder | [ ] |
| 1.1.4 | `pip3 install -e .` | Install completes | [ ] |
| 1.1.5 | `quad --version` | Version shown | [ ] |

### Option C: Using pip (When Published)

```bash
pip3 install quad-cli
```

---

## STEP 1.2: Verify Installation

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1.2.1 | Run: `quad --version` | `quad, version 0.1.0` | [ ] |
| 1.2.2 | Run: `quad --help` | Commands listed | [ ] |
| 1.2.3 | Run: `which quad` | Path shown | [ ] |

### Expected Output: quad --version

```
quad, version 0.1.0
```

### Expected Output: quad --help

```
Usage: quad [OPTIONS] COMMAND [ARGS]...

  QUAD CLI - Quick Unified Agentic Development

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  burnout   Show team burnout analysis.
  chart     Show sprint charts and analytics.
  code      Generate code using PGCE algorithm.
  deploy    Deploy projects to GCP.
  hook      Run as Claude Code hook (internal use).
  init      Initialize a new project.
  login     Authenticate with QUAD via Google SSO or API key.
  question  Ask a question with org context.
  status    Show current QUAD configuration status.
  story     Generate user stories from description using PGCE.
  test      Run tests on generated code.
```

---

## STEP 1.3: Check Status (Before Login)

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 1.3.1 | Run: `quad status` | Status displayed | [ ] |
| 1.3.2 | Verify "Not authenticated" message | Warning shown | [ ] |

### Expected Output

```
  QUAD Status
  ───────────

  ⚠ Not authenticated. Run: quad login
  → No domain set
  → API URL: https://api.quadframe.work
```

---

## Files Created

| File | Location | Description |
|------|----------|-------------|
| quad binary | `/usr/local/bin/quad` or `~/.local/bin/quad` | CLI executable |
| Python package | `site-packages/quad_cli/` | Python modules |

### Verification

```bash
# Find where quad is installed
which quad
# Expected: /usr/local/bin/quad or ~/.local/bin/quad

# Check Python package
pip3 show quad-cli
# Expected: Package info displayed
```

---

## Troubleshooting

### "quad: command not found"

| Cause | Solution |
|-------|----------|
| Not in PATH | `export PATH="$HOME/.local/bin:$PATH"` |
| Not installed | Re-run `pip3 install -e .` |

**Make PATH permanent:**
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### "Permission denied"

```bash
# Make executable
chmod +x $(which quad)

# Or reinstall with --user
pip3 install --user -e .
```

### "ModuleNotFoundError"

```bash
# Reinstall dependencies
cd ~/git/a2vibes/QUAD/quad-cli
pip3 install -e .
```

### "Wrong Python version"

```bash
# Check version
python3 --version

# If < 3.10, upgrade:
brew upgrade python@3.11
```

---

## Installation Checklist

| # | Check | Command | Expected | Pass/Fail |
|---|-------|---------|----------|-----------|
| 1 | Installed | `quad --version` | 0.1.0 | [ ] |
| 2 | Help works | `quad --help` | Commands shown | [ ] |
| 3 | Status works | `quad status` | "Not authenticated" | [ ] |
| 4 | In PATH | `which quad` | Path shown | [ ] |

---

## Next Step

→ [02-DEMO-WALKTHROUGH.md](./02-DEMO-WALKTHROUGH.md) - Full Demo Flow

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
