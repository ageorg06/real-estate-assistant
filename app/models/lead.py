from dataclasses import dataclass
from datetime import datetime

@dataclass
class LeadData:
    name: str
    contact: str
    contact_type: str
    created_at: datetime
    
    def to_dict(self) -> dict:
        """Convert the LeadData instance to a dictionary"""
        return {
            'name': self.name,
            'contact': self.contact,
            'contact_type': self.contact_type,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'LeadData':
        """Create a LeadData instance from a dictionary"""
        return cls(**data)