# QUAD Setup Guide

**Choose your path based on what you want to do with QUAD.**

---

## Choose Your Path

| I want to... | You are a... | Setup Guide |
|--------------|--------------|-------------|
| **Build apps using QUAD** | QUAD Developer | [QUAD_DEVELOPER_SETUP.md](./QUAD_DEVELOPER_SETUP.md) |
| **Build QUAD itself** | QUAD Contributor | [QUAD_CONTRIBUTOR_SETUP.md](./QUAD_CONTRIBUTOR_SETUP.md) |

---

## Understanding the Roles

### QUAD Developer

**Analogy:** Like a **Java Developer** who uses `javac` to compile code.

- Uses QUAD CLI to build applications
- Doesn't need source code access
- Installs via `curl` command
- Focus: Building apps

### QUAD Contributor

**Analogy:** Like the **JDK Team** who builds `javac` itself.

- Builds and improves QUAD framework
- Needs full source code access
- Clones repository and builds locally
- Focus: Building the tool

---

## Comparison Table

| Aspect | QUAD Developer | QUAD Contributor |
|--------|---------------|------------------|
| **Analogy** | Java Developer | JDK Team |
| **Goal** | Build apps WITH QUAD | Build QUAD itself |
| **Install Method** | `curl install.sh` | Clone repo + pip install -e |
| | | |
| **Prerequisites** | | |
| VS Code | Required | Required |
| Claude CLI | Required | Required |
| Python 3.10+ | Required | Required |
| Git | Required | Required |
| Node.js 18+ | Not needed | Required |
| Firebase CLI | Not needed | Required |
| GCP CLI | Not needed | Required |
| Bitwarden CLI | Not needed | Required |
| Docker | Not needed | Required |
| | | |
| **Access** | | |
| Source Code | Not needed | a2vibes repo |
| Vaultwarden | Not needed | Required |
| Firebase Project | Not needed | Required |
| GCP Project | Not needed | Required |

---

## Quick Start

### For QUAD Developers

```bash
# 1. Install prerequisites (VS Code, Claude CLI, Python, Git)

# 2. Install QUAD CLI
curl -fsSL https://downloads.quadframe.work/install.sh | bash

# 3. Login
quad login --google

# 4. Create project
quad init my-app
cd my-app

# 5. Start building!
quad story create
quad code generate
quad test
```

### For QUAD Contributors

```bash
# 1. Complete Developer setup first

# 2. Install additional tools
brew install node@18
npm install -g firebase-tools
brew install google-cloud-sdk
brew install bitwarden-cli

# 3. Clone repository
git clone git@github.com:a2Vibes/a2vibes.git
cd a2vibes

# 4. Install from source
cd QUAD/quad-cli
pip3 install -e .

# 5. Setup Vaultwarden
bw config server https://vault.a2vibes.tech
bw login
```

---

## Detailed Guides

| Guide | Description | Time |
|-------|-------------|------|
| [QUAD_DEVELOPER_SETUP.md](./QUAD_DEVELOPER_SETUP.md) | Full developer setup | 15 min |
| [QUAD_CONTRIBUTOR_SETUP.md](./QUAD_CONTRIBUTOR_SETUP.md) | Full contributor setup | 30 min |

---

## Related Documentation

| Document | Description |
|----------|-------------|
| [Demo Walkthrough](../testing/journeys/demo/) | Step-by-step demo |
| [Developer Onboarding](../getting-started/DEVELOPER_ONBOARDING.md) | Detailed onboarding |
| [Team Access](../getting-started/TEAM_ACCESS.md) | Vaultwarden access |

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
