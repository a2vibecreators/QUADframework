# SQUAD EDU - Technical Specification

**Project:** WhatsApp Learning Platform
**Domain:** Education (proving QUAD Framework universality)
**Status:** Building (Phase 1)
**Launch Target:** March 2026

---

## Executive Summary

**SQUAD EDU** is the education-focused application of the QUAD Framework. It's a WhatsApp-based learning platform that teaches software development through daily 5-minute lessons with AI-powered Q&A.

**Why This Matters:**
SQUAD SDLC (software development) already exists and proves QUAD works. SQUAD EDU will prove QUAD works for **any industry**, opening the door to expand SUMANET across all domains.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    SQUAD EDU Ecosystem                       │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐              ┌──────────────────┐
│ WhatsApp Agent   │              │  Web App         │
│  (Phase 1)       │◄────────────►│  (Phase 2)       │
│                  │              │  Future          │
│ - Poll messages  │              │  - React/Next.js │
│ - Detect Q's     │              │  - Dashboard     │
│ - Send replies   │              │  - Progress UI   │
└────────┬─────────┘              └────────┬─────────┘
         │                                 │
         │    HTTP/REST                    │
         │                                 │
         ▼                                 ▼
┌────────────────────────────────────────────────────────────┐
│               QUAD API (quadframe.work)                     │
│             Serves all SQUAD Domain Applications            │
│                                                            │
│  SQUAD EDU Endpoints (Education):                          │
│  - POST /api/edu/register (user registration)             │
│  - GET  /api/edu/user/:phone (get user profile)           │
│  - POST /api/edu/question (RAG Q&A)                       │
│  - GET  /api/edu/progress/:phone (lesson progress)        │
│  - GET  /api/edu/weak-topics/:phone (mastery analysis)    │
│  - POST /api/edu/quiz (submit quiz answers)               │
└────────┬───────────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────────────────────────┐
│              QUAD Database (PostgreSQL)                     │
│                                                            │
│  SQUAD EDU Tables (edu_* prefix):                          │
│  - edu_users (user profiles)                               │
│  - edu_lesson_progress (track progress)                    │
│  - edu_topic_mastery (weak topic detection)                │
│  - edu_questions_log (Q&A history for personalization)     │
│  - edu_achievements (gamification)                         │
│  - edu_daily_lessons (lesson metadata)                     │
│  - edu_documentation (PostgreSQL full-text search for RAG) │
└────────────────────────────────────────────────────────────┘
```

---

## Database Schema

### Design Principles
1. **Domain prefix** - All tables use `edu_*` prefix for SQUAD EDU domain
2. **PostgreSQL-native** - Use PostgreSQL features (tsvector, triggers, etc.)
3. **No separate database** - Add to existing QUAD database
4. **Simple and clear** - Easy to understand and maintain

### Table Definitions

#### 1. `edu_users` - User Profiles

```sql
CREATE TABLE edu_users (
    phone_number VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),  -- Optional, for future web login
    skill_level VARCHAR(50) DEFAULT 'beginner',  -- beginner, intermediate, advanced
    goal VARCHAR(50) DEFAULT 'web',  -- web, mobile, both
    current_day INTEGER DEFAULT 0,  -- 0-90
    streak_days INTEGER DEFAULT 0,
    last_active_day TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_edu_users_email ON edu_users(email);
CREATE INDEX idx_edu_users_current_day ON edu_users(current_day);
```

**Purpose:** Track student profiles and progress

**Key Fields:**
- `phone_number` - Primary key (WhatsApp number)
- `current_day` - Which lesson they're on (0-90)
- `streak_days` - Consecutive days of activity (gamification)

#### 2. `edu_lesson_progress` - Lesson Completion

```sql
CREATE TABLE edu_lesson_progress (
    id SERIAL PRIMARY KEY,
    user_phone VARCHAR(20) REFERENCES edu_users(phone_number) ON DELETE CASCADE,
    day INTEGER NOT NULL,
    lesson_name VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    quiz_score INTEGER DEFAULT 0,  -- 0-100
    time_spent_minutes INTEGER DEFAULT 0,
    attempts INTEGER DEFAULT 1,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_progress_user ON edu_lesson_progress(user_phone);
CREATE INDEX idx_progress_day ON edu_lesson_progress(day);
CREATE INDEX idx_progress_completed ON edu_lesson_progress(completed);
```

**Purpose:** Track which lessons students completed and their scores

**Key Fields:**
- `quiz_score` - 0-100 score on lesson quiz
- `attempts` - How many times they tried
- `completed_at` - When they finished

#### 3. `edu_topic_mastery` - Weak Topic Detection ⭐

```sql
CREATE TABLE edu_topic_mastery (
    id SERIAL PRIMARY KEY,
    user_phone VARCHAR(20) REFERENCES edu_users(phone_number) ON DELETE CASCADE,
    topic VARCHAR(100) NOT NULL,  -- variables, loops, functions, arrays, etc.
    total_questions INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    mastery_percentage DECIMAL(5,2) DEFAULT 0.0,  -- 0-100
    needs_practice BOOLEAN DEFAULT FALSE,  -- TRUE if < 70%
    last_practiced TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_phone, topic)
);

-- Auto-calculate mastery percentage
CREATE OR REPLACE FUNCTION update_mastery_percentage()
RETURNS TRIGGER AS $$
BEGIN
    NEW.mastery_percentage := (NEW.correct_answers::DECIMAL / NULLIF(NEW.total_questions, 0)) * 100;
    NEW.needs_practice := NEW.mastery_percentage < 70;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_mastery
    BEFORE INSERT OR UPDATE ON edu_topic_mastery
    FOR EACH ROW
    EXECUTE FUNCTION update_mastery_percentage();

CREATE INDEX idx_mastery_user ON edu_topic_mastery(user_phone);
CREATE INDEX idx_mastery_needs_practice ON edu_topic_mastery(needs_practice);
```

**Purpose:** Track student performance per topic and detect weaknesses

**Key Features:**
- **Auto-calculates mastery %** - Trigger updates percentage automatically
- **Flags weak topics** - Sets `needs_practice = true` if < 70%
- **Personalized feedback** - API can tell students "You're weak in loops, practice more!"

#### 4. `edu_questions_log` - Q&A History

```sql
CREATE TABLE edu_questions_log (
    id SERIAL PRIMARY KEY,
    user_phone VARCHAR(20) REFERENCES edu_users(phone_number) ON DELETE CASCADE,
    question TEXT NOT NULL,
    topic_detected VARCHAR(100),  -- AI-detected topic
    day_asked INTEGER,
    answer TEXT,  -- RAG-generated answer
    answer_helpful BOOLEAN,  -- User feedback (thumbs up/down)
    follow_up_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_questions_user ON edu_questions_log(user_phone);
CREATE INDEX idx_questions_topic ON edu_questions_log(topic_detected);
CREATE INDEX idx_questions_day ON edu_questions_log(day_asked);
```

**Purpose:** Log all questions for personalization and improving RAG

**Key Features:**
- **Topic detection** - AI determines what topic the question is about
- **User feedback** - Track if answer was helpful
- **Follow-up tracking** - See if students ask more questions on same topic

#### 5. `edu_achievements` - Gamification

```sql
CREATE TABLE edu_achievements (
    id SERIAL PRIMARY KEY,
    user_phone VARCHAR(20) REFERENCES edu_users(phone_number) ON DELETE CASCADE,
    achievement_name VARCHAR(255) NOT NULL,  -- "Week Warrior", "Code Ninja"
    achievement_type VARCHAR(50) NOT NULL,  -- streak, completion, score
    description TEXT,
    unlocked_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_achievements_user ON edu_achievements(user_phone);
```

**Purpose:** Motivate students with badges and achievements

**Examples:**
- "Week Warrior" - Completed 7 days in a row
- "Perfect Score" - 100% on 3 quizzes in a row
- "Question Master" - Asked 50 questions

#### 6. `edu_daily_lessons` - Lesson Metadata

```sql
CREATE TABLE edu_daily_lessons (
    id SERIAL PRIMARY KEY,
    day INTEGER UNIQUE NOT NULL,
    lesson_name VARCHAR(255) NOT NULL,
    topic VARCHAR(100) NOT NULL,
    content_path TEXT NOT NULL,  -- Path to markdown file
    quiz_questions INTEGER DEFAULT 3,
    estimated_minutes INTEGER DEFAULT 5
);

-- Pre-populate with 90 days
INSERT INTO edu_daily_lessons (day, lesson_name, topic, content_path, quiz_questions, estimated_minutes) VALUES
(1, 'What is Code?', 'introduction', 'lessons/week_1/day_1.md', 3, 5),
(2, 'Variables', 'variables', 'lessons/week_1/day_2.md', 3, 5),
(3, 'Data Types', 'data-types', 'lessons/week_1/day_3.md', 3, 5),
(4, 'If/Else Statements', 'conditionals', 'lessons/week_1/day_4.md', 3, 5),
(5, 'Loops', 'loops', 'lessons/week_1/day_5.md', 3, 5),
(6, 'Functions', 'functions', 'lessons/week_1/day_6.md', 3, 5),
(7, 'Mini Project', 'project', 'lessons/week_1/day_7.md', 5, 10);
-- ... continue for 90 days
```

**Purpose:** Store lesson curriculum metadata

**Key Features:**
- Maps day numbers to lesson names
- Tracks which topic each lesson covers
- Points to markdown files with lesson content

#### 7. `edu_documentation` - RAG Search ⭐

```sql
CREATE TABLE edu_documentation (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    file_path TEXT NOT NULL,  -- Source file (e.g., 'QUAD/documentation/basics.md')
    topic VARCHAR(100),  -- variables, loops, functions, etc.
    search_vector tsvector,  -- PostgreSQL full-text search index
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Full-text search index using GIN
CREATE INDEX idx_doc_search_vector ON edu_documentation USING GIN(search_vector);
CREATE INDEX idx_doc_topic ON edu_documentation(topic);

-- Auto-update search vector on insert/update
CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', coalesce(NEW.title, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(NEW.content, '')), 'B');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_search_vector
    BEFORE INSERT OR UPDATE ON edu_documentation
    FOR EACH ROW
    EXECUTE FUNCTION update_search_vector();
```

**Purpose:** Enable RAG (Retrieval Augmented Generation) for Q&A

**Key Features:**
- **PostgreSQL full-text search** - No need for separate vector database (ChromaDB)
- **GIN index** - Fast text search using native PostgreSQL
- **Auto-updating** - Trigger maintains search_vector automatically
- **Topic filtering** - Can filter by topic before searching

**How RAG Works:**
1. Student asks: "What is a loop?"
2. Convert question to search query: `loop | loops | iteration`
3. Search documentation table using `ts_rank()`:
```sql
SELECT id, title, file_path, ts_rank(search_vector, query) AS rank
FROM edu_documentation, to_tsquery('english', 'loop | loops | iteration') AS query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 5;
```
4. Send top 3-5 docs to Gemini AI with student's question
5. Gemini generates answer using documentation context
6. Return answer with source citations

**Benefits over ChromaDB:**
- ✅ No separate database needed
- ✅ All data in one place
- ✅ Fast search with GIN index
- ✅ No embeddings API calls
- ✅ Simpler deployment

---

## API Endpoints

### Design Principles
1. **Domain-based routing** - All endpoints under `/api/edu/*`
2. **RESTful** - Use proper HTTP methods (GET, POST, PUT, DELETE)
3. **Consistent responses** - Always return `{ success, data/error, meta }`
4. **Phone number as ID** - Use phone numbers for user identification

### Endpoint Specifications

#### 1. POST /api/edu/register

**Purpose:** Register a new student

**Request:**
```json
{
  "phone": "+17322309573",
  "name": "Pradeep",
  "skill_level": "beginner",  // optional
  "goal": "web"  // optional
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "phone": "+17322309573",
    "name": "Pradeep",
    "skill_level": "beginner",
    "goal": "web",
    "current_day": 0,
    "streak_days": 0
  },
  "meta": {
    "isNewUser": true
  }
}
```

**Logic:**
1. Check if user exists in `edu_users`
2. If exists, return existing user
3. If new, insert into `edu_users`
4. Return user profile

#### 2. GET /api/edu/user/:phone

**Purpose:** Get student profile and current status

**Response:**
```json
{
  "success": true,
  "data": {
    "phone": "+17322309573",
    "name": "Pradeep",
    "skill_level": "beginner",
    "goal": "web",
    "current_day": 5,
    "streak_days": 3,
    "last_active": "2026-01-20T10:30:00Z",
    "next_lesson": {
      "day": 6,
      "name": "Functions",
      "topic": "functions"
    }
  }
}
```

#### 3. POST /api/edu/question ⭐ (RAG-powered)

**Purpose:** Answer student questions using documentation

**Request:**
```json
{
  "phone": "+17322309573",
  "question": "What is a loop?"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "answer": "A loop is like washing dishes - you repeat the same action until you're done...",
    "sources": [
      {
        "title": "Loops - Getting Started",
        "file_path": "documentation/getting-started/loops.md"
      },
      {
        "title": "Loop Examples",
        "file_path": "documentation/examples/loops.md"
      }
    ],
    "topic_detected": "loops"
  }
}
```

**Logic:**
1. Search `edu_documentation` using PostgreSQL full-text search
2. Get top 5 relevant documents
3. Build prompt with docs + question
4. Call Gemini API to generate answer
5. Log question in `edu_questions_log`
6. Return answer with sources

#### 4. GET /api/edu/progress/:phone

**Purpose:** Get student's learning progress

**Response:**
```json
{
  "success": true,
  "data": {
    "current_day": 5,
    "completed_lessons": 4,
    "total_lessons": 90,
    "progress_percentage": 4.4,
    "streak_days": 3,
    "lessons": [
      {
        "day": 1,
        "lesson_name": "What is Code?",
        "topic": "introduction",
        "completed": true,
        "quiz_score": 100,
        "completed_at": "2026-01-15T09:30:00Z"
      },
      {
        "day": 2,
        "lesson_name": "Variables",
        "topic": "variables",
        "completed": true,
        "quiz_score": 66,
        "completed_at": "2026-01-16T10:15:00Z"
      }
    ]
  }
}
```

#### 5. GET /api/edu/weak-topics/:phone ⭐

**Purpose:** Analyze student's weak topics and recommend practice

**Response:**
```json
{
  "success": true,
  "data": {
    "weak_topics": [
      {
        "topic": "loops",
        "mastery_percentage": 60.0,
        "total_questions": 10,
        "correct_answers": 6,
        "needs_practice": true,
        "recommendation": "Practice loops more - you got 6/10 questions correct."
      }
    ],
    "strong_topics": [
      {
        "topic": "variables",
        "mastery_percentage": 90.0,
        "total_questions": 10,
        "correct_answers": 9
      }
    ]
  }
}
```

**Logic:**
1. Query `edu_topic_mastery` where `needs_practice = true`
2. Sort by mastery percentage (lowest first)
3. Return weak topics with recommendations

#### 6. POST /api/edu/quiz

**Purpose:** Submit quiz answers and update topic mastery

**Request:**
```json
{
  "phone": "+17322309573",
  "day": 5,
  "answers": [
    {
      "question_id": 1,
      "answer": "A",
      "correct": true,
      "topic": "loops"
    },
    {
      "question_id": 2,
      "answer": "B",
      "correct": false,
      "topic": "loops"
    },
    {
      "question_id": 3,
      "answer": "C",
      "correct": true,
      "topic": "loops"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "score": 66,  // 2/3 correct
    "total_questions": 3,
    "correct_answers": 2,
    "weak_topics": ["loops"],
    "recommendation": "You scored 66% on loops. Review Day 5 lesson and try practice questions."
  }
}
```

**Logic:**
1. Calculate score
2. Update `edu_lesson_progress` with quiz score
3. Update `edu_topic_mastery` for each topic
4. Check if `mastery_percentage < 70%` → set `needs_practice = true`
5. Return score and weak topic recommendations

---

## WhatsApp Agent

### Architecture

```python
# whatsapp_agent/agent.py

import time
import requests
from datetime import datetime
from .client import WhatsAppBusinessClient
from .question_detector import is_question

class WhatsAppSchoolAgent:
    """Polls WhatsApp and routes to QUAD School API"""

    def __init__(self):
        self.whatsapp = WhatsAppBusinessClient()
        self.api_base = "http://localhost:3201/api/edu"
        self.polling_interval = 30  # seconds

    def run(self):
        """Main polling loop"""
        while True:
            messages = self.whatsapp.get_messages()
            for msg in messages:
                self.process_message(msg)
            time.sleep(self.polling_interval)

    def process_message(self, msg):
        """Process incoming message"""
        phone = msg.from_number
        text = msg.text.strip()

        # Handle registration
        if text.upper() == "START":
            self.handle_registration(phone)
            return

        # Handle questions
        if is_question(text):
            self.handle_question(phone, text)
            return

    def handle_question(self, phone, question):
        """Answer question via RAG API"""
        response = requests.post(
            f"{self.api_base}/question",
            json={"phone": phone, "question": question}
        )

        if response.status_code == 200:
            data = response.json()
            answer = data['data']['answer']
            self.whatsapp.send_message(phone, answer)
```

### Key Features

**1. Polling Loop**
- Checks for new messages every 30 seconds
- In production, would use webhooks instead

**2. Question Detection**
```python
def is_question(text: str) -> bool:
    """Detect if message is a question"""
    patterns = [
        r'\?$',                          # Ends with ?
        r'^(what|how|why|when|where)',   # Question words
        r'^(can|could|would|should)',    # Modal verbs
    ]
    return any(re.search(p, text.lower()) for p in patterns)
```

**3. Registration Flow**
- Student sends "START"
- Agent asks for name
- Creates user in database via API
- Sends welcome message with Day 1 lesson

---

## Documentation Indexer

### Purpose
Parse QUAD markdown documentation and insert into `edu_documentation` table for RAG search.

### Implementation

```python
# indexer/index_docs.py

import os
import glob
from database import get_db_connection

def index_documentation():
    """Index all QUAD markdown files"""

    # Find all .md files in QUAD/documentation/
    doc_files = glob.glob("QUAD/documentation/**/*.md", recursive=True)

    conn = get_db_connection()
    cursor = conn.cursor()

    for file_path in doc_files:
        # Read file
        with open(file_path, 'r') as f:
            content = f.read()

        # Extract title (first # heading)
        title = extract_title(content)

        # Detect topic from file path or content
        topic = detect_topic(file_path, content)

        # Insert into database
        cursor.execute("""
            INSERT INTO edu_documentation (title, content, file_path, topic)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (file_path) DO UPDATE
            SET content = EXCLUDED.content,
                title = EXCLUDED.title,
                topic = EXCLUDED.topic,
                updated_at = NOW()
        """, (title, content, file_path, topic))

    conn.commit()
    print(f"Indexed {len(doc_files)} documentation files")
```

**Key Features:**
- Parses all `.md` files in QUAD/documentation/
- Extracts title from first # heading
- Detects topic from file path or keywords
- Inserts into database (trigger auto-creates search_vector)
- Updates existing docs if content changed

---

## Technology Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| **Backend API** | Node.js + Express | Existing QUAD API |
| **Database** | PostgreSQL | Existing QUAD database |
| **Full-Text Search** | PostgreSQL tsvector + GIN | No separate vector DB needed |
| **AI** | Gemini API | Free tier (1500 req/day) |
| **WhatsApp** | Meta Cloud API | Free (1000 conversations/mo) |
| **WhatsApp Agent** | Python | Easy to script polling logic |
| **Hosting** | Local (MVP) → VPS (production) | Free for MVP |

**Total Cost: $0 for MVP!**

---

## Implementation Checklist

### Phase 1: Database
- [ ] Create migration script with all 7 tables
- [ ] Run migration on QUAD database
- [ ] Test with sample data
- [ ] Verify triggers work (mastery_percentage, search_vector)

### Phase 2: API
- [ ] Create `/api/edu` router in QUAD API
- [ ] Implement 6 endpoints
- [ ] Test with Postman/curl
- [ ] Add error handling

### Phase 3: Documentation Indexer
- [ ] Write indexer script (Python)
- [ ] Parse QUAD markdown files
- [ ] Insert into `edu_documentation`
- [ ] Test full-text search queries

### Phase 4: WhatsApp Agent
- [ ] Get Meta WhatsApp API token
- [ ] Create agent script (Python)
- [ ] Implement polling loop
- [ ] Test message sending/receiving

### Phase 5: Testing
- [ ] Register test user
- [ ] Send test question
- [ ] Verify RAG response
- [ ] Check topic mastery updates
- [ ] Test weak topic detection

### Phase 6: Content
- [ ] Write Week 1 lessons (7 markdown files)
- [ ] Create quiz questions for each lesson
- [ ] Test lesson delivery flow

### Phase 7: Beta Launch
- [ ] Recruit 10-20 testers
- [ ] Send daily lessons (manual for MVP)
- [ ] Monitor Q&A interactions
- [ ] Gather feedback
- [ ] Iterate!

---

## Success Metrics

**Week 1:**
- 80% of students complete Day 1 lesson
- Average 3+ questions asked per student
- 70%+ quiz pass rate

**Month 1:**
- 50% of students reach Week 2
- 90%+ satisfaction rating
- Weak topic detection working correctly

**Quarter 1 (March 2026):**
- 100 active users
- 80% completion rate for Week 1
- Proof that QUAD Framework works for education!

---

## Why This Will Succeed

**1. No App Install Needed**
WhatsApp is already on everyone's phone. Zero friction to start learning.

**2. Microlearning**
5-minute lessons fit into busy schedules. Students can learn during commute, lunch break, etc.

**3. Personalized**
RAG-powered Q&A + weak topic detection = truly personalized learning experience.

**4. Gamification**
Streaks, badges, achievements = motivation to keep going.

**5. Free**
No cost for students = no barrier to entry = viral growth.

**6. Proves Universality**
If QUAD works for education (not just software), it proves SUMANET vision is real!

---

**Copyright © 2026 Gopi Suman Addanke. All Rights Reserved.**
