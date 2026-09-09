# QUAD Demo - Step 0: Prerequisites

**Document:** Prerequisites for QUAD CLI Demo
**Version:** 1.0
**Last Updated:** January 2026
**Author:** Suman Addanke

---

## Overview

This document covers setting up a **new laptop** before running QUAD CLI commands.

**Time Required:** ~15 minutes

---

## Required Software

| Software | Version | Purpose | Verification |
|----------|---------|---------|--------------|
| VS Code | Latest | IDE | `code --version` |
| Claude CLI | Latest | AI assistant | `claude --version` |
| Python | 3.10+ | QUAD runtime | `python3 --version` |
| Git | Latest | Version control | `git --version` |

---

## STEP 0.1: Install Visual Studio Code

### macOS Installation

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 0.1.1 | Download from https://code.visualstudio.com | Download starts | [ ] |
| 0.1.2 | Open DMG and drag to Applications | VS Code in Applications | [ ] |
| 0.1.3 | Open VS Code | App launches | [ ] |
| 0.1.4 | Cmd+Shift+P → "Shell Command: Install 'code'" | Success message | [ ] |

### Alternative: Homebrew

```bash
brew install --cask visual-studio-code
```

### Verification

```bash
code --version
```

**Expected Output:**
```
1.85.0
abc123def456
x64
```

---

## STEP 0.2: Install Claude CLI

### Installation

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 0.2.1 | Run: `npm install -g @anthropic-ai/claude-code` | Install completes | [ ] |
| 0.2.2 | Run: `claude --version` | Version displayed | [ ] |
| 0.2.3 | Run: `claude login` | Browser opens | [ ] |
| 0.2.4 | Login with Anthropic account | "Login successful" | [ ] |
| 0.2.5 | Run: `claude status` | Shows logged in | [ ] |

### Alternative: Homebrew

```bash
brew install claude-code
```

### Verification

```bash
claude --version
# Expected: claude-code version X.X.X

claude status
# Expected: Shows authentication status
```

### Files Created

| File | Location | Purpose |
|------|----------|---------|
| Config | `~/.claude/config.json` | Settings |
| Auth | `~/.claude/credentials.json` | Tokens |

### Verification Query

```bash
ls -la ~/.claude/
# Should show config.json and credentials.json
```

---

## STEP 0.3: Install Python

### macOS Installation

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 0.3.1 | Run: `brew install python@3.11` | Install completes | [ ] |
| 0.3.2 | Run: `python3 --version` | Python 3.11.x shown | [ ] |
| 0.3.3 | Run: `pip3 --version` | pip version shown | [ ] |

### Verification

```bash
python3 --version
# Expected: Python 3.11.x

pip3 --version
# Expected: pip 23.x.x from ...
```

### Troubleshooting

```bash
# If python3 not found, add to PATH:
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## STEP 0.4: Install Git

### macOS Installation

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 0.4.1 | Run: `xcode-select --install` | Xcode tools install | [ ] |
| 0.4.2 | Run: `git --version` | git 2.x.x shown | [ ] |

### Alternative: Homebrew

```bash
brew install git
```

### Verification

```bash
git --version
# Expected: git version 2.x.x
```

---

## STEP 0.5: Create Demo Workspace

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| 0.5.1 | Run: `mkdir -p ~/github-demo` | Directory created | [ ] |
| 0.5.2 | Run: `cd ~/github-demo` | In github-demo folder | [ ] |
| 0.5.3 | Run: `pwd` | Shows ~/github-demo | [ ] |

### Verification

```bash
mkdir -p ~/github-demo
cd ~/github-demo
pwd
# Expected: /Users/<username>/github-demo
```

---

## Final Checklist

Before proceeding to QUAD installation, verify ALL items:

| # | Check | Command | Expected | Pass/Fail |
|---|-------|---------|----------|-----------|
| 1 | VS Code | `code --version` | Version number | [ ] |
| 2 | Claude CLI | `claude --version` | Version number | [ ] |
| 3 | Claude Auth | `claude status` | Logged in | [ ] |
| 4 | Python | `python3 --version` | 3.10+ | [ ] |
| 5 | pip | `pip3 --version` | Version number | [ ] |
| 6 | Git | `git --version` | 2.x.x | [ ] |
| 7 | Workspace | `ls ~/github-demo` | Empty dir | [ ] |

---

## Troubleshooting

### "command not found: code"

```bash
# Open VS Code manually, then:
# Cmd+Shift+P → "Shell Command: Install 'code' command in PATH"
```

### "command not found: claude"

```bash
# Check npm global bin directory
npm config get prefix
# Add to PATH if needed
export PATH="$(npm config get prefix)/bin:$PATH"
```

### "command not found: python3"

```bash
# Check if Python installed via brew
brew list python@3.11

# If not, install:
brew install python@3.11
```

### Permission Denied

```bash
# Use --user flag for pip installs
pip3 install --user <package>

# Or fix npm permissions
sudo chown -R $(whoami) ~/.npm
```

---

## Next Step

→ [01-INSTALLATION.md](./01-INSTALLATION.md) - Install QUAD CLI

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
