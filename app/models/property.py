from dataclasses import dataclass
from typing import Dict, List, Optional
from random import randint, choice, uniform, sample
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

# Cyprus-specific data
CYPRUS_LOCATIONS = [
    "Larnaca",
    "Pervolia",
    "Kiti",
    "Meneou",
    "Aradippou",
    "Livadia",
    "Dromolaxia",
    "Kornos",
    "Delikipos",
    "Alethriko"
]

PROPERTY_TYPES = {
    "apartment": {
        "min_price_rent": 500,
        "max_price_rent": 3000,
        "min_price_buy": 190000,
        "max_price_buy": 300000,
        "min_size": 50,
        "max_size": 200,
        "titles": ["Modern {} Apartment", "Luxury {} Flat", "Urban {} Apartment", 
                  "Contemporary {} Apartment", "Stylish {} Flat"]
    },
    "house": {
        "min_price_rent": 1000,
        "max_price_rent": 5000,
        "min_price_buy": 220000,
        "max_price_buy": 400000,
        "min_size": 120,
        "max_size": 400,
        "titles": ["Spacious {} Villa", "Family {} Home", "Detached {} House", 
                  "Modern {} Villa", "Luxury {} House"]
    },
    "studio": {
        "min_price_rent": 400,
        "max_price_rent": 1200,
        "min_price_buy": 120000,
        "max_price_buy": 200000,
        "min_size": 30,
        "max_size": 60,
        "titles": ["Cozy {} Studio", "Modern {} Studio", "Compact {} Studio", 
                  "Urban {} Studio", "Stylish {} Studio"]
    }
}

# Unsplash collections for different property types
PROPERTY_IMAGES = {
    "apartment": [
        "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00",
        "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688",
        "https://images.unsplash.com/photo-1536376072261-38c75010e6c9",
        "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2",
        # Add more apartment images...
    ],
    "house": [
        "https://images.unsplash.com/photo-1518780664697-55e3ad937233",
        "https://images.unsplash.com/photo-1512917774080-9991f1c4c750",
        "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9",
        "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c",
        # Add more house images...
    ],
    "studio": [
        "https://images.unsplash.com/photo-1536376072261-38c75010e6c9",
        "https://images.unsplash.com/photo-1554995207-c18c203602cb",
        "https://images.unsplash.com/photo-1626178793926-22b28830aa30",
        # Add more studio images...
    ]
}

FEATURES = {
    "parking": 0.8,
    "pool": 0.3,
    "gym": 0.2,
    "security": 0.6,
    "garden": 0.4,
    "terrace": 0.5,
    "beach_access": 0.15,
    "garage": 0.4,
    "fireplace": 0.2,
    "laundry": 0.9,
    "balcony": 0.7,
    "storage": 0.6,
    "elevator": 0.5,
    "air_conditioning": 0.9
}

def generate_description(property_type: str, location: str, features: Dict[str, bool]) -> str:
    """Generate a realistic property description"""
    features_list = [k for k, v in features.items() if v]
    features_text = ", ".join(features_list)
    
    templates = [
        f"Beautiful {property_type} in {location} featuring {features_text}. Perfect for modern living.",
        f"Stunning {property_type} located in the heart of {location}. Includes {features_text}.",
        f"Exceptional {property_type} in prime {location} location. Comes with {features_text}.",
        f"Charming {property_type} situated in {location}. Highlights include {features_text}.",
    ]
    return choice(templates)

def generate_sample_properties(count: int = 100) -> List[Property]:
    """Generate a list of sample properties with realistic Cyprus data"""
    properties = []
    
    for i in range(count):
        # Select basic property attributes
        property_type = choice(list(PROPERTY_TYPES.keys()))
        transaction_type = choice(["buy", "rent"])
        location = choice(CYPRUS_LOCATIONS)
        
        # Get price ranges based on property type and transaction
        type_info = PROPERTY_TYPES[property_type]
        if transaction_type == "rent":
            price = round(uniform(type_info["min_price_rent"], type_info["max_price_rent"]), -1)
        else:
            # Round to nearest thousand for sale prices
            price = round(uniform(type_info["min_price_buy"], type_info["max_price_buy"]), -3)
        
        # Generate features
        features = {k: uniform(0, 1) < v for k, v in FEATURES.items()}
        
        # Calculate reasonable room numbers
        bedrooms = randint(1, 4) if property_type != "studio" else 1
        bathrooms = min(bedrooms, randint(1, 3))
        
        # Calculate square feet based on property type
        square_feet = round(uniform(type_info["min_size"], type_info["max_size"]), 1)
        
        # Generate title
        area_desc = choice(["", "Central ", "Beachfront ", "Downtown ", "Suburban "])
        title = choice(type_info["titles"]).format(area_desc)
        
        # Select image
        image_url = f"{choice(PROPERTY_IMAGES[property_type])}?w=800"
        
        properties.append(Property(
            id=i + 1,
            title=title.strip(),
            type=property_type,
            transaction_type=transaction_type,
            price=price,
            location=location,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            square_feet=square_feet,
            description=generate_description(property_type, location, features),
            image_url=image_url,
            features=features
        ))
    
    return properties

# Generate the sample properties
SAMPLE_PROPERTIES = generate_sample_properties(100)