import streamlit as st

def initialize_session_state():
    """Initialize all session state variables"""
    if "lead_data" not in st.session_state:
        st.session_state["lead_data"] = None
        
    # Initialize property preferences
    if "transaction_type" not in st.session_state:
        st.session_state.transaction_type = None
    if "property_type" not in st.session_state:
        st.session_state.property_type = None
    if "location" not in st.session_state:
        st.session_state.location = None
    if "min_price" not in st.session_state:
        st.session_state.min_price = None
    if "max_price" not in st.session_state:
        st.session_state.max_price = None
    if "min_bedrooms" not in st.session_state:
        st.session_state.min_bedrooms = None