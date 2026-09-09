# QUAD Developer Setup

**For developers who want to USE QUAD to build applications**

**Version:** 1.0
**Last Updated:** January 2026
**Author:** Suman Addanke

---

## Overview

This guide is for **QUAD Developers** - people who use QUAD to build applications.

**Analogy:** You are like a **Java Developer** who uses `javac` to compile code. You don't need to know how `javac` is built - you just need it installed and working.

**What you will do:**
- Install QUAD CLI
- Use `quad` commands to generate user stories
- Use `quad` commands to generate code
- Use `quad` commands to run tests

**What you will NOT need:**
- Build QUAD from source
- Access to QUAD infrastructure (GCP, Firebase)
- Vaultwarden secrets access

---

## Prerequisites

### Required Software

| Software | Version | Purpose | Verify Command |
|----------|---------|---------|----------------|
| VS Code | Latest | IDE for development | `code --version` |
| Claude CLI | Latest | AI assistant | `claude --version` |
| Python | 3.10+ | QUAD CLI runtime | `python3 --version` |
| Git | 2.x+ | Version control | `git --version` |

### NOT Required

| Software | Why NOT Needed |
|----------|----------------|
| Node.js | Only for building QUAD itself |
| Firebase CLI | Only for deploying QUAD infrastructure |
| GCP CLI | Only for QUAD cloud infrastructure |
| Source Code | Install via curl (no repo clone needed) |
| Vaultwarden | Only for QUAD Contributors |

---

## Step 1: Install Prerequisites

### 1.1 Install VS Code

**macOS (Homebrew):**
```bash
brew install --cask visual-studio-code
```

**Or download from:** https://code.visualstudio.com

**Verify:**
```bash
code --version
```

### 1.2 Install Claude CLI

```bash
npm install -g @anthropic-ai/claude-code
```

**Or via Homebrew:**
```bash
brew install claude-code
```

**Login to Claude:**
```bash
claude login
```

**Verify:**
```bash
claude --version
claude status
```

### 1.3 Install Python

**macOS (Homebrew):**
```bash
brew install python@3.11
```

**Verify:**
```bash
python3 --version
# Expected: Python 3.11.x or higher

pip3 --version
# Expected: pip 23.x.x or higher
```

### 1.4 Install Git

**macOS:**
```bash
xcode-select --install
```

**Or via Homebrew:**
```bash
brew install git
```

**Verify:**
```bash
git --version
# Expected: git version 2.x.x
```

---

## Step 2: Install QUAD CLI

### One-Line Install

```bash
curl -fsSL https://downloads.quadframe.work/install.sh | bash
```

This will:
1. Download QUAD CLI package
2. Install Python dependencies
3. Add `quad` command to your PATH

### Verify Installation

```bash
quad --version
# Expected: quad, version 0.1.0

quad --help
# Expected: Shows all available commands
```

### Expected Commands

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
  init      Initialize a new project.
  login     Authenticate with QUAD via Google SSO.
  question  Ask a question with org context.
  status    Show current QUAD configuration status.
  story     Generate user stories from description.
  test      Run tests on generated code.
```

---

## Step 3: Login to QUAD

```bash
quad login --google
```

This will:
1. Open browser for Google authentication
2. Authenticate with QUAD API
3. Store credentials locally

**Verify:**
```bash
quad status
```

Expected output shows your organization and authentication status.

---

## Step 4: Create Your First Project

### Initialize Project

```bash
# Create project directory
mkdir ~/github-demo
cd ~/github-demo

# Open in VS Code
code .

# In VS Code terminal, initialize QUAD project
quad init banking-portal
```

### Navigate to Project

```bash
cd banking-portal
```

---

## Step 5: Use QUAD Commands

### Generate User Stories

```bash
quad story create
```

Follow the prompts to describe your feature. QUAD will generate prioritized user stories.

### Generate Code

```bash
quad code generate
```

QUAD will generate code based on your stories using the PGCE algorithm.

### Run Tests

```bash
quad test
```

Run automated tests on generated code.

### View Analytics

```bash
quad burnout
quad chart
```

View team burnout analysis and sprint charts.

---

## Quick Reference

### Daily Workflow

```bash
# 1. Open project
cd ~/github-demo/banking-portal
code .

# 2. Check status
quad status

# 3. Create stories
quad story create

# 4. Generate code
quad code generate

# 5. Run tests
quad test

# 6. View analytics
quad burnout
quad chart
```

### All QUAD Commands

| Command | Description |
|---------|-------------|
| `quad login --google` | Authenticate with Google SSO |
| `quad status` | Show configuration status |
| `quad init <name>` | Initialize new project |
| `quad story create` | Generate user stories |
| `quad code generate` | Generate code |
| `quad test` | Run tests |
| `quad burnout` | Show burnout analysis |
| `quad chart` | Show sprint charts |
| `quad deploy` | Deploy to GCP |
| `quad question` | Ask question with context |

---

## Troubleshooting

### "quad: command not found"

```bash
# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Make permanent
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### "No such option: --google"

You have an old version installed. Reinstall:

```bash
pip3 uninstall quad-cli
curl -fsSL https://downloads.quadframe.work/install.sh | bash
```

### "Not authenticated"

```bash
quad login --google
```

### "Python not found"

```bash
brew install python@3.11
```

---

## Prerequisites Checklist

Before you start, verify all items:

| # | Check | Command | Expected |
|---|-------|---------|----------|
| 1 | VS Code | `code --version` | Version number |
| 2 | Claude CLI | `claude --version` | Version number |
| 3 | Claude Auth | `claude status` | Logged in |
| 4 | Python | `python3 --version` | 3.10+ |
| 5 | pip | `pip3 --version` | Version number |
| 6 | Git | `git --version` | 2.x.x |
| 7 | QUAD CLI | `quad --version` | 0.1.0 |
| 8 | QUAD Auth | `quad status` | Organization shown |

---

## Next Steps

- **Detailed Demo:** See [testing/journeys/demo/](../testing/journeys/demo/) for step-by-step walkthrough
- **QUAD Methodology:** See [methodology/QUAD.md](../methodology/QUAD.md)
- **Become Contributor:** See [QUAD_CONTRIBUTOR_SETUP.md](./QUAD_CONTRIBUTOR_SETUP.md)

---

## Getting Help

- **Documentation:** https://quadframe.work/docs
- **Email:** contact@a2vibecreators.com

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
