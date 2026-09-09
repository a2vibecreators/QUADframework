# Context Memory System - Deep Dive Discussion
**Date:** January 15, 2026
**Status:** Phase 1 Complete - Need to Discuss Next Steps

---

## What We Built (Phase 1)

### 1. Hook System Architecture

#### The Problem We're Solving
**Current:** Every time you run a QUAD command, it starts fresh. No memory of past projects, preferences, or decisions.

**Solution:** Pre/post hooks that capture context from every command execution and build a memory over time.

#### How Hooks Work

```
┌─────────────────────────────────────────────────────────────┐
│                    USER RUNS COMMAND                         │
│              quad story create "banking app"                 │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                      PRE-HOOK                                │
│  1. Capture request:                                         │
│     - Command: "story"                                       │
│     - Input: "banking app"                                   │
│     - Timestamp                                              │
│                                                              │
│  2. Enrich with past context:                                │
│     - Check: Have we built banking apps before?              │
│     - Load: Past architecture decisions                      │
│     - Load: User's preferred tech stack                      │
│     - Add: Compliance requirements for finance               │
│                                                              │
│  3. Return enriched context to command                       │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  EXECUTE COMMAND                             │
│   - Generate stories with enriched context                   │
│   - PGCE algorithm runs                                      │
│   - Stories prioritized                                      │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                     POST-HOOK                                │
│  1. Capture response:                                        │
│     - Stories generated: 6 stories                           │
│     - Tech stack used: Next.js, Spring Boot, PostgreSQL      │
│     - Patterns used: JWT auth, REST API                      │
│                                                              │
│  2. Analyze context:                                         │
│     - Topics: ["finance", "project", "architecture"]         │
│     - Decisions: ["JWT for auth", "PostgreSQL database"]     │
│     - Preferences: ["Spring Boot backend"]                   │
│                                                              │
│  3. Store in context trees:                                  │
│     - Finance context: "Banking app requirements"            │
│     - Project context: "Tech stack: Next.js + Spring Boot"   │
│     - Preferences: "User prefers Spring Boot"                │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  CONTEXT STORED                              │
│   Next time you build a banking app, QUAD remembers!         │
└─────────────────────────────────────────────────────────────┘
```

#### Files Created

**1. hook_manager.py**
- **What:** Orchestrates when hooks run
- **Key Function:** `execute_with_hooks(command, args, command_func)`
- **How it works:**
  ```python
  # Before command
  pre_context = pre_hook.execute("story", {"description": "..."})

  # Run command with enriched context
  result = generate_stories(enriched_context=pre_context)

  # After command
  post_hook.execute("story", args, result, pre_context)
  ```

**2. pre_hook.py**
- **What:** Captures request and enriches with past context
- **Key Functions:**
  - `_capture_request()` - Save what user asked for
  - `_enrich_context()` - Add past patterns/decisions
  - `_load_past_project_patterns()` - Get similar projects

**3. post_hook.py**
- **What:** Analyzes response and stores context
- **Key Functions:**
  - `_capture_response()` - Save command output
  - `_analyze_context()` - Extract topics/decisions
  - `_store_context()` - Save to appropriate context tree

**4. config.py**
- **What:** Hook configuration
- **Key Settings:**
  ```json
  {
    "enabled": true,
    "exclude_topics": ["politics", "religion", "passwords"],
    "retention_days": 365,
    "auto_cleanup": true
  }
  ```

---

## 🤔 Discussion Point #1: Hook Execution Flow

### Question 1: When Should Hooks Fire?

**Option A: Every Command** (Current)
- Fire hooks for `story`, `code`, `init`, `test`, `deploy`
- ✅ Pro: Maximum context capture
- ❌ Con: Performance overhead

**Option B: Selective Commands**
- Only fire for "important" commands: `story`, `code`, `init`
- ✅ Pro: Better performance
- ❌ Con: Miss some context

**Your Decision:** Which approach do you prefer?

---

### Question 2: What Should Pre-Hook Enrich?

**Example Scenario:** User runs `quad story create` for a banking app.

**Pre-hook could enrich with:**
1. **Past project patterns**
   - "You built a banking app 3 months ago"
   - "You used JWT auth and PostgreSQL"
   - Should we auto-suggest same stack?

2. **User preferences**
   - "You always use Spring Boot for backend"
   - "You prefer REST over GraphQL"
   - Should we auto-apply these?

3. **Domain knowledge**
   - "Banking apps need compliance features"
   - "Finance domain requires audit logs"
   - Should we auto-add these requirements?

**Your Decision:** How aggressive should enrichment be?

---

### Question 3: Privacy and Security

**What should we NEVER capture?**
- ❌ Passwords, API keys, secrets
- ❌ Personal health details (unless user enables health context)
- ❌ Financial account numbers
- ❌ Anything in `exclude_topics` list

**Sensitive Data Detection:**
```python
# Current approach: Simple keyword matching
sensitive_keys = ["password", "api_key", "secret", "token"]
if key in sensitive_keys:
    value = "***REDACTED***"
```

**Your Decision:** Is keyword matching enough, or do we need AI-based PII detection?

---

## What We Built (Phase 1) - Context Storage

### 2. Context Types

We created **5 context trees**, each storing different types of information:

#### Context Type 1: PROJECT
**Storage:** `.quad/project-memory.json` (project-local)

**What it stores:**
```json
{
  "context_type": "project",
  "entries": [
    {
      "timestamp": "2026-01-15T10:30:00",
      "text": "Tech stack: Next.js, Spring Boot, PostgreSQL",
      "metadata": {
        "command": "init",
        "decision": "tech_stack"
      }
    },
    {
      "timestamp": "2026-01-15T10:35:00",
      "text": "Authentication: JWT with refresh tokens",
      "metadata": {
        "command": "story",
        "decision": "auth_method"
      }
    }
  ]
}
```

**Use case:** When you run `quad code generate`, it loads project context to understand what tech stack you chose.

---

#### Context Type 2: HEALTH
**Storage:** `~/.quad/contexts/health.json` (user-global)

**What it stores:**
```json
{
  "context_type": "health",
  "entries": [
    {
      "timestamp": "2026-01-10T14:20:00",
      "text": "User mentioned building a fitness tracking app",
      "metadata": {
        "topics": ["health", "fitness", "tracking"]
      }
    }
  ]
}
```

**Use case:** If user mentions health-related needs, QUAD can reference past health projects.

**Keywords that trigger health context:**
- health, medical, doctor, medicine, allergy, symptom, nutrition, exercise

---

#### Context Type 3: FINANCE
**Storage:** `~/.quad/contexts/finance.json` (user-global)

**What it stores:**
```json
{
  "context_type": "finance",
  "entries": [
    {
      "timestamp": "2026-01-15T10:30:00",
      "text": "Building banking app with account transfers",
      "metadata": {
        "domain": "finance",
        "features": ["accounts", "transfers", "transactions"]
      }
    }
  ]
}
```

**Use case:** Next time you build a finance app, QUAD remembers compliance requirements.

**Keywords that trigger finance context:**
- finance, banking, payment, transaction, account, balance, budget, investment

---

#### Context Type 4: PREFERENCES
**Storage:** `~/.quad/contexts/preferences.json` (user-global)

**What it stores:**
```json
{
  "context_type": "preferences",
  "entries": [
    {
      "timestamp": "2026-01-15T10:30:00",
      "text": "User prefers Spring Boot for backend",
      "metadata": {
        "preference_type": "framework",
        "value": "Spring Boot"
      }
    }
  ]
}
```

**Use case:** Auto-suggest Spring Boot next time user creates a backend project.

**Keywords that trigger preferences:**
- prefer, like, dislike, always, never, usually, style, convention

---

#### Context Type 5: MEMORY
**Storage:** `~/.quad/contexts/memory.json` (user-global)

**What it stores:**
```json
{
  "context_type": "memory",
  "entries": [
    {
      "timestamp": "2026-01-15T10:30:00",
      "text": "User working on MassMutual demo preparation",
      "metadata": {
        "general": true
      }
    }
  ]
}
```

**Use case:** Catch-all for anything that doesn't fit other categories.

---

## 🤔 Discussion Point #2: Context Storage

### Question 4: Storage Location Strategy

**Current Design:**
- **Project-local:** `.quad/project-memory.json` (PROJECT context only)
- **User-global:** `~/.quad/contexts/*.json` (all other contexts)

**Reasoning:**
- Project context is specific to that project
- Health/Finance/Preferences are user-wide

**Your Decision:** Is this the right separation?

**Alternative:** Everything user-global, but tagged with project ID?

---

### Question 5: Data Retention

**Current:** 365 days (1 year)

**Cleanup Logic:**
```python
# In post_hook, after storing context
if entry_age > 365 days:
    delete entry
```

**Your Decision:**
- Is 1 year right, or should we keep forever?
- Should users control retention per context type?
- Should we have size limits (e.g., max 1000 entries)?

---

### Question 6: Context Classification

**How we classify:** Keyword matching

```python
def classify_context(text: str) -> ContextType:
    if "banking" in text or "payment" in text:
        return ContextType.FINANCE
    elif "health" in text or "medical" in text:
        return ContextType.HEALTH
    # ... etc
```

**Problem:** Not very smart. "I'm building a healthy banking app" could be misclassified.

**Better approach:** AI classification with Gemini

```python
def classify_context_ai(text: str) -> ContextType:
    prompt = f"""
    Classify this text into one category:
    - project (technical decisions)
    - health (health/medical)
    - finance (banking/payments)
    - preferences (user preferences)
    - memory (general)

    Text: {text}

    Return only the category name.
    """
    return gemini.classify(prompt)
```

**Your Decision:** Keyword matching or AI classification?

---

## What We Built (Phase 1) - CLI Commands

### 3. Context Management Commands

#### quad context list
**What it does:** Shows all context types with status

```
┌─────────────┬──────────┬──────────┬────────────────────────┐
│ Context     │ Enabled  │ Entries  │ Last Updated           │
├─────────────┼──────────┼──────────┼────────────────────────┤
│ project     │    ✓     │    5     │ 2026-01-15 10:35:00    │
│ health      │    ✓     │    0     │ Never                  │
│ finance     │    ✓     │    3     │ 2026-01-15 10:30:00    │
│ preferences │    ✓     │    2     │ 2026-01-15 10:30:00    │
│ memory      │    ✓     │    1     │ 2026-01-15 10:30:00    │
└─────────────┴──────────┴──────────┴────────────────────────┘
```

---

#### quad context show <name>
**What it does:** Shows details and recent entries

```
Context: finance
────────────────

→ Type: finance
→ Entries: 3
→ Storage: ~/.quad/contexts/finance.json
→ Created: 2026-01-15 10:30:00
→ Updated: 2026-01-15 10:35:00

→ Recent entries:

1. [2026-01-15 10:35:00]
   Building banking app with account transfers...

2. [2026-01-15 10:32:00]
   User needs JWT authentication for API...
```

---

#### quad context enable/disable <name>
**What it does:** Turn context types on/off

```bash
quad context disable health
# ✓ Disabled context: health

# Health context will no longer capture data
```

**Use case:** Privacy control. Disable health context if you don't want health info stored.

---

#### quad context clear <name>
**What it does:** Delete all data in a context

```bash
quad context clear finance
# ✓ Cleared context: finance

# All finance entries deleted
```

---

#### quad context search <query>
**What it does:** Search across all contexts

```bash
quad context search "banking"

Search: banking
───────────────

FINANCE
────────────────────────────────────────
1. [2026-01-15 10:30:00]
   Building banking app with account transfers...

PROJECT
────────────────────────────────────────
1. [2026-01-15 10:30:00]
   Tech stack for banking portal: Next.js + Spring Boot...
```

---

#### quad context export/import
**What it does:** Backup and restore contexts

```bash
# Export
quad context export finance finance-backup.json
# ✓ Exported finance to finance-backup.json

# Import
quad context import finance finance-backup.json
# ✓ Imported finance-backup.json to finance
```

**Use case:** Share contexts between machines or team members.

---

## 🤔 Discussion Point #3: CLI Commands

### Question 7: Context Sharing

**Scenario:** You and Pradeep both work on banking apps.

**Option A: Share contexts**
```bash
# You export your finance context
quad context export finance finance-context.json

# Pradeep imports it
quad context import finance finance-context.json

# Now Pradeep has your banking knowledge
```

**Option B: Keep contexts private**
- Each developer builds their own context
- No sharing between team members

**Your Decision:** Should contexts be shareable?

---

### Question 8: Context Sync Across Devices

**Scenario:** You work on MacBook and Linux desktop.

**Should contexts sync automatically?**

**Option A: Manual sync** (current)
```bash
# On MacBook
quad context export preferences prefs.json
scp prefs.json linux-desktop:~/

# On Linux
quad context import preferences prefs.json
```

**Option B: Auto-sync via cloud**
- Store contexts in Firebase/S3
- Auto-sync across devices
- Requires authentication

**Your Decision:** Manual or auto-sync?

---

## What's Next - Remaining Tasks

### Task 4: Integrate Hooks with Existing Commands

#### What Needs to Change

**Current: story.py**
```python
def create_stories():
    # Get user input
    description = ask_for_description()

    # Generate stories
    stories = generate_stories_from_description(description)

    # Save stories
    save_stories(stories)
```

**With Hooks: story.py**
```python
def create_stories():
    # PRE-HOOK captures request and enriches
    hook_manager = get_hook_manager()

    def run_command():
        description = ask_for_description()
        stories = generate_stories_from_description(description)
        save_stories(stories)
        return stories

    # Execute with hooks
    result = hook_manager.execute_with_hooks(
        "story",
        {"description": description},
        run_command
    )
    # POST-HOOK analyzes and stores context
```

**Changes needed in:**
- ✅ story.py (story generation)
- ✅ code.py (code generation)
- ✅ init.py (project initialization)
- ✅ test.py (testing)

---

### Task 5: Add Gemini API Integration

#### Current: Rule-Based Context Analysis

**post_hook.py** (current)
```python
def _rule_based_analysis(command, args, result):
    # Simple keyword matching
    if command == "init":
        return {"topics": ["project"], "decisions": [...]}
    elif command == "story":
        return {"topics": ["project"], "memory": {...}}
```

**Problem:** Not smart. Can't understand nuance.

---

#### Proposed: AI-Powered Context Analysis

**post_hook.py** (with Gemini)
```python
def _analyze_context_ai(command, args, result):
    prompt = f"""
    Analyze this QUAD command execution and extract:

    1. Topics discussed (health, finance, project, etc.)
    2. Decisions made (tech stack, architecture, etc.)
    3. User preferences expressed
    4. Information to remember for future

    Command: {command}
    Input: {args}
    Output: {result}

    Return JSON:
    {{
      "topics": ["finance", "project"],
      "decisions": [
        {{"type": "tech_stack", "value": "Spring Boot"}},
        {{"type": "auth", "value": "JWT"}}
      ],
      "preferences": [
        {{"type": "framework", "value": "Spring Boot"}}
      ],
      "memory": {{
        "project_type": "banking_app",
        "features": ["accounts", "transfers"]
      }}
    }}
    """

    # Call Gemini API
    response = gemini.generate(prompt)
    return json.loads(response)
```

---

## 🤔 Discussion Point #4: AI Integration

### Question 9: Which AI Model?

**Option A: Gemini (Free)**
- ✅ Free tier available
- ✅ Good at text analysis
- ❌ Less smart than Claude
- ❌ Rate limits

**Option B: Claude (Paid)**
- ✅ Very smart
- ✅ Better context understanding
- ❌ Costs money (user's API key)
- ❌ Rate limits

**Option C: Both (Let User Choose)**
```json
{
  "context_analysis": {
    "provider": "gemini",  // or "claude"
    "model": "gemini-pro", // or "claude-sonnet-4"
    "api_key": "..."       // user provides
  }
}
```

**Your Decision:** Which AI model should we use?

---

### Question 10: When to Run AI Analysis?

**Option A: Real-time** (During post-hook)
```
Command completes → POST-HOOK → Call Gemini → Store context
                       ↑
                  User waits 2-3 seconds
```
- ✅ Immediate context storage
- ❌ Slows down commands

**Option B: Background** (After command returns)
```
Command completes → Return to user immediately
                    ↓
                Background thread → Call Gemini → Store context
```
- ✅ Fast commands
- ❌ Slight delay in context storage

**Your Decision:** Real-time or background?

---

### Question 11: AI Analysis Depth

**Light Analysis** (Fast, cheap)
```
Prompt: "What's the main topic of this conversation?"
Response: "finance"
```
- ✅ Quick (1 second)
- ✅ Cheap API cost
- ❌ Limited insight

**Deep Analysis** (Slow, expensive)
```
Prompt: "Analyze this conversation in detail. Extract:
- All topics discussed
- Technical decisions made
- User preferences
- Domain requirements
- Compliance needs
- Security concerns
- ...etc (20 bullet points)"
```
- ✅ Rich insights
- ❌ Slow (5-10 seconds)
- ❌ Higher API cost

**Your Decision:** How deep should analysis be?

---

## Implementation Plan - Next Steps

### Step 4A: Integrate Hooks into story.py

**What we'll do:**
1. Import HookManager
2. Wrap `create_stories()` function
3. Test: Run `quad story create` and verify hooks fire
4. Check: Logs in `~/.quad/logs/pre_hook.log` and `post_hook.log`

**Estimated time:** 15 minutes

---

### Step 4B: Integrate Hooks into code.py

**What we'll do:**
1. Import HookManager
2. Wrap `generate_code()` function
3. Test: Run `quad code generate` and verify context captured

**Estimated time:** 15 minutes

---

### Step 4C: Integrate Hooks into init.py

**What we'll do:**
1. Import HookManager
2. Wrap `run_init()` function
3. Test: Run `quad init test-project` and verify project context stored

**Estimated time:** 15 minutes

---

### Step 4D: Integrate Hooks into test.py

**What we'll do:**
1. Import HookManager
2. Wrap `run_test()` function
3. Test: Run `quad test` and verify test patterns stored

**Estimated time:** 15 minutes

---

### Step 5: Add Gemini API Integration

**What we'll do:**
1. Install `google-generativeai` library
2. Create `quad_cli/ai/gemini.py` wrapper
3. Update `post_hook.py` to use AI analysis
4. Add API key configuration
5. Test: Run commands and verify smart context extraction

**Estimated time:** 30 minutes

---

## Testing Plan

### Test Case 1: Basic Hook Execution
```bash
# Initialize project
quad init banking-portal

# Check: project context created
quad context show project
# Should show: "Project type: Full Stack"

# Generate stories
quad story create

# Check: finance context created (because "banking")
quad context show finance
# Should show: Banking app features

# Check: preferences captured
quad context show preferences
# Should show: Tech stack preferences
```

---

### Test Case 2: Context Enrichment
```bash
# Create first banking project
quad init bank-app-1
quad story create

# Create second banking project
quad init bank-app-2
quad story create

# Check: Pre-hook should enrich with patterns from bank-app-1
# Should auto-suggest similar features/architecture
```

---

### Test Case 3: Privacy Controls
```bash
# Disable health context
quad context disable health

# Try to store health data
# Should NOT be captured

# Enable again
quad context enable health
```

---

### Test Case 4: Search
```bash
# Build several projects over time
quad init project-1
quad init project-2
quad init project-3

# Search across all contexts
quad context search "authentication"
# Should find all projects that mentioned auth
```

---

## Key Decisions Needed

### Decision Summary

| # | Question | Options | Your Choice |
|---|----------|---------|-------------|
| 1 | When should hooks fire? | A) Every command<br>B) Selective | ⏸️ TBD |
| 2 | How aggressive should enrichment be? | A) Auto-suggest<br>B) Auto-apply<br>C) Manual | ⏸️ TBD |
| 3 | Sensitive data detection | A) Keywords<br>B) AI-based PII | ⏸️ TBD |
| 4 | Storage location | A) Current (split)<br>B) All user-global | ⏸️ TBD |
| 5 | Data retention | A) 365 days<br>B) Forever<br>C) Configurable | ⏸️ TBD |
| 6 | Context classification | A) Keywords<br>B) AI | ⏸️ TBD |
| 7 | Context sharing | A) Shareable<br>B) Private | ⏸️ TBD |
| 8 | Device sync | A) Manual<br>B) Auto-sync | ⏸️ TBD |
| 9 | AI model | A) Gemini<br>B) Claude<br>C) Both | ⏸️ TBD |
| 10 | AI timing | A) Real-time<br>B) Background | ⏸️ TBD |
| 11 | AI depth | A) Light<br>B) Deep | ⏸️ TBD |

---

## Your Turn! 🎤

Please review and provide your thoughts on:

1. **Overall Architecture** - Does the hook + context storage design make sense?

2. **The 11 Decision Points** - What's your preference for each?

3. **Priority** - Which task should we tackle first?
   - Task 4: Integrate hooks into commands (story, code, init, test)
   - Task 5: Add Gemini AI integration

4. **Testing** - How should we test this? MassMutual demo or internal testing first?

5. **Timeline** - When do you want this ready by?

6. **Any concerns or questions?**

---

**Let's discuss! I'm ready to explain any part in more detail or make changes based on your feedback.**

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
