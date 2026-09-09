# QUAD CLI Demo Journey

**Version:** 1.0
**Last Updated:** January 2026
**Author:** Suman Addanke

---

## Overview

This folder contains the complete test journey for demonstrating QUAD CLI on a fresh laptop. Use these documents in sequence.

---

## Document Index

| # | Document | Description | Time |
|---|----------|-------------|------|
| 0 | [00-PREREQUISITES.md](./00-PREREQUISITES.md) | Install VS Code, Claude CLI, Python, Git | 15 min |
| 1 | [01-INSTALLATION.md](./01-INSTALLATION.md) | Install QUAD CLI and verify | 5 min |
| 2 | [02-DEMO-WALKTHROUGH.md](./02-DEMO-WALKTHROUGH.md) | Full demo: login → init → story → code → test → charts | 20 min |

---

## Quick Flow

```
┌────────────────────┐
│  00-PREREQUISITES  │  Install VS Code, Claude CLI, Python
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  01-INSTALLATION   │  Install QUAD CLI
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│  02-DEMO-WALKTHROUGH│
├────────────────────┤
│  Step 1: quad login │
│  Step 2: quad init  │
│  Step 3: quad story │
│  Step 4: quad code  │
│  Step 5: quad test  │
│  Step 6: quad charts│
└────────────────────┘
```

---

## Demo Commands Summary

```bash
# After prerequisites installed:
quad login --google           # Step 1: Login with Google SSO
quad init banking-portal      # Step 2: Create project
cd banking-portal
quad story create             # Step 3: Generate stories
quad code generate            # Step 4: Generate code
quad test                     # Step 5: Run tests
quad burnout                  # Step 6a: Team analytics
quad chart velocity           # Step 6b: Sprint charts
```

---

## Files Created During Demo

| Step | Files Created |
|------|---------------|
| Login | `~/.quad/config.json` |
| Init | `banking-portal/.quad/config.json` |
| Init | `banking-portal/README.md` |
| Init | `banking-portal/CLAUDE.md` |
| Init | `banking-portal/documentation/*/README.md` |
| Story | `banking-portal/.quad/stories.json` |

---

## Database Tables Affected

| Step | Table | Operation |
|------|-------|-----------|
| Login | `quad_users` | INSERT/UPDATE |
| Login | `quad_user_activity` | INSERT |
| Init | `quad_domains` | INSERT |
| Story | `quad_stories` | INSERT |
| Code | `quad_code_generations` | INSERT |
| Test | `quad_test_runs` | INSERT |

---

## Verification Queries

```sql
-- After Login
SELECT * FROM quad_users ORDER BY created_at DESC LIMIT 1;

-- After Init
SELECT * FROM quad_domains WHERE slug = 'banking-portal';

-- After Story
SELECT * FROM quad_stories WHERE project_slug = 'banking-portal';

-- Full activity log
SELECT * FROM quad_user_activity ORDER BY created_at DESC LIMIT 20;
```

---

## Related Documents

- [TEST_JOURNEYS.md](../../TEST_JOURNEYS.md) - All test journeys
- [JOURNEY_AUTH_LOGIN.md](../JOURNEY_AUTH_LOGIN.md) - Detailed auth testing

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
