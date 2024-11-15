import streamlit as st
from typing import Optional, List, Dict
from dataclasses import dataclass
from datetime import datetime
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.storage.assistant.postgres import PgAssistantStorage
from db.session import db_url
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Data structures
@dataclass
class LeadData:
    name: str
    contact: str
    contact_type: str
    created_at: datetime

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

# Dummy property data
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
        image_url="https://www.google.com/imgres?q=house&imgurl=https%3A%2F%2Fimages.pexels.com%2Fphotos%2F106399%2Fpexels-photo-106399.jpeg%3Fauto%3Dcompress%26cs%3Dtinysrgb%26dpr%3D1%26w%3D500&imgrefurl=https%3A%2F%2Fwww.pexels.com%2Fsearch%2Fhouse%2F&docid=w_edFuvJNI2ApM&tbnid=34nSrA-03D_frM&vet=12ahUKEwix1OWVmN6JAxVzBdsEHeInHXwQM3oECBoQAA..i&w=500&h=333&hcb=2&ved=2ahUKEwix1OWVmN6JAxVzBdsEHeInHXwQM3oECBoQAA",
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
        image_url="https://www.google.com/imgres?q=house&imgurl=https%3A%2F%2Fpostandporch.com%2Fcdn%2Fshop%2Farticles%2FAdobeStock_209124760.jpg%3Fv%3D1662575433%26width%3D1440&imgrefurl=https%3A%2F%2Fpostandporch.com%2Fblogs%2Fnews%2Fyour-guide-to-modern-house-design&docid=nRObsuF3sXBXpM&tbnid=1guebcXJjy0DgM&vet=12ahUKEwix1OWVmN6JAxVzBdsEHeInHXwQM3oECGEQAA..i&w=1440&h=872&hcb=2&ved=2ahUKEwix1OWVmN6JAxVzBdsEHeInHXwQM3oECGEQAA",
        features={"garage": True, "garden": True}
    ),
    # Add more sample properties...
]

# Initialize storage
real_estate_storage = PgAssistantStorage(
    table_name="real_estate_sessions",
    db_url=db_url
)

def get_real_estate_assistant(user_id: str) -> Assistant:
    """Create a specialized real estate assistant"""
    
    system_prompt = """You are a helpful real estate assistant. Your goal is to understand 
    the client's needs and preferences to find their perfect property. 
    
    Follow these guidelines:
    1. Ask one question at a time about:
       - Whether they want to buy or rent
       - Property type preference (house, apartment, etc.)
       - Location preferences
       - Budget range
       - Number of bedrooms/bathrooms needed
    
    2. Keep track of their preferences and acknowledge them in your responses
    
    3. Be conversational but focused on gathering the necessary information
    
    4. Once you have collected the key preferences, summarize them and indicate you'll show matching properties
    """
    
    return Assistant(
        name="Real Estate Assistant",
        llm=OpenAIChat(
            model="gpt-4",  # or "gpt-3.5-turbo" for faster/cheaper responses
            max_tokens=500,
            temperature=0.7
        ),
        system_prompt=system_prompt,
        user_id=user_id,
        storage=real_estate_storage,
        show_tool_calls=True,
    )

def display_property_card(property: Property):
    """Display a property in a nice card format"""
    col1, col2 = st.columns([1, 2])
    uploaded_image = None
    with col1:
        st.image(
            "https://placehold.co/600x400",  # Placeholder image
            caption=property.title,
            use_column_width=True
        )
        logger.debug("Loading chat history")
    with col2:
        st.subheader(property.title)
        st.write(f"**Price:** ${property.price:,.2f}")
        st.write(f"**Location:** {property.location}")
        st.write(f"**Type:** {property.type.capitalize()}")
        st.write(f"**Specs:** {property.bedrooms} beds, {property.bathrooms} baths, {property.square_feet:,.0f} sq ft")
        with st.expander("Description"):
            st.write(property.description)
            st.write("**Features:**")
            for feature, value in property.features.items():
                if value:
                    st.write(f"- {feature.capitalize()}")

def property_search():
    """Property search conversation interface"""
    st.header(f"Welcome back, {st.session_state['lead_data'].name}! 👋")
    
    # Initialize chat messages if not in session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm here to help you find your perfect property. What kind of property are you looking for?"}
        ]
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Get user input
    if prompt := st.chat_input("Tell me about your property preferences..."):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        assistant = get_real_estate_assistant(st.session_state['lead_data'].name)
        with st.chat_message("assistant"):
            response_container = st.empty()
            full_response = ""
            
            try:
                # Stream the response
                for delta in assistant.run(prompt, stream=True):
                    if isinstance(delta, str):
                        full_response += delta
                        response_container.markdown(full_response + "▌")
                response_container.markdown(full_response)
                # Save the full response to chat history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error: {str(e)}")
                return
        
        # Show properties after collecting enough preferences
        if len(st.session_state.messages) >= 6:  # After a few interactions
            st.subheader("Based on your preferences, here are some properties you might like:")
            col1, col2 = st.columns(2)
            
            # Display properties in a grid
            for idx, property in enumerate(SAMPLE_PROPERTIES[:4]):
                with col1 if idx % 2 == 0 else col2:
                    display_property_card(property)

def validate_email(email: str) -> bool:
    """Basic email validation"""
    return "@" in email and "." in email.split("@")[1]

def validate_phone(phone: str) -> bool:
    """Basic phone number validation"""
    digits = ''.join(filter(str.isdigit, phone))
    return len(digits) >= 10

def capture_lead() -> Optional[LeadData]:
    """Lead capture form with validation"""
    
    st.header("🏠 Welcome to Real Estate Assistant")
    st.write("Let's find your perfect property! First, please tell us about yourself.")
    
    with st.form("lead_capture", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*")
        
        with col2:
            contact_type = st.selectbox(
                "Preferred Contact Method*",
                options=["Email", "Phone"]
            )
        
        contact = st.text_input(
            f"Your {contact_type}*",
            placeholder="Enter your contact information"
        )
        
        submitted = st.form_submit_button("Start Property Search", use_container_width=True)
        
        if submitted:
            # Validate inputs
            if not name:
                st.error("Please enter your name")
                return None
                
            if contact_type == "Email" and not validate_email(contact):
                st.error("Please enter a valid email address")
                return None
            elif contact_type == "Phone" and not validate_phone(contact):
                st.error("Please enter a valid phone number (minimum 10 digits)")
                return None
                
            # Create lead data
            lead = LeadData(
                name=name,
                contact=contact,
                contact_type=contact_type.lower(),
                created_at=datetime.now()
            )
            
            # Store in session state
            st.session_state["lead_data"] = lead
            return lead
            
    return None

def main():
    # Page config
    st.set_page_config(
        page_title="Real Estate Assistant",
        page_icon="🏠",
        layout="centered"
    )
    
    # Initialize session state
    if "lead_data" not in st.session_state:
        st.session_state["lead_data"] = None
        
    # Show lead capture if no lead data
    if st.session_state["lead_data"] is None:
        lead = capture_lead()
        if lead:
            st.success("Thank you! Let's find your perfect property.")
            st.balloons()
            # Add slight delay for better UX
            st.rerun()
    else:
        # Show property search interface
        property_search()

if __name__ == "__main__":
    main()
