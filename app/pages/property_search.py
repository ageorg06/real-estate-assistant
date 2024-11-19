import streamlit as st
from app.components.preferences_sidebar import display_preferences_sidebar
from app.components.chat_interface import initialize_chat, display_chat_interface
from app.utils.preferences import is_preferences_complete, display_matching_properties

def property_search():
    """Property search page with chat interface"""
    user_id = st.session_state.get('lead_data', {}).get('name', 'anonymous')
    st.header(f"🏠 Let's find your dream property, {user_id}! ")
    
    # Display debug sidebar
    display_preferences_sidebar()
    
    # Check if preferences are complete and display properties
    if is_preferences_complete():
        display_matching_properties()
    
    # Initialize and display chat interface
    initialize_chat(user_id)
    display_chat_interface()