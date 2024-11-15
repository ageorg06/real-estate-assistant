import streamlit as st
from app.models.property import Property

def display_property_card(property: Property):
    """Display a property in a nice card format"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(
            "https://placehold.co/600x400",
            caption=property.title,
            use_column_width=True
        )
    
    with col2:
        st.subheader(property.title)
        st.write(f"**Price:** ${property.price:,.2f}")
        st.write(f"**Location:** {property.location}")
        st.write(f"**Type:** {property.type.capitalize()}")
        st.write(f"**Specs:** {property.bedrooms} beds, {property.bathrooms} baths, {property.square_feet:,.0f} sq ft")
        with st.expander("Description"):
            st.write(property.description)
            st.write("**Features:**")
            for feature, value in property.features.items():
                if value:
                    st.write(f"- {feature.capitalize()}")