# SUMA Scaling Strategy: From MVP to Enterprise

**Date:** January 15, 2026
**Purpose:** Plan database architecture evolution as SUMA grows

---

## The Scaling Wall: Single Database Limitations

### Phase 1: Single Database with RLS (0-10K Users) ✅ CURRENT

**Architecture:**
```
One PostgreSQL database
All users' data in same tables
Row-Level Security enforces isolation
```

**Works great until:**
- **5K users:** Still fine
- **10K users:** Starting to feel it
- **50K users:** BREAKING POINT (see cons below)

---

## Performance Cons at Scale (50K+ Users)

| Issue | Symptoms | When It Breaks |
|-------|----------|-----------------|
| **Query Overhead** | `SELECT * FROM devices WHERE org_id = X` now scans 5M rows to find 10 | 20K+ users |
| **RLS Complexity** | Adding WHERE clauses to every query adds 5-20% latency | 50K users |
| **Lock Contention** | One user's command blocks others' queries | 100K+ concurrent users |
| **Backup Size** | 500GB database takes 4+ hours to backup | 500K+ users |
| **Restore Time** | If database crashes, recovery takes 6+ hours | 1M+ rows |
| **Indexing Hell** | Need 50+ indexes to cover all queries | 100K+ users |
| **Memory Usage** | PostgreSQL cache thrashing, constant disk I/O | 500K+ users |
| **Connection Pooling** | 10K connection requests saturate pool | 100K concurrent |

---

## Real-World Numbers: SOMA Current vs Scale

```
TODAY (Single DB + RLS):
├─ Users: You + 10 friends = 11 users ✅
├─ Devices: ~5 devices
├─ Queries/second: ~2 req/sec
├─ Database size: 100MB
├─ Backup time: 10 seconds
├─ Query latency: 5-10ms
└─ Cost: $5/month

YEAR 1 (Popular in community):
├─ Users: 5,000 users
├─ Devices: 50,000 devices
├─ Queries/second: ~500 req/sec
├─ Database size: 50GB
├─ Backup time: 30 minutes
├─ Query latency: 50-100ms (degraded)
├─ Cost: $50/month
└─ Status: Still works but slow

YEAR 2 (Network effect kicks in):
├─ Users: 50,000 users ⚠️ SCALING WALL
├─ Devices: 500,000 devices
├─ Queries/second: ~5,000 req/sec
├─ Database size: 500GB
├─ Backup time: 4+ hours (risky)
├─ Query latency: 200-500ms (users complain)
├─ Cost: $300+/month
├─ Status: NEEDS MIGRATION
└─ Action: Migrate to Phase 2

YEAR 3 (Enterprise):
├─ Users: 500,000 users
├─ Devices: 5,000,000 devices
├─ Queries/second: ~50,000 req/sec
├─ Database size: 5TB
├─ Backup time: 24+ hours (impossible)
├─ Query latency: 2+ seconds (broken)
├─ Cost: $5,000+/month
├─ Status: BROKEN - Full migration needed
└─ Action: Move to Phase 3 (multi-database)
```

---

## Scaling Ladder: 4 Phases

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  PHASE 4: Multi-Region Enterprise                       │
│  (1M+ users)                                             │
│  ├─ Database per organization                           │
│  ├─ Sharded by region (US, EU, APAC)                    │
│  ├─ Geo-replicated backups                              │
│  ├─ CDN for reads                                       │
│  └─ Cost: $50K+/month                                   │
│                                                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  PHASE 3: Multi-Database + Sharding                     │
│  (100K-1M users)                                         │
│  ├─ Shard by organization_id (1-50 databases)           │
│  ├─ Each shard handles 10-20K users                     │
│  ├─ Consistent hashing for routing                      │
│  ├─ Independent backups per shard                       │
│  └─ Cost: $10K-50K/month                                │
│                                                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  PHASE 2: Schema-per-Organization                       │
│  (10K-100K users)                                        │
│  ├─ Same database, separate schemas                     │
│  ├─ Org A: SCHEMA org_abc                               │
│  ├─ Org B: SCHEMA org_xyz                               │
│  ├─ RLS removed (schema isolation)                      │
│  ├─ Faster queries (no RLS overhead)                    │
│  └─ Cost: $500-5K/month                                 │
│                                                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  PHASE 1: Single Database + RLS (YOU ARE HERE)          │
│  (0-10K users)                                           │
│  ├─ One database, all users                             │
│  ├─ Row-Level Security isolation                        │
│  ├─ Simple deployment                                   │
│  ├─ Perfect for MVP                                     │
│  └─ Cost: $5-100/month                                  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## PHASE 1 → PHASE 2 Migration (10K Users)

### When to Migrate

**Trigger:** When you have 10K+ users AND experiencing ANY of:
- Query latency > 100ms
- CPU usage > 80% on database
- Monthly AWS/GCP bill > $200
- Backup time > 1 hour

### Migration Plan (Zero Downtime)

```
BEFORE (All in one database):
┌──────────────────────────────────────────┐
│  Database: quad_suma                     │
├──────────────────────────────────────────┤
│  Table: users                            │
│  Table: devices (org_abc + org_xyz data) │
│  Table: constraints (all orgs)           │
│  Table: command_history (all orgs)       │
└──────────────────────────────────────────┘

AFTER (Schema per organization):
┌──────────────────────────────────────────┐
│  Database: quad_suma                     │
├──────────────────────────────────────────┤
│  Schema: org_abc                         │
│  ├─ devices (org_abc only)               │
│  ├─ constraints (org_abc only)           │
│  └─ command_history (org_abc only)       │
│                                          │
│  Schema: org_xyz                         │
│  ├─ devices (org_xyz only)               │
│  ├─ constraints (org_xyz only)           │
│  └─ command_history (org_xyz only)       │
│                                          │
│  Schema: shared                          │
│  └─ users (all orgs)                     │
└──────────────────────────────────────────┘
```

### Step-by-Step Migration Process

```bash
STEP 1: Plan (1 week before migration)
─────────────────────────────────────
- Identify all organizations
- Create migration mapping document
- Plan rollback procedure
- Get stakeholder approval

STEP 2: Create new schemas (offline testing)
───────────────────────────────────────────
# Create schema for each org
CREATE SCHEMA org_abc;
CREATE SCHEMA org_xyz;
CREATE SCHEMA shared;

# Create tables in schemas (use migrations)
psql < migrations/create_schemas.sql

STEP 3: Copy data (read-only mode)
──────────────────────────────────
# Put old database in read-only
ALTER DATABASE quad_suma SET default_transaction_read_only = on;

# Copy org_abc data
INSERT INTO org_abc.devices
SELECT * FROM public.devices WHERE organization_id = 'org_abc_uuid';

# Verify row counts match
SELECT COUNT(*) FROM public.devices WHERE organization_id = 'org_abc_uuid';
SELECT COUNT(*) FROM org_abc.devices;

STEP 4: Dual-write (code change)
────────────────────────────────
# Update API to write to BOTH old + new locations
# New devices go to: org_abc.devices (schema)
# BUT ALSO read from: shared.users (cross-schema)

STEP 5: Switch reads (3 hours window)
────────────────────────────────────
# Update API config:
# FROM: SELECT * FROM public.devices WHERE org_id = X
# TO:   SELECT * FROM org_X.devices

# Monitor error logs during switch

STEP 6: Cleanup (after 1 week stable)
────────────────────────────────────
# Remove old tables from public schema
DROP TABLE public.devices CASCADE;

# Restore write permissions
ALTER DATABASE quad_suma SET default_transaction_read_only = off;

RESULT:
✅ Zero downtime migration
✅ Easy rollback if issues
✅ Data completely isolated by schema
✅ Faster queries (no RLS overhead)
✅ Can add more organizations easily
```

### Code Changes for Schema-per-Org

```typescript
// BEFORE (Phase 1)
const query = `
  SELECT * FROM devices
  WHERE organization_id = $1
`;

// AFTER (Phase 2)
const schemaName = `org_${organizationId}`;
const query = `
  SELECT * FROM ${schemaName}.devices
`;

// OR use function
function getOrgSchema(orgId: string): string {
  const mapping = {
    'org_abc': 'org_abc',
    'org_xyz': 'org_xyz'
  };
  return mapping[orgId] || 'shared';
}

const query = `
  SELECT * FROM ${getOrgSchema(orgId)}.devices
`;
```

---

## PHASE 2 → PHASE 3 Migration (100K Users)

### When to Migrate

**Trigger:** When you have 100K+ users AND:
- Single database approaching 1TB
- Backup time > 4 hours
- Query latency > 200ms
- Monthly bill > $5,000

### Migration Plan (Sharding)

```
BEFORE (Schema per org, single database):
┌─────────────────────────────────────────┐
│  Database 1: quad_suma                  │
│  ├─ Schema: org_abc                     │
│  ├─ Schema: org_xyz                     │
│  ├─ Schema: org_pqr                     │
│  └─ ... (50 orgs, 1TB total)            │
└─────────────────────────────────────────┘

AFTER (Distributed shards):
┌─────────────────────┐  ┌─────────────────────┐
│  Shard 1 (US-EAST)  │  │  Shard 2 (US-WEST)  │
├─────────────────────┤  ├─────────────────────┤
│ org_abc             │  │ org_xyz             │
│ org_def             │  │ org_pqr             │
│ org_ghi             │  │ org_stu             │
│ org_jkl             │  │ ...                 │
│ ...                 │  │                     │
│ (10K users)         │  │ (10K users)         │
└─────────────────────┘  └─────────────────────┘

┌─────────────────────┐  ┌─────────────────────┐
│  Shard 3 (EU)       │  │  Shard 4 (APAC)     │
├─────────────────────┤  ├─────────────────────┤
│ org_vwx             │  │ org_yza             │
│ org_bcd             │  │ org_efg             │
│ ...                 │  │ ...                 │
│ (10K users)         │  │ (10K users)         │
└─────────────────────┘  └─────────────────────┘
```

### Sharding Strategy (Consistent Hashing)

```typescript
// Map organization to shard
function getShardForOrganization(orgId: string): string {
  const hash = hashCode(orgId);
  const shardIndex = hash % SHARD_COUNT;  // SHARD_COUNT = 4

  const shards = [
    'postgres://shard1.gcp.com/quad_suma_1',
    'postgres://shard2.gcp.com/quad_suma_2',
    'postgres://shard3.gcp.com/quad_suma_3',
    'postgres://shard4.gcp.com/quad_suma_4'
  ];

  return shards[shardIndex];
}

// Usage in API
const connectionString = getShardForOrganization(orgId);
const connection = await createConnection(connectionString);
const devices = await connection.query('SELECT * FROM org_${orgId}.devices');
```

### Backup Strategy per Shard

```
Shard 1 (100GB) → Backup in 5 minutes
Shard 2 (100GB) → Backup in 5 minutes
Shard 3 (100GB) → Backup in 5 minutes
Shard 4 (100GB) → Backup in 5 minutes
────────────────
Total: 4x parallel backups = 5 minutes (vs 60 minutes for 400GB)
```

---

## PHASE 3 → PHASE 4 Migration (1M+ Users)

### When to Migrate

**Trigger:** When you have 1M+ users AND need:
- Data residency (data must stay in specific countries)
- Sub-100ms latency globally
- 99.99% uptime requirement
- Compliance (GDPR, CCPA)

### Architecture

```
┌──────────────────────────────────────────────────┐
│          Global Router (Edge Function)            │
│  Detects user location, routes to nearest region │
└──────────────┬───────────────────────────────────┘
               │
     ┌─────────┼─────────┬─────────┐
     │         │         │         │
     ▼         ▼         ▼         ▼
┌─────────┐ ┌──────┐ ┌──────┐ ┌──────┐
│ US EAST │ │US W. │ │ EU   │ │APAC  │
├─────────┤ ├──────┤ ├──────┤ ├──────┤
│Shard 1a │ │Shard │ │Shard │ │Shard │
│Shard 1b │ │2a/2b │ │3a/3b │ │4a/4b │
│Replica  │ │Rep.  │ │Rep.  │ │Rep.  │
└─────────┘ └──────┘ └──────┘ └──────┘
│
├─ Users in US automatically route to US EAST shard
├─ Users in EU automatically route to EU shard
├─ Each region has read replicas for failover
└─ Data stays in region (compliance)
```

---

## Growth Checklist: When to Migrate

### PHASE 1 → PHASE 2 Trigger

```
✅ When ANY of these happen:
   □ Users > 10,000
   □ Database > 200GB
   □ Queries > 1,000/sec
   □ Backup time > 1 hour
   □ Query latency > 100ms
   □ Database CPU > 80%
   □ Monthly database cost > $200

Timeline: Migration takes 1 week, plan 2 weeks before trigger
```

### PHASE 2 → PHASE 3 Trigger

```
✅ When ANY of these happen:
   □ Users > 100,000
   □ Database > 1TB
   □ Queries > 10,000/sec
   □ Backup time > 4 hours
   □ Query latency > 200ms
   □ Database CPU > 90%
   □ Monthly database cost > $5,000

Timeline: Migration takes 2-3 weeks, plan 1 month before
```

### PHASE 3 → PHASE 4 Trigger

```
✅ When ANY of these happen:
   □ Users > 1,000,000
   □ Queries > 100,000/sec
   □ Need 99.99% uptime SLA
   □ Data residency required (GDPR)
   □ Monthly database cost > $50,000

Timeline: Migration takes 1-2 months, hire scaling consultant
```

---

## Cost Analysis: All Phases

```
PHASE 1 (Single DB, 0-10K users):
├─ Database: $5-100/month
├─ Storage: $50/month
├─ Backup: $10/month
├─ CDN: $0 (not needed yet)
└─ TOTAL: $65-160/month

PHASE 2 (Schema-per-org, 10K-100K users):
├─ Database: $200-500/month (larger instance)
├─ Storage: $200/month
├─ Backup: $50/month
├─ CDN: $50/month
├─ Migration effort: $10K (engineer time)
└─ TOTAL: $510-800/month + $10K one-time

PHASE 3 (Sharded, 100K-1M users):
├─ Database (4 shards × $500): $2,000/month
├─ Storage (4 shards): $400/month
├─ Backup: $200/month
├─ CDN: $200/month
├─ Monitoring/alerting: $100/month
├─ Migration effort: $50K (bigger project)
└─ TOTAL: $2,900/month + $50K one-time

PHASE 4 (Multi-region, 1M+ users):
├─ Database: $10K-50K/month
├─ Storage: $2K+/month
├─ Backup/DR: $1K+/month
├─ CDN (global): $5K+/month
├─ Monitoring/SRE: $5K+/month
└─ TOTAL: $23K-63K+/month
```

---

## Monitoring: Know When You're Hitting Limits

```typescript
// Add these metrics to track
class DatabaseMetrics {
  private metrics = {
    queryLatency: [],      // p95 latency
    connPoolUsage: 0,      // % of connections used
    diskSpace: 0,          // GB used
    backupTime: 0,         // minutes
    cpuUsage: 0,           // % CPU
    activeTransactions: 0, // number
    slowQueryCount: 0      // > 100ms
  };

  startMonitoring() {
    setInterval(async () => {
      this.metrics.queryLatency.push(await this.getP95Latency());
      this.metrics.cpuUsage = await this.getDBCPU();
      this.metrics.connPoolUsage = await this.getConnPoolUsage();

      // Alert if approaching limits
      if (this.metrics.cpuUsage > 80) {
        this.alert('HIGH CPU - Consider migration to Phase 2');
      }
      if (this.metrics.queryLatency.at(-1) > 100) {
        this.alert('SLOW QUERIES - RLS overhead increasing');
      }
      if (this.metrics.connPoolUsage > 90) {
        this.alert('CONNECTION POOL EXHAUSTED - Need sharding');
      }
    }, 60000);
  }
}
```

---

## Summary: Your Scaling Path

```
TODAY (Week 1):
└─ PHASE 1: Single DB + RLS
   └─ You + 10 friends testing
   └─ Perfect MVP setup
   └─ Zero scaling worries

NEXT 6 MONTHS:
└─ Still PHASE 1
└─ Community grows to 1K users
└─ Performance still great
└─ Cost: ~$100/month

YEAR 1 (10K users):
└─ PHASE 1 → PHASE 2 Migration
└─ Schema-per-organization
└─ 1 week migration window
└─ Cost: $500/month

YEAR 2 (100K users):
└─ PHASE 2 → PHASE 3 Migration
└─ Distributed sharding
└─ 2-3 week migration
└─ Cost: $3K/month

YEAR 3 (1M+ users):
└─ PHASE 3 → PHASE 4 Migration
└─ Multi-region, global deployment
└─ Hire scaling consultant
└─ Cost: $30K+/month

IMPORTANT: You don't need to plan this now!
Start PHASE 1, when you hit limits, execute migration.
```

---

## Decision Matrix: Which Phase?

```
Users   | Phase | Strategy | Cost | Action
────────┼───────┼──────────┼──────┼────────────────────
<10K    | 1     | RLS      | $100 | Go build!
10K-50K | 1→2   | Monitor  | $200 | Plan migration
50K-100K| 2     | Schema   | $500 | Execute migration
100K+   | 2→3   | Shard    | $3K+ | Timeline: 2-3 weeks
1M+     | 3→4   | Global   | $30K+| Hire consultant
```

---

## What You Should Do NOW

✅ **Start with PHASE 1 (Single DB + RLS)**
- It's perfect for your MVP
- Scales to 10K+ users
- Migration is well-defined when needed
- Cost is minimal ($5-100/month)

✅ **Add monitoring from day 1**
- Track query latency
- Track database CPU
- Track connection pool usage
- Know exactly when to migrate

✅ **Don't pre-optimize**
- Don't build for 1M users when you have 11
- Follow this migration path when needed
- Each phase buys you time

✅ **Plan migration 1 month ahead**
- When you hit trigger, you have time
- No emergency rewrites needed
- Migrations are designed to have zero downtime

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
