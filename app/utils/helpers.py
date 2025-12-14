"""
Utility helper functions
"""
from typing import List
from app.models import StoredTask

def format_task_timeline(tasks: List[StoredTask]) -> dict:
    """
    Format tasks into timeline structure.
    FEATURE: Task Timeline Visualizer
    """
    timeline = []
    
    for task in tasks:
        if task.predicted_deadline:
            timeline.append({
                "task": task.task_name,
                "due": task.predicted_deadline,
                "priority": task.priority,
                "owner": task.owner_mapped
            })
    
    # Sort by date
    timeline.sort(key=lambda x: x["due"])
    
    return {
        "timeline": timeline,
        "total_tasks": len(timeline)
    }

def generate_instant_preview(tasks: List) -> str:
    """
    Generate instant preview text.
    FEATURE: Instant Preview
    """
    if not tasks:
        return "No tasks to preview"
    
    preview_lines = ["📋 **Tasks Preview:**\n"]
    
    for idx, task in enumerate(tasks, 1):
        priority_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(task.priority, "⚪")
        preview_lines.append(
            f"{idx}. {priority_emoji} **{task.task_name}**\n"
            f"   👤 {task.owner} | 📅 {task.due_date} | 📊 {task.difficulty}"
        )
    
    return "\n".join(preview_lines)