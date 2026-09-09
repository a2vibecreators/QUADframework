# QUAD Roadmap

**Quick Unified Agentic Development - Product Roadmap**

Last Updated: January 14, 2026

---

## Vision

Build a platform where **anyone can create AI agents visually** - describe in English, drag-and-drop components, and QUAD generates production-ready code in any language. Inspired by BEA WebLogic JPD (Java Process Definition), but for the AI age.

---

## Phases Overview (5 Phases)

```
Phase 1 (Current)     Phase 2              Phase 3              Phase 4              Phase 5
─────────────────     ─────────────────    ─────────────────    ─────────────────    ─────────────────
CLI + Demo            API + AI             Website              QUAD Plugin          Full Product
                                           (quadframe.work)     (VS Code)            (QUAD Editor)
Jan 2026              Feb-Mar 2026         Mar-Apr 2026         May-Jun 2026         Jul+ 2026
```

---

## Phase 1: CLI + Demo (January 2026) 🔄

**Status:** In Progress
**Goal:** Working CLI commands for full demo flow

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Phase 1: Pure CLI (No AI on api.quadframe.work yet)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TERMINAL                        CLAUDE CLI                     │
│  ────────                        ──────────                     │
│  $ quad login                    $ claude                       │
│  $ quad init                     > "help me..."                 │
│  $ quad story                          │                        │
│  $ quad code                           │                        │
│  $ quad test                           ▼                        │
│  $ quad deploy                   ┌──────────┐                   │
│  $ quad burnout                  │ QUAD Hook│ (context inject)  │
│  $ quad chart                    └──────────┘                   │
│        │                               │                        │
│        │                               │                        │
│        ▼                               ▼                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  api.quadframe.work (No AI - just data storage)          │  │
│  │  - User/Org management                                    │  │
│  │  - Project storage                                        │  │
│  │  - Ticket tracking                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  AI comes from: Claude CLI (Anthropic's tool)                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Deliverables

| Component | Status | Description |
|-----------|--------|-------------|
| quad-cli | 🔄 Building | CLI commands (login, init, story, code, test, deploy) |
| quad-hook | ✅ Done | Context injection for Claude Code |
| Database | ✅ Done | PostgreSQL schema on Cloud SQL |
| Downloads | ✅ Done | downloads.quadframe.work (install.sh) |

### Commands for Demo

| Command | Status | Description |
|---------|--------|-------------|
| `quad login` | 🔄 Building | Google SSO authentication |
| `quad init` | 🔧 Fix | Create project + docs structure |
| `quad story create` | 📋 Planned | Generate user stories with PGCE |
| `quad code generate` | 📋 Planned | Generate code from stories |
| `quad test` | 📋 Planned | Run tests on generated code |
| `quad deploy` | ✅ Done | Deploy to GCP |
| `quad burnout` | 📋 Planned | Team burnout analysis |
| `quad chart` | 📋 Planned | Sprint velocity charts |

### Key Features
- `quad login` - Google SSO (opens browser, callback to CLI)
- `quad init` - Create project with standardized docs structure
- `quad story` - AI generates prioritized user stories (PGCE)
- `quad code` - AI generates production code (PGCE engine)
- Context hook for Claude Code integration

---

## Phase 2: API + AI (February-March 2026)

**Status:** Planned
**Goal:** Add AI capabilities to api.quadframe.work

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Phase 2: API with AI Channel                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TERMINAL                        api.quadframe.work             │
│  ────────                        ─────────────────              │
│  $ quad login ──────────────────▶ /api/auth/login              │
│  $ quad story ──────────────────▶ /api/story/generate          │
│  $ quad code  ──────────────────▶ /api/code/generate           │
│                                         │                       │
│                                         ▼                       │
│                                  ┌──────────────┐               │
│                                  │  AI Channel  │               │
│                                  │  - Claude    │               │
│                                  │  - Gemini    │               │
│                                  │  - OpenAI    │               │
│                                  └──────────────┘               │
│                                                                 │
│  Now API does the AI work (not just Claude CLI)                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Deliverables

| Component | Description |
|-----------|-------------|
| QUAD API v1 | REST API at api.quadframe.work |
| AI Channel | Multi-provider AI (Claude/Gemini/OpenAI) |
| Agent Registry | Store and discover agents |
| Agent Executor | Run agents with lifecycle management |
| QUAD WIRE | Agent-to-agent routing |

### API Endpoints

```
POST /api/auth/login          - SSO login
POST /api/auth/me             - Get current user
POST /api/story/generate      - Generate stories with AI
POST /api/code/generate       - Generate code with AI (PGCE)
POST /api/context             - Get org context
POST /api/agents/register     - Register new agent
POST /api/agents/execute      - Execute agent
GET  /api/agents/{id}/health  - Health check
```

### Agent Lifecycle

```python
class QUADAgent:
    # Lifecycle (like Servlet)
    def init(self):           # Called once at startup
    def execute(self, data):  # Called for each task
    def cleanup(self):        # Called at shutdown

    # Health & Monitoring
    def heartbeat(self) -> dict:  # Health check
    def metrics(self) -> dict:    # Usage stats

    # Callbacks
    def on_complete(self, result):  # Success
    def on_error(self, error):      # Error/self-heal
    def on_timeout(self):           # Timeout handler
```

---

## Phase 3: Website (March-April 2026)

**Status:** Planned
**Goal:** Beautiful web UI at quadframe.work

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Phase 3: quadframe.work Web UI                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Browser: quadframe.work                                        │
│  ──────────────────────                                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Dashboard                                               │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │   │
│  │  │ Projects │ │ Stories  │ │ Tickets  │ │ Burnout  │   │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │   │
│  │                                                         │   │
│  │  Sprint Velocity                                        │   │
│  │  ████████████████████ 42 pts                           │   │
│  │  ██████████████████░░ 38 pts                           │   │
│  │                                                         │   │
│  │  Team Workload                                          │   │
│  │  Pradeep ████████░░ 80%                                │   │
│  │  Manju   ██████░░░░ 60%                                │   │
│  │  Suman   █████░░░░░ 50%                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Technology: Next.js + Tailwind                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Features

| Feature | Description |
|---------|-------------|
| Dashboard | Project overview, recent activity |
| Projects | List/create projects |
| Stories | View generated stories, PGCE priority |
| Tickets | Ticket management, assignment |
| Burnout | Team health visualization |
| Charts | Velocity, capacity, trends |
| Settings | User/org configuration |

### Pages

| Route | Description |
|-------|-------------|
| `/` | Landing page |
| `/login` | Google SSO |
| `/dashboard` | Main dashboard |
| `/projects` | Project list |
| `/projects/:id` | Project details |
| `/stories` | Story board |
| `/tickets` | Ticket list |
| `/burnout` | Team health |
| `/settings` | Settings |

---

## Phase 4: QUAD Plugin - VS Code Extension (May-June 2026)

**Status:** Planned
**Goal:** Standalone VS Code extension with AI-agnostic backend

### Vision

A VS Code extension where users can:
1. **Drag-and-drop** agents onto a visual canvas
2. **Write in English** - QUAD generates code in any language
3. **Connect with wires** - Visual flow between agents
4. **Configure properties** - Lifecycle, health, callbacks
5. **Deploy with one click** - To GCP, AWS, or local

### Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│  QUAD STUDIO (VS Code Extension)                                        │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     VISUAL CANVAS                                │   │
│  │                                                                  │   │
│  │   ┌──────────┐         ┌──────────┐         ┌──────────┐       │   │
│  │   │  Agent   │────────▶│ Condition│────────▶│  Agent   │       │   │
│  │   │ (Parse)  │         │ (If...)  │         │ (Store)  │       │   │
│  │   └──────────┘         └──────────┘         └──────────┘       │   │
│  │        │                    │                     │             │   │
│  │        │                    │ else                │             │   │
│  │        │                    ▼                     │             │   │
│  │        │              ┌──────────┐                │             │   │
│  │        │              │  Agent   │                │             │   │
│  │        │              │ (Notify) │                │             │   │
│  │        │              └──────────┘                │             │   │
│  │        │                                          │             │   │
│  └────────┼──────────────────────────────────────────┼─────────────┘   │
│           │                                          │                  │
│  ┌────────▼──────────────────────────────────────────▼─────────────┐   │
│  │                    PROPERTIES PANEL                              │   │
│  │  ┌─────────────────────────────────────────────────────────┐    │   │
│  │  │ Name: ParseExcelAgent                                    │    │   │
│  │  │ Language: [Python ▼]                                     │    │   │
│  │  │                                                          │    │   │
│  │  │ Description (English):                                   │    │   │
│  │  │ ┌──────────────────────────────────────────────────────┐│    │   │
│  │  │ │ Parse the Excel file, extract team members,          ││    │   │
│  │  │ │ validate email formats, store in database            ││    │   │
│  │  │ └──────────────────────────────────────────────────────┘│    │   │
│  │  │                                                          │    │   │
│  │  │ Lifecycle:                                               │    │   │
│  │  │   init():     [Load Excel library, connect DB]          │    │   │
│  │  │   execute():  [Parse rows, validate, transform]         │    │   │
│  │  │   cleanup():  [Close handles, disconnect]               │    │   │
│  │  │                                                          │    │   │
│  │  │ Health:                                                  │    │   │
│  │  │   heartbeat_url: /health    interval: 30s               │    │   │
│  │  │                                                          │    │   │
│  │  │ Callbacks:                                               │    │   │
│  │  │   on_complete: → StoreAgent                             │    │   │
│  │  │   on_error:    → NotifyAgent                            │    │   │
│  │  └─────────────────────────────────────────────────────────┘    │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ COMPONENT PALETTE                                                 │  │
│  │  [Agent]  [Condition]  [Loop]  [Parallel]  [Wait]  [Timer]       │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

### Visual Components

| Component | Icon | Description |
|-----------|------|-------------|
| **Agent** | 🤖 | Drag to canvas, describe in English |
| **Condition** | ◇ | If/else branching |
| **Wire** | → | Connect agents (QUAD WIRE) |
| **Loop** | ↻ | Iterate over collection |
| **Parallel** | ⫴ | Run agents concurrently |
| **Wait** | ⏸ | Wait for event/callback |
| **Timer** | ⏱ | Schedule/delay execution |
| **Error Handler** | ⚠ | Catch and handle errors |

### Agent Properties Panel

```yaml
# Basic Info
name: ParseExcelAgent
description: "Parse Excel file and extract org data"
language: python  # python, java, typescript, go

# English Description (AI generates code from this)
english: |
  Parse the Excel file at the given path.
  Extract team members from the 'Team' sheet.
  Validate email formats using regex.
  Store valid records in the database.
  Log warnings for invalid emails but continue processing.

# Lifecycle Hooks (like Servlet)
lifecycle:
  init: "Load openpyxl library, establish database connection"
  execute: "Read Excel rows, validate, transform, insert to DB"
  cleanup: "Close workbook, disconnect from database"

# Health & Monitoring
health:
  heartbeat_url: /agents/{id}/health
  interval: 30s
  timeout: 5s
  retry_count: 3

# PRETEXT - AI Modifiable Sections
pretext:
  allowed:
    - "Update parsing logic"
    - "Add new validation rules"
    - "Modify column mappings"
  restricted:
    - "Cannot delete existing data"
    - "Cannot access other organizations"
    - "Cannot modify auth tokens"

# Callbacks
callbacks:
  on_complete:
    target: StoreAgent
    pass_data: true
  on_error:
    target: NotifyAgent
    include_stack: true
  on_timeout:
    target: RetryAgent
    max_retries: 3

# Input/Output Schema
input:
  file_path: string
  sheet_name: string?
  batch_size: number?
output:
  records: array
  warnings: array
  stats: object
```

### Code Generation

User describes in English → QUAD generates production code:

**Input (English):**
```
Parse the Excel file, extract team members from the 'Team' sheet,
validate their email formats, and store them in the database.
If any email is invalid, log a warning but continue.
```

**Output (Python):**
```python
# Generated by QUAD Studio
# Agent: ParseExcelAgent
# Generated: 2026-04-15T10:30:00Z

from quad_agent import QUADAgent
from openpyxl import load_workbook
import re

class ParseExcelAgent(QUADAgent):
    """Parse Excel file and extract org data"""

    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    def init(self):
        """Load Excel library, establish database connection"""
        self.db = self.get_database()
        self.workbook = None
        self.log.info("ParseExcelAgent initialized")

    # PRETEXT_START: execute
    # Allowed: Update parsing logic, add validation rules
    # Restricted: Cannot delete data, cannot access other orgs
    def execute(self, input_data: dict) -> dict:
        """Read Excel rows, validate, transform, insert to DB"""
        file_path = input_data['file_path']
        sheet_name = input_data.get('sheet_name', 'Team')

        self.workbook = load_workbook(file_path, read_only=True)
        worksheet = self.workbook[sheet_name]

        records = []
        warnings = []

        for row in worksheet.iter_rows(min_row=2, values_only=True):
            name, title, email = row[0], row[1], row[2]

            # Validate email
            if not re.match(self.EMAIL_REGEX, email or ''):
                warnings.append(f"Invalid email for {name}: {email}")
                self.log.warn(f"Invalid email for {name}: {email}")
                continue

            # Store in database
            record = {
                'name': name,
                'title': title,
                'email': email
            }
            self.db.insert('team_members', record)
            records.append(record)

        return {
            'records': records,
            'warnings': warnings,
            'stats': {
                'total': len(records) + len(warnings),
                'success': len(records),
                'warnings': len(warnings)
            }
        }
    # PRETEXT_END

    def cleanup(self):
        """Close workbook, disconnect from database"""
        if self.workbook:
            self.workbook.close()
        self.db.disconnect()
        self.log.info("ParseExcelAgent cleaned up")

    def heartbeat(self) -> dict:
        """Health check"""
        return {
            'status': 'healthy',
            'db_connected': self.db.is_connected(),
            'uptime': self.get_uptime()
        }
```

### Comparison: BEA JPD vs QUAD Studio

| Feature | BEA WebLogic JPD | QUAD Studio |
|---------|------------------|-------------|
| IDE | WebLogic Workshop | VS Code Extension |
| Visual Designer | Java Process Definition | Agent Flow Designer |
| Language | Java only | Any (Python, Java, TS, Go) |
| Nodes | Controls, Callbacks | Agents, Conditions, Wires |
| Lifecycle | Start, Finish, OnError | init, execute, cleanup, heartbeat |
| Routing | Conversation | QUAD WIRE |
| Properties | XML annotations | YAML + English descriptions |
| Code Generation | Java stubs only | Full code from English |
| Self-Healing | No | Yes (PRETEXT sections) |
| Deployment | WebLogic Server | GCP, AWS, Local, K8s |

---

## Phase 5: Full Product - QUAD Editor (July 2026+)

**Status:** Future
**Goal:** Standalone QUAD Editor (like WebStorm, but for agents)

### Vision

Own editor with:
- Full IDE experience (not just VS Code extension)
- Built-in AI chat (Claude/Gemini/OpenAI selectable)
- Visual agent designer
- Integrated deployment
- Team collaboration

### Planned Features

| Feature | Description |
|---------|-------------|
| **Multi-tenant** | Organization isolation, RBAC |
| **SSO Integration** | Okta, Azure AD, SAML |
| **Audit Logging** | Full trace of agent executions |
| **Cost Tracking** | Per-org API usage billing |
| **Agent Marketplace** | Share/sell agents |
| **Team Collaboration** | Real-time co-editing |
| **Version Control** | Git integration for agents |
| **CI/CD Pipelines** | Auto-deploy on commit |

### Enterprise Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        QUAD Enterprise                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │ Org A       │  │ Org B       │  │ Org C       │  │ Org D      │ │
│  │ (MM)        │  │ (Bank)      │  │ (Startup)   │  │ (Agency)   │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └─────┬──────┘ │
│         │                │                │               │         │
│         └────────────────┼────────────────┼───────────────┘         │
│                          │                │                         │
│                          ▼                ▼                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    QUAD Control Plane                         │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │  │
│  │  │ Auth     │  │ Billing  │  │ Audit    │  │ Marketplace  │  │  │
│  │  │ (SSO)    │  │ (Usage)  │  │ (Logs)   │  │ (Agents)     │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                          │                                          │
│                          ▼                                          │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    QUAD Runtime Cluster                       │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │  │
│  │  │ Agent    │  │ SUMA     │  │ Health   │  │ Scheduler    │  │  │
│  │  │ Executor │  │ WIRE     │  │ Monitor  │  │ (Cron/Event) │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────┘  │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Success Metrics

| Phase | Metric | Target |
|-------|--------|--------|
| Phase 1 | POC Demo | ✅ Working hook + context |
| Phase 2 | API Requests | 1,000/day |
| Phase 3 | VS Code Installs | 500+ |
| Phase 4 | Enterprise Customers | 5+ orgs |

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| VS Code Extension | TypeScript, React (webview) |
| API | Python (Flask/FastAPI) |
| Database | PostgreSQL (Cloud SQL) |
| Agent Runtime | Python, with polyglot support |
| Deployment | GCP Cloud Run, Kubernetes |
| AI | Anthropic Claude (Haiku for speed) |

---

## Timeline Summary

```
2026
────────────────────────────────────────────────────────────────────
Jan         Feb         Mar         Apr         May         Jun
 │           │           │           │           │           │
 ▼           ▼           ▼           ▼           ▼           ▼
┌─────────┐ ┌───────────────────┐ ┌───────────┐ ┌───────────────────┐
│ Phase 1 │ │     Phase 2       │ │  Phase 3  │ │     Phase 4       │
│ CLI +   │ │   API + AI        │ │  Website  │ │   QUAD Plugin     │
│ Demo    │ │  (multi-provider) │ │  (Next.js)│ │   (VS Code)       │
└─────────┘ └───────────────────┘ └───────────┘ └───────────────────┘
    🔄              📅                 📅               📅

Jul         Aug         Sep         Oct         Nov         Dec
 │           │           │           │           │           │
 ▼           ▼           ▼           ▼           ▼           ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Phase 5                                  │
│              Full Product - QUAD Editor + Marketplace            │
└─────────────────────────────────────────────────────────────────┘
                              📅
```

---

## Related Documents

- [QUAD Agent Architecture](documentation/agents/QUAD-AGENT-ARCHITECTURE.md)
- [QUAD Agent Protocol](documentation/agents/QUAD-AGENT-PROTOCOL.md)
- [POC Plan](documentation/planning/POC-JAN13-PLAN.md)
- [Development Roadmap](documentation/planning/DEVELOPMENT-ROADMAP.md)

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**

*QUAD, QUAD WIRE, QUAD STUDIO, SUMA are trademarks of a2Vibes.*
