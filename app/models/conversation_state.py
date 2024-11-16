from dataclasses import dataclass
from typing import Optional

@dataclass
class PropertyPreferences:
    transaction_type: Optional[str] = None
    property_type: Optional[str] = None
    location: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_bedrooms: Optional[int] = None
    
    def is_complete(self) -> bool:
        """Check if we have gathered essential preferences"""
        return all([
            self.transaction_type is not None,
            self.property_type is not None,
            self.location is not None,
            # Price range is optional
            # Bedrooms is optional
        ])
    
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