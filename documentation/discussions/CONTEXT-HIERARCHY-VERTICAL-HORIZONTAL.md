# Context Hierarchy: Vertical vs Horizontal

**Date:** January 15, 2026
**Inventor:** Gopi Suman Addanke
**Status:** Patent Pending - NEW INNOVATION

---

## The Problem: Multi-Dimensional Context Management

AI assistants need to understand BOTH:
1. **Vertical hierarchy** (depth): Org → Project Group → Project → Ticket → User
2. **Horizontal switching** (breadth): Multiple projects/tickets in parallel

**Current limitation:** Existing systems only support ONE active context at a time.

**Our innovation:** Support BOTH vertical hierarchy AND horizontal switching with intelligent priority weighting.

---

## Vertical Hierarchy (Depth)

**Definition:** Nested context levels from broad to specific.

```
Organization (a2Vibes)
    │
    ├──> Project Group (SQUAD Domains)
    │       │
    │       ├──> Project (SQUAD EDU)
    │       │       │
    │       │       ├──> Ticket (SQUAD-123: "Build WhatsApp agent")
    │       │       │       │
    │       │       │       └──> User (Suman)
    │       │       │
    │       │       └──> Ticket (SQUAD-124: "Setup database")
    │       │               │
    │       │               └──> User (Suman)
    │       │
    │       └──> Project (SQUAD Health)
    │               │
    │               └──> Ticket (HEALTH-45: "Build NutriNine API")
    │                       │
    │                       └──> User (Suman)
    │
    └──> Project Group (Core Products)
            │
            └──> Project (QUAD Framework)
                    │
                    └──> Ticket (QUAD-789: "Implement hooks")
                            │
                            └──> User (Suman)
```

### Vertical Hierarchy Levels

| Level | Description | Example | Weight | Scope |
|-------|-------------|---------|--------|-------|
| **1. Organization** | Company/team | a2Vibes | 5.0 | Broadest |
| **2. Project Group** | Domain/category | SQUAD Domains, Core Products | 4.0 | Domain-level |
| **3. Project** | Specific project | SQUAD EDU, QUAD Framework | 3.0 | Project-level |
| **4. Ticket** | Specific task | SQUAD-123, QUAD-789 | 2.0 | Task-level |
| **5. User** | Individual | Suman | 1.0 | Personal |

### Vertical Priority Rule

**Context at lower level INHERITS from upper levels:**
- Working on Ticket → Has context from Project, Project Group, Org
- Working on Project → Has context from Project Group, Org
- Working on User → Has only personal context

**Example:**
```
User working on ticket SQUAD-123:
- Ticket context (SQUAD-123: "Build WhatsApp agent") - weight 2.0
- Project context (SQUAD EDU) - weight 3.0
- Project Group context (SQUAD Domains) - weight 4.0
- Org context (a2Vibes) - weight 5.0
- User context (Suman) - weight 1.0
```

---

## Horizontal Switching (Breadth)

**Definition:** Multiple contexts at the SAME level, switching between them.

### Example Scenario

User is working on **3 projects simultaneously:**

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  SQUAD EDU      │  │  QUAD Framework │  │  NutriNine      │
│  (Active)       │  │  (Paused)       │  │  (Paused)       │
│                 │  │                 │  │                 │
│  Last: 2m ago   │  │  Last: 15m ago  │  │  Last: 2h ago   │
│  Weight: 3.0    │  │  Weight: 3.0    │  │  Weight: 3.0    │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### Horizontal Priority Rules

1. **Recency weight** - More recent = higher priority
2. **Explicit activation** - User can say "switch to Project X"
3. **Time decay** - Context weight decreases over time

**Formula:**
```
Effective Weight = Base Weight × Recency Factor × Activation Boost

Recency Factor = e^(-time_since_last_activity / decay_constant)
Activation Boost = 1.5 if explicitly activated, 1.0 otherwise
```

**Example Calculation:**
```
SQUAD EDU:
- Base weight: 3.0
- Last activity: 2 minutes ago
- Recency factor: e^(-2/30) = 0.94
- Activation boost: 1.0 (not explicitly activated)
- Effective weight: 3.0 × 0.94 × 1.0 = 2.82

QUAD Framework:
- Base weight: 3.0
- Last activity: 15 minutes ago
- Recency factor: e^(-15/30) = 0.61
- Activation boost: 1.0
- Effective weight: 3.0 × 0.61 × 1.0 = 1.83

NutriNine:
- Base weight: 3.0
- Last activity: 120 minutes ago
- Recency factor: e^(-120/30) = 0.02
- Activation boost: 1.0
- Effective weight: 3.0 × 0.02 × 1.0 = 0.06

Result: SQUAD EDU has highest effective weight (2.82) → Active context
```

---

## Combined: Vertical + Horizontal Hierarchy

**Real-world scenario:**

User is Suman (a2Vibes) working on:
1. SQUAD EDU project → Ticket SQUAD-123 (active)
2. QUAD Framework project → Ticket QUAD-789 (paused 15 min ago)
3. NutriNine project → Ticket HEALTH-45 (paused 2 hours ago)

### Context Graph

```
┌─────────────────────────────────────────────────────────────┐
│  Organization: a2Vibes (weight 5.0)                         │
│  ┌──────────────────────────────────┐                       │
│  │  Project Group: SQUAD Domains    │                       │
│  │  (weight 4.0)                    │                       │
│  │  ┌──────────────────────────┐    │                       │
│  │  │  Project: SQUAD EDU      │ ←───── ACTIVE (2m ago)    │
│  │  │  (weight 3.0)            │    │   Effective: 2.82    │
│  │  │  ┌─────────────────┐     │    │                      │
│  │  │  │ Ticket: SQUAD-123│ ←──────── ACTIVE              │
│  │  │  │ (weight 2.0)    │     │    │                      │
│  │  │  │ User: Suman     │     │    │                      │
│  │  │  │ (weight 1.0)    │     │    │                      │
│  │  │  └─────────────────┘     │    │                      │
│  │  └──────────────────────────┘    │                      │
│  └──────────────────────────────────┘                       │
│                                                             │
│  ┌──────────────────────────────────┐                       │
│  │  Project Group: Core Products    │                       │
│  │  (weight 4.0)                    │                       │
│  │  ┌──────────────────────────┐    │                       │
│  │  │  Project: QUAD Framework │ ←───── PAUSED (15m ago)   │
│  │  │  (weight 3.0)            │    │   Effective: 1.83    │
│  │  │  ┌─────────────────┐     │    │                      │
│  │  │  │ Ticket: QUAD-789│     │    │                      │
│  │  │  │ (weight 2.0)    │     │    │                      │
│  │  │  └─────────────────┘     │    │                      │
│  │  └──────────────────────────┘    │                      │
│  └──────────────────────────────────┘                       │
│                                                             │
│  ┌──────────────────────────────────┐                       │
│  │  Project Group: SQUAD Domains    │                       │
│  │  (weight 4.0)                    │                       │
│  │  ┌──────────────────────────┐    │                       │
│  │  │  Project: NutriNine      │ ←───── PAUSED (2h ago)    │
│  │  │  (weight 3.0)            │    │   Effective: 0.06    │
│  │  │  ┌─────────────────┐     │    │                      │
│  │  │  │ Ticket: HEALTH-45│    │    │                      │
│  │  │  │ (weight 2.0)    │     │    │                      │
│  │  │  └─────────────────┘     │    │                      │
│  │  └──────────────────────────┘    │                      │
│  └──────────────────────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

### Current Active Context Resolution

**Step 1: Find deepest active context (vertical)**
- SQUAD-123 (ticket level) - weight 2.0
- QUAD-789 (ticket level) - weight 2.0
- HEALTH-45 (ticket level) - weight 2.0

**Step 2: Apply recency (horizontal)**
- SQUAD-123: 2.0 × 0.94 = 1.88 ✅ **HIGHEST**
- QUAD-789: 2.0 × 0.61 = 1.22
- HEALTH-45: 2.0 × 0.02 = 0.04

**Result:** Active context is **SQUAD-123** (SQUAD EDU project, SQUAD Domains group, a2Vibes org)

**Memory lookup:**
- Primary: Memories tagged with ticket SQUAD-123
- Secondary: Memories tagged with project SQUAD EDU
- Tertiary: Memories tagged with project group SQUAD Domains
- Fallback: Memories tagged with org a2Vibes
- Personal: Memories tagged with user Suman

---

## Context Switching Commands

### Vertical Switching (Change Level)

```bash
# Initialize organization
quad init org a2Vibes

# Initialize project group
quad init group "SQUAD Domains"

# Initialize project
quad init project "SQUAD EDU"

# Start ticket
quad ticket start SQUAD-123 "Build WhatsApp agent"

# Stop ticket (go back to project level)
quad ticket stop

# Stop project (go back to group level)
quad project stop

# Navigate up/down
quad context up    # Go up one level
quad context down  # Go down one level
```

### Horizontal Switching (Change Context at Same Level)

```bash
# Switch between projects (same level)
quad project switch "SQUAD EDU"
quad project switch "QUAD Framework"
quad project switch "NutriNine"

# Switch between tickets (same level)
quad ticket switch SQUAD-123
quad ticket switch QUAD-789
quad ticket switch HEALTH-45

# List active contexts at current level
quad context list

# Show context hierarchy
quad context tree
```

---

## Patent Claims

### Claim 1: Vertical Context Hierarchy

A method for managing nested context levels comprising:
- **Multi-level hierarchy** (org → group → project → ticket → user)
- **Inheritance rule** where lower levels inherit context from upper levels
- **Priority weighting** based on specificity (ticket > project > org)
- **Automatic traversal** to find deepest active context

### Claim 2: Horizontal Context Switching

A method for managing parallel contexts at same level comprising:
- **Recency-based priority** using exponential decay function
- **Explicit activation boost** when user switches manually
- **Time-based decay** reducing priority of inactive contexts
- **Effective weight calculation** combining base weight + recency + activation

### Claim 3: Combined Vertical + Horizontal Hierarchy (NOVEL!)

A method for managing multi-dimensional context comprising:
- **Vertical hierarchy** (nested levels)
- **Horizontal switching** (parallel contexts at same level)
- **Unified resolution** finding active context using both vertical depth and horizontal recency
- **Cascading memory lookup** searching from deepest to broadest level
- **Automatic context inference** detecting switches from user input

**Novel Aspect:** First system to support BOTH vertical hierarchy AND horizontal switching in AI conversation systems.

---

## Token Optimization with Multi-Dimensional Context

### Problem Without Context Hierarchy

**User working on 3 projects:**
- All memories from ALL projects sent as context EVERY TIME
- Example: 100 memories per project × 3 projects = 300 memories
- 300 memories × 100 tokens each = **30,000 tokens per request**

### Solution With Vertical Hierarchy

**Cascading memory lookup:**
1. Ticket level (most relevant): 10 memories = 1,000 tokens
2. Project level (relevant): 20 memories = 2,000 tokens
3. Project group level (context): 5 memories = 500 tokens
4. Org level (general): 2 memories = 200 tokens
5. User level (personal): 3 memories = 300 tokens

**Total: 40 memories × 100 tokens = 4,000 tokens**

**Savings: 30,000 → 4,000 = 87% reduction**

### Solution With Horizontal Switching

**Recency-based filtering:**
- Active project (2m ago): 30 memories
- Recent project (15m ago): 5 memories (only high importance)
- Old project (2h ago): 0 memories (too old, not relevant)

**Total: 35 memories × 100 tokens = 3,500 tokens**

**Savings: 30,000 → 3,500 = 88% reduction**

### Combined Optimization

**Vertical + Horizontal filtering:**
1. Find active context (SQUAD-123 ticket in SQUAD EDU project)
2. Load memories with cascading:
   - Ticket SQUAD-123: 10 memories (high relevance)
   - Project SQUAD EDU: 15 memories (medium relevance)
   - Group SQUAD Domains: 3 memories (low relevance)
   - Org a2Vibes: 1 memory (general context)
   - User Suman: 2 memories (personal)
3. Apply recency filter:
   - Recent contexts (< 30m): All memories
   - Old contexts (> 30m): Only high importance (score >= 8)

**Total: 31 memories × 100 tokens = 3,100 tokens**

**Savings: 30,000 → 3,100 = 90% reduction**

---

## Database Schema for Multi-Dimensional Context

```sql
-- Organizations table
CREATE TABLE quad_organizations (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Project groups table
CREATE TABLE quad_project_groups (
  id UUID PRIMARY KEY,
  org_id UUID REFERENCES quad_organizations(id),
  name VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Projects table (existing, add group_id)
ALTER TABLE quad_projects ADD COLUMN group_id UUID REFERENCES quad_project_groups(id);

-- Context hierarchy tracking
CREATE TABLE quad_context_hierarchy (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,

  -- Vertical hierarchy
  org_id UUID REFERENCES quad_organizations(id),
  group_id UUID REFERENCES quad_project_groups(id),
  project_id UUID,
  ticket_id UUID,

  -- Horizontal management
  context_level VARCHAR(50) NOT NULL,  -- 'org', 'group', 'project', 'ticket', 'user'
  is_active BOOLEAN DEFAULT FALSE,
  last_active_at TIMESTAMP DEFAULT NOW(),

  -- Priority weights
  base_weight DECIMAL(3,1) NOT NULL,
  recency_factor DECIMAL(5,4),
  activation_boost DECIMAL(3,1) DEFAULT 1.0,
  effective_weight DECIMAL(5,2),

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Function to calculate effective weight
CREATE OR REPLACE FUNCTION calculate_effective_weight(
  p_base_weight DECIMAL(3,1),
  p_last_active_at TIMESTAMP,
  p_activation_boost DECIMAL(3,1)
) RETURNS DECIMAL(5,2) AS $$
DECLARE
  time_diff_minutes INTEGER;
  decay_constant CONSTANT INTEGER := 30;  -- 30 minutes
  recency_factor DECIMAL(5,4);
BEGIN
  -- Calculate time difference in minutes
  time_diff_minutes := EXTRACT(EPOCH FROM (NOW() - p_last_active_at)) / 60;

  -- Calculate recency factor using exponential decay
  recency_factor := EXP(-(time_diff_minutes::DECIMAL / decay_constant));

  -- Calculate effective weight
  RETURN p_base_weight * recency_factor * p_activation_boost;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update effective weight
CREATE TRIGGER trigger_update_effective_weight
  BEFORE INSERT OR UPDATE ON quad_context_hierarchy
  FOR EACH ROW
  EXECUTE FUNCTION update_effective_weight();
```

---

## Implementation Example

```typescript
class MultiDimensionalContextDetector {
  // Find active context using vertical + horizontal resolution
  async getActiveContext(userId: string): Promise<Context> {
    // Query database for all user's contexts
    const contexts = await db.query(`
      SELECT *,
             calculate_effective_weight(base_weight, last_active_at, activation_boost) as effective_weight
      FROM quad_context_hierarchy
      WHERE user_id = $1
      ORDER BY effective_weight DESC
      LIMIT 1
    `, [userId]);

    const activeContext = contexts[0];

    // Load cascading memory
    const memories = await this.loadCascadingMemory(activeContext);

    return {
      ...activeContext,
      memories: memories
    };
  }

  // Load memories from deepest to broadest level
  async loadCascadingMemory(context: Context): Promise<Memory[]> {
    const memories: Memory[] = [];

    // 1. Ticket level (deepest, most relevant)
    if (context.ticket_id) {
      const ticketMemories = await db.query(`
        SELECT * FROM quad_hook_memories
        WHERE context_type = 'ticket' AND context_id = $1
        ORDER BY importance_score DESC
        LIMIT 10
      `, [context.ticket_id]);
      memories.push(...ticketMemories);
    }

    // 2. Project level
    if (context.project_id) {
      const projectMemories = await db.query(`
        SELECT * FROM quad_hook_memories
        WHERE context_type = 'project' AND context_id = $1
        ORDER BY importance_score DESC
        LIMIT 20
      `, [context.project_id]);
      memories.push(...projectMemories);
    }

    // 3. Project group level
    if (context.group_id) {
      const groupMemories = await db.query(`
        SELECT * FROM quad_hook_memories
        WHERE context_type = 'group' AND context_id = $1
        AND importance_score >= 7  -- Only high importance at group level
        ORDER BY importance_score DESC
        LIMIT 5
      `, [context.group_id]);
      memories.push(...groupMemories);
    }

    // 4. Org level (broadest)
    if (context.org_id) {
      const orgMemories = await db.query(`
        SELECT * FROM quad_hook_memories
        WHERE context_type = 'org' AND context_id = $1
        AND importance_score >= 8  -- Only critical at org level
        ORDER BY importance_score DESC
        LIMIT 2
      `, [context.org_id]);
      memories.push(...orgMemories);
    }

    // 5. User level (personal)
    const userMemories = await db.query(`
      SELECT * FROM quad_hook_memories
      WHERE context_type = 'user' AND context_id = $1
      AND importance_score >= 7
      ORDER BY importance_score DESC
      LIMIT 3
    `, [context.user_id]);
    memories.push(...userMemories);

    return memories;
  }
}
```

---

## Commercial Applications

1. **Enterprise AI assistants** - Multiple teams, projects, tickets in parallel
2. **Multi-tenant SaaS platforms** - Org → Customer → Project → Feature
3. **Healthcare AI** - Hospital → Department → Patient → Visit
4. **Legal AI** - Firm → Practice Area → Case → Document
5. **Financial AI** - Institution → Portfolio → Account → Transaction

---

## Conclusion

**Multi-dimensional context hierarchy (vertical + horizontal) is a NOVEL innovation that:**

1. ✅ Supports nested context levels (org → group → project → ticket → user)
2. ✅ Supports parallel contexts at same level with intelligent switching
3. ✅ Optimizes tokens by 90% through cascading memory lookup
4. ✅ Works for any AI system with hierarchical data (not just coding)

**Patent Recommendation:** File as enhancement to "Intelligent Hook System" patent OR as standalone patent on "Multi-Dimensional Context Management for AI Systems"

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
