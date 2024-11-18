from typing import List, Optional
from app.models.property import Property, SAMPLE_PROPERTIES

def filter_properties(
    transaction_type: Optional[str] = None,
    property_type: Optional[str] = None,
    location: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_bedrooms: Optional[int] = None
) -> List[Property]:
    """Filter properties based on preferences"""
    filtered = SAMPLE_PROPERTIES
    
    if transaction_type:
        filtered = [p for p in filtered if hasattr(p, 'transaction_type') and 
                   p.transaction_type.lower() == transaction_type.lower()]
    
    if property_type:
        filtered = [p for p in filtered if hasattr(p, 'type') and
                   p.type.lower() == property_type.lower()]
    
    if min_price is not None:
        filtered = [p for p in filtered if hasattr(p, 'price') and p.price >= min_price]
    if max_price is not None:
        filtered = [p for p in filtered if hasattr(p, 'price') and p.price <= max_price]
    
    if min_bedrooms is not None:
        filtered = [p for p in filtered if hasattr(p, 'bedrooms') and p.bedrooms >= min_bedrooms]
    
    return filtered