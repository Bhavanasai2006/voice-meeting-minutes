"""
JSON file storage with enhanced task data.
"""
import json
from pathlib import Path
from datetime import datetime
from app.models import EnhancedTask, StoredTask
from typing import List
import threading

class JSONStorage:
    
    def __init__(self, file_path: str = "tasks.json"):
        self.file_path = Path(file_path)
        self.lock = threading.Lock()
        self._ensure_file_exists()
        print(f"[STORAGE] Using JSON storage: {self.file_path.absolute()}")
    
    def _ensure_file_exists(self):
        """Create file if it doesn't exist."""
        if not self.file_path.exists():
            self.file_path.write_text("[]")
            print(f"[STORAGE] Created new storage file: {self.file_path}")
    
    def _read_tasks(self) -> List[dict]:
        """Read all tasks from file."""
        with self.lock:
            try:
                content = self.file_path.read_text()
                return json.loads(content)
            except json.JSONDecodeError:
                print("[STORAGE] Warning: Corrupted JSON, reinitializing")
                return []
            except Exception as e:
                print(f"[STORAGE] Error reading tasks: {e}")
                return []
    
    def _write_tasks(self, tasks: List[dict]):
        """Write all tasks to file."""
        with self.lock:
            try:
                self.file_path.write_text(
                    json.dumps(tasks, indent=2, ensure_ascii=False)
                )
            except Exception as e:
                print(f"[STORAGE] Error writing tasks: {e}")
                raise
    
    def create_task(self, task: EnhancedTask, note_id: str) -> bool:
        """Add an enhanced task to JSON storage."""
        try:
            tasks = self._read_tasks()
            
            new_task = {
                "id": len(tasks) + 1,
                "created_at": datetime.now().isoformat(),
                "task_name": task.task_name,
                "owner": task.owner,
                "owner_mapped": task.owner,  # Already mapped
                "due_date": task.due_date,
                "predicted_deadline": task.predicted_deadline,
                "priority": task.priority,
                "priority_reason": f"Confidence: {task.confidence_score:.2f}",
                "confidence_score": task.confidence_score,
                "difficulty": task.difficulty,
                "category": task.category,
                "has_dependency": task.has_dependency,
                "dependency_info": task.dependency_info,
                "risk_level": task.risk_level,
                "risk_description": task.risk_description,
                "progress_estimate": task.progress_estimate,
                "source_note_id": note_id,
                "status": "pending"
            }
            
            tasks.append(new_task)
            self._write_tasks(tasks)
            
            print(f"[STORAGE] ✓ Created task #{new_task['id']}: {task.task_name}")
            return True
            
        except Exception as e:
            print(f"[STORAGE] ✗ Failed to save task: {e}")
            return False
    
    def create_tasks_batch(self, tasks: List[EnhancedTask], note_id: str) -> tuple[int, int]:
        """Add multiple tasks in batch."""
        successful = 0
        failed = 0
        
        for task in tasks:
            if self.create_task(task, note_id):
                successful += 1
            else:
                failed += 1
        
        print(f"[STORAGE] Batch complete: {successful} succeeded, {failed} failed")
        return successful, failed
    
    def get_all_tasks(self) -> List[StoredTask]:
        """Retrieve all tasks."""
        tasks = self._read_tasks()
        return [StoredTask(**task) for task in reversed(tasks)]
    
    def get_tasks_by_note(self, note_id: str) -> List[StoredTask]:
        """Get tasks from specific note."""
        all_tasks = self._read_tasks()
        filtered = [t for t in all_tasks if t.get("source_note_id") == note_id]
        return [StoredTask(**task) for task in filtered]
    
    def get_task_count(self) -> int:
        """Get total number of tasks."""
        return len(self._read_tasks())
    
    def get_analytics(self) -> dict:
        """
        Get analytics about stored tasks.
        FEATURE: Data Intelligence
        """
        tasks = self._read_tasks()
        
        if not tasks:
            return {
                "total_tasks": 0,
                "by_priority": {},
                "by_category": {},
                "by_difficulty": {},
                "high_risk_count": 0,
                "with_dependencies": 0
            }
        
        analytics = {
            "total_tasks": len(tasks),
            "by_priority": {},
            "by_category": {},
            "by_difficulty": {},
            "by_risk": {},
            "high_risk_count": 0,
            "with_dependencies": 0,
            "avg_confidence": 0.0
        }
        
        # Count by priority
        for task in tasks:
            priority = task.get("priority", "Medium")
            analytics["by_priority"][priority] = analytics["by_priority"].get(priority, 0) + 1
            
            category = task.get("category", "General")
            analytics["by_category"][category] = analytics["by_category"].get(category, 0) + 1
            
            difficulty = task.get("difficulty", "Medium")
            analytics["by_difficulty"][difficulty] = analytics["by_difficulty"].get(difficulty, 0) + 1
            
            risk = task.get("risk_level", "Low")
            analytics["by_risk"][risk] = analytics["by_risk"].get(risk, 0) + 1
            
            if risk == "High":
                analytics["high_risk_count"] += 1
            
            if task.get("has_dependency", False):
                analytics["with_dependencies"] += 1
        
        # Calculate average confidence
        confidences = [t.get("confidence_score", 0.7) for t in tasks]
        analytics["avg_confidence"] = sum(confidences) / len(confidences) if confidences else 0.0
        
        return analytics
    
    def clear_all_tasks(self) -> bool:
        """Clear all tasks (for testing)."""
        try:
            self._write_tasks([])
            print("[STORAGE] All tasks cleared")
            return True
        except Exception as e:
            print(f"[STORAGE] Failed to clear tasks: {e}")
            return False
    def delete_task(self, task_id: int) -> bool:
        """Delete a single task by ID."""
        try:
            tasks = self._read_tasks()
            
            # Find task with matching ID
            task_to_delete = None
            for task in tasks:
                if task.get("id") == task_id:
                    task_to_delete = task
                    break
            
            if not task_to_delete:
                print(f"[STORAGE] Task #{task_id} not found")
                return False
            
            # Remove the task
            tasks.remove(task_to_delete)
            
            # Write back to file
            self._write_tasks(tasks)
            
            print(f"[STORAGE] ✅ Deleted task #{task_id}: {task_to_delete.get('task_name', 'Unknown')}")
            return True
            
        except Exception as e:
            print(f"[STORAGE] ❌ Failed to delete task #{task_id}: {e}")
            return False