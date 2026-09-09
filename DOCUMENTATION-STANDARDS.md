# QUAD Project Documentation Standards

**Version:** 1.0
**Last Updated:** January 15, 2026
**Purpose:** Define where documentation goes for QUAD framework itself

---

## The Problem

Currently, documentation is inconsistent:
- Sometimes files go in `documentation/`
- Sometimes in `doc/`
- Sometimes in project root
- No clear rules for where things belong

**Result:** Confusion, duplication, hard to find things

---

## The Solution: One Standard Structure

### QUAD Project Structure (This Repo)

```
a2vibes/
├── QUAD/                                    # QUAD framework
│   ├── README.md                            # Project overview
│   ├── CLAUDE.md                            # AI context for QUAD development
│   ├── BACKLOG.md                           # Product backlog
│   ├── CHANGELOG.md                         # Version history
│   ├── CONTRIBUTING.md                      # How to contribute
│   ├── LICENSE.md                           # License
│   │
│   ├── quad-cli/                            # CLI implementation
│   │   ├── README.md                        # CLI-specific readme
│   │   ├── setup.py                         # Python package
│   │   ├── requirements.txt                 # Dependencies
│   │   └── quad_cli/                        # Source code
│   │
│   ├── quad-agent-sdk/                      # Agent SDK (future)
│   │   └── README.md
│   │
│   └── documentation/                       # ← ALL DOCUMENTATION HERE
│       ├── README.md                        # Documentation index
│       │
│       ├── getting-started/                 # For QUAD contributors
│       │   ├── GETTING_STARTED.md
│       │   ├── DEVELOPER_ONBOARDING.md
│       │   ├── SETUP_INSTRUCTIONS.md
│       │   └── TEAM_ACCESS.md
│       │
│       ├── setup/                           # For QUAD users
│       │   ├── README.md                    # Choose your path
│       │   ├── QUAD_DEVELOPER_SETUP.md      # Use QUAD to build apps
│       │   └── QUAD_CONTRIBUTOR_SETUP.md    # Build QUAD itself
│       │
│       ├── methodology/                     # QUAD methodology
│       │   ├── PGCE-ALGORITHM.md
│       │   ├── QUAD-CONCEPT.md
│       │   └── SUMA-PLATFORM.md
│       │
│       ├── architecture/                    # System architecture
│       │   ├── SYSTEM-ARCHITECTURE.md
│       │   ├── QUAD-AGENT-ARCHITECTURE.md
│       │   ├── AI-ROUTER.md
│       │   ├── CONTEXT-MEMORY.md
│       │   └── diagrams/
│       │
│       ├── api/                             # API documentation
│       │   ├── SUMA-API-REFERENCE.md
│       │   ├── CLI-COMMANDS.md
│       │   └── AGENT-PROTOCOL.md
│       │
│       ├── database/                        # Database schemas
│       │   ├── QUAD-DATABASE-SCHEMA.md
│       │   └── migrations/
│       │
│       ├── testing/                         # Testing docs
│       │   ├── TEST-PLAN.md
│       │   └── journeys/
│       │       └── demo/
│       │           ├── 00-PREREQUISITES.md
│       │           ├── 01-INSTALLATION.md
│       │           └── 02-DEMO-WALKTHROUGH.md
│       │
│       ├── deployment/                      # Deployment docs
│       │   ├── FIREBASE-DEPLOYMENT.md
│       │   └── GCP-SETUP.md
│       │
│       ├── security/                        # Security docs
│       │   └── SECURITY-POLICY.md
│       │
│       ├── discussions/                     # Design discussions
│       │   ├── DISCUSSION-1-CONTEXT-MEMORY.md
│       │   ├── DISCUSSION-2-GEMINI-STANDALONE.md
│       │   ├── DISCUSSION-3-WHATSAPP-QUAD-SCHOOL.md
│       │   └── DISCUSSION-4-AGENT-STANDARDS.md
│       │
│       ├── implementation/                  # Implementation logs
│       │   ├── 2026-01-15-IMPLEMENTATION-PLAN.md
│       │   ├── 2026-01-15-IMPLEMENTATION-COMPLETE.md
│       │   ├── 2026-01-15-TEST-PLAN.md
│       │   └── 2026-01-15-INTEGRATION-SUMMARY.md
│       │
│       ├── company/                         # Company info
│       │   └── COMPANY-INFO.md
│       │
│       ├── domains/                         # Domain registry
│       │   └── DOMAIN-REGISTRY.md
│       │
│       ├── trademarks/                      # Trademark filings
│       │   └── TRADEMARKS-TO-FILE.md
│       │
│       ├── patents/                         # Patent docs
│       │   ├── PATENT-001-QUAD.md
│       │   ├── PATENT-002-AGENT-GENERATION.md
│       │   └── PATENT-003-PGCE.md
│       │
│       └── misc/                            # Everything else
│           ├── GLOSSARY.md
│           ├── FAQ.md
│           └── ROADMAP.md
```

---

## Rules for QUAD Documentation

### Rule 1: One Documentation Folder

**✅ CORRECT:**
```
QUAD/documentation/architecture/SYSTEM-ARCHITECTURE.md
```

**❌ WRONG:**
```
QUAD/doc/architecture/SYSTEM-ARCHITECTURE.md      # Wrong folder name
QUAD/docs/architecture/SYSTEM-ARCHITECTURE.md     # Wrong folder name
QUAD/architecture/SYSTEM-ARCHITECTURE.md          # Not in documentation/
```

### Rule 2: Folder Structure by Topic

**Categories:**
1. **getting-started/** - For QUAD contributors (build QUAD)
2. **setup/** - For QUAD users (use QUAD)
3. **methodology/** - PGCE, QUAD concept, etc.
4. **architecture/** - System design, diagrams
5. **api/** - API references
6. **database/** - Schemas, migrations
7. **testing/** - Test plans, journeys
8. **deployment/** - Deployment guides
9. **security/** - Security policies
10. **discussions/** - Design discussions (DISCUSSION-*.md)
11. **implementation/** - Implementation logs (YYYY-MM-DD-*.md)
12. **misc/** - Everything else

### Rule 3: File Naming

**Format:**
```
<CATEGORY>-<NAME>.md

Examples:
SYSTEM-ARCHITECTURE.md
API-REFERENCE.md
TEST-PLAN.md
```

**Dated files:**
```
YYYY-MM-DD-<NAME>.md

Examples:
2026-01-15-IMPLEMENTATION-PLAN.md
2026-01-15-TEST-PLAN.md
```

**Discussion files:**
```
DISCUSSION-<NUMBER>-<TOPIC>.md

Examples:
DISCUSSION-1-CONTEXT-MEMORY.md
DISCUSSION-2-GEMINI-STANDALONE.md
```

### Rule 4: README.md in Every Folder

Every folder must have README.md that:
1. Explains what's in this folder
2. Links to important files
3. Shows folder structure

**Example: documentation/architecture/README.md**
```markdown
# QUAD Architecture Documentation

## Overview
System architecture, design decisions, and technical diagrams.

## Files
- [SYSTEM-ARCHITECTURE.md](SYSTEM-ARCHITECTURE.md) - High-level architecture
- [QUAD-AGENT-ARCHITECTURE.md](QUAD-AGENT-ARCHITECTURE.md) - Agent system design
- [AI-ROUTER.md](AI-ROUTER.md) - AI routing algorithm
- [CONTEXT-MEMORY.md](CONTEXT-MEMORY.md) - Context memory system

## Diagrams
See [diagrams/](diagrams/) folder for visual representations.
```

---

## Configuration System

### quad-cli/.quad/doc-config.json

Create a configuration file that defines documentation paths:

```json
{
  "documentation_root": "documentation",
  "structure": {
    "getting-started": "documentation/getting-started",
    "setup": "documentation/setup",
    "methodology": "documentation/methodology",
    "architecture": "documentation/architecture",
    "api": "documentation/api",
    "database": "documentation/database",
    "testing": "documentation/testing",
    "deployment": "documentation/deployment",
    "security": "documentation/security",
    "discussions": "documentation/discussions",
    "implementation": "documentation/implementation",
    "misc": "documentation/misc"
  },
  "rules": {
    "file_naming": {
      "standard": "<CATEGORY>-<NAME>.md",
      "dated": "YYYY-MM-DD-<NAME>.md",
      "discussion": "DISCUSSION-<NUMBER>-<TOPIC>.md"
    },
    "required_files": [
      "README.md",
      "CLAUDE.md"
    ],
    "index_file": "documentation/README.md"
  },
  "validation": {
    "check_broken_links": true,
    "check_missing_readme": true,
    "check_naming_convention": true
  }
}
```

### Usage in Code

**When creating documentation:**

```python
from pathlib import Path
import json

def get_doc_path(category: str, filename: str) -> Path:
    """Get correct documentation path based on config"""

    # Load config
    config_file = Path(__file__).parent.parent / ".quad" / "doc-config.json"

    if config_file.exists():
        config = json.loads(config_file.read_text())
        doc_root = config["documentation_root"]
        category_path = config["structure"].get(category, f"{doc_root}/{category}")
    else:
        # Fallback to default
        doc_root = "documentation"
        category_path = f"{doc_root}/{category}"

    # Ensure path exists
    full_path = Path(category_path)
    full_path.mkdir(parents=True, exist_ok=True)

    return full_path / filename


# Usage
doc_path = get_doc_path("architecture", "SYSTEM-ARCHITECTURE.md")
doc_path.write_text("# System Architecture\n...")
```

### Validation Command

```bash
# Validate documentation structure
quad doc validate

# Output:
# ✓ Documentation root: documentation/ exists
# ✓ All required folders exist
# ✗ Missing README.md in: documentation/api/
# ✗ Wrong folder: doc/ should be documentation/
# ✓ File naming conventions followed
# ✗ Broken link in: SYSTEM-ARCHITECTURE.md → missing-file.md
#
# Score: 80% (4/5 checks passed)
```

---

## AI Agent Rules

### For Claude/AI Assistants

When asked to create documentation, ALWAYS:

1. **Check if documentation folder exists:**
```python
if Path("documentation").exists():
    doc_root = "documentation"
elif Path("docs").exists():
    doc_root = "docs"  # Legacy
elif Path("doc").exists():
    doc_root = "doc"   # Legacy
else:
    doc_root = "documentation"  # Create new
    Path(doc_root).mkdir(parents=True, exist_ok=True)
```

2. **Use correct category:**
```python
# Map intent to category
category_map = {
    "architecture": "architecture",
    "system design": "architecture",
    "api": "api",
    "endpoint": "api",
    "database": "database",
    "schema": "database",
    "test": "testing",
    "deployment": "deployment",
    "security": "security",
    "discussion": "discussions",
    "implementation": "implementation",
    "company": "company"
}

category = category_map.get(intent_keyword, "misc")
```

3. **Follow naming convention:**
```python
# Discussion file
if is_discussion:
    filename = f"DISCUSSION-{next_number}-{topic.upper()}.md"

# Dated file
elif is_dated:
    filename = f"{date.today()}-{name.upper()}.md"

# Standard file
else:
    filename = f"{category.upper()}-{name.upper()}.md"
```

4. **Create README if missing:**
```python
readme_path = doc_root / category / "README.md"
if not readme_path.exists():
    create_readme(readme_path, category)
```

---

## Migration Plan

### Step 1: Audit Current Docs

```bash
# Find all doc/docs folders
find . -type d -name "doc" -o -name "docs"

# List all markdown files
find . -name "*.md" | grep -E "(doc|docs|documentation)"
```

### Step 2: Move to Standard Structure

```bash
# Example: Move incorrectly placed files
mv QUAD/doc/SYSTEM-ARCHITECTURE.md QUAD/documentation/architecture/
mv QUAD/docs/api-ref.md QUAD/documentation/api/API-REFERENCE.md
```

### Step 3: Update Links

```bash
# Find and update broken links
grep -r "](doc/" QUAD/
grep -r "](docs/" QUAD/

# Replace with:
# sed -i 's|](doc/|](documentation/|g' file.md
```

### Step 4: Validate

```bash
quad doc validate
```

---

## Tools for Maintaining Standards

### 1. Pre-commit Hook

**.git/hooks/pre-commit**
```bash
#!/bin/bash

# Validate doc structure before commit
if command -v quad &> /dev/null; then
    quad doc validate
    if [ $? -ne 0 ]; then
        echo "Documentation validation failed!"
        echo "Run: quad doc validate"
        exit 1
    fi
fi
```

### 2. GitHub Action

**.github/workflows/validate-docs.yml**
```yaml
name: Validate Documentation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install QUAD CLI
        run: pip install -e quad-cli/
      - name: Validate Documentation
        run: quad doc validate
```

### 3. Documentation Linter

```bash
# Check all docs follow standards
quad doc lint

# Output:
# documentation/architecture/SYSTEM-ARCHITECTURE.md
#   ✓ Naming convention
#   ✓ Has README.md in folder
#   ✓ No broken links
#   ✗ Missing required section: "Overview"
#
# Score: 75%
```

---

## Quick Reference

### Where Does This File Go?

| File Type | Category | Example |
|-----------|----------|---------|
| System design | architecture/ | SYSTEM-ARCHITECTURE.md |
| API docs | api/ | API-REFERENCE.md |
| Database schema | database/ | DATABASE-SCHEMA.md |
| Test plans | testing/ | TEST-PLAN.md |
| Deployment guide | deployment/ | FIREBASE-DEPLOYMENT.md |
| Design discussion | discussions/ | DISCUSSION-1-CONTEXT.md |
| Implementation log | implementation/ | 2026-01-15-SUMMARY.md |
| Getting started | getting-started/ | GETTING_STARTED.md |
| User setup | setup/ | QUAD_DEVELOPER_SETUP.md |
| Methodology | methodology/ | PGCE-ALGORITHM.md |
| Company info | company/ | COMPANY-INFO.md |
| Patents | patents/ | PATENT-001-QUAD.md |
| Other | misc/ | GLOSSARY.md |

### Common Mistakes

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `doc/system.md` | `documentation/architecture/SYSTEM-ARCHITECTURE.md` |
| `docs/api.md` | `documentation/api/API-REFERENCE.md` |
| `QUAD/system-arch.md` | `QUAD/documentation/architecture/SYSTEM-ARCHITECTURE.md` |
| `discussion-memory.md` | `documentation/discussions/DISCUSSION-1-CONTEXT-MEMORY.md` |
| `2026-plan.md` | `documentation/implementation/2026-01-15-PLAN.md` |

---

## Configuration Commands

```bash
# Show current doc config
quad doc config show

# Update doc root
quad doc config set documentation_root "documentation"

# Validate current structure
quad doc validate

# Migrate from old structure
quad doc migrate --from "doc" --to "documentation"

# Generate index
quad doc index generate
```

---

## Summary

1. **One folder:** `documentation/` (not doc/, docs/, or root)
2. **Categories:** architecture, api, database, testing, etc.
3. **Naming:** CATEGORY-NAME.md or YYYY-MM-DD-NAME.md
4. **README:** Every folder must have one
5. **Config:** .quad/doc-config.json defines paths
6. **Validation:** quad doc validate checks structure

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
