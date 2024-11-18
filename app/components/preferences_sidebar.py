import streamlit as st
from datetime import datetime

def format_datetime(dt: datetime) -> str:
    """Format datetime for display"""
    return dt.strftime("%Y-%m-%d %H:%M")

def display_preferences_sidebar():
    """Display lead and appointment data in the sidebar"""
    with st.sidebar:
        st.header("Debug Info 🔍")
        
        # Lead Information
        st.subheader("Lead Data")
        lead_data = st.session_state.get("lead_data")
        if lead_data:
            st.write("Name:", lead_data.get("name"))
            st.write("Contact:", lead_data.get("contact"))
            st.write("Contact Type:", lead_data.get("contact_type"))
            if created_at := lead_data.get("created_at"):
                st.write("Created:", format_datetime(created_at))
        else:
            st.write("No lead data available")
            
        # Appointment Information
        st.markdown("---")
        st.subheader("Appointment Data")
        appointment_data = st.session_state.get("appointment_data")
        if appointment_data:
            if appointment_data.get("skipped"):
                st.write("Status: Skipped")
            else:
                st.write("Date:", format_datetime(appointment_data.get("date")))
                st.write("Time Slot:", appointment_data.get("time_slot"))
                st.write("Meeting Type:", appointment_data.get("meeting_type"))
                if notes := appointment_data.get("notes"):
                    st.write("Notes:", notes)
        else:
            st.write("No appointment data available")