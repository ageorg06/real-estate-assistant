from dataclasses import dataclass, asdict
from typing import Optional
import json
import streamlit as st

@dataclass
class PropertyPreferences:
    transaction_type: Optional[str] = None
    property_type: Optional[str] = None
    location: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_bedrooms: Optional[int] = None
    
    @classmethod
    def from_json(cls, json_str: str) -> "PropertyPreferences":
        """Create PropertyPreferences from JSON string"""
        if not json_str:
            return cls()
        try:
            data = json.loads(json_str)
            return cls(**data)
        except (json.JSONDecodeError, TypeError):
            return cls()
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(asdict(self))
    
    def save_to_storage(self, user_id: str) -> None:
        """Save preferences to session state"""
        key = f"property_preferences_{user_id}"
        st.session_state[key] = self.to_json()
    
    @classmethod
    def load_from_storage(cls, user_id: str) -> "PropertyPreferences":
        """Load preferences from session state"""
        key = f"property_preferences_{user_id}"
        stored_data = st.session_state.get(key)
        if stored_data:
            return cls.from_json(stored_data)
        return cls()
    
    def is_complete(self) -> bool:
        """Check if we have gathered essential preferences"""
        complete = all([
            self.transaction_type is not None,
            self.property_type is not None,
            self.location is not None,
        ])
        print(f"Preferences complete: {complete}")
        print(f"transaction_type: {self.transaction_type}")
        print(f"property_type: {self.property_type}")
        print(f"location: {self.location}")
        return complete
    
    def missing_fields(self) -> list[str]:
        """Return list of missing essential fields"""
        missing = []
        if not self.transaction_type:
            missing.append("transaction type (buy or rent)")
        if not self.property_type:
            missing.append("property type (house, apartment, etc)")
        if not self.location:
            missing.append("preferred location")
        return missing 