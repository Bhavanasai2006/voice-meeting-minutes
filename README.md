# Voice Meeting Executor

AI-powered meeting task extractor with 15+ intelligent features for SpeakSpace integration.

---

## 🎯 One-Line Description

Converts meeting voice notes into structured, actionable tasks using OpenAI GPT with intelligent priority detection, deadline prediction, risk assessment, dependency tracking, and meeting summarization.

---

## 🚀 Live API Endpoint

**Production URL:** https://voice-meeting-executor-XXXX.onrender.com

**Health Check:** https://voice-meeting-executor-XXXX.onrender.com/health

**API Documentation:** https://voice-meeting-executor-XXXX.onrender.com/docs

**Status:** ✅ LIVE AND OPERATIONAL

---

## 🔐 Authorization Credentials for Testing

**Bearer Token:**
```
YOUR_ACTUAL_BEARER_TOKEN_HERE
```

**Usage Example:**
```bash
Authorization: Bearer YOUR_ACTUAL_BEARER_TOKEN_HERE
```

**Important:** This token is required for all authenticated endpoints.

---

## 📋 Setup Instructions

### Prerequisites
- Python 3.10 or 3.11
- pip package manager
- OpenAI API key

### Local Installation

**1. Extract the project:**
```bash
cd voice-meeting-executor
```

**2. Create virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables:**
```bash
cp .env.example .env
```

Edit `.env` file and add:
- `OPENAI_API_KEY` - Your OpenAI API key from https://platform.openai.com/api-keys
- `BEARER_TOKEN` - Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- `STORAGE_FILE` - Keep as `tasks.json`
- `ENVIRONMENT` - Keep as `production`

**5. Run the server:**
```bash
uvicorn app.main:app --reload
```

**6. Test locally:**
- Open browser: http://localhost:8000
- API docs: http://localhost:8000/docs

---

## 🌐 Deployment Guide (How Judges Can Test)

### Option 1: Test Live API 

**Quick Health Check:**
```bash
curl https://voice-meeting-executor-dmqt.onrender.com//health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "openai_configured": true,
  "storage_type": "JSON",
  "tasks_count": 0
}
```

**Process a Meeting Note:**
```bash
curl -X POST https://voice-meeting-executor-dmqt.onrender.com//speakspace/process \
  -H "Authorization: Bearer FxvL4FeK8VV-Fz1KvFcaCUWfklHmzh_Wkg74J3h0-2o" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Team meeting: Riya needs to finish the homepage design by Friday. Arjun should fix the critical login bug ASAP as it is blocking users.",
    "note_id": "judge-test-001",
    "timestamp": "2025-12-14T10:00:00Z"
  }'
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "2 tasks created successfully"
}
```

**View Created Tasks:**
```bash
curl https://voice-meeting-executor-dmqt.onrender.com//tasks \
  -H "Authorization: Bearer FxvL4FeK8VV-Fz1KvFcaCUWfklHmzh_Wkg74J3h0-2o"
```

**Interactive Testing:**

Open in browser: https://voice-meeting-executor-dmqt.onrender.com//docs

1. Click any endpoint with 🔒 icon
2. Click "Try it out"
3. Click the 🔒 icon, paste Bearer token, click "Authorize"
4. Fill in request body
5. Click "Execute"

### Option 2: Deploy Your Own Instance

**Deploy to Render:**

1. Fork the GitHub repository
2. Go to https://render.com and sign up
3. Create new Web Service
4. Connect your forked repository
5. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables (see .env.example)
6. Deploy and test

---

## 🎤 SpeakSpace Custom Action Configuration (Copy-Paste Ready)
```json
{
  "title": "Smart Meeting Minutes",
  "description": "Extract tasks from meeting notes with AI-powered analysis",
  "api_url": "https://voice-meeting-executor-dmqt.onrender.com//speakspace/process",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer FxvL4FeK8VV-Fz1KvFcaCUWfklHmzh_Wkg74J3h0-2o",
    "Content-Type": "application/json"
  },
  "body_template": {
    "prompt": "{{transcript}}",
    "note_id": "{{note_id}}",
    "timestamp": "{{timestamp}}"
  },
  "success_message": "✅ Tasks extracted and saved successfully!",
  "error_message": "❌ Failed to process meeting note. Please try again."
}
```

**Replace:**
- `YOUR_BEARER_TOKEN` with the actual Bearer token from credentials above
- Test in SpeakSpace by recording a voice note and triggering the action

---

## 📡 API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/` | GET | No | Health check and features list |
| `/health` | GET | No | Detailed system status |
| `/speakspace/process` | POST | Yes | Process meeting note (simple response) |
| `/process` | POST | Yes | Process meeting note (detailed response) |
| `/tasks` | GET | Yes | View all tasks with analytics |
| `/tasks/{note_id}` | GET | Yes | View tasks from specific note |
| `/timeline` | GET | Yes | Task timeline visualization |
| `/analytics` | GET | Yes | Detailed task analytics |
| `/tasks/clear` | DELETE | Yes | Clear all tasks (testing only) |

---

## 🧪 Example Test Cases

### Test Case 1: Simple Meeting
```json
{
  "prompt": "Quick standup: Sarah needs to update user documentation by Monday.",
  "note_id": "test-simple",
  "timestamp": "2025-12-14T10:00:00Z"
}
```
**Expected:** 1 task, Medium priority, Sarah as owner

### Test Case 2: Complex Meeting with Multiple Features
```json
{
  "prompt": "URGENT team meeting: Riya needs to finish homepage design by Friday - critical for client demo. Arjun should fix login bug ASAP as it's blocking users. Schedule product demo next week. Sarah will prepare slides when she has time. Note: API integration depends on Arjun finishing bug fix first.",
  "note_id": "test-complex",
  "timestamp": "2025-12-14T10:00:00Z"
}
```
**Expected:** 4 tasks, mixed priorities, dependency detection, risk detection

### Test Case 3: Risk Detection
```json
{
  "prompt": "Critical update: Production API is unstable. Waiting for client approval. Tight Friday deadline with unclear dependencies.",
  "note_id": "test-risk",
  "timestamp": "2025-12-14T10:00:00Z"
}
```
**Expected:** High-risk tasks identified with descriptions

---

## ✨ Features Implemented

1. **Priority Intelligence Engine** - Automatic High/Medium/Low detection
2. **Smart Owner Mapping** - Name standardization (e.g., "Riya" → "Riya Kumar")
3. **Deadline Prediction** - Natural language date conversion
4. **Task Difficulty Estimator** - Easy/Medium/Hard classification
5. **Auto-Classification** - Category assignment (Development, Design, etc.)
6. **Dependency Detection** - Identifies task relationships
7. **Risk Assessment** - Flags high-risk tasks
8. **Progress Estimation** - Predicts task status from keywords
9. **Meeting Summary Generator** - Creates executive summaries
10. **Task Timeline Visualizer** - Chronological task view
11. **Validation Layer** - Data quality checks
12. **Auto-Correction Engine** - Fixes common mistakes
13. **Cleanup Engine** - Removes filler words
14. **Analytics Dashboard** - Task insights and statistics
15. **Instant Preview** - Pre-creation task review

---

## 🏗️ Technical Architecture

**Backend Framework:** FastAPI (Python)
**AI Engine:** OpenAI GPT-4o-mini
**Storage:** JSON file-based (scalable to PostgreSQL/MongoDB)
**Authentication:** Bearer token
**Deployment:** Render
**API Style:** RESTful with OpenAPI documentation

---

## 📊 Response Examples

### Successful Processing
```json
{
  "status": "success",
  "message": "3 tasks created successfully"
}
```

### Task Data Structure
```json
{
  "id": 1,
  "created_at": "2025-12-14T10:00:00",
  "task_name": "Finish homepage design",
  "owner": "Riya Kumar",
  "due_date": "Friday",
  "predicted_deadline": "2025-12-20",
  "priority": "High",
  "confidence_score": 0.92,
  "difficulty": "Medium",
  "category": "Design",
  "risk_level": "Medium",
  "risk_description": "Risk: Tight deadline",
  "has_dependency": false,
  "dependency_info": null,
  "progress_estimate": "Not Started",
  "status": "pending"
}
```

---

## 🔧 Environment Variables

See `.env.example` for complete template.

**Required:**
- `OPENAI_API_KEY` - OpenAI API key for GPT access
- `BEARER_TOKEN` - API authentication token (generate securely)
- `STORAGE_FILE` - Storage filename (default: tasks.json)
- `ENVIRONMENT` - Environment name (production)
- `LOG_LEVEL` - Logging level (INFO)

---

## 🐛 Troubleshooting

**API returns 401 Unauthorized:**
- Verify Bearer token is correct
- Check Authorization header format: `Bearer YOUR_TOKEN`

**API returns 500 Internal Server Error:**
- Check OpenAI API key is valid
- Verify you have OpenAI credits: https://platform.openai.com/account/billing

**Server not responding:**
- Check if Render service is active
- First request after inactivity takes 30-60 seconds (cold start)

**Tasks not saving:**
- This is expected behavior on Render free tier (ephemeral storage)
- Tasks reset on server restart
- For persistent storage, upgrade to paid tier or use external database

---



Thank you for evaluating Voice Meeting Executor!
