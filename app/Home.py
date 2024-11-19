import streamlit as st
import logging
from dotenv import load_dotenv
from app.utils.state_management import initialize_session_state
from app.pages.lead_capture import capture_lead
from app.pages.property_search import property_search
from app.pages.appointment_booking import book_appointment
from app.utils.auth import init_google_auth, google_login
# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(
        page_title="Real Estate Assistant",
        page_icon="🏠",
        layout="centered"
    )
    
    # Initialize authentication and session state
    init_google_auth()
    initialize_session_state()
    
    # Show lead capture, appointment booking, or property search
    if st.session_state["lead_data"] is None:
        lead = capture_lead()
        if lead:
            st.success("Thank you! Let's schedule a meeting with our agent.")
            st.balloons()
            st.rerun()
    elif st.session_state["appointment_data"] is None:
        appointment = book_appointment()
        if appointment:
            st.success("Great! Your appointment has been scheduled.")
            st.balloons()
            st.rerun()
        elif appointment is False:  # Explicitly check for False to handle skipped case
            st.rerun()
    else:
        property_search()

if __name__ == "__main__":
    main()

