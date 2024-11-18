import streamlit as st
import json
import logging
from app.assistants.real_estate import get_real_estate_assistant
from app.utils.preferences import is_preferences_complete, display_matching_properties

logger = logging.getLogger(__name__)

def initialize_chat(user_id: str):
    """Initialize chat state"""
    if "assistant" not in st.session_state:
        st.session_state.assistant = get_real_estate_assistant(user_id)
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi! I'm here to help you find your perfect property. What kind of property are you looking for?"}
        ]

def process_preferences_json(json_text: str) -> bool:
    """Process JSON preferences from assistant response"""
    try:
        json_start = json_text.find('{"property_preferences":')
        if json_start == -1:
            return False
            
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
            return False
            
        prefs_json = json_text[json_start:json_end]
        prefs = json.loads(prefs_json)
        
        if "property_preferences" in prefs:
            updated_fields = []
            for key, value in prefs["property_preferences"].items():
                if key in ["transaction_type", "property_type", "location", 
                         "min_price", "max_price", "min_bedrooms"]:
                    if st.session_state[key] != value:
                        st.session_state[key] = value
                        updated_fields.append(f"{key}: {value}")
            
            if updated_fields:
                st.toast(
                    "Updated preferences:\n" + "\n".join(updated_fields),
                    icon="✅"
                )
                return True
                
    except Exception as e:
        logger.debug(f"Error processing preferences: {e}")
    return False

def display_chat_interface():
    """Display and handle chat interface"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
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
                    if isinstance(delta, str):
                        full_response += delta
                        response_container.markdown(full_response + "▌")
                
                response_container.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                if '"property_preferences"' in full_response:
                    if process_preferences_json(full_response):
                        if is_preferences_complete():
                            display_matching_properties()
                        st.rerun()
                        
            except Exception as e:
                st.error("An error occurred while processing your request.")
                logger.debug(f"Request error: {e}")