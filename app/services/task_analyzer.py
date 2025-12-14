"""
Task Analysis Engine
FEATURES: Difficulty estimation, category classification, dependency detection, risk analysis
"""
import re

class TaskAnalyzer:
    
    # Difficulty keywords
    HARD_KEYWORDS = [
        "integrate", "architecture", "refactor", "migrate", "scale",
        "optimize", "complex", "full module", "system", "infrastructure"
    ]
    
    EASY_KEYWORDS = [
        "update", "fix typo", "change text", "minor", "small", "quick",
        "simple", "basic", "easy"
    ]
    
    # Category keywords
    CATEGORIES = {
        "Development": ["code", "develop", "build", "implement", "api", "backend", "frontend", "bug", "fix"],
        "Design": ["design", "ui", "ux", "mockup", "wireframe", "prototype", "interface"],
        "Testing": ["test", "qa", "quality", "verify", "validate", "check"],
        "Client": ["client", "customer", "demo", "presentation", "meeting", "call"],
        "Documentation": ["document", "write", "documentation", "readme", "guide", "wiki"],
        "Deployment": ["deploy", "release", "launch", "production", "publish"],
        "Personal": ["personal", "learn", "research", "study", "training"],
    }
    
    # Risk keywords
    RISK_KEYWORDS = {
        "High": ["blocked", "dependency", "waiting for", "uncertain", "unclear", "tight deadline", "critical path"],
        "Medium": ["needs approval", "requires review", "pending", "complex"],
    }
    
    # Progress keywords
    PROGRESS_KEYWORDS = {
        "Completed": ["done", "completed", "finished", "shipped"],
        "In Progress": ["working on", "in progress", "started", "almost done"],
        "Blocked": ["blocked", "stuck", "waiting", "dependency"],
        "50%": ["halfway", "50%", "partially", "needs revision"],
    }
    
    @classmethod
    def estimate_difficulty(cls, task_name: str) -> str:
        """
        Estimate task difficulty based on keywords and complexity.
        FEATURE: Task Difficulty Estimator
        """
        
        task_lower = task_name.lower()
        
        # Count steps/complexity indicators
        word_count = len(task_name.split())
        has_multiple_steps = " and " in task_lower or "," in task_name
        
        # Check for difficulty keywords
        is_hard = any(kw in task_lower for kw in cls.HARD_KEYWORDS)
        is_easy = any(kw in task_lower for kw in cls.EASY_KEYWORDS)
        
        if is_hard or word_count > 15 or has_multiple_steps:
            difficulty = "Hard"
        elif is_easy or word_count < 5:
            difficulty = "Easy"
        else:
            difficulty = "Medium"
        
        print(f"[ANALYZER] Difficulty: {difficulty} for '{task_name}'")
        return difficulty
    
    @classmethod
    def classify_category(cls, task_name: str) -> str:
        """
        Classify task into category.
        FEATURE: Auto-Classification
        """
        
        task_lower = task_name.lower()
        
        # Score each category
        scores = {}
        for category, keywords in cls.CATEGORIES.items():
            score = sum(1 for kw in keywords if kw in task_lower)
            if score > 0:
                scores[category] = score
        
        # Return highest scoring category
        if scores:
            category = max(scores, key=scores.get)
            print(f"[ANALYZER] Category: {category} for '{task_name}'")
            return category
        
        return "General"
    
    @classmethod
    def detect_dependency(cls, task_name: str, all_tasks: list) -> tuple[bool, str]:
        """
        Detect task dependencies.
        FEATURE: Task Dependency Chain Builder
        """
        
        task_lower = task_name.lower()
        
        # Dependency indicators
        dependency_phrases = [
            "after", "once", "when", "depends on", "requires",
            "needs", "then", "following"
        ]
        
        has_dependency = any(phrase in task_lower for phrase in dependency_phrases)
        
        if has_dependency:
            # Try to extract what it depends on
            for phrase in dependency_phrases:
                if phrase in task_lower:
                    parts = task_lower.split(phrase)
                    if len(parts) > 1:
                        dependency_info = f"Depends on: {parts[1].strip()[:50]}"
                        print(f"[ANALYZER] Dependency detected: {dependency_info}")
                        return True, dependency_info
            
            return True, "Has dependencies (details unclear)"
        
        return False, None
    
    @classmethod
    def assess_risk(cls, task_name: str, due_date: str, owner: str) -> tuple[str, str]:
        """
        Assess task risk level.
        FEATURE: Risk Detection
        """
        
        combined_text = f"{task_name} {due_date}".lower()
        
        # Check for high risk keywords
        for keyword in cls.RISK_KEYWORDS["High"]:
            if keyword in combined_text:
                risk_desc = f"Risk: {keyword.title()}"
                print(f"[ANALYZER] High risk: {risk_desc}")
                return "High", risk_desc
        
        # Check for medium risk
        for keyword in cls.RISK_KEYWORDS["Medium"]:
            if keyword in combined_text:
                risk_desc = f"Risk: {keyword.title()}"
                print(f"[ANALYZER] Medium risk: {risk_desc}")
                return "Medium", risk_desc
        
        # Check if deadline is uncertain
        if due_date == "Needs Review" or "uncertain" in combined_text:
            return "Medium", "Risk: Unclear deadline"
        
        # Check if owner is unclear
        if owner == "Self" and "team" in combined_text:
            return "Medium", "Risk: Unclear ownership"
        
        return "Low", None
    
    @classmethod
    def estimate_progress(cls, task_name: str) -> str:
        """
        Estimate task progress from description.
        FEATURE: Progress Prediction Engine
        """
        
        task_lower = task_name.lower()
        
        # Check progress keywords
        for progress, keywords in cls.PROGRESS_KEYWORDS.items():
            if any(kw in task_lower for kw in keywords):
                print(f"[ANALYZER] Progress: {progress}")
                return progress
        
        return "Not Started"