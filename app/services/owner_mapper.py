"""
Smart Owner Mapping Engine
FEATURE: Maps owner names to standardized identifiers
"""

class OwnerMapper:
    
    # Predefined owner mappings
    # In production, this would come from a database or configuration
    OWNER_MAPPINGS = {
        "riya": "Riya Kumar",
        "arjun": "Arjun Patel",
        "sarah": "Sarah Johnson",
        "mike": "Mike Chen",
        "john": "John Doe",
        "self": "Self (You)",
        "me": "Self (You)",
        "i": "Self (You)",
        "team": "Team",
    }
    
    @classmethod
    def map_owner(cls, owner: str) -> tuple[str, str]:
        """
        Map owner name to standardized identifier.
        
        Returns:
            (original_name, mapped_name)
        """
        
        if not owner or owner.strip() == "":
            return "Self", "Self (You)"
        
        owner_lower = owner.lower().strip()
        
        # Check for exact mapping
        if owner_lower in cls.OWNER_MAPPINGS:
            mapped = cls.OWNER_MAPPINGS[owner_lower]
            print(f"[OWNER_MAPPER] Mapped '{owner}' → '{mapped}'")
            return owner, mapped
        
        # Check for partial matches
        for key, value in cls.OWNER_MAPPINGS.items():
            if key in owner_lower or owner_lower in key:
                print(f"[OWNER_MAPPER] Partial match '{owner}' → '{value}'")
                return owner, value
        
        # No mapping found, use titlecase
        mapped = owner.title()
        print(f"[OWNER_MAPPER] No mapping for '{owner}', using: '{mapped}'")
        return owner, mapped
    
    @classmethod
    def add_mapping(cls, alias: str, full_name: str):
        """Add new owner mapping dynamically"""
        cls.OWNER_MAPPINGS[alias.lower()] = full_name
        print(f"[OWNER_MAPPER] Added mapping: {alias} → {full_name}")