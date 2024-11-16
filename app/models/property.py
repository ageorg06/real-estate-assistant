from dataclasses import dataclass
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

@dataclass
class Property:
    id: int
    title: str
    type: str
    transaction_type: str
    price: float
    location: str
    bedrooms: int
    bathrooms: int
    square_feet: float
    description: str
    image_url: str
    features: Dict[str, bool]
    amenities: Optional[List[str]] = None

# Sample properties with diverse characteristics
SAMPLE_PROPERTIES = [
    Property(
        id=1,
        title="Modern Downtown Apartment",
        type="apartment",
        transaction_type="rent",
        price=2500.00,
        location="Larnaca",
        bedrooms=2,
        bathrooms=2,
        square_feet=1000.0,
        description="Luxury apartment with city views and modern finishes",
        image_url="https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800",
        features={"parking": True, "gym": True, "pool": True}
    ),
    Property(
        id=2,
        title="Suburban Family Home",
        type="house",
        transaction_type="buy",
        price=450000.00,
        location="Larnaca",
        bedrooms=4,
        bathrooms=3,
        square_feet=2500.0,
        description="Spacious family home with large backyard and modern kitchen",
        image_url="https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=800",
        features={"garage": True, "garden": True, "fireplace": True}
    ),
    Property(
        id=3,
        title="Cozy Studio Loft",
        type="studio",
        transaction_type="rent",
        price=1800.00,
        location="Larnaca",
        bedrooms=1,
        bathrooms=1,
        square_feet=600.0,
        description="Industrial-style loft with high ceilings and exposed brick walls",
        image_url="https://images.unsplash.com/photo-1536376072261-38c75010e6c9?w=800",
        features={"security": True, "laundry": True}
    ),
    Property(
        id=4,
        title="Luxury Beach House",
        type="house",
        transaction_type="buy",
        price=850000.00,
        location="Larnaca",
        bedrooms=3,
        bathrooms=2,
        square_feet=2000.0,
        description="Stunning beachfront property with panoramic ocean views",
        image_url="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800",
        features={"pool": True, "terrace": True, "beach_access": True}
    ),
    Property(
        id=5,
        title="Modern Larnaca Villa",
        type="house",
        transaction_type="buy",
        price=250000.00,
        location="Larnaca",
        bedrooms=3,
        bathrooms=2,
        square_feet=1800.0,
        description="Beautiful modern villa in Larnaca with garden and parking",
        image_url="https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800",
        features={"parking": True, "garden": True, "security": True}
    )
]

def filter_properties(
    transaction_type: str = None,
    min_price: float = None,
    max_price: float = None,
    location: str = None,
    property_type: str = None,
    min_bedrooms: int = None
) -> List[Property]:
    """Filter properties based on user preferences"""
    
    filtered = SAMPLE_PROPERTIES.copy()
    
    if transaction_type:
        filtered = [p for p in filtered if p.transaction_type.lower() == transaction_type.lower()]
    
    if min_price:
        filtered = [p for p in filtered if p.price >= min_price]
    
    if max_price:
        filtered = [p for p in filtered if p.price <= max_price]
    
    if location:
        filtered = [p for p in filtered if location.lower() in p.location.lower()]
    
    if property_type:
        filtered = [p for p in filtered if p.type.lower() == property_type.lower()]
    
    if min_bedrooms:
        filtered = [p for p in filtered if p.bedrooms >= min_bedrooms]
    
    return filtered