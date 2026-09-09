# Discussion #1: Context Memory System
**Date:** January 15, 2026
**Topic:** Building Long-Term Memory for QUAD

---

## The Vision

**Problem:** Every time you use QUAD, it starts fresh. No memory of past projects, preferences, or patterns.

**Solution:** Context Memory System - QUAD remembers everything and gets smarter over time.

---

## How It Works

### The Memory Loop

```
Day 1:
User: "Build a banking app with login and transfers"
QUAD: *generates stories*
Memory: Stores "User built banking app, used JWT auth"

Day 7:
User: "Build another banking app"
QUAD: *remembers Day 1*
QUAD: "I see you built a banking app before. Same architecture?"
User: "Yes!"
QUAD: *auto-applies patterns from Day 1*

Day 30:
User: "Build third banking app"
QUAD: *remembers Days 1 and 7*
QUAD: "I know your banking app pattern. JWT + Spring Boot?"
User: "Yes!"
QUAD: *instantly applies proven pattern*
```

**Result:** QUAD gets faster and smarter over time.

---

## Five Context Trees

### 1. PROJECT Context (Project-Level Memory)

**Storage:** `.quad/project-memory.json` (in each project folder)

**What it remembers:**
- Tech stack decisions (Next.js, Spring Boot, PostgreSQL)
- Architecture choices (microservices vs monolith)
- API patterns (REST, GraphQL)
- Security decisions (JWT, OAuth, session-based)
- Database schema evolution
- Deployment configurations

**Example Entry:**
```json
{
  "timestamp": "2026-01-15T10:30:00",
  "decision": "Authentication",
  "value": "JWT with refresh tokens",
  "reasoning": "Better security for banking app",
  "metadata": {
    "command": "story",
    "confidence": "high"
  }
}
```

**Use Case:**
```
User runs: quad code generate

Pre-hook loads project context:
- "This project uses JWT auth"
- "Database is PostgreSQL"
- "Backend is Spring Boot"

Code generation includes:
- JWT service implementation
- PostgreSQL connection setup
- Spring Boot configuration
```

---

### 2. HEALTH Context (User-Level Memory)

**Storage:** `~/.quad/contexts/health.json` (user-global)

**What it remembers:**
- Health-related projects (fitness apps, medical records)
- Health data requirements (HIPAA compliance)
- Medical domain patterns

**Keywords that trigger:**
- health, medical, doctor, medicine, allergy, symptom, treatment
- nutrition, exercise, wellness, fitness, healthcare

**Example Entry:**
```json
{
  "timestamp": "2026-01-10T14:20:00",
  "text": "Built fitness tracking app with calorie counter",
  "metadata": {
    "domain": "health",
    "compliance": ["HIPAA"],
    "features": ["calorie_tracking", "exercise_logging"]
  }
}
```

**Use Case:**
```
User: "Build a nutrition tracking app"

Pre-hook loads health context:
- "User built fitness app before"
- "Included calorie tracking"
- "HIPAA compliance required"

Stories include:
- Calorie tracking (from past pattern)
- HIPAA compliance checks
- Exercise integration (learned pattern)
```

---

### 3. FINANCE Context (User-Level Memory)

**Storage:** `~/.quad/contexts/finance.json` (user-global)

**What it remembers:**
- Banking/fintech projects
- Payment integrations (Stripe, PayPal)
- Compliance requirements (PCI-DSS, SOX)
- Financial domain patterns

**Keywords that trigger:**
- finance, banking, payment, transaction, account, balance
- transfer, budget, investment, loan, credit, debit

**Example Entry:**
```json
{
  "timestamp": "2026-01-15T10:30:00",
  "text": "Banking app with account transfers and transaction history",
  "metadata": {
    "domain": "finance",
    "compliance": ["PCI-DSS", "SOC2"],
    "integrations": ["Plaid API"],
    "features": ["transfers", "transaction_history", "balance_check"]
  }
}
```

**Use Case:**
```
User: "Build a payment processing system"

Pre-hook loads finance context:
- "User built banking app before"
- "Used Plaid API for bank connections"
- "PCI-DSS compliance required"

Stories automatically include:
- PCI-DSS compliance checks
- Plaid integration pattern
- Transaction audit logs (learned requirement)
```

---

### 4. PREFERENCES Context (User-Level Memory)

**Storage:** `~/.quad/contexts/preferences.json` (user-global)

**What it remembers:**
- Coding style preferences
- Preferred frameworks (Spring Boot vs Node.js)
- Architecture preferences (monolith vs microservices)
- Testing preferences (Jest vs JUnit)
- Deployment preferences (AWS vs GCP vs Azure)

**Keywords that trigger:**
- prefer, like, dislike, always, never, usually
- style, convention, format, standard

**Example Entry:**
```json
{
  "timestamp": "2026-01-15T10:30:00",
  "preference_type": "framework",
  "category": "backend",
  "value": "Spring Boot",
  "frequency": 5,  // Used 5 times
  "last_used": "2026-01-15T10:30:00"
}
```

**Use Case:**
```
User: "Build a new API"

Pre-hook loads preferences:
- "User prefers Spring Boot (used 5x)"
- "Always uses PostgreSQL (used 5x)"
- "Prefers JUnit for testing (used 5x)"

QUAD auto-suggests:
- Backend: Spring Boot ← Auto-filled
- Database: PostgreSQL ← Auto-filled
- Testing: JUnit ← Auto-filled

User just confirms instead of typing!
```

---

### 5. MEMORY Context (User-Level Memory)

**Storage:** `~/.quad/contexts/memory.json` (user-global)

**What it remembers:**
- General conversations
- Project context that doesn't fit other categories
- Learning moments
- Error patterns and solutions

**Use Case:** Catch-all for everything else

**Example Entry:**
```json
{
  "timestamp": "2026-01-15T10:30:00",
  "text": "User working on MassMutual demo preparation",
  "metadata": {
    "topic": "demo",
    "client": "MassMutual"
  }
}
```

---

## Hook Architecture

### Pre-Hook: Before Command Runs

```python
def pre_hook(command, args):
    """
    Runs BEFORE command executes.
    Enriches request with historical context.
    """

    # Load relevant context
    if command == "story":
        context = load_past_stories()
        patterns = load_similar_projects()
        preferences = load_user_preferences()

        return {
            "enriched_context": {
                "past_projects": patterns,
                "preferences": preferences,
                "suggested_features": derive_from_context()
            }
        }
```

**What it does:**
1. Analyzes command and args
2. Loads relevant context from appropriate trees
3. Enriches request with historical patterns
4. Returns enriched context to command

**Example:**
```
User: quad story create

Pre-hook:
- Detects: "story" command
- Loads: Project context (tech stack)
- Loads: Finance context (if banking keywords)
- Loads: Preferences (preferred frameworks)
- Returns: Enriched context to story generator

Story generator uses enriched context:
- Auto-includes compliance features
- Follows past architectural patterns
- Uses preferred tech stack
```

---

### Post-Hook: After Command Completes

```python
def post_hook(command, args, result):
    """
    Runs AFTER command completes.
    Analyzes result and stores context.
    """

    # Analyze what happened
    analysis = analyze_result(command, args, result)

    # Extract learnings
    topics = extract_topics(analysis)
    decisions = extract_decisions(analysis)
    preferences = extract_preferences(analysis)

    # Store in appropriate context trees
    for topic in topics:
        store_context(topic, analysis)
```

**What it does:**
1. Captures command result
2. Analyzes what happened (using AI or rules)
3. Extracts topics, decisions, preferences
4. Stores in appropriate context trees

**Example:**
```
User: quad story create (completes)

Post-hook:
- Captures: 6 stories generated
- Analyzes: "Banking app with JWT auth"
- Extracts:
  - Topic: finance
  - Decision: JWT authentication
  - Preference: Spring Boot backend
- Stores:
  - Finance context: "Banking app pattern"
  - Project context: "JWT auth decision"
  - Preferences: "Spring Boot +1 usage"
```

---

## Privacy & Security

### Excluded Topics (Never Captured)

```json
{
  "exclude_topics": [
    "politics",
    "religion",
    "personal_secrets",
    "passwords",
    "api_keys",
    "private_keys",
    "credit_card_numbers",
    "social_security_numbers"
  ]
}
```

### Sensitive Data Detection

**Automatic Redaction:**
```python
sensitive_patterns = {
    "api_key": r"sk-[a-zA-Z0-9]+",
    "password": r"password\s*=\s*['\"].*['\"]",
    "credit_card": r"\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}"
}

# Before storing
text = redact_sensitive_data(text, sensitive_patterns)
```

### User Controls

```bash
# Disable specific context
quad context disable health

# Clear specific context
quad context clear finance

# View what's stored
quad context show project

# Export for review
quad context export preferences prefs.json

# Import from backup
quad context import preferences prefs.json
```

---

## Data Retention

**Default:** 365 days

**Auto-Cleanup:**
```python
def cleanup_old_entries(entries):
    """Remove entries older than retention period"""
    cutoff = datetime.now() - timedelta(days=365)
    return [e for e in entries if e['timestamp'] > cutoff]
```

**Configurable:**
```json
{
  "retention_days": 365,  // 1 year
  "auto_cleanup": true,
  "max_entries_per_context": 1000
}
```

---

## Context Usage Patterns

### Pattern 1: Tech Stack Memory

```
Project 1: Banking App
- Backend: Spring Boot
- Frontend: Next.js
- DB: PostgreSQL

Project 2: E-commerce App
- Backend: Spring Boot  ← Remembered
- Frontend: Next.js     ← Remembered
- DB: PostgreSQL        ← Remembered

Project 3: Healthcare App
- Backend: Spring Boot  ← Auto-suggested!
- Frontend: Next.js     ← Auto-suggested!
- DB: PostgreSQL        ← Auto-suggested!
```

### Pattern 2: Domain Knowledge Accumulation

```
Finance Project 1:
- Learns: Banking apps need PCI-DSS compliance

Finance Project 2:
- Applies: Auto-adds PCI-DSS stories
- Learns: Need transaction audit logs

Finance Project 3:
- Applies: PCI-DSS + audit logs
- Learns: Need fraud detection

Finance Project 4:
- Applies: All previous learnings automatically!
```

### Pattern 3: Architecture Evolution

```
Project 1: Monolith
- Learns: Simple structure, single deployment

Project 2: Monolith with issues
- Learns: Performance bottlenecks with monolith

Project 3: Microservices
- Learns: Better scalability, more complex deployment

Project 4:
- Suggests: "Try microservices? (learned from Project 3)"
```

---

## Benefits

### For Developer

1. **Faster Development**
   - No repeating same decisions
   - Auto-apply proven patterns
   - Instant project setup

2. **Consistency**
   - Same architecture across projects
   - Consistent coding style
   - Proven patterns reused

3. **Learning**
   - QUAD learns from mistakes
   - Improves suggestions over time
   - Adapts to developer's style

### For Organization

1. **Knowledge Retention**
   - Team patterns preserved
   - Architectural decisions documented
   - Compliance requirements remembered

2. **Onboarding**
   - New developers inherit team patterns
   - Consistent project structure
   - Faster ramp-up time

3. **Best Practices**
   - Successful patterns propagated
   - Failed patterns avoided
   - Continuous improvement

---

## Implementation Status

### ✅ Phase 1: Complete

- Hook infrastructure (pre_hook, post_hook, hook_manager)
- Context storage system (5 context types)
- CLI commands (list, show, enable, disable, clear, search)
- Privacy controls (exclude topics, sensitive data detection)
- Data retention (auto-cleanup after 365 days)

### ⏳ Phase 2: In Progress

- Integration with story.py
- Integration with code.py
- Integration with init.py
- Integration with test.py

### 📅 Phase 3: Planned

- AI-powered context analysis (Gemini)
- Semantic search
- Context sharing between team members
- Cloud sync across devices

---

## Next Steps

1. **Integrate hooks into commands** (story, code, init, test)
2. **Test basic flow** (capture → store → enrich)
3. **Add Gemini for smart analysis** (optional but recommended)
4. **Deploy and test** (validate in real usage)

**Timeline:** 2-4 hours for full implementation

---

## Questions for Discussion

1. **Should contexts be shareable between team members?**
   - Pro: Team knowledge sharing
   - Con: Privacy concerns

2. **Should contexts sync across devices?**
   - Pro: Seamless experience
   - Con: Requires cloud infrastructure

3. **How aggressive should auto-suggestions be?**
   - Option A: Suggest only
   - Option B: Auto-fill (with confirmation)
   - Option C: Auto-apply (silent)

4. **Should we use AI or keyword-based classification?**
   - Keywords: Fast, free, less accurate
   - AI (Gemini): Smart, free tier, more accurate

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
