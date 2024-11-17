import streamlit as st
from datetime import datetime
import logging
from typing import Optional
from dotenv import load_dotenv
import json
from dataclasses import asdict

from app.models.lead import LeadData
from app.models.property import SAMPLE_PROPERTIES
from app.assistants.real_estate import get_real_estate_assistant
from app.components.property_card import display_property_card
from app.utils.validators import validate_email, validate_phone
from app.models.conversation_state import PropertyPreferences
from db.session import get_db

# Configure minimal logging
logging.basicConfig(
    level=logging.WARNING,
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

def property_search():
    """Property search conversation interface"""
    user_id = st.session_state.get('lead_data', {}).get('name', 'anonymous')
    st.header(f"Welcome back, {user_id}! 👋")
    
    # Initialize or load preferences
    if "preferences" not in st.session_state:
        st.session_state.preferences = PropertyPreferences()
    
    # Initialize state
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
                                    for key, value in prefs["property_preferences"].items():
                                        if hasattr(st.session_state.preferences, key):
                                            setattr(st.session_state.preferences, key, value)
                                    st.session_state.preferences.save_to_storage(user_id)
                                    st.rerun()
                        except json.JSONDecodeError:
                            pass
                        
                        response_container.markdown(full_response + "▌")
                
                response_container.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error("An error occurred while processing your request.")

def display_matching_properties(prefs: PropertyPreferences):
    """Display properties that match the current preferences"""
    filtered_properties = filter_properties(
        transaction_type=prefs.transaction_type,
        property_type=prefs.property_type,
        location=prefs.location,
        min_price=prefs.min_price,
        max_price=prefs.max_price,
        min_bedrooms=prefs.min_bedrooms
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

