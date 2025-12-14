"""
Automatic Deadline Prediction
FEATURE: Smart deadline normalization and prediction
"""
from datetime import datetime, timedelta
from dateutil import parser
import re

class DeadlinePredictor:
    
    @classmethod
    def predict_deadline(cls, due_date_text: str, timestamp: str) -> tuple[str, str, bool]:
        """
        Predict and normalize deadline.
        
        Returns:
            (normalized_date, predicted_date, is_uncertain)
        """
        
        if not due_date_text or due_date_text.strip() == "":
            return "Needs Review", None, True
        
        text_lower = due_date_text.lower().strip()
        
        try:
            # Parse the meeting timestamp
            meeting_time = parser.parse(timestamp)
        except:
            meeting_time = datetime.now()
        
        # Relative date predictions
        today = meeting_time.date()
        
        predictions = {
            "today": today,
            "asap": today,
            "immediately": today,
            "tomorrow": today + timedelta(days=1),
            "this week": today + timedelta(days=(7 - today.weekday())),
            "next week": today + timedelta(days=(7 - today.weekday() + 7)),
            "this month": today.replace(day=28),
            "next month": (today.replace(day=28) + timedelta(days=4)).replace(day=1) + timedelta(days=27),
        }
        
        # Check for exact matches
        for phrase, predicted_date in predictions.items():
            if phrase in text_lower:
                normalized = due_date_text.title()
                predicted = predicted_date.strftime("%Y-%m-%d")
                is_uncertain = False
                print(f"[DEADLINE] '{due_date_text}' → {predicted} (certain)")
                return normalized, predicted, is_uncertain
        
        # Try to parse as specific date
        try:
            parsed_date = parser.parse(due_date_text, fuzzy=True)
            normalized = parsed_date.strftime("%b %d, %Y")
            predicted = parsed_date.strftime("%Y-%m-%d")
            is_uncertain = False
            print(f"[DEADLINE] Parsed '{due_date_text}' → {predicted}")
            return normalized, predicted, is_uncertain
        except:
            pass
        
        # Check for day of week
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for idx, day in enumerate(weekdays):
            if day in text_lower:
                days_ahead = (idx - today.weekday()) % 7
                if days_ahead == 0:
                    days_ahead = 7  # Next week
                predicted_date = today + timedelta(days=days_ahead)
                normalized = predicted_date.strftime("%A, %b %d")
                predicted = predicted_date.strftime("%Y-%m-%d")
                is_uncertain = "next" not in text_lower  # Uncertain if not explicitly "next"
                print(f"[DEADLINE] Day '{due_date_text}' → {predicted} (uncertain: {is_uncertain})")
                return normalized, predicted, is_uncertain
        
        # Uncertain deadline
        print(f"[DEADLINE] Uncertain: '{due_date_text}'")
        return due_date_text, None, True
    
    @classmethod
    def extract_fallback_deadline(cls, due_date_text: str) -> str:
        """
        Extract fallback deadline from text like "Wednesday or Thursday latest"
        """
        
        # Look for "or" patterns
        if " or " in due_date_text.lower():
            parts = due_date_text.lower().split(" or ")
            # Return first option as primary
            return parts[0].strip().title()
        
        return due_date_text