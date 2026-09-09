# QUAD Contributor Setup

**For developers who want to BUILD QUAD itself**

**Version:** 1.0
**Last Updated:** January 2026
**Author:** Suman Addanke

---

## Overview

This guide is for **QUAD Contributors** - people who build QUAD itself.

**Analogy:** You are like the **JDK Team** who builds `javac`. You need access to source code, build tools, and infrastructure.

**What you will do:**
- Clone QUAD source code
- Build and test QUAD CLI locally
- Deploy QUAD infrastructure (Firebase, GCP)
- Access secrets via Vaultwarden

**Prerequisite:** Complete [QUAD_DEVELOPER_SETUP.md](./QUAD_DEVELOPER_SETUP.md) first!

---

## Prerequisites

### Developer Prerequisites (Required First)

Complete the [QUAD Developer Setup](./QUAD_DEVELOPER_SETUP.md) first:

| Software | Version | Verify Command |
|----------|---------|----------------|
| VS Code | Latest | `code --version` |
| Claude CLI | Latest | `claude --version` |
| Python | 3.10+ | `python3 --version` |
| Git | 2.x+ | `git --version` |

### Additional Contributor Prerequisites

| Software | Version | Purpose | Install |
|----------|---------|---------|---------|
| Node.js | 18+ | QUAD platform dev | `brew install node@18` |
| npm | 9+ | Package management | Comes with Node.js |
| Firebase CLI | Latest | Deploy downloads site | `npm install -g firebase-tools` |
| GCP CLI | Latest | Cloud infrastructure | `brew install google-cloud-sdk` |
| Bitwarden CLI | Latest | Vaultwarden access | `brew install bitwarden-cli` |
| Docker | Latest | Local databases | Docker Desktop |

### Access Requirements

| Access | Purpose | Request From |
|--------|---------|--------------|
| GitHub (a2Vibes org) | Source code | Suman |
| Vaultwarden | Secrets | Suman |
| Firebase Project | Deploy | Suman |
| GCP Project | Cloud | Suman |

---

## Step 1: Install Additional Tools

### 1.1 Install Node.js

```bash
brew install node@18
```

**Verify:**
```bash
node --version
# Expected: v18.x.x or higher

npm --version
# Expected: 9.x.x or higher
```

### 1.2 Install Firebase CLI

```bash
npm install -g firebase-tools
```

**Login:**
```bash
firebase login
```

**Verify:**
```bash
firebase --version
# Expected: 13.x.x or higher
```

### 1.3 Install GCP CLI

```bash
brew install google-cloud-sdk
```

**Login:**
```bash
gcloud auth login
gcloud config set project quad-framework
```

**Verify:**
```bash
gcloud --version
```

### 1.4 Install Bitwarden CLI

```bash
brew install bitwarden-cli
```

**Configure Vaultwarden:**
```bash
bw config server https://vault.a2vibes.tech
bw login
```

**Unlock:**
```bash
export BW_SESSION=$(bw unlock --raw)
```

**Verify:**
```bash
bw list organizations
# Should show QUAD organization
```

### 1.5 Install Docker

Download Docker Desktop from: https://www.docker.com/products/docker-desktop

**Verify:**
```bash
docker --version
docker-compose --version
```

---

## Step 2: Clone Repository

### 2.1 Clone a2vibes Repository

```bash
cd ~/git
git clone git@github.com:a2Vibes/a2vibes.git
cd a2vibes
```

### 2.2 Initialize Submodules

```bash
git submodule update --init --recursive
```

---

## Step 3: Install QUAD CLI from Source

### 3.1 Navigate to quad-cli

```bash
cd ~/git/a2vibes/QUAD/quad-cli
```

### 3.2 Install in Development Mode

```bash
pip3 install -e .
```

This installs QUAD CLI from source code (editable mode).

### 3.3 Verify

```bash
quad --version
# Expected: quad, version 0.1.0

which quad
# Should point to your local installation
```

---

## Step 4: Setup Development Environment

### 4.1 Run Setup Script

```bash
cd ~/git/a2vibes/QUAD
chmod +x scripts/setup-dev-environment.sh
./scripts/setup-dev-environment.sh
```

This will:
- Fetch secrets from Vaultwarden
- Create `.env.local` files
- Configure local environment

### 4.2 Start Local Databases

```bash
# Start QUAD dev database
docker-compose -f docker/docker-compose.dev.yml up -d
```

---

## Step 5: Build and Deploy

### 5.1 Build QUAD CLI Package

```bash
cd ~/git/a2vibes/QUAD/quad-cli
./build-package.sh
```

Creates: `dist/quad-cli-0.1.0.tar.gz`

### 5.2 Deploy to downloads.quadframe.work

```bash
# Copy package to web folder
cp dist/quad-cli-0.1.0.tar.gz ~/git/a2vibes/QUAD-web/public/

# Deploy via Firebase
cd ~/git/a2vibes/QUAD-web
firebase deploy --only hosting
```

### 5.3 Verify Deployment

```bash
curl -I https://downloads.quadframe.work/install.sh
# Should return HTTP/2 200
```

---

## Project Structure

```
a2vibes/
├── QUAD/                        # QUAD Framework
│   ├── quad-cli/                # CLI source code
│   │   ├── quad_cli/            # Python package
│   │   ├── setup.py             # Package config
│   │   └── build-package.sh     # Build script
│   ├── documentation/           # All docs (you are here)
│   └── scripts/                 # Dev scripts
├── QUAD-web/                    # Downloads site
│   ├── public/                  # Static files
│   │   ├── install.sh           # Installer script
│   │   └── quad-cli-*.tar.gz    # CLI packages
│   └── firebase.json            # Firebase config
├── SUMA/                        # SUMA Platform
└── NutriNine/                   # NutriNine App
```

---

## Development Workflow

### Making Changes to QUAD CLI

```bash
# 1. Navigate to quad-cli
cd ~/git/a2vibes/QUAD/quad-cli

# 2. Make changes to Python code
# Edit files in quad_cli/

# 3. Test locally (already in dev mode)
quad --version
quad story create

# 4. Build package
./build-package.sh

# 5. Test package locally
pip3 install dist/quad-cli-0.1.0.tar.gz

# 6. Deploy
cp dist/quad-cli-0.1.0.tar.gz ~/git/a2vibes/QUAD-web/public/
cd ~/git/a2vibes/QUAD-web
firebase deploy --only hosting
```

### Updating Documentation

```bash
# 1. Navigate to documentation
cd ~/git/a2vibes/QUAD/documentation

# 2. Edit markdown files

# 3. Commit changes
git add .
git commit -m "docs: Update setup guide"
git push
```

---

## Quick Reference

### Key Commands

```bash
# Vaultwarden
bw config server https://vault.a2vibes.tech
export BW_SESSION=$(bw unlock --raw)

# QUAD CLI (dev mode)
cd ~/git/a2vibes/QUAD/quad-cli
pip3 install -e .

# Build & Deploy
./build-package.sh
firebase deploy --only hosting

# Databases
docker-compose -f docker/docker-compose.dev.yml up -d
docker-compose -f docker/docker-compose.dev.yml down
```

### Key URLs

| URL | Purpose |
|-----|---------|
| https://vault.a2vibes.tech | Vaultwarden |
| https://downloads.quadframe.work | Downloads site |
| https://quadframe.work | Main site |
| https://dev.quadframe.work | Dev environment |
| https://qa.quadframe.work | QA environment |

### Key Ports

| Port | Service |
|------|---------|
| 14001 | QUAD DEV Web |
| 14101 | QUAD DEV API |
| 14201 | QUAD DEV Database |
| 15001 | QUAD QA Web |
| 15101 | QUAD QA API |
| 15201 | QUAD QA Database |

---

## Detailed Documentation

For more detailed setup instructions, see:

| Document | Description |
|----------|-------------|
| [DEVELOPER_ONBOARDING.md](../getting-started/DEVELOPER_ONBOARDING.md) | Full onboarding with Vaultwarden |
| [TEAM_ACCESS.md](../getting-started/TEAM_ACCESS.md) | Vaultwarden access guide |
| [GETTING_STARTED.md](../getting-started/GETTING_STARTED.md) | Platform development |
| [SETUP_INSTRUCTIONS.md](../getting-started/SETUP_INSTRUCTIONS.md) | Database & OAuth setup |

---

## Prerequisites Checklist

### Developer Prerequisites

| # | Check | Command | Expected |
|---|-------|---------|----------|
| 1 | VS Code | `code --version` | Version number |
| 2 | Claude CLI | `claude --version` | Version number |
| 3 | Python | `python3 --version` | 3.10+ |
| 4 | Git | `git --version` | 2.x.x |

### Contributor Prerequisites

| # | Check | Command | Expected |
|---|-------|---------|----------|
| 5 | Node.js | `node --version` | v18+ |
| 6 | npm | `npm --version` | 9+ |
| 7 | Firebase | `firebase --version` | 13+ |
| 8 | GCP | `gcloud --version` | Version info |
| 9 | Bitwarden | `bw --version` | Version number |
| 10 | Docker | `docker --version` | Version number |
| 11 | Vault Access | `bw list organizations` | QUAD org shown |
| 12 | Repo Clone | `ls ~/git/a2vibes` | Directory exists |

---

## Getting Help

- **Slack:** #quad-dev channel
- **Email:** suman.addanki@gmail.com
- **Vaultwarden:** https://vault.a2vibes.tech

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
