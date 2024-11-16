from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from db.tables.base import Base

class PropertyPreferencesDB(Base):
    __tablename__ = "property_preferences"

    id = Column(Integer, primary_key=True)
    lead_id = Column(String, nullable=False)  # Link to lead's name as identifier
    transaction_type = Column(String)
    property_type = Column(String)
    location = Column(String)
    min_price = Column(Float)
    max_price = Column(Float)
    min_bedrooms = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())