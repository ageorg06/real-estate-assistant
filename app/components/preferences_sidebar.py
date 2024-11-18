import streamlit as st
from app.utils.property_filters import filter_properties
from app.components.property_card import display_property_card

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

def display_preferences_sidebar():
    """Display property preferences in the sidebar"""
    with st.sidebar:
        st.header("Debug: Property Preferences 🔍")
        
        st.subheader("Required Fields")
        st.write("Transaction Type:", st.session_state.transaction_type)
        st.write("Property Type:", st.session_state.property_type)
        st.write("Location:", st.session_state.location)
        
        st.subheader("Optional Fields")
        st.write("Min Price:", st.session_state.min_price)
        st.write("Max Price:", st.session_state.max_price)
        st.write("Min Bedrooms:", st.session_state.min_bedrooms)
        
        st.markdown("---")
        st.subheader("Status")
        if is_preferences_complete():
            st.success("All required fields are set! ✅")
        else:
            st.warning("Missing fields: " + ", ".join(get_missing_preferences()))

def display_matching_properties():
    """Display properties that match current preferences"""
    filtered_properties = filter_properties(
        transaction_type=st.session_state.transaction_type,
        property_type=st.session_state.property_type,
        location=st.session_state.location,
        min_price=st.session_state.min_price,
        max_price=st.session_state.max_price,
        min_bedrooms=st.session_state.min_bedrooms
    )
    
    if filtered_properties:
        st.markdown("---")
        st.subheader("🏠 Matching Properties")
        tab1, tab2 = st.tabs(["Grid View", "List View"])
        with tab1:
            col1, col2 = st.columns(2)
            for idx, property in enumerate(filtered_properties[:4]):
                with col1 if idx % 2 == 0 else col2:
                    display_property_card(property)
        with tab2:
            for property in filtered_properties[:4]:
                display_property_card(property)