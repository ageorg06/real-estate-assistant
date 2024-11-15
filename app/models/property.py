from dataclasses import dataclass
from typing import Dict

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
    features: Dict

# Sample data
SAMPLE_PROPERTIES = [
    Property(
        id=1,
        title="Modern Downtown Apartment",
        type="apartment",
        transaction_type="rent",
        price=2500.00,
        location="Downtown",
        bedrooms=2,
        bathrooms=2,
        square_feet=1000.0,
        description="Luxury apartment with city views",
        image_url="https://placehold.co/600x400",
        features={"parking": True, "gym": True}
    ),
    Property(
        id=2,
        title="Suburban Family Home",
        type="house",
        transaction_type="buy",
        price=450000.00,
        location="Suburbs",
        bedrooms=4,
        bathrooms=3,
        square_feet=2500.0,
        description="Spacious family home with large backyard",
        image_url="https://placehold.co/600x400",
        features={"garage": True, "garden": True}
    ),
]