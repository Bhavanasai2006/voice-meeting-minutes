"""
OpenAI-powered task extraction from meeting notes.
Enhanced with meeting summary generation.
"""
from openai import OpenAI
from app.config import get_settings
from app.models import ExtractedTask, TaskExtractionResponse, MeetingSummary
import json

class LLMExtractor:
    def __init__(self):
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def extract_tasks(self, meeting_text: str) -> list[ExtractedTask]:
        """
        Extract structured tasks from meeting text.
        """
        
        system_prompt = """You are a precise task extraction AI. Extract actionable tasks from meeting notes.

EXTRACTION RULES:
1. Extract ONLY actionable tasks (things that need to be done)
2. Ignore general discussion, decisions, or background info
3. For each task, identify:
   - task_name: Clear, concise description (10-50 words)
   - owner: Person responsible (use "Self" if unclear or if it says "I", "me", "we need to")
   - due_date: Deadline as text (e.g., "Today", "Tomorrow", "Friday", "Next Week", "Dec 15", "Needs Review")
   - priority: High / Medium / Low

PRIORITY DETECTION:
- High: "ASAP", "urgent", "critical", "today", "blocker", "emergency", "immediately", "right now"
- Medium: Standard tasks with reasonable deadlines, "this week", "soon"
- Low: Nice-to-have, "when you get a chance", "eventually", "future", "someday"

DEADLINE DETECTION:
- "today", "ASAP" → "Today"
- "tomorrow" → "Tomorrow"
- "this week", "by end of week" → "This Week"
- "next week" → "Next Week"
- "next month" → "Next Month"
- Specific dates → Keep as mentioned
- No deadline → "Needs Review"

OWNER DETECTION:
- Named person (Riya, Arjun, Sarah) → Use their name
- "I will", "I'll", "I need to" → "Self"
- "We need to", "Someone should" → "Self"
- "Team will" → "Team"
- Unclear → "Self"

OUTPUT FORMAT:
Return ONLY valid JSON:
{
  "tasks": [
    {
      "task_name": "string",
      "owner": "string",
      "due_date": "string",
      "priority": "High|Medium|Low"
    }
  ]
}

If no tasks found, return: {"tasks": []}"""

        user_prompt = f"""Extract all actionable tasks from this meeting summary:

{meeting_text}

Remember: Return ONLY the JSON object, nothing else."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            parsed = json.loads(content)
            extraction = TaskExtractionResponse(**parsed)
            
            print(f"[LLM] Extracted {len(extraction.tasks)} tasks")
            return extraction.tasks
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON parsing error: {e}")
            return []
        except Exception as e:
            print(f"[ERROR] OpenAI extraction error: {e}")
            return []
    
    def generate_meeting_summary(self, meeting_text: str) -> MeetingSummary:
        """
        Generate a comprehensive meeting summary.
        FEATURE: Meeting Summary Generator
        """
        
        system_prompt = """You are a meeting summarization expert. Generate a crisp meeting summary.

Extract:
1. Summary: 2-3 sentence overview of the meeting
2. Key Decisions: Important decisions made
3. Blockers: Any obstacles or blockers mentioned
4. Risks: Potential risks or concerns
5. Participants: People mentioned in the meeting

Return JSON format:
{
  "summary": "string",
  "key_decisions": ["string"],
  "blockers": ["string"],
  "risks": ["string"],
  "participants": ["string"]
}"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Summarize this meeting:\n\n{meeting_text}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.4,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            parsed = json.loads(content)
            return MeetingSummary(**parsed)
            
        except Exception as e:
            print(f"[ERROR] Summary generation error: {e}")
            return MeetingSummary(
                summary="Summary unavailable",
                key_decisions=[],
                blockers=[],
                risks=[],
                participants=[]
            )