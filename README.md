# Voice Meeting Executor - Full Featured Edition

AI-powered meeting task extractor with 15+ advanced features for SpeakSpace Hackathon.

## 🚀 Features

### Core Features
- ✅ Voice → Clean Meeting Tasks extraction
- ✅ Automatic task creation from meeting notes
- ✅ Real-time processing with OpenAI

### Advanced Features (All Implemented!)
1. **Priority Intelligence Engine (PIE)** - Smart priority detection with confidence scores
2. **Smart Owner Mapping** - Standardized name mapping with auto-correction
3. **Deadline Prediction** - Auto-normalize dates and predict deadlines
4. **Task Difficulty Estimator** - Easy/Medium/Hard classification
5. **Auto-Classification** - Category assignment (Development, Design, Testing, etc.)
6. **Dependency Detection** - Find task relationships and dependencies
7. **Risk Assessment** - Identify high-risk tasks with descriptions
8. **Progress Estimation** - Predict task status from keywords
9. **Meeting Summary Generator** - Executive summary with decisions and blockers
10. **Task Timeline Visualizer** - Visual timeline of all tasks
11. **Validation Layer** - Data quality checks and duplicate detection
12. **Auto-Correction Engine** - Fix common name and date mistakes
13. **Cleanup Engine** - Remove filler words from task descriptions
14. **Analytics Dashboard** - Task insights and statistics
15. **Instant Preview** - Pre-creation task preview

## 📦 Installation
```bash
# Clone repository
git clone <your-repo>
cd voice-meeting-executor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and BEARER_TOKEN
```

## ⚙️ Configuration

Create a `.env` file with:
```env
OPENAI_API_KEY=sk-proj-your-key-here
BEARER_TOKEN=your-secure-token-here
STORAGE_FILE=tasks.json
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## 🚀 Running Locally
```bash
# Start server
uvicorn app.main:app --reload

# Server will start at http://localhost:8000
# API docs at http://localhost:8000/docs
```

## 🧪 Testing
```bash
# Test health check
curl http://localhost:8000/health

# Process a meeting note
curl -X POST http://localhost:8000/process \
  -H "Authorization: Bearer YOUR_BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Team meeting: Riya needs to urgently finish the homepage design by Friday. Arjun should fix the critical login bug ASAP. Schedule client demo next week.",
    "note_id": "test-001",
    "timestamp": "2025-12-11T14:30:00Z"
  }'

# View all tasks
curl http://localhost:8000/tasks \
  -H "Authorization: Bearer YOUR_BEARER_TOKEN"

# View timeline
curl http://localhost:8000/timeline \
  -H "Authorization: Bearer YOUR_BEARER_TOKEN"

# View analytics
curl http://localhost:8000/analytics \
  -H "Authorization: Bearer YOUR_BEARER_TOKEN"
```

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check and feature list |
| `/health` | GET | Detailed health status with analytics |
| `/process` | POST | Process meeting note (main endpoint) |
| `/tasks` | GET | View all tasks with analytics |
| `/tasks/{note_id}` | GET | View tasks by note ID |
| `/timeline` | GET | View task timeline |
| `/analytics` | GET | Detailed analytics |
| `/tasks/clear` | DELETE | Clear all tasks (testing only) |

## 📊 Response Format

### `/process` endpoint returns:
```json
{
  "status": "success",
  "message": "✅ 3 tasks created successfully with advanced analysis",
  "tasks_created": 3,
  "summary": {
    "meeting_summary": "Team discussed urgent homepage design and critical bug fixes...",
    "key_decisions": ["Prioritize homepage design", "Fix login bug immediately"],
    "blockers": ["API stability issues"],
    "risks": ["Tight deadline for Friday delivery"],
    "participants": ["Riya", "Arjun"],
    "tasks_preview": "📋 **Tasks Preview:**\n1. 🔴 **Finish homepage design**...",
    "high_priority_count": 2,
    "high_risk_count": 1,
    "dependencies_count": 0
  }
}
```

## 💾 Storage

Tasks are stored in `tasks.json` with rich metadata:
```json
{
  "id": 1,
  "created_at": "2025
  -12-11T14:30:00",
"task_name": "Finish homepage design",
"owner": "Riya",
"owner_mapped": "Riya Kumar",
"due_date": "Friday",
"predicted_deadline": "2025-12-13",
"priority": "High",
"priority_reason": "Confidence: 0.92",
"confidence_score": 0.92,
"difficulty": "Medium",
"category": "Design",
"has_dependency": false,
"dependency_info": null,
"risk_level": "Medium",
"risk_description": "Risk: Tight deadline",
"progress_estimate": "Not Started",
"source_note_id": "test-001",
"status": "pending"
}

## 🚀 Deployment

### Deploy to Render

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Service
4. Connect your repository
5. Add environment variables:
   - `OPENAI_API_KEY`
   - `BEARER_TOKEN`
   - `STORAGE_FILE=tasks.json`
   - `ENVIRONMENT=production`
6. Deploy!

See `render.yaml` for automatic configuration.

## 🎤 SpeakSpace Integration

Configure custom action in SpeakSpace:
```json
{
  "name": "Smart Meeting Minutes",
  "description": "Extract tasks with AI-powered analysis",
  "endpoint": "https://your-app.onrender.com/process",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer YOUR_BEARER_TOKEN",
    "Content-Type": "application/json"
  },
  "body_template": {
    "prompt": "{{transcript}}",
    "note_id": "{{note_id}}",
    "timestamp": "{{timestamp}}"
  },
  "success_message": "✅ Tasks extracted with advanced analysis!",
  "error_message": "❌ Failed to process note"
}
```

## 🏆 Hackathon Features Showcase

**What makes this special:**
- 15+ AI-powered features (most teams have 3-5)
- Advanced analytics and insights
- Meeting summary generation
- Risk detection and dependency tracking
- Production-quality code with proper architecture
- Comprehensive error handling
- Full feature logging for demos

## 📄 License

MIT License - Free for hackathon use!

## 🤝 Contributing

This is a hackathon project. Feel free to fork and enhance!

## 📧 Contact

Built for SpeakSpace Annual Hackathon 2025