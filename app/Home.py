import streamlit as st
import logging
from dotenv import load_dotenv
from app.utils.state_management import initialize_session_state
from app.pages.lead_capture import capture_lead
from app.pages.property_search import property_search

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
    
    # Initialize session state
    initialize_session_state()
    
    # Show lead capture or property search
    if st.session_state["lead_data"] is None:
        lead = capture_lead()
        if lead:
            st.success("Thank you! Let's find your perfect property.")
            st.balloons()
            st.rerun()
    else:
        property_search()

if __name__ == "__main__":
    main()

