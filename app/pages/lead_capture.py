import streamlit as st
from datetime import datetime
from typing import Optional
from app.models.lead import LeadData
from app.utils.validators import validate_email, validate_phone

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
            if not name:
                st.error("Please enter your name")
                return None
                
            if contact_type == "Email" and not validate_email(contact):
                st.error("Please enter a valid email address")
                return None
            elif contact_type == "Phone" and not validate_phone(contact):
                st.error("Please enter a valid phone number (minimum 10 digits)")
                return None
                
            lead = LeadData(
                name=name,
                contact=contact,
                contact_type=contact_type.lower(),
                created_at=datetime.now()
            )
            
            st.session_state["lead_data"] = lead.to_dict()
            return lead
            
    return None