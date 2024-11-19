import streamlit as st
from datetime import datetime
from typing import Optional
from app.models.lead import LeadData
from app.utils.validators import validate_email, validate_phone
from app.utils.auth import google_login

def capture_lead() -> Optional[LeadData]:
    """Lead capture form with validation"""
    st.header("🏠 Welcome to Real Estate Assistant")
    st.write("Let's find your perfect property! First, please tell us about yourself.")
    
    # Add Google Sign-in option
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("Quick sign up with Google:")
    with col2:
        google_login()
    
    st.markdown("---")
    st.write("Or fill in your details manually:")
    
    # Pre-fill form with Google data if available
    user_info = st.session_state.get("user_info") or {}
    
    with st.form("lead_capture", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*", value=user_info.get("name", ""))
        
        with col2:
            contact_type = st.selectbox(
                "Preferred Contact Method*",
                options=["Phone", "Email"],
                index=0
            )
        
        if "previous_contact_type" not in st.session_state:
            st.session_state.previous_contact_type = contact_type
        elif st.session_state.previous_contact_type != contact_type:
            st.session_state.contact_value = ""
            st.session_state.previous_contact_type = contact_type
        
        contact = st.text_input(
            f"Your {contact_type}*",
            value=st.session_state.get("contact_value", user_info.get("email", "") if contact_type == "Email" else ""),
            placeholder="99XXXXXX" if contact_type == "Phone" else "email@example.com"
        )
        
        if contact:
            st.session_state.contact_value = contact
        
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