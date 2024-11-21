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

    st.markdown("""
        <style>
        .property-card {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 0.75rem;
            margin: 0.5rem 0;
            background-color: white;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        .property-image {
            max-height: 200px;
            object-fit: cover;
            width: 100%;
            border-radius: 5px;
            margin-top: 0;
        }
        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.5rem;
            background: transparent;
            position: absolute;
            width: 100%;
            z-index: 1;
            pointer-events: none;
        }
        .nav-button {
            background-color: rgba(255, 255, 255, 0.8);
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            pointer-events: auto;
            transition: background-color 0.3s;
        }
        .nav-button:hover {
            background-color: rgba(255, 255, 255, 0.9);
        }
        .property-counter {
            background-color: rgba(0, 0, 0, 0.5);
            color: white;
            padding: 0.2rem 0.5rem;
            border-radius: 12px;
            font-size: 0.8rem;
            pointer-events: auto;
        }
        @media (max-width: 640px) {
            .property-card {
                padding: 0.5rem;
                margin: 0.3rem 0;
                max-width: 100%;
            }
            .property-image {
                max-height: 150px;
            }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Property card with navigation overlay
    property = properties[st.session_state.carousel_index]
    st.markdown('<div class="property-card">', unsafe_allow_html=True)
    
    # Create columns for navigation and counter
    col1, col2, col3 = st.columns([1, 10, 1])
    
    # Navigation overlay
    with col1:
        if st.button("←", key="prev_main", use_container_width=True):
            st.session_state.carousel_index = (st.session_state.carousel_index - 1) % len(properties)
            st.rerun()
    
    with col2:
        st.markdown(f'<img src="{property.image_url}" class="property-image">', unsafe_allow_html=True)
        st.markdown(f'<div style="text-align: center; font-size: 0.8rem; color: #666;">Property {st.session_state.carousel_index + 1} of {len(properties)}</div>', unsafe_allow_html=True)
    
    with col3:
        if st.button("→", key="next_main", use_container_width=True):
            st.session_state.carousel_index = (st.session_state.carousel_index + 1) % len(properties)
            st.rerun()

    # Property details
    st.markdown(f'<div class="property-title">{property.title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="property-price">€{property.price:,.2f}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="property-details">📍 Location: {property.location}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="property-details">🏠 Type: {property.type.capitalize()}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="property-details">🛏️ {property.bedrooms} beds • 🚿 {property.bathrooms} baths • 📐 {property.square_feet:,.0f} sq ft</div>', unsafe_allow_html=True)
    
    # Details section with proper markdown
    with st.expander("✨ View Details"):
        st.write(property.description)
        if property.features:
            st.markdown("### Features")
            cols = st.columns(2)
            for idx, (feature, has_feature) in enumerate(property.features.items()):
                if has_feature:
                    with cols[idx % 2]:
                        st.markdown(f"✓ {feature.capitalize()}")
    
    st.markdown('</div>', unsafe_allow_html=True) 