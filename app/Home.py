import streamlit as st
from typing import Optional
from dataclasses import dataclass
from datetime import datetime
from phi.assistant import Assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from db.session import db_url

# Data structure for leads
@dataclass
class LeadData:
    name: str
    contact: str
    contact_type: str
    created_at: datetime

# Initialize storage
real_estate_storage = PgAssistantStorage(
    table_name="real_estate_sessions",
    db_url=db_url
)

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
        st.header(f"Welcome back, {st.session_state['lead_data'].name}! 👋")
        
        # Add restart button in sidebar
        if st.sidebar.button("Start New Search"):
            st.session_state["lead_data"] = None
            st.rerun()
            
        # Property search implementation will go here
        st.info("Property search coming soon!")

if __name__ == "__main__":
    main()
