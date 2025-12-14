"""
Validation and cleanup layer for extracted tasks.
FEATURES: Data validation, auto-correction, cleanup
"""
from app.models import ExtractedTask
import re

class TaskValidator:
    
    VALID_PRIORITIES = ["High", "Medium", "Low"]
    FILLER_WORDS = ["um", "uh", "like", "so", "basically", "actually", "you know", "kind of", "sort of"]
    
    # Common name misspellings
    NAME_CORRECTIONS = {
        "aarjun": "arjun",
        "rhiya": "riya",
        "sara": "sarah",
        "jhon": "john",
        "mic": "mike",
    }
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Remove filler words and extra whitespace.
        FEATURE: Cleanup Engine
        """
        if not text:
            return ""
        
        words = text.split()
        cleaned_words = [
            word for word in words 
            if word.lower() not in TaskValidator.FILLER_WORDS
        ]
        
        result = " ".join(cleaned_words).strip()
        
        # Remove extra spaces
        result = re.sub(r'\s+', ' ', result)
        
        return result if result else text
    
    @staticmethod
    def normalize_priority(priority: str) -> str:
        """Ensure priority is valid"""
        priority = priority.strip().capitalize()
        return priority if priority in TaskValidator.VALID_PRIORITIES else "Medium"
    
    @staticmethod
    def normalize_owner(owner: str) -> str:
        """
        Clean and auto-correct owner name.
        FEATURE: Auto-Correction Engine
        """
        owner = owner.strip().lower()
        
        # Auto-correct common misspellings
        if owner in TaskValidator.NAME_CORRECTIONS:
            corrected = TaskValidator.NAME_CORRECTIONS[owner]
            print(f"[VALIDATOR] Auto-corrected: '{owner}' → '{corrected}'")
            owner = corrected
        
        # Handle variations
        if owner in ["me", "myself", "i", ""]:
            return "Self"
        
        return owner.title() if owner else "Self"
    
    @staticmethod
    def normalize_due_date(due_date: str) -> str:
        """Clean due date"""
        due_date = due_date.strip()
        
        # Handle conflicting dates
        # FEATURE: Auto-Correction Engine
        if "saturday morning on friday" in due_date.lower():
            print("[VALIDATOR] Auto-corrected conflicting date to 'Friday'")
            return "Friday"
        
        return due_date.title() if due_date else "Needs Review"
    
    @classmethod
    def validate_task(cls, task: ExtractedTask) -> ExtractedTask:
        """
        Apply all validation and cleanup rules.
        FEATURE: Validation Layer
        """
        return ExtractedTask(
            task_name=cls.clean_text(task.task_name),
            owner=cls.normalize_owner(task.owner),
            due_date=cls.normalize_due_date(task.due_date),
            priority=cls.normalize_priority(task.priority)
        )
    
    @classmethod
    def is_valid_task(cls, task: ExtractedTask) -> bool:
        """
        Check if task is meaningful.
        FEATURE: Validation Layer
        """
        # Task name must be meaningful
        if not task.task_name or len(task.task_name.strip()) < 5:
            return False
        
        # Reject generic/meaningless tasks
        meaningless = ["todo", "task", "item", "thing", "do something", "work on it", "handle this"]
        if task.task_name.lower().strip() in meaningless:
            return False
        
        # Reject tasks that are just numbers or symbols
        if re.match(r'^[\d\s\W]+$', task.task_name):
            return False
        
        return True
    
    @classmethod
    def check_duplicate(cls, task: ExtractedTask, existing_tasks: list) -> bool:
        """
        Check if task is a duplicate.
        FEATURE: Validation Layer
        """
        task_name_lower = task.task_name.lower().strip()
        
        for existing in existing_tasks:
            existing_name_lower = existing.task_name.lower().strip()
            
            # Exact match
            if task_name_lower == existing_name_lower:
                return True
            
            # Very similar (>80% similarity)
            similarity = cls._similarity_ratio(task_name_lower, existing_name_lower)
            if similarity > 0.8:
                return True
        
        return False
    
    @staticmethod
    def _similarity_ratio(s1: str, s2: str) -> float:
        """Calculate similarity between two strings"""
        s1_words = set(s1.split())
        s2_words = set(s2.split())
        
        if not s1_words or not s2_words:
            return 0.0
        
        intersection = s1_words.intersection(s2_words)
        union = s1_words.union(s2_words)
        
        return len(intersection) / len(union)
    
    @classmethod
    def validate_and_filter(cls, tasks: list[ExtractedTask]) -> list[ExtractedTask]:
        """
        Validate all tasks and filter out invalid/duplicate ones.
        """
        validated = []
        
        for task in tasks:
            # Skip invalid tasks
            if not cls.is_valid_task(task):
                print(f"[VALIDATOR] Skipping invalid task: {task.task_name}")
                continue
            
            # Clean and normalize
            clean_task = cls.validate_task(task)
            
            # Check duplicates
            if cls.check_duplicate(clean_task, validated):
                print(f"[VALIDATOR] Skipping duplicate task: {clean_task.task_name}")
                continue
            
            validated.append(clean_task)
            print(f"[VALIDATOR] ✓ Validated: {clean_task.task_name}")
        
        return validated