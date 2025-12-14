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
curl https://voice-meeting-executor-dmqt.onrender.com/health
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
curl -X POST https://voice-meeting-executor-dmqt.onrender.com/speakspace/process \
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
curl https://voice-meeting-executor-dmqt.onrender.com/tasks \
  -H "Authorization: Bearer FxvL4FeK8VV-Fz1KvFcaCUWfklHmzh_Wkg74J3h0-2o"
```

**Delete a Specific Task:**
```bash
curl -X DELETE https://voice-meeting-executor-dmqt.onrender.com/tasks/1 \
  -H "Authorization: Bearer FxvL4FeK8VV-Fz1KvFcaCUWfklHmzh_Wkg74J3h0-2o"
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Task #1 deleted successfully"
}
```

**Interactive Testing:**

Open in browser: https://voice-meeting-executor-dmqt.onrender.com/docs

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
  "api_url": "https://voice-meeting-executor-dmqt.onrender.com/speakspace/process",
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
| `/tasks/{task_id}` | DELETE | Yes | Delete a specific task by ID |
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

### Test Case 4: Delete Task
```bash
# First, get all tasks to find task IDs
curl https://voice-meeting-executor-dmqt.onrender.com/tasks \
  -H "Authorization: Bearer FxvL4FeK8VV-Fz1KvFcaCUWfklHmzh_Wkg74J3h0-2o"

# Then delete a specific task (replace {task_id} with actual ID)
curl -X DELETE https://voice-meeting-executor-dmqt.onrender.com/tasks/5 \
  -H "Authorization: Bearer FxvL4FeK8VV-Fz1KvFcaCUWfklHmzh_Wkg74J3h0-2o"
```
**Expected:** `{"status": "success", "message": "Task #5 deleted successfully"}`

---

## 🪟 PowerShell Commands (For Windows Users)

### View All Tasks
```powershell
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer FxvL4FeK8VV-Fz1KvFcaCUWfklHmzh_Wkg74J3h0-2o"
}

$response = Invoke-WebRequest -Uri "https://voice-meeting-executor-dmqt.onrender.com/tasks" -Method GET -Headers $headers
$response.Content
```

### Create Tasks
```powershell
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer FxvL4FeK8VV-Fz1KvFcaCUWfklHmzh_Wkg74J3h0-2o"
}

$body = @{
    prompt = "Fix login bug and assign to Ravi by Friday. Update landing page UI and assign to Self by Monday."
    note_id = "demo_001"
    timestamp = "2025-12-14T10:00:00Z"
} | ConvertTo-Json

Invoke-WebRequest -Uri "https://voice-meeting-executor-dmqt.onrender.com/process" -Method POST -Headers $headers -Body $body
```

### Delete a Task
```powershell
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer FxvL4FeK8VV-Fz1KvFcaCUWfklHmzh_Wkg74J3h0-2o"
}

$taskId = 4  # Replace with actual task ID

Invoke-WebRequest -Uri "https://voice-meeting-executor-dmqt.onrender.com/tasks/$taskId" -Method DELETE -Headers $headers
```

### View Tasks by Note ID
```powershell
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer FxvL4FeK8VV-Fz1KvFcaCUWfklHmzh_Wkg74J3h0-2o"
}

$noteId = "demo_001"

$response = Invoke-WebRequest -Uri "https://voice-meeting-executor-dmqt.onrender.com/tasks/$noteId" -Method GET -Headers $headers
$response.Content
```

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
16. **Task Management** - Individual task deletion support

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

### Successful Deletion
```json
{
  "status": "success",
  "message": "Task #5 deleted successfully"
}
```

### Task Not Found (404)
```json
{
  "detail": "Task #999 not found"
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

**API returns 404 Not Found (when deleting):**
- Verify the task ID exists by calling `/tasks` first
- Task IDs are integers, not strings

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

## 🎯 Task Management Workflow

1. **Create tasks** - Process meeting notes via `/process` or `/speakspace/process`
2. **View tasks** - List all tasks via `/tasks` or filter by note with `/tasks/{note_id}`
3. **Analyze tasks** - Get insights via `/analytics` or timeline via `/timeline`
4. **Delete tasks** - Remove individual tasks via `/tasks/{task_id}` or clear all via `/tasks/clear`

---

Thank you for evaluating Voice Meeting Executor!
