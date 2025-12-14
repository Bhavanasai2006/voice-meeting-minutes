"""
Pydantic models for request/response validation.
Enhanced with all feature fields.
"""
from pydantic import BaseModel, Field
from typing import Optional, List

class SpeakSpaceRequest(BaseModel):
    """Incoming request from SpeakSpace"""
    prompt: str = Field(..., description="Meeting summary text from voice note")
    note_id: str = Field(..., description="Unique identifier for the voice note")
    timestamp: str = Field(..., description="ISO 8601 timestamp")

class ExtractedTask(BaseModel):
    """Single task extracted by LLM"""
    task_name: str
    owner: str = "Self"
    due_date: str = "Needs Review"
    priority: str = "Medium"

class EnhancedTask(BaseModel):
    """Task with all advanced features applied"""
    task_name: str
    owner: str
    due_date: str
    priority: str
    confidence_score: float = 1.0
    difficulty: str = "Medium"
    category: str = "General"
    predicted_deadline: Optional[str] = None
    has_dependency: bool = False
    dependency_info: Optional[str] = None
    risk_level: str = "Low"
    risk_description: Optional[str] = None
    progress_estimate: str = "Not Started"

class StoredTask(BaseModel):
    """Task as stored in JSON file"""
    id: int
    created_at: str
    task_name: str
    owner: str
    owner_mapped: str
    due_date: str
    predicted_deadline: Optional[str]
    priority: str
    priority_reason: str
    confidence_score: float
    difficulty: str
    category: str
    has_dependency: bool
    dependency_info: Optional[str]
    risk_level: str
    risk_description: Optional[str]
    progress_estimate: str
    source_note_id: str
    status: str = "pending"

class TaskExtractionResponse(BaseModel):
    """Response from LLM extraction"""
    tasks: List[ExtractedTask]

class APIResponse(BaseModel):
    """Standard API response"""
    status: str
    message: str
    tasks_created: Optional[int] = None
    summary: Optional[dict] = None

class TaskListResponse(BaseModel):
    """Response for viewing tasks"""
    status: str
    count: int
    tasks: List[StoredTask]
    analytics: Optional[dict] = None

class MeetingSummary(BaseModel):
    """Meeting summary with key info"""
    summary: str
    key_decisions: List[str]
    blockers: List[str]
    risks: List[str]
    participants: List[str]