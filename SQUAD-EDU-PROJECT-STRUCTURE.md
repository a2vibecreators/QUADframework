# SQUAD EDU - Project Structure & Management

**Date:** January 15, 2026

---

## Overview

**SQUAD EDU** is a B2B white-label education platform. We build industry-standard education PRODUCTS that ANY school/institution can license and customize with their branding.

**Business Model:** Like Shopify (for e-commerce) but for EDUCATION!

```
SQUAD EDU (Platform)
    │
    ├──> Domain Infrastructure (Shared by all products)
    │    - Multi-tenant database (edu_* tables with tenant_id)
    │    - API endpoints (/api/edu/*)
    │    - White-label system (branding, domains)
    │    - Documentation indexer
    │    - Shared utilities
    │
    └──> WHITE-LABEL PRODUCTS
         │
         ├──> SQUAD School (Product #1 - WhatsApp Learning)
         │    │
         │    ├──> Delhi Public School (Customer 1)
         │    │    "DPS Learn powered by SQUAD"
         │    │    - Android app (DPS branding)
         │    │    - iOS app (DPS branding)
         │    │    - Web: learn.dpsdelhi.com
         │    │    - WhatsApp: +91-XXX
         │    │
         │    ├──> XYZ Academy (Customer 2)
         │    │    "XYZ Academy powered by SQUAD"
         │    │    - Their apps (branded)
         │    │    - Their domain
         │    │    - Their WhatsApp
         │    │
         │    └──> 100+ more schools...
         │
         ├──> SQUAD Courses (Product #2 - Video Platform)
         │    └──> Each school gets branded Netflix-like platform
         │
         ├──> SQUAD Tutoring (Product #3 - Tutor Marketplace)
         │    └──> Each school gets branded Uber-for-tutors platform
         │
         └──> SQUAD Assessment (Product #4 - Exam & Certification)
              └──> Each school gets branded exam platform
```

**Key Point:** Each product is WHITE-LABEL. Schools get their own:
- ✅ Android app (their branding)
- ✅ iOS app (their branding)
- ✅ Web platform (their domain)
- ✅ WhatsApp number (their number)
- ✅ Look & feel (their colors/logo)
- ✅ "Powered by SQUAD" badge

---

## File Structure

```
a2vibes/
├── QUAD/                                    # QUAD Framework (Development Hub)
│   ├── documentation/                       # QUAD framework docs (indexed for RAG)
│   ├── quad-cli/                            # QUAD CLI
│   ├── vscode-plugin/                       # VS Code plugin
│   │
│   └── SQUAD-EDU/                           # 🎓 EDUCATION DOMAIN
│       │
│       ├── DOMAIN-INFRASTRUCTURE/           # Shared by all SQUAD EDU apps
│       │   │
│       │   ├── database/                    # Database schema & migrations
│       │   │   ├── migrations/
│       │   │   │   └── 001_create_edu_tables.sql
│       │   │   ├── schema.md                # Schema documentation
│       │   │   └── seed_data.sql            # Initial data (90 lessons)
│       │   │
│       │   ├── api/                         # SQUAD EDU API endpoints
│       │   │   ├── edu-routes.ts            # /api/edu/* endpoints
│       │   │   ├── controllers/
│       │   │   │   ├── user.controller.ts
│       │   │   │   ├── lesson.controller.ts
│       │   │   │   ├── question.controller.ts
│       │   │   │   ├── quiz.controller.ts
│       │   │   │   └── mastery.controller.ts
│       │   │   ├── services/
│       │   │   │   ├── rag.service.ts       # PostgreSQL full-text search
│       │   │   │   ├── mastery.service.ts   # Weak topic detection
│       │   │   │   └── gamification.service.ts
│       │   │   └── types/
│       │   │       └── edu.types.ts
│       │   │
│       │   ├── indexer/                     # Documentation indexer (Python)
│       │   │   ├── index_docs.py            # QUAD docs → edu_documentation table
│       │   │   ├── requirements.txt
│       │   │   └── config.py
│       │   │
│       │   └── shared/                      # Shared utilities
│       │       ├── question-detector.ts     # Detect if text is question
│       │       ├── topic-classifier.ts      # Classify question topic
│       │       └── streak-calculator.ts     # Calculate streaks
│       │
│       ├── squad-school/                    # 📱 FIRST APP: WhatsApp Learning
│       │   │
│       │   ├── whatsapp-agent/              # WhatsApp polling agent
│       │   │   ├── agent.py                 # Main polling loop
│       │   │   ├── whatsapp_client.py       # Meta API client
│       │   │   ├── message_handler.py       # Route messages
│       │   │   ├── registration_flow.py     # Multi-step registration
│       │   │   ├── requirements.txt
│       │   │   ├── .env.example
│       │   │   └── README.md
│       │   │
│       │   ├── curriculum/                  # 90-day curriculum content
│       │   │   ├── CURRICULUM.md            # Overview
│       │   │   │
│       │   │   ├── beginner/                # Beginner track
│       │   │   │   ├── week_1/
│       │   │   │   │   ├── day_1.md
│       │   │   │   │   ├── day_2.md
│       │   │   │   │   └── ...
│       │   │   │   ├── week_2/
│       │   │   │   └── ...
│       │   │   │
│       │   │   ├── intermediate/            # Intermediate track
│       │   │   │   ├── week_1/
│       │   │   │   └── ...
│       │   │   │
│       │   │   └── advanced/                # Advanced track
│       │   │       ├── week_1/
│       │   │       └── ...
│       │   │
│       │   ├── tests/                       # SQUAD School tests
│       │   │   ├── test_whatsapp_agent.py
│       │   │   └── test_registration.py
│       │   │
│       │   └── README.md                    # SQUAD School documentation
│       │
│       ├── squad-courses/                   # 🎥 FUTURE APP: Video Courses
│       │   └── (future)
│       │
│       ├── squad-tutoring/                  # 👨‍🏫 FUTURE APP: Live Tutoring
│       │   └── (future)
│       │
│       ├── DOCUMENTATION/                   # SQUAD EDU domain docs
│       │   ├── SQUAD-EDU-VISION.md
│       │   ├── SQUAD-EDU-SPEC.md
│       │   ├── API.md                       # API documentation
│       │   ├── DATABASE.md                  # Database schema docs
│       │   └── PROJECT-STRUCTURE.md         # This file
│       │
│       └── README.md                        # SQUAD EDU overview
│
└── quad-suma-api/                           # QUAD API (serves all domains)
    └── src/
        └── api/
            ├── edu.ts                        # → SQUAD-EDU/DOMAIN-INFRASTRUCTURE/api/
            ├── sdlc.ts                       # SQUAD SDLC endpoints
            └── health.ts                     # SQUAD Health endpoints (future)
```

---

## Multi-Tenant Architecture

### Database Design

All `edu_*` tables include `tenant_id` to separate data by school:

```sql
-- Tenants table (one per school)
CREATE TABLE edu_tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE,  -- learn.dpsdelhi.com
    whatsapp_number VARCHAR(20),
    branding JSONB,  -- {logo, colors, fonts}
    features JSONB,  -- {whatsapp_bot: true, live_classes: true}
    subscription_plan VARCHAR(50),  -- starter, pro, enterprise
    created_at TIMESTAMP DEFAULT NOW()
);

-- Users table (with tenant_id)
CREATE TABLE edu_users (
    phone_number VARCHAR(20),
    tenant_id UUID NOT NULL REFERENCES edu_tenants(id),
    name VARCHAR(255) NOT NULL,
    skill_level VARCHAR(50) DEFAULT 'beginner',
    current_day INTEGER DEFAULT 0,
    streak_days INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),

    PRIMARY KEY (phone_number, tenant_id)  -- Composite key
);

-- All other tables follow same pattern
CREATE TABLE edu_lesson_progress (
    id SERIAL PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES edu_tenants(id),
    user_phone VARCHAR(20),
    day INTEGER NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    ...
    FOREIGN KEY (user_phone, tenant_id) REFERENCES edu_users(phone_number, tenant_id)
);
```

**Benefits:**
- One database for all schools (cost-efficient)
- Complete data isolation (DPS can't see XYZ Academy data)
- Easy to migrate to dedicated DB later (for enterprise customers)

---

## How It Works

### 1. Domain Infrastructure (Shared)

**All SQUAD EDU products** share the infrastructure, but each CUSTOMER (school) gets isolated data via `tenant_id`:

**Shared Infrastructure:**
- ✅ Same database (`edu_*` tables with `tenant_id`)
- ✅ Same API endpoints (`/api/edu/*`)
- ✅ Same codebase
- ✅ Same features

**Isolated by Tenant:**
- ✅ DPS students can't see XYZ Academy students
- ✅ Each school has own branding
- ✅ Each school has own domain
- ✅ Each school has own WhatsApp number

**Example: Student Journey (Within One School)**
- Student enrolls at **Delhi Public School**
- Learns on **SQUAD School** (WhatsApp) via +91-XXX-XXX-XXXX
- Progress tracked in `edu_lesson_progress` with `tenant_id = 'dps-delhi'`
- Later enrolls in **SQUAD Courses** (video platform) at learn.dpsdelhi.com
- Same user account, same tenant!
- Takes **SQUAD Assessment** exam
- Tutor sees their weak topics via **SQUAD Tutoring**
- **All within DPS ecosystem!**

### 2. White-Label Products (squad-school, squad-courses, etc.)

Each product is a template that can be customized per customer:

**Product = Template:**
- Base codebase (Android, iOS, Web)
- Core features
- Standard curriculum (for SQUAD School)

**Customer = Branded Instance:**
- Delhi Public School gets:
  - Android app: "DPS Learn" (Play Store)
  - iOS app: "DPS Learn" (App Store)
  - Web: learn.dpsdelhi.com
  - WhatsApp: +91-11-XXXX-XXXX
  - DPS colors (blue/white)
  - DPS logo
  - Custom curriculum (base + DPS additions)

**Customization by:**
- QUAD developers (we charge $10K-$50K)
- Third-party certified developers (they keep 80%, we get 20%)

---

## Development Workflow

### Phase 1: Build Domain Infrastructure (FIRST!)

**Location:** `QUAD/SQUAD-EDU/DOMAIN-INFRASTRUCTURE/`

**Tasks:**
1. **Database Schema**
   ```bash
   cd QUAD/SQUAD-EDU/DOMAIN-INFRASTRUCTURE/database/
   # Create 001_create_edu_tables.sql migration
   # Run migration on QUAD database
   psql quad_db < migrations/001_create_edu_tables.sql
   ```

2. **API Endpoints**
   ```bash
   cd QUAD/SQUAD-EDU/DOMAIN-INFRASTRUCTURE/api/
   # Implement 6 endpoints in edu-routes.ts
   # Copy to quad-suma-api/src/api/edu.ts
   ```

3. **Documentation Indexer**
   ```bash
   cd QUAD/SQUAD-EDU/DOMAIN-INFRASTRUCTURE/indexer/
   # Create Python script to index QUAD docs
   python index_docs.py
   ```

4. **Test Domain Infrastructure**
   ```bash
   # Test API endpoints with Postman/curl
   curl -X POST http://localhost:3201/api/edu/register \
     -H "Content-Type: application/json" \
     -d '{"phone": "+1234567890", "name": "Test User"}'
   ```

### Phase 2: Build SQUAD School (First App)

**Location:** `QUAD/SQUAD-EDU/squad-school/`

**Tasks:**
1. **WhatsApp Agent**
   ```bash
   cd QUAD/SQUAD-EDU/squad-school/whatsapp-agent/
   # Implement polling agent
   python agent.py
   ```

2. **Write Curriculum**
   ```bash
   cd QUAD/SQUAD-EDU/squad-school/curriculum/beginner/week_1/
   # Write day_1.md through day_7.md
   ```

3. **Test End-to-End**
   ```bash
   # Send WhatsApp message to +17322309573
   # Verify registration works
   # Verify Q&A works
   # Verify progress tracking works
   ```

### Phase 3: Launch Beta

1. Recruit 10-20 testers
2. Manual daily lesson broadcasts
3. Automated Q&A 24/7
4. Gather feedback

### Phase 4: Build More Apps (Future)

Repeat pattern:
- Create `squad-courses/` directory
- Build web app that calls `/api/edu/*` endpoints
- Same user data, same progress tracking!

---

## Git Management

### Branch Strategy

```bash
# Main branch (stable)
main

# Feature branches (one per component)
feature/edu-database-schema
feature/edu-api-endpoints
feature/edu-documentation-indexer
feature/squad-school-whatsapp-agent
feature/squad-school-curriculum-week1
```

### Commit Pattern

```bash
# Domain infrastructure commits
git commit -m "feat(edu): Add edu_* database tables"
git commit -m "feat(edu-api): Implement /api/edu/register endpoint"
git commit -m "feat(edu-rag): Add PostgreSQL full-text search"

# SQUAD School commits
git commit -m "feat(squad-school): Add WhatsApp polling agent"
git commit -m "content(squad-school): Add Week 1 beginner curriculum"
```

---

## Checklist (Check In/Check Out System)

### Domain Infrastructure Checklist

**Database:**
- [ ] Create 7 `edu_*` tables
- [ ] Add triggers for mastery calculation
- [ ] Add full-text search index
- [ ] Seed with 90 lesson metadata
- [ ] Test with sample data

**API:**
- [ ] Implement `/api/edu/register`
- [ ] Implement `/api/edu/user/:phone`
- [ ] Implement `/api/edu/question` (RAG)
- [ ] Implement `/api/edu/progress/:phone`
- [ ] Implement `/api/edu/weak-topics/:phone`
- [ ] Implement `/api/edu/quiz`
- [ ] Test all endpoints with Postman
- [ ] Deploy to quad-suma-api repository

**Indexer:**
- [ ] Parse QUAD markdown files
- [ ] Insert into `edu_documentation` table
- [ ] Test full-text search queries
- [ ] Schedule daily sync

**Shared Utilities:**
- [ ] Question detector (regex)
- [ ] Topic classifier (AI-based)
- [ ] Streak calculator
- [ ] Achievement unlock logic

### SQUAD School Checklist

**WhatsApp Agent:**
- [ ] Polling loop (30 seconds)
- [ ] Message handler (route START, questions, etc.)
- [ ] Registration flow (multi-step)
- [ ] Question detection
- [ ] Send replies via WhatsApp API
- [ ] Error handling
- [ ] Logging

**Curriculum:**
- [ ] Write Week 1 (beginner) - 7 lessons
- [ ] Write Week 2 (beginner) - 7 lessons
- [ ] Design quiz questions for each day
- [ ] Test lesson delivery via WhatsApp

**Testing:**
- [ ] Unit tests for agent
- [ ] Integration tests with API
- [ ] End-to-end test with real WhatsApp

**Documentation:**
- [ ] Meta WhatsApp API setup guide
- [ ] Agent deployment instructions
- [ ] Beta testing process

---

## Skill Level Tracks (Answering Your Question!)

### How It Works

1. **User Registration:**
   ```
   Bot: "Welcome! What's your coding experience?"
   Options:
   1️⃣ Beginner (Never coded before)
   2️⃣ Intermediate (Know basics, want to level up)
   3️⃣ Advanced (Experienced, want mastery)
   ```

2. **Stored in Database:**
   ```sql
   INSERT INTO edu_users (phone_number, name, skill_level)
   VALUES ('+1234567890', 'Pradeep', 'beginner');
   ```

3. **Curriculum Selection:**
   ```python
   # In WhatsApp agent
   user = get_user(phone_number)

   if user.skill_level == 'beginner':
       curriculum_path = 'curriculum/beginner/week_1/day_1.md'
   elif user.skill_level == 'intermediate':
       curriculum_path = 'curriculum/intermediate/week_1/day_1.md'
   else:
       curriculum_path = 'curriculum/advanced/week_1/day_1.md'
   ```

### Curriculum Structure

**Beginner (90 days - Zero to Job Ready):**
- Week 1-4: Fundamentals (variables, loops, functions)
- Week 5-8: Web basics (HTML, CSS, JavaScript)
- Week 9-12: Backend basics (Node.js, databases)
- Week 13+: Projects + job prep

**Intermediate (60 days - Basics to Advanced):**
- Week 1-2: Quick fundamentals review
- Week 3-6: Modern frameworks (React, Next.js)
- Week 7-8: Advanced backend (APIs, auth)
- Week 9+: Complex projects

**Advanced (30 days - Mastery Track):**
- Week 1: Architecture patterns
- Week 2: Performance optimization
- Week 3: System design
- Week 4+: Real-world production projects

**Each track adapts based on user's mastery percentage!**

If beginner struggles with loops (< 70%), system sends:
- Extra practice questions
- Different analogies
- Mini review lessons

---

## Deployment Strategy

### Phase 1: Local Development (MVP)
- Run everything locally
- PostgreSQL on localhost
- SQUAD School agent on laptop
- 100% FREE

### Phase 2: Beta Testing (10-20 users)
- Deploy QUAD API to VPS ($10/month)
- Run SQUAD School agent on VPS
- PostgreSQL on same VPS

### Phase 3: Public Launch (100+ users)
- Scale API to dedicated server
- Separate database server
- Consider managed PostgreSQL (Neon, Supabase)

### Phase 4: Scale (1000+ users)
- Load balancer
- Multiple API instances
- CDN for content
- Redis for caching

---

## Success Metrics

### Domain Infrastructure
- [ ] All 7 tables created and working
- [ ] All 6 API endpoints functional
- [ ] RAG returning accurate answers (>80%)
- [ ] Weak topic detection working (< 70% threshold)
- [ ] Response time < 500ms

### SQUAD School
- [ ] 10-20 beta testers recruited
- [ ] Daily lesson delivery at 9 AM
- [ ] Q&A response time < 2 minutes
- [ ] 80% completion rate for Week 1
- [ ] 90% user satisfaction

---

## Next Steps (In Order!)

1. ✅ Domain infrastructure → Database schema
2. ✅ Domain infrastructure → API endpoints
3. ✅ Domain infrastructure → Documentation indexer
4. → SQUAD School → WhatsApp agent
5. → SQUAD School → Week 1 curriculum (beginner)
6. → SQUAD School → Beta testing
7. → SQUAD School → Launch

---

**Ready to build SQUAD EDU domain with SQUAD School as the first killer app?**

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
