import streamlit as st
from app.models.property import Property
from app.components.property_card import display_property_card
from app.utils.preferences import is_preferences_complete
from app.utils.property_filters import filter_properties

def display_preferences_sidebar():
    """Display property cards in the sidebar"""
    with st.sidebar:
        st.header("Matching Properties 🏠")
        
        # Check if preferences are complete and filter properties
        if is_preferences_complete():
            properties = filter_properties(
                transaction_type=st.session_state.transaction_type,
                property_type=st.session_state.property_type,
                location=st.session_state.location,
                min_price=st.session_state.min_price,
                max_price=st.session_state.max_price,
                min_bedrooms=st.session_state.min_bedrooms
            )
            
            if properties:
                for property in properties:
                    with st.container():
                        st.markdown("""
                            <style>
                            .sidebar-property-card {
                                border: 1px solid #ddd;
                                border-radius: 10px;
                                padding: 0.5rem;
                                margin-bottom: 0.5rem;
                                background-color: white;
                                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                            }
                            </style>
                            """, unsafe_allow_html=True)
                        
                        with st.container():
                            st.markdown('<div class="sidebar-property-card">', unsafe_allow_html=True)
                            
                            # Image
                            st.image(property.image_url, use_column_width=True)
                            
                            # Title and Price
                            st.markdown(f"#### {property.title}")
                            st.markdown(f"**€{property.price:,.2f}**")
                            
                            # Basic Info
                            st.markdown(f"📍 {property.location}")
                            st.markdown(f"🏠 {property.type.capitalize()}")
                            st.markdown(f"🛏️ {property.bedrooms} beds • 🚿 {property.bathrooms} baths")
                            
                            # View Details button
                            with st.expander("View Details"):
                                st.write(property.description)
                                st.markdown("**Features:**")
                                for feature, value in property.features.items():
                                    if value:
                                        st.markdown(f"✓ {feature.capitalize()}")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No properties match your current preferences.")
        else:
            st.info("Complete your preferences to see matching properties.")