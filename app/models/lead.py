from dataclasses import dataclass
from datetime import datetime

@dataclass
class LeadData:
    name: str
    contact: str
    contact_type: str
    created_at: datetime