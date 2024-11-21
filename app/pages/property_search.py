import streamlit as st
from app.components.preferences_sidebar import display_preferences_sidebar
from app.components.chat_interface import initialize_chat, display_chat_interface

def property_search():
    """Property search page with chat interface"""
    user_id = st.session_state.get('lead_data', {}).get('name', 'anonymous')
    st.header(f"🏠 Let's find your dream property, {user_id}! ")
    
    # Display sidebar with property matches
    # display_preferences_sidebar() # The sidebar is not needed for the property search
    
    # Initialize and display chat interface
    initialize_chat(user_id)
    display_chat_interface()