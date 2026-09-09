# QUAD Demo - Step 2: Demo Walkthrough

**Document:** Complete QUAD CLI Demo Flow
**Version:** 1.0
**Last Updated:** January 2026
**Author:** Suman Addanke

---

## Overview

This document contains the full demo walkthrough for QUAD CLI.

**Prerequisites:** Complete [01-INSTALLATION.md](./01-INSTALLATION.md) first.
**Time Required:** ~20 minutes

**Features Covered:**
- Google SSO Authentication
- Project Initialization
- Story Generation (PGCE Algorithm)
- Code Generation
- Test Execution
- Team Analytics & Charts

---

## Demo Flow Diagram

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Login  │───▶│  Init   │───▶│  Story  │───▶│  Code   │───▶│  Test   │───▶│ Charts  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
   Step 1         Step 2         Step 3         Step 4         Step 5         Step 6
```

---

## SECTION A: ENVIRONMENT SETUP

---

### Scenario A.1: Open VS Code

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| A.1.1 | Open VS Code | VS Code launches | [ ] |
| A.1.2 | File → Open Folder → `~/github-demo` | Folder opens | [ ] |
| A.1.3 | View → Terminal (or Ctrl+`) | Terminal panel opens | [ ] |
| A.1.4 | Run: `pwd` | Shows `/Users/<username>/github-demo` | [ ] |

---

## SECTION B: LOGIN (quad login)

---

### Scenario B.1: Google SSO Login

**Features Tested:** Authentication, SSO Flow, Config Creation

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| B.1.1 | Run: `quad login --google` | Browser opens | [ ] |
| B.1.2 | See QUAD login page | quadframe.work/auth/login visible | [ ] |
| B.1.3 | Click "Sign in with Google" | Google auth page | [ ] |
| B.1.4 | Select Google account | Redirects back | [ ] |
| B.1.5 | Browser shows "Login successful!" | Can close browser tab | [ ] |
| B.1.6 | Terminal prompts for org code | "Organization Code:" prompt | [ ] |
| B.1.7 | Enter: `DEMO` | Input accepted | [ ] |
| B.1.8 | Press Enter | Login completes | [ ] |

### Expected Terminal Output

```
  QUAD Login
  ──────────

  → Opening browser for Google SSO...
  → Waiting for authentication...

  → Please enter your organization code
  → (Contact your admin if you don't know it)

  Organization Code: DEMO

  ✓ Login successful!
  ✓ Welcome, Gopi Suman Addanke!
  → Organization: DEMO (DEMO)
  → Config saved to: /Users/<username>/.quad/config.json
```

### Files Created

| File | Location | Content |
|------|----------|---------|
| Global Config | `~/.quad/config.json` | Token, user info, org code |

### Verification Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| B.1.9 | Run: `cat ~/.quad/config.json` | JSON with token shown | [ ] |
| B.1.10 | Run: `quad status` | "Authenticated" shown | [ ] |

### Expected Config Content

```json
{
  "token": "eyJ...",
  "auth_type": "google",
  "api_url": "https://api.quadframe.work",
  "logged_in_at": "2026-01-14T...",
  "org_code": "DEMO",
  "org_name": "DEMO",
  "user_email": "user@gmail.com",
  "user_name": "Gopi Suman Addanke"
}
```

### Database Verification (if API connected)

```sql
-- Check user created/updated
SELECT id, email, name, provider, created_at
FROM quad_users
WHERE email = 'user@gmail.com';

-- Check activity logged
SELECT * FROM quad_user_activity
WHERE user_id = '<user_id>'
ORDER BY created_at DESC
LIMIT 1;
```

---

## SECTION C: INIT (quad init)

---

### Scenario C.1: Initialize Project

**Features Tested:** Project Creation, Config Generation, Documentation Structure

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| C.1.1 | Run: `quad init banking-portal` | Init starts | [ ] |
| C.1.2 | See "Project type?" prompt | Options 1-4 shown | [ ] |
| C.1.3 | Enter: `4` (Full Stack) | Selection accepted | [ ] |
| C.1.4 | See "Frontend?" prompt | Options 1-3 shown | [ ] |
| C.1.5 | Enter: `1` (Next.js) | Selection accepted | [ ] |
| C.1.6 | See "Backend?" prompt | Options 1-3 shown | [ ] |
| C.1.7 | Enter: `1` (Spring Boot) | Selection accepted | [ ] |
| C.1.8 | See "Database?" prompt | Options 1-3 shown | [ ] |
| C.1.9 | Enter: `1` (PostgreSQL) | Selection accepted | [ ] |
| C.1.10 | Wait for completion | Files created | [ ] |

### Expected Terminal Output

```
  QUAD Project Initialization
  ───────────────────────────

  → Creating project: banking-portal
  → Project type?
      [1] Web App
      [2] API
      [3] Mobile
      [4] Full Stack
  Select [4]: 4

  → Frontend?
      [1] Next.js
      [2] React
      [3] Vue
  Select [1]: 1

  → Backend?
      [1] Spring Boot
      [2] Node.js
      [3] Python
  Select [1]: 1

  → Database?
      [1] PostgreSQL
      [2] MySQL
      [3] MongoDB
  Select [1]: 1

  ✓ Created: banking-portal/.quad/config.json
  ✓ Created: banking-portal/README.md
  ✓ Created: banking-portal/CLAUDE.md
  ✓ Created: banking-portal/documentation/architecture/README.md
  ✓ Created: banking-portal/documentation/database/README.md
  ✓ Created: banking-portal/documentation/api/README.md
  ✓ Created: banking-portal/documentation/web/README.md
  ✓ Created: banking-portal/documentation/mobile/README.md
  ✓ Created: banking-portal/documentation/deployment/README.md
  ✓ Created: banking-portal/documentation/security/README.md
  ✓ Created: banking-portal/documentation/testing/README.md
  ✓ Created: banking-portal/documentation/misc/README.md

  ✓ Project initialized!
  →
  →   cd banking-portal
  →   quad story create
```

### Files Created

| File | Path | Content |
|------|------|---------|
| Project Config | `banking-portal/.quad/config.json` | Project settings |
| README | `banking-portal/README.md` | Project overview |
| AI Context | `banking-portal/CLAUDE.md` | Claude Code context |
| Docs | `banking-portal/documentation/*/README.md` | 9 doc folders |

### Verification Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| C.1.11 | Run: `ls -la banking-portal/` | .quad, README.md, etc. | [ ] |
| C.1.12 | Run: `cat banking-portal/.quad/config.json` | JSON with project info | [ ] |
| C.1.13 | Run: `ls banking-portal/documentation/` | 9 folders listed | [ ] |

### Expected Project Config

```json
{
  "domain_slug": "banking-portal",
  "project_name": "banking-portal",
  "org_code": "DEMO",
  "org_name": "DEMO",
  "project_type": "fullstack",
  "frontend": "nextjs",
  "backend": "springboot",
  "database": "postgresql",
  "created_at": "2026-01-14T...",
  "created_by": "user@gmail.com",
  "api_url": "https://api.quadframe.work"
}
```

### Database Verification (if API connected)

```sql
-- Check domain created
SELECT id, name, slug, methodology, created_at
FROM quad_domains
WHERE slug = 'banking-portal';
```

---

### Scenario C.2: Navigate to Project

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| C.2.1 | Run: `cd banking-portal` | In project folder | [ ] |
| C.2.2 | Run: `pwd` | Shows .../banking-portal | [ ] |

---

## SECTION D: STORY (quad story)

---

### Scenario D.1: Generate User Stories

**Features Tested:** PGCE Algorithm, Story Generation, Priority Calculation

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| D.1.1 | Run: `quad story create` | Story generator starts | [ ] |
| D.1.2 | See "Describe what you want to build:" | Input prompt shown | [ ] |
| D.1.3 | Type: `User login with authentication` | Input accepted | [ ] |
| D.1.4 | Press Enter | New line | [ ] |
| D.1.5 | Type: `Account balance viewing` | Input accepted | [ ] |
| D.1.6 | Press Enter | New line | [ ] |
| D.1.7 | Type: `Transaction history` | Input accepted | [ ] |
| D.1.8 | Press Enter | New line | [ ] |
| D.1.9 | Type: `Money transfer between accounts` | Input accepted | [ ] |
| D.1.10 | Press Enter twice (blank line) | Generation starts | [ ] |
| D.1.11 | Wait for stories | Table displayed | [ ] |

### Expected Terminal Output

```
  QUAD Story Generator
  ────────────────────

  → Project: banking-portal

  Describe what you want to build:
  Features
  (Enter blank line to finish)
  > User login with authentication
  > Account balance viewing
  > Transaction history
  > Money transfer between accounts
  >

  → Generating user stories using PGCE algorithm...
  → Analyzing requirements...
  → Calculating dependencies...
  → Prioritizing by PGCE formula: P = (D × 0.5) + (I × 0.3) + (C' × 0.2)

  ✓ Generated 10 stories in priority order:

  ┌────┬─────────────────────────────────┬──────────┬───────┐
  │ #  │ Story                           │ Priority │ Phase │
  ├────┼─────────────────────────────────┼──────────┼───────┤
  │ 1  │ Database schema setup           │   0.64   │   1   │
  │ 2  │ User authentication API         │   0.57   │   2   │
  │ 3  │ JWT token management            │   0.50   │   2   │
  │ 4  │ Account balance API             │   0.44   │   3   │
  │ 5  │ Transaction history API         │   0.40   │   3   │
  │ 6  │ Money transfer API              │   0.42   │   3   │
  │ 7  │ Login page UI                   │   0.38   │   3   │
  │ 8  │ Dashboard UI                    │   0.32   │   4   │
  │ 9  │ Transfer form UI                │   0.28   │   4   │
  │ 10 │ Transaction list UI             │   0.28   │   4   │
  └────┴─────────────────────────────────┴──────────┴───────┘

  ✓ Saved 10 stories to database
  ✓ Created: banking-portal/.quad/stories.json

  → Ready to generate code? Run: quad code
```

### Files Created

| File | Path | Content |
|------|------|---------|
| Stories | `.quad/stories.json` | Generated user stories with PGCE priority |

### Verification Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| D.1.12 | Run: `cat .quad/stories.json` | JSON with stories | [ ] |
| D.1.13 | Run: `quad story list` | Stories grouped by phase | [ ] |

### Database Verification (if API connected)

```sql
-- Check stories created
SELECT id, title, priority, phase, status
FROM quad_stories
WHERE project_slug = 'banking-portal'
ORDER BY priority DESC;

-- Count by phase
SELECT phase, COUNT(*) as count
FROM quad_stories
WHERE project_slug = 'banking-portal'
GROUP BY phase
ORDER BY phase;
```

---

## SECTION E: CODE (quad code)

---

### Scenario E.1: Generate Code

**Features Tested:** Phase-by-Phase Generation, File Creation, Progress Tracking

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| E.1.1 | Run: `quad code generate` | Code generator starts | [ ] |
| E.1.2 | See Phase 1 header | "Foundation" shown | [ ] |
| E.1.3 | Wait for Phase 1 files | Files created | [ ] |
| E.1.4 | See "Continue to Phase 2?" | Prompt shown | [ ] |
| E.1.5 | Enter: `y` | Continues | [ ] |
| E.1.6 | Wait for Phase 2 files | Files created | [ ] |
| E.1.7 | Enter: `y` for Phase 3 | Continues | [ ] |
| E.1.8 | Wait for Phase 3 files | Files created | [ ] |
| E.1.9 | Enter: `y` for Phase 4 | Continues | [ ] |
| E.1.10 | Wait for completion | Summary shown | [ ] |

### Expected Terminal Output (abbreviated)

```
  QUAD Code Generator (PGCE Engine)
  ─────────────────────────────────


  Phase 1: Foundation (Stories 1-1)
  ─────────────────────────────────

  [1/10] Database schema setup...

  → Using pattern: Spring Boot
  → Generating files in banking-portal-database/...

  ✓ Created: sql/tables/users.sql
  ✓ Created: sql/tables/accounts.sql
  ✓ Created: sql/tables/transactions.sql
  ✓ Created: migrations/V1__initial_schema.sql

  Phase 1 Complete! ██░░░░░░░░░░░░░░░░░░ 10%

  Continue to Phase 2? [Y/n]: y


  Phase 2: Core Features (Stories 2-3)
  ────────────────────────────────────
  ...

  ════════════════════════════════════════
  Code Generation Complete! ████████████████████ 100%
  ════════════════════════════════════════

  Summary:
  ├── banking-portal-database/  (1 stories)
  ├── banking-portal-api/       (5 stories)
  └── banking-portal-web/       (4 stories)

  Total: 24 files generated

  → Next: quad test
```

### Verification Steps

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| E.1.11 | Run: `quad code status` | 100% progress shown | [ ] |
| E.1.12 | Check stories updated | All status = "done" | [ ] |

### Expected Status Output

```
  Code Generation Status
  ──────────────────────

  Stories: 10
    ● Done: 10
    ◐ In Progress: 0
    ○ Pending: 0

  Progress: ████████████████████ 100%
```

---

## SECTION F: TEST (quad test)

---

### Scenario F.1: Run All Tests

**Features Tested:** Test Runner, Coverage Report

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| F.1.1 | Run: `quad test` | Test runner starts | [ ] |
| F.1.2 | See database tests | 3 tests pass | [ ] |
| F.1.3 | See API tests | 15 tests pass | [ ] |
| F.1.4 | See web tests | 8 tests pass | [ ] |
| F.1.5 | See summary | 26/26 passed | [ ] |

### Expected Terminal Output

```
  QUAD Test Runner
  ────────────────

  → [Database] Running schema validation...
  ✓ All tables valid
  ✓ Foreign keys correct
  ✓ Indexes optimized

  → [API] Running unit tests...
  ✓ AuthControllerTest - 5/5 passed
  ✓ AccountControllerTest - 4/4 passed
  ✓ TransferControllerTest - 6/6 passed
  ✓ All 15 tests passed

  → [Web] Running component tests...
  ✓ LoginForm.test.tsx - passed
  ✓ TransferForm.test.tsx - passed
  ✓ All 8 tests passed

  ════════════════════════════════════════
  Total: 26 tests, 26 passed, 0 failed
  Coverage: 85%
  ════════════════════════════════════════

  ✓ All tests passed!
  → Next: quad deploy dev
```

### Verification Checklist

| Test Suite | Count | Status | Pass/Fail |
|------------|-------|--------|-----------|
| Database | 3 | Passed | [ ] |
| API | 15 | Passed | [ ] |
| Web | 8 | Passed | [ ] |
| **Total** | **26** | **100%** | [ ] |

---

## SECTION G: ANALYTICS (quad burnout, quad chart)

---

### Scenario G.1: Team Burnout Analysis

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| G.1.1 | Run: `quad burnout` | Analysis shown | [ ] |
| G.1.2 | See team table | 3 members listed | [ ] |
| G.1.3 | See alert | Pradeep at risk | [ ] |

### Expected Terminal Output

```
  Team Burnout Analysis
  ─────────────────────

  → Organization: DEMO

  ┌─────────────────┬───────────┬────────────┐
  │ Team Member     │ Workload  │ Status     │
  ├─────────────────┼───────────┼────────────┤
  │ Pradeep Kumar   │ ████████░░│ 80% - High │
  │ Manju Singh     │ ██████░░░░│ 60% - OK   │
  │ Suman Addanki   │ █████░░░░░│ 50% - OK   │
  └─────────────────┴───────────┴────────────┘

  ⚠ Alert: Pradeep Kumar is at risk of burnout
  → Suggestion: Reassign 4 tickets to others
```

---

### Scenario G.2: Sprint Velocity Chart

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| G.2.1 | Run: `quad chart velocity` | Chart shown | [ ] |
| G.2.2 | See 4 sprints | Points displayed | [ ] |
| G.2.3 | See trend | "Improving" shown | [ ] |

### Expected Terminal Output

```
  Sprint Velocity (Last 4 Sprints)
  ────────────────────────────────

  Sprint 1: ████████████████████ 42 pts
  Sprint 2: ██████████████████░░ 38 pts
  Sprint 3: █████████████████░░░ 35 pts
  Sprint 4: █████████████████████ 45 pts

  Average: 40 pts/sprint
  Trend: ↑ Improving
```

---

### Scenario G.3: Ticket Status Chart

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| G.3.1 | Run: `quad chart tickets` | Chart shown | [ ] |
| G.3.2 | See 4 statuses | Counts displayed | [ ] |
| G.3.3 | See total | 83 tickets | [ ] |

### Expected Terminal Output

```
  Ticket Status Distribution
  ──────────────────────────

  ● Done         █████████        45 (54%)
  ◐ In Progress  ██               12 (14%)
  ○ To Do        ████             23 (28%)
  ✗ Blocked      ░                3 (4%)

  Total: 83 tickets
```

---

### Scenario G.4: Workload Chart

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| G.4.1 | Run: `quad chart workload` | Chart shown | [ ] |
| G.4.2 | See 3 members | Tickets displayed | [ ] |
| G.4.3 | See recommendations | 2 suggestions | [ ] |

### Expected Terminal Output

```
  Team Workload Distribution
  ──────────────────────────

  Pradeep Kumar        ▓▓▓▓▓▓▓▓░░ 8 tickets (80%)
  Manju Singh          ▓▓▓▓▓░░░░░ 5 tickets (60%)
  Suman Addanki        ▓▓▓▓░░░░░░ 4 tickets (50%)

  → Recommendations:
      • Move 2 tickets from Pradeep to Manju
      • Suman has capacity for 2 more tickets
```

---

## SECTION H: CLEANUP (Optional)

---

### Scenario H.1: Clean Up Demo

| Step | Action | Expected Result | Pass/Fail |
|------|--------|-----------------|-----------|
| H.1.1 | Run: `cd ~/github-demo` | In demo folder | [ ] |
| H.1.2 | Run: `rm -rf banking-portal` | Project deleted | [ ] |
| H.1.3 | Run: `quad login --logout` | Logged out | [ ] |
| H.1.4 | Run: `quad status` | "Not authenticated" | [ ] |

---

## COMPLETE DEMO CHECKLIST

### Section A: Environment
- [ ] VS Code open
- [ ] Terminal in ~/github-demo

### Section B: Login
- [ ] `quad login --google` ran
- [ ] Browser opened
- [ ] SSO completed
- [ ] Org code entered
- [ ] Config file created

### Section C: Init
- [ ] `quad init banking-portal` ran
- [ ] Project type: fullstack
- [ ] Frontend: nextjs
- [ ] Backend: springboot
- [ ] Database: postgresql
- [ ] All files created

### Section D: Story
- [ ] `quad story create` ran
- [ ] Description entered
- [ ] 10 stories generated
- [ ] PGCE priorities calculated
- [ ] stories.json created

### Section E: Code
- [ ] `quad code generate` ran
- [ ] All 4 phases completed
- [ ] 24 files created
- [ ] Stories marked "done"

### Section F: Test
- [ ] `quad test` ran
- [ ] 26/26 tests passed
- [ ] 85% coverage shown

### Section G: Analytics
- [ ] `quad burnout` shows team
- [ ] `quad chart velocity` shows sprints
- [ ] `quad chart tickets` shows status
- [ ] `quad chart workload` shows recommendations

---

## Files Created Summary

| Location | Files | Purpose |
|----------|-------|---------|
| `~/.quad/` | `config.json` | Global user config |
| `banking-portal/.quad/` | `config.json` | Project config |
| `banking-portal/.quad/` | `stories.json` | Generated stories |
| `banking-portal/` | `README.md` | Project docs |
| `banking-portal/` | `CLAUDE.md` | AI context |
| `banking-portal/documentation/` | 9 folders | Doc structure |

---

## Database Tables Summary

| Table | Operation | When |
|-------|-----------|------|
| `quad_users` | INSERT/UPDATE | Login |
| `quad_user_activity` | INSERT | Login |
| `quad_domains` | INSERT | Init |
| `quad_stories` | INSERT | Story create |
| `quad_code_generations` | INSERT | Code generate |
| `quad_test_runs` | INSERT | Test |

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
