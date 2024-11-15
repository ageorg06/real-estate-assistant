import streamlit as st
from app.models.property import Property

def display_property_card(property: Property):
    """Display a property in a nice card format"""
    # Create a container with border and padding
    with st.container():
        # Add a border and padding using markdown
        st.markdown("""
            <style>
            .property-card {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 1rem;
                margin-bottom: 1rem;
                background-color: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            </style>
            """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div class="property-card">', unsafe_allow_html=True)
            
            # Image section
            st.image(
                property.image_url,
                caption=None,  # Remove caption as we'll show title below
                use_column_width=True
            )
            
            # Title and Price row
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"### {property.title}")
            with col2:
                st.markdown(f"<h3 style='color: #4CAF50;text-align: right'>${property.price:,.2f}</h3>", 
                          unsafe_allow_html=True)
            
            # Location and Type row
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"📍 **Location:** {property.location}")
            with col2:
                st.markdown(f"🏠 **Type:** {property.type.capitalize()}")
            
            # Specs row with icons
            st.markdown(f"🛏️ **{property.bedrooms}** beds • 🚿 **{property.bathrooms}** baths • 📐 **{property.square_feet:,.0f}** sq ft")
            
            # Features section
            with st.expander("✨ View Details"):
                st.write(property.description)
                st.markdown("**Features:**")
                # Create a grid of features
                feature_cols = st.columns(2)
                for idx, (feature, value) in enumerate(property.features.items()):
                    if value:
                        with feature_cols[idx % 2]:
                            st.markdown(f"✓ {feature.capitalize()}")
            
            st.markdown('</div>', unsafe_allow_html=True)