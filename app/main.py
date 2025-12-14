"""
Main FastAPI application with ALL FEATURES enabled.
Includes both detailed endpoint and SpeakSpace-compatible endpoint.
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from app.models import SpeakSpaceRequest, APIResponse, TaskListResponse, EnhancedTask
from app.auth import verify_token
from app.services.llm_extractor import LLMExtractor
from app.services.validator import TaskValidator
from app.services.json_storage import JSONStorage
from app.services.priority_intelligence import PriorityIntelligenceEngine
from app.services.owner_mapper import OwnerMapper
from app.services.deadline_predictor import DeadlinePredictor
from app.services.task_analyzer import TaskAnalyzer
from app.utils.helpers import format_task_timeline, generate_instant_preview
from app.config import get_settings

app = FastAPI(
    title="Voice Meeting Executor - Full Featured",
    description="AI-powered meeting task extractor with advanced features",
    version="2.0.0"
)

# Initialize all services
settings = get_settings()
llm_extractor = LLMExtractor()
validator = TaskValidator()
json_storage = JSONStorage(settings.storage_file)
pie = PriorityIntelligenceEngine()
owner_mapper = OwnerMapper()
deadline_predictor = DeadlinePredictor()
task_analyzer = TaskAnalyzer()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Voice Meeting Executor",
        "version": "2.0.0",
        "features": [
            "Priority Intelligence Engine",
            "Smart Owner Mapping",
            "Deadline Prediction",
            "Task Difficulty Estimator",
            "Auto-Classification",
            "Dependency Detection",
            "Risk Assessment",
            "Progress Estimation",
            "Meeting Summary Generator",
            "Task Timeline Visualizer"
        ],
        "storage": "JSON",
        "tasks_stored": json_storage.get_task_count(),
        "endpoints": {
            "detailed": "/process",
            "speakspace": "/speakspace/process"
        }
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    analytics = json_storage.get_analytics()
    
    return {
        "status": "healthy",
        "environment": settings.environment,
        "openai_configured": bool(settings.openai_api_key),
        "storage_type": "JSON",
        "storage_file": settings.storage_file,
        "tasks_count": json_storage.get_task_count(),
        "analytics": analytics
    }

@app.post("/process", response_model=APIResponse)
async def process_meeting_note(
    request: SpeakSpaceRequest,
    token: str = Depends(verify_token)
):
    """
    Main endpoint: Process meeting note with ALL FEATURES.
    Returns detailed response with full analytics.
    Use this for testing and demos.
    """
    
    try:
        print(f"\n{'='*70}")
        print(f"🎯 PROCESSING NEW MEETING NOTE")
        print(f"{'='*70}")
        print(f"📝 Note ID: {request.note_id}")
        print(f"📏 Text length: {len(request.prompt)} characters")
        print(f"⏰ Timestamp: {request.timestamp}")
        print(f"{'='*70}\n")
        
        # STEP 1: Extract tasks with LLM
        print("🤖 STEP 1: LLM Task Extraction")
        print("-" * 70)
        raw_tasks = llm_extractor.extract_tasks(request.prompt)
        print(f"✓ Extracted {len(raw_tasks)} raw tasks\n")
        
        # STEP 2: Validate and clean
        print("🧹 STEP 2: Validation & Cleanup")
        print("-" * 70)
        validated_tasks = validator.validate_and_filter(raw_tasks)
        print(f"✓ {len(validated_tasks)} tasks passed validation\n")
        
        if not validated_tasks:
            print("⚠️  No actionable tasks found\n")
            return APIResponse(
                status="success",
                message="No actionable tasks found in the meeting note",
                tasks_created=0
            )
        
        # STEP 3: Generate meeting summary
        print("📊 STEP 3: Meeting Summary Generation")
        print("-" * 70)
        meeting_summary = llm_extractor.generate_meeting_summary(request.prompt)
        print(f"✓ Generated summary with {len(meeting_summary.key_decisions)} decisions\n")
        
        # STEP 4: Apply all advanced features
        print("🚀 STEP 4: Applying Advanced Features")
        print("-" * 70)
        
        enhanced_tasks = []
        for task in validated_tasks:
            print(f"\n  Processing: {task.task_name[:50]}...")
            
            # Priority Intelligence Engine
            priority, priority_reason, confidence = pie.analyze_priority(
                task.task_name, task.due_date, task.owner, task.priority
            )
            
            # Smart Owner Mapping
            original_owner, mapped_owner = owner_mapper.map_owner(task.owner)
            
            # Deadline Prediction
            normalized_date, predicted_date, is_uncertain = deadline_predictor.predict_deadline(
                task.due_date, request.timestamp
            )
            
            # Task Analysis
            difficulty = task_analyzer.estimate_difficulty(task.task_name)
            category = task_analyzer.classify_category(task.task_name)
            has_dependency, dependency_info = task_analyzer.detect_dependency(
                task.task_name, validated_tasks
            )
            risk_level, risk_desc = task_analyzer.assess_risk(
                task.task_name, task.due_date, task.owner
            )
            progress = task_analyzer.estimate_progress(task.task_name)
            
            # Create enhanced task
            enhanced_task = EnhancedTask(
                task_name=task.task_name,
                owner=mapped_owner,
                due_date=normalized_date,
                priority=priority,
                confidence_score=confidence,
                difficulty=difficulty,
                category=category,
                predicted_deadline=predicted_date,
                has_dependency=has_dependency,
                dependency_info=dependency_info,
                risk_level=risk_level,
                risk_description=risk_desc,
                progress_estimate=progress
            )
            
            enhanced_tasks.append(enhanced_task)
            print(f"  ✓ Enhanced: {priority} priority, {difficulty} difficulty, {category} category")
        
        print(f"\n✓ Enhanced all {len(enhanced_tasks)} tasks\n")
        
        # STEP 5: Store tasks
        print("💾 STEP 5: Storing Tasks")
        print("-" * 70)
        successful, failed = json_storage.create_tasks_batch(
            enhanced_tasks, 
            request.note_id
        )
        print(f"✓ Stored {successful} tasks, {failed} failed\n")
        
        # STEP 6: Generate response
        print("📤 STEP 6: Generating Response")
        print("-" * 70)
        
        # Create instant preview
        preview = generate_instant_preview(enhanced_tasks)
        
        # Get analytics
        analytics = json_storage.get_analytics()
        
        summary_data = {
            "meeting_summary": meeting_summary.summary,
            "key_decisions": meeting_summary.key_decisions,
            "blockers": meeting_summary.blockers,
            "risks": meeting_summary.risks,
            "participants": meeting_summary.participants,
            "tasks_preview": preview,
            "high_priority_count": analytics["by_priority"].get("High", 0),
            "high_risk_count": analytics["high_risk_count"],
            "dependencies_count": analytics["with_dependencies"]
        }
        
        print(f"{'='*70}")
        print(f"✅ PROCESSING COMPLETE")
        print(f"{'='*70}\n")
        
        return APIResponse(
            status="success",
            message=f"✅ {successful} task{'s' if successful != 1 else ''} created successfully with advanced analysis",
            tasks_created=successful,
            summary=summary_data
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/speakspace/process")
async def process_for_speakspace(
    request: SpeakSpaceRequest,
    token: str = Depends(verify_token)
):
    """
    Simplified endpoint for SpeakSpace integration.
    Returns minimal response as required by SpeakSpace specification.
    
    SpeakSpace sends:
    {
      "prompt": "meeting text",
      "note_id": "unique-id",
      "timestamp": "ISO-8601"
    }
    
    We return:
    {
      "status": "success",
      "message": "X tasks created successfully"
    }
    """
    
    try:
        print(f"\n{'='*70}")
        print(f"🎤 SPEAKSPACE REQUEST")
        print(f"{'='*70}")
        print(f"📝 Note ID: {request.note_id}")
        print(f"📏 Text length: {len(request.prompt)} characters")
        print(f"{'='*70}\n")
        
        # STEP 1: Extract tasks
        raw_tasks = llm_extractor.extract_tasks(request.prompt)
        print(f"[SPEAKSPACE] Extracted {len(raw_tasks)} raw tasks")
        
        # STEP 2: Validate
        validated_tasks = validator.validate_and_filter(raw_tasks)
        print(f"[SPEAKSPACE] {len(validated_tasks)} tasks validated")
        
        if not validated_tasks:
            print(f"[SPEAKSPACE] No actionable tasks found\n")
            return {
                "status": "success",
                "message": "No actionable tasks found in the meeting note"
            }
        
        # STEP 3: Generate meeting summary
        meeting_summary = llm_extractor.generate_meeting_summary(request.prompt)
        
        # STEP 4: Enhance all tasks
        enhanced_tasks = []
        for task in validated_tasks:
            # Apply all features
            priority, _, confidence = pie.analyze_priority(
                task.task_name, task.due_date, task.owner, task.priority
            )
            _, mapped_owner = owner_mapper.map_owner(task.owner)
            normalized_date, predicted_date, _ = deadline_predictor.predict_deadline(
                task.due_date, request.timestamp
            )
            difficulty = task_analyzer.estimate_difficulty(task.task_name)
            category = task_analyzer.classify_category(task.task_name)
            has_dep, dep_info = task_analyzer.detect_dependency(task.task_name, validated_tasks)
            risk_level, risk_desc = task_analyzer.assess_risk(task.task_name, task.due_date, task.owner)
            progress = task_analyzer.estimate_progress(task.task_name)
            
            enhanced_tasks.append(EnhancedTask(
                task_name=task.task_name,
                owner=mapped_owner,
                due_date=normalized_date,
                priority=priority,
                confidence_score=confidence,
                difficulty=difficulty,
                category=category,
                predicted_deadline=predicted_date,
                has_dependency=has_dep,
                dependency_info=dep_info,
                risk_level=risk_level,
                risk_description=risk_desc,
                progress_estimate=progress
            ))
        
        # STEP 5: Store tasks
        successful, failed = json_storage.create_tasks_batch(enhanced_tasks, request.note_id)
        print(f"[SPEAKSPACE] Stored {successful} tasks, {failed} failed")
        
        print(f"{'='*70}")
        print(f"✅ SPEAKSPACE PROCESSING COMPLETE")
        print(f"{'='*70}\n")
        
        # STEP 6: Return SIMPLE response (SpeakSpace requirement)
        # Do NOT return large payloads - only status and message
        return {
            "status": "success",
            "message": f"{successful} task{'s' if successful != 1 else ''} created successfully"
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        print(f"[SPEAKSPACE] ❌ Error: {e}\n")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process meeting note: {str(e)}"
        )

@app.get("/tasks", response_model=TaskListResponse)
async def view_tasks(token: str = Depends(verify_token)):
    """View all stored tasks with analytics."""
    try:
        tasks = json_storage.get_all_tasks()
        analytics = json_storage.get_analytics()
        
        return TaskListResponse(
            status="success",
            count=len(tasks),
            tasks=tasks,
            analytics=analytics
        )
    except Exception as e:
        print(f"[ERROR] Failed to retrieve tasks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks"
        )

@app.get("/tasks/{note_id}")
async def view_tasks_by_note(note_id: str, token: str = Depends(verify_token)):
    """View tasks from a specific note."""
    try:
        tasks = json_storage.get_tasks_by_note(note_id)
        return {
            "status": "success",
            "note_id": note_id,
            "count": len(tasks),
            "tasks": tasks
        }
    except Exception as e:
        print(f"[ERROR] Failed to retrieve tasks for note {note_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks"
        )

@app.get("/timeline")
async def view_timeline(token: str = Depends(verify_token)):
    """
    View task timeline.
    FEATURE: Task Timeline Visualizer
    """
    try:
        tasks = json_storage.get_all_tasks()
        timeline = format_task_timeline(tasks)
        
        return {
            "status": "success",
            **timeline
        }
    except Exception as e:
        print(f"[ERROR] Failed to generate timeline: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate timeline"
        )

@app.get("/analytics")
async def view_analytics(token: str = Depends(verify_token)):
    """View detailed analytics."""
    try:
        analytics = json_storage.get_analytics()
        
        return {
            "status": "success",
            "analytics": analytics
        }
    except Exception as e:
        print(f"[ERROR] Failed to retrieve analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve analytics"
        )

@app.delete("/tasks/clear")
async def clear_all_tasks(token: str = Depends(verify_token)):
    """Clear all tasks (for testing only)."""
    try:
        success = json_storage.clear_all_tasks()
        if success:
            return {
                "status": "success",
                "message": "All tasks cleared"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to clear tasks"
            )
    except Exception as e:
        print(f"[ERROR] Failed to clear tasks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear tasks"
        )
@app.delete("/tasks/{task_id}")
async def delete_single_task(task_id: int, token: str = Depends(verify_token)):
    """Delete a single task by ID."""
    try:
        success = json_storage.delete_task(task_id)
        
        if success:
            return {
                "status": "success",
                "message": f"Task #{task_id} deleted successfully"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task #{task_id} not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Failed to delete task #{task_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    print(f"[CRITICAL] Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An unexpected error occurred. Please try again."
        }
    )


# Run with: uvicorn app.main:app --reload