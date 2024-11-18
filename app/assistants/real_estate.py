import os
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.storage.assistant.postgres import PgAssistantStorage
from db.session import db_url
from typing import Optional
from app.models.property import filter_properties

# Initialize storage
real_estate_storage = PgAssistantStorage(
    table_name="real_estate_sessions",
    db_url=db_url
)

def get_real_estate_assistant(user_id: str) -> Assistant:
    """Create a specialized real estate assistant"""
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    system_prompt = """You are a helpful real estate assistant. Your goal is to understand 
    the client's needs and help them find their perfect property. Follow these guidelines:

    1. Gather essential information in a natural conversation:
       - Transaction type (buy or rent)
       - Property type (house, apartment, studio)
       - Location preference
       - Budget range (optional)
       - Number of bedrooms (optional)
    
    2. After each user response, extract any property preferences and output them in this exact JSON format:
       {{"property_preferences": {
         "transaction_type": "buy/rent",
         "property_type": "house/apartment/studio",
         "location": "downtown/suburbs/etc",
         "min_price": number,
         "max_price": number,
         "min_bedrooms": number
       }}}
    
    3. Only include fields in the JSON that were mentioned by the user.
    
    4. If any essential information is missing, ask about it naturally.
    
    5. Keep responses conversational but focused on gathering necessary details.
    
    Remember: Always output the preferences JSON after identifying any preferences, even if only one field is filled."""
    
    return Assistant(
        name="Real Estate Assistant",
        llm=OpenAIChat(
            model="gpt-4",
            api_key=api_key,
            max_tokens=500,
            temperature=0.7
        ),
        system_prompt=system_prompt + """
        IMPORTANT: Before responding, review the chat history to maintain context.
        If the user repeats information they've already provided, use it to confirm
        and update the preferences, don't ask for it again.
        
        Example:
        If user says "house" after already saying "buy", respond with both preferences:
        {"property_preferences": {
            "transaction_type": "buy",
            "property_type": "house"
        }}
        """,
        user_id=user_id,
        storage=real_estate_storage,
        show_tool_calls=True,
        read_chat_history=True,
        num_history_messages=10
    )