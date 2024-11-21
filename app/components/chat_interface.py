import streamlit as st
import json
import logging
from app.assistants.real_estate import get_real_estate_assistant
from app.utils.preferences import is_preferences_complete, display_matching_properties, get_matching_properties
from typing import Optional
from app.components.property_carousel import display_property_carousel

logger = logging.getLogger(__name__)

def initialize_chat(user_id: str):
    """Initialize chat state"""
    if "assistant" not in st.session_state:
        st.session_state.assistant = get_real_estate_assistant(user_id)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm here to help you find your perfect property. What kind of property are you looking for?"}
        ]
    if "current_properties" not in st.session_state:
        st.session_state.current_properties = None

def process_preferences_json(json_text: str) -> tuple[bool, str, Optional[str]]:
    """Process JSON preferences from assistant response and return (has_json, message, json_str)"""
    try:
        # Look for JSON object anywhere in the text
        json_start = json_text.find('{')
        if json_start == -1:
            return False, json_text, None
            
        # Find complete JSON object
        brace_count = 0
        json_end = -1
        for i in range(json_start, len(json_text)):
            if json_text[i] == '{':
                brace_count += 1
            elif json_text[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    json_end = i + 1
                    break
        
        if json_end == -1:
            return False, json_text, None
            
        # Split message and JSON
        message = json_text[:json_start].strip()
        json_str = json_text[json_start:json_end].strip()
        
        try:
            prefs = json.loads(json_str)
        except json.JSONDecodeError:
            return False, json_text, None
        
        if "property_preferences" in prefs:
            updated_fields = []
            for key, value in prefs["property_preferences"].items():
                if key in ["transaction_type", "property_type", "location", 
                         "min_price", "max_price", "min_bedrooms"]:
                    if st.session_state.get(key) != value:
                        st.session_state[key] = value
                        updated_fields.append(f"{key}: {value}")
            
            if updated_fields:
                st.toast(
                    "Updated preferences:\n" + "\n".join(updated_fields),
                    icon="✅"
                )
                
            return True, message, json_str
                
    except Exception as e:
        logger.debug(f"Error processing preferences: {e}")
    return False, json_text, None

def display_chat_interface():
    """Display and handle chat interface"""
    # Initialize carousel visibility state if not present
    if "show_properties" not in st.session_state:
        st.session_state.show_properties = True
    
    # Display chat messages first
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message.get("content"):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Tell me about your property preferences..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            response_container = st.empty()
            full_response = ""
            
            try:
                for delta in st.session_state.assistant.run(
                    prompt,
                    stream=True,
                    messages=st.session_state.messages[-6:],
                    user_id=st.session_state.get('lead_data', {}).get('name', 'anonymous')
                ):
                    full_response += delta
                
                # Process message and JSON separately but only display message
                has_json, message, json_str = process_preferences_json(full_response)
                if has_json:
                    if message:  # Only update message if we have conversational content
                        response_container.markdown(message)
                    
                    message_data = {
                        "role": "assistant",
                        "content": message if message else None,
                        "json": json_str
                    }
                    
                    # If preferences are complete, update properties
                    if is_preferences_complete():
                        properties = get_matching_properties()
                        if properties:
                            st.session_state.current_properties = properties
                            message_data["properties"] = properties
                    
                    st.session_state.messages.append(message_data)
                else:
                    response_container.markdown(full_response)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": full_response
                    })
            except Exception as e:
                logger.error(f"Error processing response: {e}")
                response_container.error("I encountered an error processing your request.")
    
    # Display property carousel at the bottom if properties exist
    if st.session_state.current_properties:
        st.markdown("---")  # Add a visual separator
        
        # Add toggle for carousel visibility
        col1, col2 = st.columns([10, 2])
        with col1:
            st.markdown("### 🏠 Matching Properties")
        with col2:
            st.session_state.show_properties = st.toggle(
                "Show Properties",
                value=st.session_state.show_properties,
                key="property_toggle"
            )
        
        if st.session_state.show_properties:
            with st.container():
                display_property_carousel(st.session_state.current_properties)