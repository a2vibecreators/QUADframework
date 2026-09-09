# QUAD Documentation Standards

**Version:** 1.0
**Last Updated:** January 15, 2026
**Status:** Draft

---

## Overview

QUAD generates industry-standard documentation automatically using the `quad doc` command. This document defines:
1. Standard documentation structure
2. Template system (QUAD defaults + org overrides)
3. Test journey format
4. Generation rules

---

## quad doc Command

### Commands

```bash
# Initialize documentation structure
quad doc init

# Generate specific docs
quad doc generate api           # API documentation
quad doc generate db            # Database documentation
quad doc generate arch          # Architecture documentation
quad doc generate journey       # Test journeys

# Generate all
quad doc generate all

# Update existing docs
quad doc update

# Validate documentation
quad doc validate

# Export
quad doc export --format pdf
quad doc export --format html
```

---

## Standard Documentation Structure

Every QUAD project has this structure:

```
<project-root>/
├── README.md                           # Project overview
├── CLAUDE.md                           # AI context
├── .quad/
│   └── config.json                     # Project config
└── documentation/
    ├── README.md                       # Documentation index
    ├── architecture/
    │   ├── README.md                   # Architecture overview
    │   ├── SYSTEM-ARCHITECTURE.md      # High-level design
    │   ├── diagrams/
    │   │   ├── system-context.png
    │   │   ├── component-diagram.png
    │   │   └── deployment-diagram.png
    │   └── decisions/
    │       ├── 001-use-spring-boot.md
    │       ├── 002-use-postgresql.md
    │       └── 003-use-jwt.md
    ├── api/
    │   ├── README.md                   # API overview
    │   ├── API-REFERENCE.md            # Complete API reference
    │   ├── endpoints/
    │   │   ├── auth.md                 # Auth endpoints
    │   │   ├── accounts.md             # Account endpoints
    │   │   └── transactions.md         # Transaction endpoints
    │   ├── schemas/
    │   │   ├── user.json
    │   │   ├── account.json
    │   │   └── transaction.json
    │   └── swagger.yaml                # OpenAPI 3.0 spec
    ├── database/
    │   ├── README.md                   # Database overview
    │   ├── SCHEMA.md                   # Complete schema
    │   ├── schema.sql                  # Full DDL
    │   ├── erd.png                     # Entity relationship diagram
    │   └── tables/
    │       ├── users.md
    │       ├── accounts.md
    │       └── transactions.md
    ├── test-journeys/
    │   ├── README.md                   # Journey index
    │   ├── auth/
    │   │   ├── login.md
    │   │   ├── logout.md
    │   │   └── forgot-password.md
    │   ├── accounts/
    │   │   ├── view-balance.md
    │   │   ├── view-history.md
    │   │   └── export-statement.md
    │   └── transfers/
    │       ├── initiate-transfer.md
    │       ├── confirm-transfer.md
    │       └── cancel-transfer.md
    ├── deployment/
    │   ├── README.md                   # Deployment overview
    │   ├── DEPLOYMENT-GUIDE.md         # Step-by-step guide
    │   ├── environments/
    │   │   ├── dev.md
    │   │   ├── staging.md
    │   │   └── production.md
    │   └── infrastructure/
    │       └── aws-setup.md
    ├── security/
    │   ├── README.md
    │   ├── SECURITY-POLICY.md
    │   └── AUTHENTICATION.md
    └── misc/
        ├── GLOSSARY.md                 # Terms and definitions
        └── FAQ.md
```

---

## Template System

### Three-Tier Template Hierarchy

```
QUAD Defaults (Built-in)
    ↓
Organization Templates (~/quad/templates/<org-code>/)
    ↓
Project Overrides (.quad/templates/)
```

### How It Works

1. **QUAD Defaults** - Built into QUAD CLI, industry standards
2. **Organization Templates** - Customized per client (e.g., MassMutual style)
3. **Project Overrides** - Specific to this project

**Resolution Order:**
```python
# quad doc generate api

# 1. Check project override
if exists(".quad/templates/api/README.md"):
    use_template(".quad/templates/api/README.md")

# 2. Check org template
elif exists("~/.quad/templates/MM/api/README.md"):
    use_template("~/.quad/templates/MM/api/README.md")

# 3. Use QUAD default
else:
    use_template("quad-cli/templates/api/README.md")
```

---

## Test Journey Format

### Journey File Structure

```markdown
# Test Journey: <Feature Name>

## Metadata
- **ID:** TJ-001
- **Feature:** <Feature Area>
- **Story:** <Related User Story>
- **Priority:** P0/P1/P2/P3
- **Status:** Draft/Review/Approved

## Overview
Brief description of what this journey tests.

## Prerequisites
- [ ] Precondition 1
- [ ] Precondition 2
- [ ] Precondition 3

## Test Steps

### Step 1: <Action Name>
**Action:**
Describe what the user/tester does.

**Expected Result:**
What should happen.

**APIs Called:**
- `<METHOD> <ENDPOINT>`
  - Request: `<JSON>`
  - Response: `<JSON>`
  - Status: `<Code>`

**Database Impact:**
| Table | Operation | Rows Affected |
|-------|-----------|---------------|
| users | SELECT | 1 |
| sessions | INSERT | 1 |

---

### Step 2: <Next Action>
...

---

## Database Impact Summary
Complete table of all DB operations in this journey.

| Table | Operations | Fields Touched |
|-------|------------|----------------|
| users | SELECT | id, email, password_hash, name |
| sessions | INSERT, SELECT | id, user_id, token, expires_at |

## API Call Summary
Complete list of all API calls.

| Endpoint | Method | Purpose | Response Time |
|----------|--------|---------|---------------|
| /api/v1/auth/login | POST | Authenticate | <500ms |
| /api/v1/user/profile | GET | Get user | <200ms |

## Flow Diagram
```
[User] → [Login Page] → [POST /auth/login] → [DB: users, sessions]
         ↓
      [Dashboard] ← [GET /user/profile] ← [Validate Token]
```

## Error Scenarios
1. **Invalid Email**
   - Input: malformed email
   - Expected: 400 Bad Request
   - Message: "Invalid email format"

2. **Wrong Password**
   - Input: wrong password
   - Expected: 401 Unauthorized
   - Message: "Invalid credentials"

## Performance Benchmarks
- **Target:** <500ms end-to-end
- **Acceptable:** <2s
- **Unacceptable:** >2s

## Dependencies
- Story: US-001 (User Login)
- APIs: Auth Service
- Tables: users, sessions

## Notes
Additional context, edge cases, etc.
```

---

## Generation Rules

### API Documentation

**Auto-Generated From:**
- Code annotations
- OpenAPI/Swagger specs
- Route definitions
- Request/response schemas

**Format:**
```markdown
# API Endpoint: Login

## POST /api/v1/auth/login

Authenticate user with email and password.

### Request

**Headers:**
- `Content-Type: application/json`

**Body:**
```json
{
  "email": "string (required, format: email)",
  "password": "string (required, min: 8)"
}
```

### Response

**Success (200 OK):**
```json
{
  "token": "string (JWT)",
  "user": {
    "id": "uuid",
    "name": "string",
    "email": "string"
  },
  "expiresAt": "string (ISO 8601)"
}
```

**Errors:**
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Wrong credentials
- `403 Forbidden` - Account locked
- `500 Internal Server Error` - Server error

### Example

**cURL:**
```bash
curl -X POST https://api.example.com/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "Test123!"}'
```

**JavaScript:**
```javascript
const response = await fetch('/api/v1/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: 'test@example.com',
    password: 'Test123!'
  })
});
const data = await response.json();
```

### Database Impact
- **Tables:** users (SELECT), sessions (INSERT)
- **Expected Time:** <100ms

### Security
- Password is hashed (bcrypt, 10 rounds)
- JWT expires after 24 hours
- Rate limit: 5 attempts per minute
```

---

### Database Documentation

**Auto-Generated From:**
- Schema definition (DDL)
- Migrations
- ORM models
- Foreign key relationships

**Format:**
```markdown
# Table: users

## Overview
Stores user account information.

## Schema

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique user ID |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password |
| name | VARCHAR(100) | NOT NULL | User's full name |
| created_at | TIMESTAMP | DEFAULT NOW() | Account creation |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update |
| deleted_at | TIMESTAMP | NULL | Soft delete |

## Indexes
- `users_email_idx` on email (UNIQUE)
- `users_created_at_idx` on created_at

## Relationships
- **Has Many:** sessions (user_id → sessions.user_id)
- **Has Many:** accounts (user_id → accounts.user_id)

## DDL
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

CREATE INDEX users_email_idx ON users(email);
CREATE INDEX users_created_at_idx ON users(created_at);
```

## Sample Data
```sql
INSERT INTO users (email, password_hash, name)
VALUES ('test@example.com', '$2a$10$...', 'Test User');
```

## Access Patterns
1. **Lookup by email** (login)
   - Query: `SELECT * FROM users WHERE email = ?`
   - Frequency: High
   - Index: users_email_idx

2. **Lookup by ID** (profile)
   - Query: `SELECT * FROM users WHERE id = ?`
   - Frequency: Very High
   - Index: PRIMARY KEY

## Notes
- Soft delete (deleted_at) preserves data for auditing
- Password is hashed using bcrypt (10 rounds)
- Email is case-insensitive (lowercased before storage)
```

---

### Architecture Documentation

**Auto-Generated From:**
- Project config (.quad/config.json)
- Code structure analysis
- Dependency analysis

**Format:**
```markdown
# System Architecture: <Project Name>

## Overview
High-level description of system architecture.

## Technology Stack

### Frontend
- **Framework:** Next.js 14
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **State:** Zustand
- **HTTP:** React Query

### Backend
- **Framework:** Spring Boot 3
- **Language:** Java 17
- **Database:** PostgreSQL 15
- **ORM:** JPA/Hibernate
- **Auth:** JWT

### Infrastructure
- **Hosting:** AWS
- **CI/CD:** GitHub Actions
- **Monitoring:** Datadog

## System Context Diagram
```
[Users] → [Web App] → [API Server] → [Database]
                           ↓
                      [External APIs]
```

## Component Diagram
```
Web App:
├── Pages (Next.js)
├── Components (React)
├── API Client (Fetch)
└── State (Zustand)

API Server:
├── Controllers (REST)
├── Services (Business Logic)
├── Repositories (Data Access)
└── Models (Entities)
```

## Data Flow
```
1. User submits form
2. React component validates input
3. API client sends POST request
4. Controller receives request
5. Service processes business logic
6. Repository saves to database
7. Response sent back to client
8. UI updates with result
```

## Architecture Decisions

### ADR-001: Use Spring Boot
**Status:** Accepted
**Date:** 2026-01-15

**Context:**
Need robust backend framework for enterprise banking app.

**Decision:**
Use Spring Boot 3 with Java 17.

**Consequences:**
- Proven enterprise framework
- Strong security features
- Large ecosystem
- More verbose than Node.js

### ADR-002: Use PostgreSQL
...
```

---

## Organization Customization

### Setting Up Org Templates

```bash
# Create org template directory
mkdir -p ~/.quad/templates/MM

# Copy QUAD defaults
quad doc template export MM

# Customize
cd ~/.quad/templates/MM
# Edit files...

# Use in projects
quad init banking-demo --org MM
```

### MassMutual Example

```
~/.quad/templates/MM/
├── api/
│   └── README.template.md        # MM branding, style
├── test-journeys/
│   └── journey.template.md       # MM test format
└── architecture/
    └── ARCHITECTURE.template.md  # MM architecture standards
```

**MM-specific requirements:**
- Logo in header
- Compliance sections
- Specific terminology (e.g., "Member" not "User")
- Required security disclosures

---

## Validation Rules

### quad doc validate

Checks:
- [ ] All required sections present
- [ ] No broken links
- [ ] All code snippets valid
- [ ] All diagrams exist
- [ ] Test journeys reference valid stories
- [ ] API docs match code
- [ ] DB docs match schema

**Example Output:**
```
✓ README.md - OK
✓ architecture/README.md - OK
✗ api/endpoints/auth.md - Missing example request
✗ test-journeys/auth/login.md - Step 3 references invalid API
✓ database/tables/users.md - OK

Score: 80% (4/5 passed)
```

---

## Export Formats

### PDF Export
```bash
quad doc export --format pdf --output banking-docs.pdf
```

**Features:**
- Table of contents
- Syntax highlighting
- Embedded diagrams
- Branded header/footer

### HTML Export
```bash
quad doc export --format html --output docs-site/
```

**Features:**
- Static site
- Search functionality
- Navigation sidebar
- Responsive design

---

## Best Practices

### 1. Keep Docs Close to Code
- API docs → Next to route files
- DB docs → Next to migrations
- Test journeys → Next to tests

### 2. Auto-Generate Where Possible
- API from OpenAPI spec
- DB from schema
- Diagrams from code

### 3. Version Documentation
- Track in git
- Link to code version
- Update on every release

### 4. Review Regularly
- Monthly doc reviews
- Update on architecture changes
- Keep test journeys current

---

## Future Enhancements

### 1. Interactive Documentation
- Live API playground
- Embedded SQL console
- Visual flow builder

### 2. AI-Powered Search
- "Show me all authentication APIs"
- "What tables does login touch?"
- "Explain the transfer flow"

### 3. Auto-Update
- Watch code changes
- Regenerate affected docs
- Create PR with updates

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
