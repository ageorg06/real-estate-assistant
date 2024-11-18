import streamlit as st
from datetime import datetime, timedelta
from typing import Optional
from app.models.appointment import AppointmentData

def get_available_time_slots():
    """Generate available time slots between 9 AM and 5 PM"""
    return [
        "09:00 AM", "10:00 AM", "11:00 AM",
        "12:00 PM", "01:00 PM", "02:00 PM",
        "03:00 PM", "04:00 PM", "05:00 PM"
    ]

def book_appointment() -> Optional[AppointmentData]:
    """Appointment booking interface with validation"""
    st.header("📅 Schedule a Meeting with Our Agent")
    st.write("Let's schedule a time to discuss your property needs!")

    with st.form("appointment_booking", clear_on_submit=False):
        meeting_type = st.radio(
            "How would you like to meet?*",
            options=["Video Call", "Phone Call", "In-Person"],
            horizontal=True
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            min_date = datetime.now().date() + timedelta(days=1)
            max_date = min_date + timedelta(days=30)
            date = st.date_input(
                "Select a Date*",
                min_value=min_date,
                max_value=max_date,
                value=min_date
            )
        
        with col2:
            time_slot = st.selectbox(
                "Select a Time Slot*",
                options=get_available_time_slots()
            )
        
        notes = st.text_area(
            "Additional Notes",
            placeholder="Any specific topics you'd like to discuss?",
            max_chars=500
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            submitted = st.form_submit_button(
                "Schedule Appointment",
                use_container_width=True,
                type="primary"
            )
        with col2:
            skip = st.form_submit_button(
                "Skip",
                use_container_width=True,
                type="secondary"
            )
        
        if submitted:
            appointment = AppointmentData(
                date=datetime.combine(date, datetime.min.time()),
                time_slot=time_slot,
                meeting_type=meeting_type,
                notes=notes if notes else None
            )
            
            st.session_state["appointment_data"] = appointment.to_dict()
            return appointment
            
        if skip:
            st.session_state["appointment_data"] = {"skipped": True}
            return False
            
    return None