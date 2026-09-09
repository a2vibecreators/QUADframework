# QUAD Product Backlog

**Last Updated:** January 15, 2026
**Status:** Active Development

---

## Epic 1: Agent Evolution (4 Phases)

### Phase 1: Dynamic Script ✅ COMPLETED
**Status:** Done
**Description:** Current implementation - AI-powered commands with hooks and context memory

**Features:**
- [x] Pre/post hooks
- [x] Context memory (5 types)
- [x] AI Router (Gemini/Claude)
- [x] Smart fallback

---

### Phase 2: Add Reflection (Agent-Lite) 🔄 NEXT UP
**Priority:** HIGH
**Estimated Effort:** 2 weeks
**Description:** Self-validation and retry capability

**Features:**
- [ ] Story validation after generation
- [ ] Quality scoring (0.0-1.0)
- [ ] Auto-retry if quality < threshold
- [ ] Reflection loop (generate → validate → refine → validate)

**Implementation:**
```python
def create_stories_with_reflection(description):
    stories = generate_stories(description)

    # NEW: Validate
    quality = validate_stories(stories)

    # NEW: Reflect and retry
    if quality < 0.7:
        feedback = analyze_issues(stories)
        stories = refine_stories(stories, feedback)

    return stories
```

**Success Criteria:**
- Stories pass validation 95% of time
- Auto-refinement improves quality by 20%+

---

### Phase 3: Add Tools (Function-Calling Agent) 🎯 PLANNED
**Priority:** MEDIUM
**Estimated Effort:** 4 weeks
**Description:** Integrate specialized tools for better context

**Tools to Add:**
1. **analyze_dependencies()** - Check story dependencies
2. **check_database_schema()** - Validate DB design
3. **validate_business_rules()** - Check domain rules
4. **search_similar_projects()** - Find patterns in past projects
5. **estimate_complexity()** - Calculate story points

**Implementation:**
```python
tools = [
    {"name": "analyze_dependencies", "description": "..."},
    {"name": "check_database_schema", "description": "..."},
    {"name": "validate_business_rules", "description": "..."}
]

def create_stories_with_tools(description):
    # AI decides which tools to use
    plan = ai_router.plan(description, tools)

    # Execute tools
    context = {}
    for tool_name in plan.tools:
        context[tool_name] = execute_tool(tool_name, description)

    # Generate with tool results
    stories = generate_stories(description, tool_context=context)

    return stories
```

**Success Criteria:**
- Tool calls reduce errors by 30%
- Context enrichment improves story quality

---

### Phase 4: Full Agent (Reasoning Loop) 🚀 FUTURE
**Priority:** LOW (After MassMutual demo)
**Estimated Effort:** 8 weeks
**Description:** Autonomous, self-directed code generation

**Features:**
- [ ] Iterative reasoning loop (ReAct pattern)
- [ ] Multi-step planning
- [ ] Self-correction
- [ ] Autonomous goal achievement

**Implementation:**
```python
def autonomous_agent(goal):
    """
    User: "Build banking app"
    Agent: Figures out all steps autonomously
    """

    while not goal_achieved:
        # THOUGHT
        thought = ai_router.think("What do I need to do next?")

        # ACTION
        action = choose_action(thought)
        result = execute_action(action)

        # OBSERVATION
        observations.append(result)

        # REFLECTION
        if goal_met(observations):
            goal_achieved = True

    return result
```

**Success Criteria:**
- Can complete project setup without user intervention
- Generates stories + code + tests autonomously

---

## Epic 2: Smart Memory Management

### 2.1: Smart Cleanup with Age Tracking 🔥 HIGH PRIORITY
**Status:** TODO
**Estimated Effort:** 1 week
**Owner:** Pending

**Description:**
Intelligent context cleanup based on last access time and usage frequency.

**Features:**
- [ ] Track last_accessed timestamp
- [ ] Track access_count (increments on use)
- [ ] Calculate age_days (since last_accessed, not creation)
- [ ] Auto-promote to "important" if accessed 5+ times
- [ ] Three retention policies: auto, important, permanent
- [ ] Context-specific max age (Memory: 30d, Project: 90d, etc.)
- [ ] Archive before delete (nothing lost)
- [ ] User commands: tag, pin, unpin

**Schema:**
```python
{
  "timestamp": "2026-01-15T10:30:00",
  "content": {...},
  "metadata": {
    "last_accessed": "2026-01-20T14:00:00",
    "access_count": 5,
    "age_days": 0,
    "tags": ["architecture", "important"],
    "pinned": false,
    "retention_policy": "auto"  # auto/important/permanent
  }
}
```

**Commands:**
```bash
quad context cleanup --dry-run
quad context tag <id> important
quad context pin <id>
quad context stats
quad context list --aging
```

**Success Criteria:**
- Frequently used context never deleted
- Old unused context cleaned automatically
- Archive preserves deleted data

---

### 2.2: Context Privacy Controls
**Priority:** MEDIUM
**Estimated Effort:** 1 week

**Features:**
- [ ] Exclude sensitive topics (health, finance can be disabled)
- [ ] Redact API keys and secrets in context
- [ ] User-configurable retention periods
- [ ] Export with anonymization

---

## Epic 3: quad doc Command

### 3.1: Documentation Generator 📚 HIGH PRIORITY
**Status:** TODO
**Estimated Effort:** 2 weeks

**Description:**
Auto-generate industry-standard documentation for projects.

**Command:**
```bash
quad doc init              # Create doc structure
quad doc generate api      # Generate API docs
quad doc generate db       # Generate DB schema docs
quad doc generate arch     # Generate architecture diagram
quad doc journey create    # Create test journey
quad doc update            # Update all docs
```

**Standard Documentation Structure:**
```
documentation/
├── README.md                    # Overview
├── architecture/
│   ├── README.md                # System architecture
│   ├── diagrams/                # Architecture diagrams
│   └── decisions/               # ADRs
├── api/
│   ├── README.md                # API overview
│   ├── endpoints/               # Endpoint docs
│   └── swagger.yaml             # OpenAPI spec
├── database/
│   ├── README.md                # DB overview
│   ├── schema.sql               # Full schema
│   ├── erd.png                  # Entity relationship diagram
│   └── tables/                  # Per-table docs
├── test-journeys/
│   ├── README.md                # Journey overview
│   ├── auth/                    # Auth journeys
│   ├── accounts/                # Account journeys
│   └── transfers/               # Transfer journeys
└── deployment/
    ├── README.md                # Deployment guide
    └── environments/            # Env-specific docs
```

**Features:**
- [ ] Template system (QUAD defaults + org overrides)
- [ ] Auto-generation from code/DB
- [ ] Test journey integration
- [ ] Markdown + diagrams

**Success Criteria:**
- Generates complete docs in <5 minutes
- Docs pass industry standards
- Customizable per org

---

### 3.2: Test Journey System 🧪 HIGH PRIORITY
**Status:** TODO
**Estimated Effort:** 2 weeks

**Description:**
Document test scenarios with steps, expected output, API calls, and DB impact.

**From NutriNine Discussion:**
> Test case should have: (1) Steps to execute, (2) Expected output, (3) What APIs used, (4) What tables impacted. This helps QA and technical folks get started faster.

**Journey Format:**
```markdown
# Test Journey: User Login

## Overview
- **Feature:** Authentication
- **Story:** As a user, I can login with email/password
- **Priority:** P0 (Critical)

## Prerequisites
- User account exists in database
- API server running
- Frontend deployed

## Test Steps

### Step 1: Navigate to Login Page
**Action:** Open browser, navigate to /login
**Expected:**
- Login form displayed
- Email and password fields visible
- "Login" button enabled

**APIs Called:** None
**Tables Accessed:** None

---

### Step 2: Enter Credentials
**Action:**
1. Enter email: test@example.com
2. Enter password: Test123!
3. Click "Login" button

**Expected:**
- Loading spinner shown
- No validation errors

**APIs Called:**
- `POST /api/v1/auth/login`
  - Request: `{"email": "...", "password": "..."}`
  - Response: `{"token": "...", "user": {...}}`

**Tables Accessed:**
- `users` (SELECT WHERE email = ?)
- `sessions` (INSERT new session)

---

### Step 3: Verify Login Success
**Action:** Wait for response

**Expected:**
- Redirected to /dashboard
- User name displayed in header
- Session token stored in localStorage

**APIs Called:**
- `GET /api/v1/user/profile` (after redirect)
  - Headers: `Authorization: Bearer <token>`
  - Response: `{"id": "...", "name": "...", "email": "..."}`

**Tables Accessed:**
- `users` (SELECT WHERE id = ?)
- `sessions` (SELECT to validate token)

---

## Database Impact Summary
| Table | Operations | Fields |
|-------|------------|--------|
| users | SELECT | id, email, password_hash, name |
| sessions | INSERT, SELECT | id, user_id, token, expires_at |

## API Summary
| Endpoint | Method | Purpose |
|----------|--------|---------|
| /api/v1/auth/login | POST | Authenticate user |
| /api/v1/user/profile | GET | Get user details |

## Error Scenarios
1. Invalid email → 400 Bad Request
2. Wrong password → 401 Unauthorized
3. Account locked → 403 Forbidden
4. Server error → 500 Internal Server Error

## Performance
- Expected response time: <500ms
- Max response time: 2s

## Notes
- JWT token expires after 24 hours
- Session cleanup runs daily at midnight
```

**Commands:**
```bash
# Create journey
quad doc journey create auth/login

# List journeys
quad doc journey list

# Generate from story
quad doc journey generate --story "User Login"

# Validate journey
quad doc journey validate auth/login

# Export all journeys
quad doc journey export --format pdf
```

**Features:**
- [ ] Step-by-step format
- [ ] API call tracking
- [ ] DB impact tracking
- [ ] Auto-generate from stories
- [ ] Visual flow diagrams
- [ ] PDF export

**Success Criteria:**
- QA can execute tests from docs alone
- Developers understand API/DB flow
- Non-technical stakeholders can follow

---

## Epic 4: Conversational Commands (Agent Evolution)

### KEY INSIGHT 💡
**Each QUAD command is ALREADY an agent with domain restrictions!**

Current commands (story, init, code) are single-turn agents:
- Have specific domain restrictions (story generation, project setup, code generation)
- Use persistent context memory
- Call AI APIs (Gemini/Claude)
- Self-heal with fallback logic

**Evolution Path:**
```
Phase 1: Single-turn agents ✅ (Current)
   ↓
Phase 2: Multi-turn conversational agents 🔄 (Next)
   ↓
Phase 3: SUMA SQUAD 🚀 (Future)
```

**Implementation:** Just add chat loop to existing commands!

---

### 4.1: Conversational Story Agent
**Priority:** MEDIUM
**Estimated Effort:** 1 week

**Description:** Multi-turn conversation for story generation

```bash
# Current (Single-turn)
quad story create
> Enter feature description: "banking portal with accounts"
> [Generates stories immediately]

# New (Multi-turn)
quad story chat
> Story Agent: What feature are you building?
User: Banking portal with accounts and transfers
> Story Agent: What type of accounts? (Savings, Checking, Both?)
User: Both, plus credit cards
> Story Agent: Should I include fraud detection?
User: Yes, and transaction limits
> Story Agent: [Generates 15 stories with all requirements]
> Story Agent: Want to refine any stories? (yes/no)
```

**Benefits:**
- Clarifies requirements through conversation
- Maintains context across turns
- Applies domain restrictions (story generation only)
- Uses same PGCE algorithm

---

### 4.2: Conversational Init Agent
**Priority:** LOW
**Estimated Effort:** 1 week

**Description:** Multi-turn project setup with recommendations

```bash
quad init chat
> Init Agent: What type of project?
User: E-commerce site
> Init Agent: Based on your past projects (React, Node.js), should I use the same stack?
User: Yes but use PostgreSQL instead of MongoDB
> Init Agent: [Creates project with learned preferences]
```

---

### 4.3: Conversational Code Agent
**Priority:** MEDIUM
**Estimated Effort:** 1 week

**Description:** Interactive code generation with refinement

```bash
quad code chat
> Code Agent: I see 5 stories ready. Which one first?
User: US-003 Account Balance
> Code Agent: [Generates code]
> Code Agent: I used JWT auth pattern from finance context. Correct?
User: Yes, looks good
> Code Agent: Next story? (US-004 Transaction History)
```

---

### 4.4: General Assistant (quad ask/learn/suggest)
**Priority:** LOW
**Status:** DEFERRED (Pending DISCUSSION-5 review)

**Note:** See DISCUSSION-5-CONVERSATIONAL-VS-CLAUDE.md for identity analysis.
Risk of becoming "just Claude CLI clone" if not properly differentiated.

---

## Epic 5: WhatsApp QUAD School

### 5.1: Daily Micro-Lessons 📱
**Priority:** MEDIUM
**Estimated Effort:** 4 weeks

**Description:** Teach software development via WhatsApp

**Features:**
- [ ] Daily 5-minute lessons
- [ ] Simple analogies for technical concepts
- [ ] Interactive quizzes
- [ ] Streak tracking
- [ ] Gamification (badges, levels)
- [ ] 90-day curriculum

**Curriculum Topics:**
1. Week 1-2: What is Software?
2. Week 3-4: Frontend vs Backend
3. Week 5-6: Databases
4. Week 7-8: APIs
5. Week 9-10: Authentication
6. Week 11-12: Deployment
7. ...and so on

**Success Criteria:**
- 1000+ students enrolled
- 60% completion rate
- 4.5+ star rating

---

## Epic 6: SUMA Integration

### 6.1: SUMA SQUAD Integration
**Priority:** HIGH (After MassMutual)
**Estimated Effort:** 6 weeks

**Description:** Specialized conversational agents (evolution of QUAD commands)

**KEY INSIGHT:**
SUMA SQUAD agents are NOT new agents - they're conversational versions of existing QUAD commands!

**Evolution:**
```
QUAD Commands (Single-turn)  →  SUMA SQUAD (Conversational)

quad story create             →  Story Agent (multi-turn)
quad init                     →  Init Agent (multi-turn)
quad code generate            →  Code Agent (multi-turn)
quad test                     →  Test Agent (multi-turn)
quad doc generate             →  Doc Agent (multi-turn)
```

**Agents:**
- **Story Agent** - Conversational story generation (based on `quad story create`)
- **Code Agent** - Conversational code generation (based on `quad code generate`)
- **Test Agent** - Conversational test generation (based on `quad test`)
- **Doc Agent** - Conversational documentation (based on `quad doc generate`)
- **PR Agent** - Code review conversations (NEW functionality)

**Implementation:**
Each agent = Existing command + Chat loop + Same restrictions

```python
# Example: Story Agent
class StoryAgent:
    def __init__(self):
        self.context = ContextManager()  # Same context system
        self.ai_router = AIRouter()      # Same AI router
        self.restrictions = ["story generation only", "no code generation"]

    def chat(self):
        """Add chat loop to existing story command"""
        while not done:
            user_input = input("User: ")

            # Use existing story generation logic
            response = self.generate_stories_conversational(user_input)

            print(f"Story Agent: {response}")
```

**Benefits:**
- Reuse existing PGCE algorithm
- Keep domain restrictions (story agent can't write code)
- Use same context memory
- No reimplementation needed

---

### 6.2: SUMA WIRE
**Priority:** MEDIUM
**Estimated Effort:** 8 weeks

**Description:** Invisible agent routing

**Concept:**
```python
# Developer writes:
result = get_weather("NYC")

# SUMA WIRE intercepts:
# - Checks cache (5ms)
# - If miss, routes to weather agent (500ms)
# - Updates cache
# - Returns result

# Developer sees instant response!
```

---

## Epic 7: Multi-Platform Support

### 7.1: SUMA Plugin (VS Code)
**Priority:** HIGH
**Estimated Effort:** 8 weeks

**Description:** VS Code extension like Claude Code

**Features:**
- [ ] Inline code generation
- [ ] Context-aware suggestions
- [ ] QUAD commands in IDE
- [ ] Visual test journeys

---

### 7.2: QUAD Mobile CLI
**Priority:** LOW
**Estimated Effort:** 4 weeks

**Description:** Mobile app for QUAD commands

---

## Epic 8: Claude CLI Integration

### 8.1: Hook Control System 🔥 HIGH PRIORITY
**Priority:** HIGH (Testing Phase)
**Estimated Effort:** 3 days
**Status:** TODO

**Description:**
Enable/disable QUAD hooks per Claude CLI session for flexible workflow.

**Use Cases:**
1. **Developer Mode** (Hooks ON): Working on QUAD projects, want context capture
2. **Direct Mode** (Hooks OFF): Talking to Claude directly, no QUAD interception
3. **Selective** (Prefix-based): Only intercept commands starting with "quad-"

**Requirements:**
```
User Session 1 (with Claude, discussing)
  └─ Hooks: OFF (direct Claude access)

User Session 2 (VS Code, building project)
  └─ Hooks: ON (capture QUAD commands)
```

**Configuration:**
```json
// ~/.claude/quad-hooks.json
{
  "enabled": true,
  "mode": "prefix",
  "prefixes": ["quad-", "quad "],
  "commands": ["init", "story", "code", "test", "doc"],
  "session_override": {
    "session_id_123": false  // Disable for specific session
  }
}
```

**Commands:**
```bash
# Enable/disable hooks
quad hooks enable
quad hooks disable
quad hooks status

# Per-session control
quad hooks session enable
quad hooks session disable

# Configure trigger mode
quad hooks config set mode prefix     # Only "quad-" commands
quad hooks config set mode all        # All commands
quad hooks config set mode whitelist  # Specific commands only
```

**Hook Logic:**
```python
def should_invoke_hook(command: str, session_id: str) -> bool:
    """Determine if hook should intercept command"""
    config = load_hook_config()

    # Check global enable
    if not config.get("enabled", False):
        return False

    # Check session override
    session_override = config.get("session_override", {}).get(session_id)
    if session_override is not None:
        if not session_override:
            return False

    # Check trigger mode
    mode = config.get("mode", "prefix")

    if mode == "prefix":
        prefixes = config.get("prefixes", ["quad-", "quad "])
        return any(command.startswith(prefix) for prefix in prefixes)

    elif mode == "whitelist":
        commands = config.get("commands", [])
        cmd_name = command.split()[0]
        return cmd_name in commands

    elif mode == "all":
        return True

    return False
```

**Integration Points:**
1. `.claude/quad-hooks.json` - Configuration file
2. Claude CLI pre-prompt hook - Intercept before sending to Claude
3. QUAD context system - Store command + response
4. Session tracking - Remember per-session preferences

**Success Criteria:**
- Can disable hooks for direct Claude conversation
- Can enable hooks for QUAD development workflow
- Per-session control works independently
- No performance impact when disabled

---

## Quick Wins (Low Effort, High Impact)

### Export/Import Context
**Effort:** 2 days
```bash
quad context export backup.json
quad context import backup.json
```

### Story Templates
**Effort:** 1 week
```bash
quad story template banking
quad story template ecommerce
quad story template saas
```

### Batch Commands
**Effort:** 3 days
```bash
quad batch init,story,code  # Run all in sequence
```

### Dry-Run Mode
**Effort:** 2 days
```bash
quad story create --dry-run  # Show what would be generated
quad code generate --dry-run
```

---

## Bugs / Technical Debt

### Known Issues
- [ ] Context search is slow with 1000+ entries
- [ ] AI Router doesn't cache responses
- [ ] No retry logic for API failures
- [ ] Test journeys not implemented yet

### Performance Improvements
- [ ] Add caching layer for AI responses
- [ ] Optimize context search (add indexing)
- [ ] Lazy load context files
- [ ] Parallel story generation

---

## How to Use This Backlog

### For Development
1. Pick items from "High Priority"
2. Break down into smaller tasks
3. Estimate effort
4. Implement and test
5. Mark as ✅ Completed

### For Planning
- Monthly: Review and reprioritize
- Quarterly: Update effort estimates
- Yearly: Add new epics

### For Demo/Marketing
- Show completed features (✅)
- Tease upcoming features (🔥 HIGH PRIORITY)
- Discuss future vision (🚀 FUTURE)

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
