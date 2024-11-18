import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import os
import json
from urllib.parse import urlencode

# OAuth 2.0 client configuration
CLIENT_CONFIG = {
    "web": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [os.getenv("REDIRECT_URI", "http://localhost:8501")]
    }
}

def init_google_auth():
    """Initialize Google OAuth flow"""
    if 'google_auth' not in st.session_state:
        st.session_state.google_auth = None
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    
    # Handle OAuth callback
    if 'code' in st.query_params:
        handle_oauth_callback(st.query_params['code'])

def google_login():
    """Start Google OAuth flow"""
    flow = Flow.from_client_config(
        client_config=CLIENT_CONFIG,
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
    )
    
    # Get the current URL
    redirect_uri = os.getenv("REDIRECT_URI", "http://localhost:8501")
    
    # Explicitly set the redirect URI
    flow.redirect_uri = redirect_uri
    
    # Store the redirect URI in session state for the callback
    st.session_state['oauth_redirect_uri'] = redirect_uri
    
    # Generate authorization URL with state
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        state=st.session_state.get('google_auth_state', ''),
        prompt='consent'
    )
    
    st.markdown(f'<a href="{authorization_url}" target="_self"><button>Login with Google</button></a>', unsafe_allow_html=True)

def handle_oauth_callback(code: str):
    """Handle the OAuth callback"""
    try:
        flow = Flow.from_client_config(
            client_config=CLIENT_CONFIG,
            scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
            state=st.session_state.get('google_auth_state', '')
        )
        
        flow.redirect_uri = st.session_state.get('oauth_redirect_uri', os.getenv("REDIRECT_URI", "http://localhost:8501"))
        
        flow.fetch_token(code=code)
        credentials = flow.credentials
        
        user_info = get_user_info(credentials)
        if user_info:
            st.session_state.google_auth = credentials
            st.session_state.user_info = user_info
            
            # Create lead data from Google user info
            from app.models.lead import LeadData
            from datetime import datetime
            
            # Split full name into parts (if available)
            full_name = user_info.get('name', '')
            
            lead = LeadData(
                name=full_name,
                contact=user_info.get('email', ''),
                contact_type='email',
                created_at=datetime.now()
            )
            
            st.session_state["lead_data"] = lead.to_dict()
            
            # Clear query parameters and refresh
            st.query_params.clear()
            st.rerun()
    except Exception as e:
        st.error(f"Authentication failed: {str(e)}")

def get_user_info(credentials):
    """Fetch user info from Google"""
    import requests
    
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    headers = {'Authorization': f'Bearer {credentials.token}'}
    
    response = requests.get(userinfo_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None