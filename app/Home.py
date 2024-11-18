import streamlit as st
from datetime import datetime
import logging
from typing import Optional
from dotenv import load_dotenv
import json

from app.models.lead import LeadData
from app.models.property import SAMPLE_PROPERTIES
from app.assistants.real_estate import get_real_estate_assistant
from app.components.property_card import display_property_card
from app.utils.validators import validate_email, validate_phone
from db.session import get_db

# Configure minimal logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()


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
            st.session_state["lead_data"] = lead.to_dict()
            return lead
            
    return None

def display_preferences_sidebar():
    """Display property preferences in the sidebar for debugging"""
    with st.sidebar:
        st.header("Debug: Property Preferences 🔍")
        
        # Display all preferences with their current values
        st.subheader("Required Fields")
        st.write("Transaction Type:", st.session_state.transaction_type)
        st.write("Property Type:", st.session_state.property_type)
        st.write("Location:", st.session_state.location)
        
        st.subheader("Optional Fields")
        st.write("Min Price:", st.session_state.min_price)
        st.write("Max Price:", st.session_state.max_price)
        st.write("Min Bedrooms:", st.session_state.min_bedrooms)
        
        # Add completion status
        st.markdown("---")
        st.subheader("Status")
        if is_preferences_complete():
            st.success("All required fields are set! ✅")
        else:
            st.warning("Missing fields: " + ", ".join(get_missing_preferences()))

def property_search():
    """Property search conversation interface"""
    user_id = st.session_state.get('lead_data', {}).get('name', 'anonymous')
    st.header(f"Welcome back, {user_id}! 👋")
    
    # Display debug sidebar
    display_preferences_sidebar()
    
    # Initialize state for chat
    if "assistant" not in st.session_state:
        st.session_state.assistant = get_real_estate_assistant(user_id)
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
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            response_container = st.empty()
            full_response = ""
            
            try:
                for delta in st.session_state.assistant.run(
                    prompt,
                    stream=True,
                    messages=st.session_state.messages[-6:],
                    user_id=user_id
                ):
                    if isinstance(delta, str):
                        full_response += delta
                        try:
                            if '"property_preferences"' in delta:
                                prefs = json.loads(full_response[
                                    full_response.rfind('{"property_preferences":'):
                                    full_response.find('}', full_response.rfind('}')) + 1
                                ])
                                
                                if "property_preferences" in prefs:
                                    # Update session state directly
                                    preferences_updated = False
                                    for key, value in prefs["property_preferences"].items():
                                        if key in ["transaction_type", "property_type", "location", 
                                                 "min_price", "max_price", "min_bedrooms"]:
                                            if st.session_state[key] != value:  # Only update if value changed
                                                st.session_state[key] = value
                                                preferences_updated = True
                                    
                                    if preferences_updated:
                                        st.toast(f"Updated preference: {key} = {value}", icon="✅")
                                        st.rerun()
                        except json.JSONDecodeError:
                            pass
                        
                        response_container.markdown(full_response + "▌")
                
                response_container.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error("An error occurred while processing your request.")
                
def display_matching_properties():
    """Display properties that match the current preferences"""
    filtered_properties = filter_properties(
        transaction_type=st.session_state.transaction_type,
        property_type=st.session_state.property_type,
        location=st.session_state.location,
        min_price=st.session_state.min_price,
        max_price=st.session_state.max_price,
        min_bedrooms=st.session_state.min_bedrooms
    )
    
    if filtered_properties:
        st.markdown("---")
        st.subheader("🏠 Matching Properties")
        tab1, tab2 = st.tabs(["Grid View", "List View"])
        with tab1:
            col1, col2 = st.columns(2)
            for idx, property in enumerate(filtered_properties[:4]):
                with col1 if idx % 2 == 0 else col2:
                    display_property_card(property)
        with tab2:
            for property in filtered_properties[:4]:
                display_property_card(property)

def initialize_property_preferences():
    """Initialize property preferences in session state if they don't exist"""
    # Required fields
    if "transaction_type" not in st.session_state:
        st.session_state.transaction_type = None
    if "property_type" not in st.session_state:
        st.session_state.property_type = None
    if "location" not in st.session_state:
        st.session_state.location = None
        
    # Optional fields
    if "min_price" not in st.session_state:
        st.session_state.min_price = None
    if "max_price" not in st.session_state:
        st.session_state.max_price = None
    if "min_bedrooms" not in st.session_state:
        st.session_state.min_bedrooms = None

def is_preferences_complete() -> bool:
    """Check if we have gathered essential preferences"""
    complete = all([
        st.session_state.transaction_type is not None,
        st.session_state.property_type is not None,
        st.session_state.location is not None,
    ])
    return complete

def get_missing_preferences() -> list[str]:
    """Return list of missing essential fields"""
    missing = []
    if not st.session_state.transaction_type:
        missing.append("transaction type (buy or rent)")
    if not st.session_state.property_type:
        missing.append("property type (house, apartment, etc)")
    if not st.session_state.location:
        missing.append("preferred location")
    return missing

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
        
    # Initialize property preferences
    initialize_property_preferences()
        
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

