import streamlit as st
from app.models.property import Property
from typing import List

def display_property_carousel(properties: List[Property]):
    """Display properties in a carousel format"""
    if not properties:
        st.info("No properties match your current preferences.")
        return

    # Initialize carousel index in session state if not present
    if "carousel_index" not in st.session_state:
        st.session_state.carousel_index = 0

    # Create carousel navigation
    col1, col2, col3 = st.columns([1, 10, 1])
    
    with col1:
        if st.button("←", key="prev_main"):
            st.session_state.carousel_index = (st.session_state.carousel_index - 1) % len(properties)
            st.rerun()

    with col2:
        property = properties[st.session_state.carousel_index]
        
        st.markdown("""
            <style>
            .property-card {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 1rem;
                margin: 1rem 0;
                background-color: white;
            }
            .property-image {
                max-height: 300px;
                object-fit: cover;
                width: 100%;
                border-radius: 5px;
            }
            @media (max-width: 640px) {
                .property-image {
                    max-height: 200px;
                }
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="property-card">', unsafe_allow_html=True)
        st.markdown(f'<img src="{property.image_url}" class="property-image">', unsafe_allow_html=True)
        st.markdown(f"### {property.title}")
        st.markdown(f"### €{property.price:,.2f}")
        st.markdown(f"📍 **Location:** {property.location}")
        st.markdown(f"🏠 **Type:** {property.type.capitalize()}")
        st.markdown(f"🛏️ **{property.bedrooms}** beds • 🚿 **{property.bathrooms}** baths • 📐 **{property.square_feet:,.0f}** sq ft")
        
        with st.expander("✨ View Details"):
            st.write(property.description)
            if property.features:
                st.markdown("**Features:**")
                for feature, has_feature in property.features.items():
                    if has_feature:
                        st.markdown(f"✓ {feature.capitalize()}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f"*Property {st.session_state.carousel_index + 1} of {len(properties)}*")

    with col3:
        if st.button("→", key="next_main"):
            st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(properties)
            st.rerun() 