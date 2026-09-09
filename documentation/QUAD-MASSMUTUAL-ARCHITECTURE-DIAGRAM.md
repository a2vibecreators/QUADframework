# QUAD + MassMutual Architecture Diagram
## One Cloud API, Multiple Access Points

**Date:** January 15, 2026
**Purpose:** Show how QUAD framework serves MassMutual through multiple client interfaces

---

## The Complete Architecture (ASCII Diagram)

```
╔════════════════════════════════════════════════════════════════════════════╗
║                        MASSMUTUAL SQUAD SDLC                              ║
║                    Built on QUAD Framework                                ║
╚════════════════════════════════════════════════════════════════════════════╝


┌──────────────────────────────────────────────────────────────────────────────┐
│                        MASSMUTUAL DEVELOPERS                                 │
│                      (Multiple Access Methods)                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────────────┐  ┌────────────────────────┐                    │
│  │  VS Code Plugin        │  │  Command Line / Bash   │                    │
│  │  ────────────────────  │  │  ──────────────────────│                    │
│  │                        │  │                        │                    │
│  │  Developer opens VS    │  │  $ quad deploy main    │                    │
│  │  Code → Clicks button  │  │  $ quad generate api   │                    │
│  │  "Deploy to Prod"      │  │  $ quad validate build │                    │
│  │                        │  │  $ bash deploy.sh      │                    │
│  │  UI shows:             │  │  $ ./scripts/test.sh   │                    │
│  │  ├─ Generate           │  │                        │                    │
│  │  ├─ Validate           │  │  Runs on any machine:  │                    │
│  │  ├─ Deploy             │  │  ├─ Local dev machine  │                    │
│  │  ├─ Rollback           │  │  ├─ CI/CD server       │                    │
│  │  └─ Status             │  │  ├─ Cron job           │                    │
│  │                        │  │  └─ Production server  │                    │
│  └────────────────────────┘  └────────────────────────┘                    │
│           │                            │                                    │
│           └────────────────┬───────────┘                                    │
│                            │                                                │
│  ┌────────────────────────────────────────────────────┐                    │
│  │  Web Browser / Dashboard                           │                    │
│  │  ───────────────────────────────────────────────────│                    │
│  │                                                    │                    │
│  │  URL: https://quad.massmutual.com                  │                    │
│  │                                                    │                    │
│  │  UI shows list of available commands:              │                    │
│  │  ┌──────────────────────────────────────────────┐  │                    │
│  │  │ Available Actions:                           │  │                    │
│  │  ├─ [Generate Code]      Select branch, version│  │                    │
│  │  ├─ [Validate Build]     Select server, config │  │                    │
│  │  ├─ [Deploy Prod]        Select target env      │  │                    │
│  │  ├─ [Rollback Version]   Select version to go  │  │                    │
│  │  ├─ [Monitor Deployment] See live status       │  │                    │
│  │  ├─ [View Logs]          All deployment logs   │  │                    │
│  │  └─ [Run Custom Script]  Upload & execute      │  │                    │
│  │  └──────────────────────────────────────────────┘  │                    │
│  │                                                    │                    │
│  │  Just buttons/forms that send requests to API      │                    │
│  │                                                    │                    │
│  └────────────────────────────────────────────────────┘                    │
│                            │                                                │
│                            │                                                │
│  ┌────────────────────────────────────────────────────┐                    │
│  │  Programmatic / Direct API Calls                   │                    │
│  │  ───────────────────────────────────────────────────│                    │
│  │                                                    │                    │
│  │  curl -X POST https://api.quad.massmutual.com     │                    │
│  │    /api/deploy \                                  │                    │
│  │    -H "Authorization: Bearer $API_KEY" \           │                    │
│  │    -H "Content-Type: application/json" \           │                    │
│  │    -d '{                                           │                    │
│  │      "action": "deploy",                           │                    │
│  │      "branch": "main",                             │                    │
│  │      "version": "2.1.0",                           │                    │
│  │      "environment": "production"                   │                    │
│  │    }'                                              │                    │
│  │                                                    │                    │
│  │  Python / Node.js / Java / Any language            │                    │
│  │  can call the same API directly                    │                    │
│  │                                                    │                    │
│  └────────────────────────────────────────────────────┘                    │
│                            │                                                │
│                            │                                                │
└────────────────────────────┼────────────────────────────────────────────────┘
                             │
                             │ All requests go to same endpoint:
                             │ https://api.quad.massmutual.com:3201
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                      QUAD CLOUD API (Central Hub)                            │
│                    (Running on MassMutual's Server)                          │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  POST /api/generate       → Code generation (using PGCE algorithm)           │
│  POST /api/validate       → Validation engine (constraint checking)          │
│  POST /api/deploy         → Deployment executor                             │
│  POST /api/rollback       → Rollback handler                                │
│  GET  /api/status         → Deployment status                               │
│  GET  /api/logs           → Access logs                                     │
│  POST /api/hooks/capture  → Message hooking system                          │
│  POST /api/execute        → Direct command execution                        │
│                                                                              │
│  The API receives request from ANY client:                                  │
│  ├─ VS Code plugin sends: POST /api/deploy                                  │
│  ├─ CLI sends: POST /api/deploy                                             │
│  ├─ Web UI sends: POST /api/deploy                                          │
│  ├─ Bash script sends: POST /api/deploy                                     │
│  └─ All get same response, same behavior                                    │
│                                                                              │
│  Authentication:                                                             │
│  ├─ VS Code Plugin: Uses API key stored in config                           │
│  ├─ CLI: Uses API key from ~/.quad/credentials                              │
│  ├─ Web UI: Uses JWT token from browser session                             │
│  ├─ Bash Script: Uses API key in environment variable                       │
│  └─ All validated against same user/org database                            │
│                                                                              │
└────────────────────┬───────────────────────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
    ┌─────────┐ ┌──────────┐ ┌─────────────┐
    │Gemini   │ │PostgreSQL│ │Message Hooks│
    │API      │ │Database  │ │ (Ollama)    │
    │         │ │          │ │             │
    │Generate │ │Store:    │ │ Extract:    │
    │Code     │ │- Users   │ │- Intent     │
    │         │ │- Builds  │ │- Decisions  │
    │Validate │ │- Deploy  │ │- Context    │
    │Logic    │ │  History │ │             │
    │         │ │- RLS     │ │ Learn from: │
    │Call LLM │ │  (org    │ │- Commands   │
    │for      │ │  isolation)│ │- Patterns   │
    │analysis │ │          │ │- Best use   │
    │         │ │RLS:      │ │             │
    │         │ │Only MM   │ │Improve AI   │
    │         │ │sees data │ │suggestions  │
    │         │ │          │ │             │
    └─────────┘ └──────────┘ └─────────────┘
```

---

## Data Flow Examples: Same API, Different Access Points

### Example 1: VS Code Plugin Deploy

```
Developer in VS Code:
│
├─ Clicks "Deploy to Prod" button
│
├─ VS Code Plugin reads API key from config file
│
├─ VS Code Plugin sends:
│  POST https://api.quad.massmutual.com:3201/api/deploy
│  {
│    "action": "deploy",
│    "branch": "main",
│    "version": "2.1.0",
│    "environment": "production"
│  }
│
├─ API receives request
│
├─ API validates: organization_id = massmutual
│
├─ API calls Gemini: "Validate this deployment safe?"
│
├─ Gemini approves
│
├─ API executes deployment
│
├─ API logs in database: WHO deployed WHAT WHEN
│
├─ API calls Ollama hooks: Extract learnings
│
└─ API returns: { success: true, build_id: "build-456" }
   └─ VS Code Plugin shows: "✅ Deployed successfully"
```

### Example 2: CLI Bash Script Deploy

```
Developer runs in terminal:
│
├─ bash deploy.sh main 2.1.0 production
│
├─ Script reads API key from environment: $QUAD_API_KEY
│
├─ Script sends:
│  curl -X POST https://api.quad.massmutual.com:3201/api/deploy \
│    -H "Authorization: Bearer $QUAD_API_KEY" \
│    -d '{
│      "action": "deploy",
│      "branch": "main",
│      "version": "2.1.0",
│      "environment": "production"
│    }'
│
├─ API receives same request (from curl instead of VS Code)
│
├─ API validates: organization_id = massmutual (same)
│
├─ API calls Gemini: "Validate this deployment safe?"
│
├─ Gemini approves
│
├─ API executes deployment (same execution)
│
├─ API logs in database (same logging)
│
├─ API calls Ollama hooks (same learning)
│
└─ curl returns: { success: true, build_id: "build-456" }
   └─ Script outputs: "✅ Deployed successfully"
```

### Example 3: Web Dashboard Deploy

```
Developer opens browser:
│
├─ URL: https://quad.massmutual.com
│
├─ Web UI shows button: "Deploy to Prod"
│
├─ Clicks button
│
├─ Web UI JavaScript sends:
│  POST https://api.quad.massmutual.com:3201/api/deploy
│  {
│    "action": "deploy",
│    "branch": "main",
│    "version": "2.1.0",
│    "environment": "production"
│  }
│  Headers: { "Authorization": "Bearer JWT_TOKEN" }
│
├─ API receives request (from web browser instead of CLI/plugin)
│
├─ API validates: organization_id = massmutual (same)
│
├─ API calls Gemini: "Validate this deployment safe?"
│
├─ Gemini approves
│
├─ API executes deployment (same)
│
├─ API logs in database (same)
│
├─ API calls Ollama hooks (same)
│
└─ Web UI receives: { success: true, build_id: "build-456" }
   └─ Web UI shows: "✅ Deployed successfully" with live status
```

---

## Key Insight: One API Powers Everything

```
┌──────────────────────────────────────────────────────┐
│              QUAD Cloud API                          │
│         (One central implementation)                 │
└──────────────────────────────────────────────────────┘
         ▲                    ▲                    ▲
         │                    │                    │
         │                    │                    │
    ┌────┴────┐          ┌────┴────┐          ┌────┴────┐
    │ VS Code │          │ CLI/Bash │          │Web/Browser
    │ Plugin  │          │ Scripts  │          │Dashboard
    │         │          │          │          │
    │Writes to│          │Writes to │          │Writes to
    │same API │          │same API  │          │same API
    │         │          │          │          │
    │Reads    │          │Reads     │          │Reads
    │same DB  │          │same DB   │          │same DB
    │         │          │          │          │
    │Executes │          │Executes  │          │Executes
    │same     │          │same      │          │same
    │business │          │business  │          │business
    │logic    │          │logic     │          │logic
    └─────────┘          └──────────┘          └─────────┘

NO DUPLICATION:
═══════════════
✅ One code path for "deploy" action
✅ One database for all records
✅ One Gemini integration for validation
✅ One Ollama integration for learning
✅ One authentication system
✅ One audit log
✅ One API response format

Benefit: When you fix a bug in API, ALL clients benefit
         When you add feature to API, ALL clients get it
```

---

## Tomorrow: Web Application (More UI, Same API)

```
TOMORROW (Day 2):
═════════════════

Add Web Dashboard to existing architecture:

Before (Day 1):
  VS Code Plugin → API → Database
  CLI/Bash → API → Database

After (Day 2):
  VS Code Plugin → API → Database
  CLI/Bash        → API → Database
  Web Dashboard → API → Database  ← NEW!

The Web Dashboard is:
┌────────────────────────────────────────────────────────┐
│           Web Application (React/Vue/Angular)          │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │ Deployment Commands (from UI):                   │ │
│  │                                                  │ │
│  │ [Generate Code]   → POST /api/generate          │ │
│  │ [Validate Build]  → POST /api/validate          │ │
│  │ [Deploy]          → POST /api/deploy            │ │
│  │ [Rollback]        → POST /api/rollback          │ │
│  │ [View Status]     → GET /api/status             │ │
│  │ [View Logs]       → GET /api/logs               │ │
│  │ [Run Script]      → POST /api/execute           │ │
│  │                                                  │ │
│  │ Each button = Just a UI wrapper around API call │ │
│  │                                                  │ │
│  │ No separate business logic                       │ │
│  │ Same API calls as CLI and Plugin                 │ │
│  │                                                  │ │
│  └──────────────────────────────────────────────────┘ │
│                      ↓                                 │
│                 Same API                              │
│                (No changes needed)                     │
│                                                        │
└────────────────────────────────────────────────────────┘

The API stays the same, just adding new client interface!
```

---

## Architecture Table

| Access Method | Client Type | What It Does | Uses Same API |
|---|---|---|---|
| **VS Code Plugin** | IDE Extension | Click buttons in editor | ✅ Yes |
| **CLI / Bash** | Command line | `quad deploy`, `quad generate` | ✅ Yes |
| **Web Dashboard** | Browser UI | Click buttons, see live status | ✅ Yes |
| **Direct API Call** | Programmatic | curl, Python, Node.js | ✅ Yes |
| **Cron Job** | Automation | Scheduled deployment | ✅ Yes |
| **CI/CD Pipeline** | Jenkins/GitHub Actions | Auto-deploy on push | ✅ Yes |
| **Custom Script** | Shell/Python/Ruby | Any script language | ✅ Yes |

**All use the same QUAD API endpoint!**

---

## For MassMutual Pitch

```
WHAT YOU SAY TO MASSMUTUAL:
═══════════════════════════

"Here's how QUAD works:

1. We provide ONE Cloud API
   └─ Handles all SQUAD SDLC operations
   └─ Code generation, validation, deployment

2. You can access it however you want:
   ├─ VS Code Plugin (for developers)
   ├─ CLI Tools (for automation)
   ├─ Web Dashboard (for monitoring)
   ├─ Direct API calls (for custom integrations)
   ├─ Bash scripts (for legacy systems)
   └─ CI/CD pipelines (Jenkins, GitHub Actions, etc.)

3. All methods use the SAME backend:
   └─ Same database
   └─ Same business logic
   └─ Same audit trail
   └─ Same security

4. You deploy how YOU want:
   ├─ Developer in VS Code? One click deploy
   ├─ Script in CI/CD? Programmatic deploy
   ├─ Scheduled job? Cron job deploy
   ├─ Manual web dashboard? Click button deploy
   └─ All trigger SAME actions

5. One API to rule them all:
   └─ Easy to maintain
   └─ Easy to scale
   └─ Easy to extend
   └─ Easy to audit

That's QUAD."
```

---

## Complete Request/Response Flow

```
Any Client (Plugin/CLI/Web/Script)
│
├─ Sends: POST /api/deploy
│         Authorization: Bearer {token}
│         Body: { action, branch, version, environment }
│
▼
┌────────────────────────────────────────────────────────┐
│         QUAD Cloud API (Node.js/Express)               │
├────────────────────────────────────────────────────────┤
│                                                        │
│ Step 1: Validate Authentication                        │
│ ├─ Check API key / JWT token                          │
│ ├─ Look up user in database                           │
│ └─ Get user's organization_id (massmutual)            │
│                                                        │
│ Step 2: Validate Request                              │
│ ├─ Check if action is allowed                         │
│ ├─ Check parameters are valid                         │
│ └─ Check user has permissions                         │
│                                                        │
│ Step 3: Call Gemini (for smart validation)             │
│ ├─ Send: "Validate deployment of branch:main v2.1.0"  │
│ ├─ Gemini analyzes: "Is this safe?"                   │
│ └─ Gemini returns: "Yes, approved"                     │
│                                                        │
│ Step 4: Execute Business Logic                         │
│ ├─ Generate code (if needed)                          │
│ ├─ Validate constraints                               │
│ ├─ Execute deployment                                 │
│ └─ Update status                                       │
│                                                        │
│ Step 5: Log Everything (Audit Trail)                   │
│ ├─ INSERT into commands table:                         │
│ │  - user_id, organization_id, action                 │
│ │  - parameters, status, timestamp                    │
│ └─ All filtered by RLS (MassMutual only sees theirs)   │
│                                                        │
│ Step 6: Call Ollama Hooks (Learning)                   │
│ ├─ Analyze: "What did we learn from this deploy?"      │
│ ├─ Extract: Patterns, best practices, improvements     │
│ └─ Store: For future AI suggestions                    │
│                                                        │
│ Step 7: Return Response                                │
│ └─ Return: {                                           │
│     success: true,                                     │
│     build_id: "build-456",                            │
│     status: "deployed",                               │
│     message: "Deployment successful"                  │
│   }                                                   │
│                                                        │
└────────────────────────────────────────────────────────┘
│
▼
Client receives same response regardless of how it called:
  VS Code Plugin → Shows: "✅ Deployed (build-456)"
  CLI Script → Outputs: "Deployed: build-456"
  Web Dashboard → Shows: "✅ Success" with live logs
  Direct API → Gets JSON: { success: true, ... }
```

---

## Summary: One API, Infinite Clients

```
┌──────────────────────────────────────────────────────┐
│              QUAD Cloud API                          │
│     (One implementation, many access methods)        │
└──────────────────────────────────────────────────────┘

├─ VS Code Plugin
│  └─ UI for developers in their IDE
│
├─ CLI Tools (quad, bash scripts)
│  └─ Scripting and automation
│
├─ Web Dashboard
│  └─ Monitor and manage deployments
│
├─ Direct API Calls
│  └─ Custom integrations (Python, Java, Node.js, etc.)
│
├─ Cron Jobs
│  └─ Scheduled deployments
│
├─ CI/CD Pipelines
│  └─ Automated deployment on code push
│
└─ Future Clients (Mobile app, Slack bot, etc.)
   └─ All hit same API

BENEFIT: Build once, access everywhere!
```

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
