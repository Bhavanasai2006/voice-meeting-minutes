"""
Priority Intelligence Engine (PIE)
FEATURE: Advanced priority assignment with reasoning
"""

class PriorityIntelligenceEngine:
    
    # Keywords for priority detection
    HIGH_PRIORITY_KEYWORDS = [
        "urgent", "asap", "critical", "blocker", "emergency", "immediately",
        "right now", "top priority", "must", "crucial", "vital"
    ]
    
    LOW_PRIORITY_KEYWORDS = [
        "when you get a chance", "eventually", "someday", "nice to have",
        "future", "later", "optional", "if possible"
    ]
    
    # Context keywords
    CLIENT_KEYWORDS = ["client", "customer", "user", "demo", "presentation"]
    PRODUCT_KEYWORDS = ["launch", "release", "deploy", "production", "go-live"]
    
    @classmethod
    def analyze_priority(cls, task_name: str, due_date: str, owner: str, original_priority: str) -> tuple[str, str, float]:
        """
        Analyze and assign priority with reasoning and confidence.
        
        Returns:
            (priority, reason, confidence_score)
        """
        
        task_lower = task_name.lower()
        due_lower = due_date.lower()
        
        reasons = []
        score = 0.7  # Base confidence
        
        # Check urgency keywords
        has_high_keyword = any(kw in task_lower for kw in cls.HIGH_PRIORITY_KEYWORDS)
        has_low_keyword = any(kw in task_lower for kw in cls.LOW_PRIORITY_KEYWORDS)
        
        # Check deadline urgency
        urgent_deadlines = ["today", "asap", "immediately"]
        near_deadlines = ["tomorrow", "this week"]
        
        is_urgent_deadline = any(dl in due_lower for dl in urgent_deadlines)
        is_near_deadline = any(dl in due_lower for dl in near_deadlines)
        
        # Check responsibility context
        has_client_context = any(kw in task_lower for kw in cls.CLIENT_KEYWORDS)
        has_product_context = any(kw in task_lower for kw in cls.PRODUCT_KEYWORDS)
        
        # Priority calculation
        if has_high_keyword:
            score += 0.2
            reasons.append("contains urgency keywords")
        
        if is_urgent_deadline:
            score += 0.3
            reasons.append("urgent deadline")
        elif is_near_deadline:
            score += 0.1
            reasons.append("near-term deadline")
        
        if has_client_context:
            score += 0.15
            reasons.append("client-facing")
        
        if has_product_context:
            score += 0.15
            reasons.append("product launch related")
        
        if has_low_keyword:
            score -= 0.3
            reasons.append("marked as low priority")
        
        if due_date == "Needs Review":
            score -= 0.1
            reasons.append("no clear deadline")
        
        # Determine final priority
        if score >= 0.85 or has_high_keyword or is_urgent_deadline:
            final_priority = "High"
        elif score <= 0.5 or has_low_keyword:
            final_priority = "Low"
        else:
            final_priority = "Medium"
        
        # Build reason string
        if reasons:
            reason = "Auto-detected: " + ", ".join(reasons)
        else:
            reason = f"Based on LLM classification: {original_priority}"
        
        # Cap confidence between 0.5 and 1.0
        confidence = min(1.0, max(0.5, score))
        
        print(f"[PIE] Task priority: {final_priority} (confidence: {confidence:.2f}) - {reason}")
        
        return final_priority, reason, confidence