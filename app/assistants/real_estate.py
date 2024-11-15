import os
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.storage.assistant.postgres import PgAssistantStorage
from db.session import db_url

# Initialize storage
real_estate_storage = PgAssistantStorage(
    table_name="real_estate_sessions",
    db_url=db_url
)

def get_real_estate_assistant(user_id: str) -> Assistant:
    """Create a specialized real estate assistant"""
    
    # Get API key from environment or use a default (for development)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    system_prompt = """You are a helpful real estate assistant. Your goal is to understand 
    the client's needs and preferences to find their perfect property. 
    
    Follow these guidelines:
    1. Ask one question at a time about:
       - Whether they want to buy or rent
       - Property type preference (house, apartment, etc.)
       - Location preferences
       - Budget range
       - Number of bedrooms/bathrooms needed
    
    2. Keep track of their preferences and acknowledge them in your responses
    
    3. Be conversational but focused on gathering the necessary information
    """
    
    return Assistant(
        name="Real Estate Assistant",
        llm=OpenAIChat(
            model="gpt-4",
            api_key=api_key,
            max_tokens=500,
            temperature=0.7
        ),
        system_prompt=system_prompt,
        user_id=user_id,
        storage=real_estate_storage,
        show_tool_calls=True,
    )