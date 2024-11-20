import streamlit as st

def is_preferences_complete() -> bool:
    """Check if essential preferences are complete"""
    return all([
        st.session_state.transaction_type is not None,
        st.session_state.property_type is not None,
        st.session_state.location is not None,
    ])

def get_missing_preferences() -> list[str]:
    """Return list of missing essential fields"""
    missing = []
    if not st.session_state.transaction_type:
        missing.append("transaction type (buy or rent)")
    if not st.session_state.property_type:
        missing.append("property type (house, apartment, etc)")
    if not st.session_state.location:
        missing.append("preferred location")
    return missing

def get_matching_properties():
    """Get matching properties based on preferences"""
    from app.utils.property_filters import filter_properties
    
    return filter_properties(
        transaction_type=st.session_state.transaction_type,
        property_type=st.session_state.property_type,
        location=st.session_state.location,
        min_price=st.session_state.min_price,
        max_price=st.session_state.max_price,
        min_bedrooms=st.session_state.min_bedrooms
    )

def display_matching_properties():
    """Display matching properties based on preferences"""
    from app.components.property_card import display_property_card
    
    properties = get_matching_properties()
    
    if properties:
        st.subheader("🏠 Matching Properties")
        for property in properties:
            display_property_card(property)
    else:
        st.info("No properties match your current preferences.")