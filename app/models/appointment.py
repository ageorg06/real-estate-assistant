from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class AppointmentData:
    date: datetime
    time_slot: str
    meeting_type: str
    notes: Optional[str]
    
    def to_dict(self) -> dict:
        return {
            'date': self.date,
            'time_slot': self.time_slot,
            'meeting_type': self.meeting_type,
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'AppointmentData':
        """Create an AppointmentData instance from a dictionary"""
        return cls(**data)