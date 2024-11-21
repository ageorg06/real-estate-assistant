# Real Estate Assistant 🏠

A real estate assistant application built with Streamlit and PHIdata that helps qualify leads and match properties through natural conversation. The application includes lead capture, appointment booking, and AI-powered property search features.

## Prerequisites

- Python 3.9 or higher
- Docker (for database and workspace)
- OpenAI API key
- Google OAuth credentials (for authentication)
- PHIdata CLI([1](https://docs.phidata.com/cli/installation))

## Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd real-estate-assistant
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the root directory with:
```bash
OPENAI_API_KEY=your_openai_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
REDIRECT_URI=http://localhost:8501
PHI_API_KEY=your_phi_api_key  # Get from PHIdata dashboard
```

5. **Start the PHI workspace**
```bash
# Start development workspace
phi ws up

# To start production workspace
phi ws up prd
```

This command will:
- Start the PostgreSQL database with pgvector
- Run database migrations
- Start the Streamlit application
- Set up the development environment

The application will be available at `http://localhost:8501`

6. **Stop the workspace**
```bash
phi ws down  # For development
phi ws down prd  # For production
```

## Project Structure

- `app/`: Main application code
  - `Home.py`: Main entry point
  - `pages/`: Different pages of the application
  - `components/`: Reusable UI components
  - `utils/`: Utility functions
  - `models/`: Data models
  - `assistants/`: AI assistant configurations
- `db/`: Database configurations and migrations
- `workspace/`: PHIdata workspace configurations([2](https://docs.phidata.com/reference/workspace))
  - `dev_resources.py`: Development environment setup
  - `prd_resources.py`: Production environment setup
- `agents/`: AI agent configurations

## Features

1. **Lead Capture**
   - Contact information collection
   - Form validation
   - Google OAuth authentication

2. **Appointment Booking**
   - Schedule meetings with agents
   - Time slot selection
   - Appointment management

3. **Property Search**
   - AI-powered conversation interface
   - Property filtering and matching
   - Property carousel display

## Development Notes

- The application uses Streamlit for the frontend([3](https://docs.streamlit.io/))
- PostgreSQL with pgvector is used for the database
- PHIdata is used for AI assistant and agent management([4](https://docs.phidata.com/templates/ai-apps))
- The project includes Docker configurations for production deployment
- Workspace management is handled by PHIdata([5](https://docs.phidata.com/reference/workspace-settings))

## Troubleshooting

1. **Workspace Issues**
   - Check workspace logs: `phi ws logs`
   - Verify workspace status: `phi ws status`
   - Restart workspace: `phi ws restart`

2. **Database Connection Issues**
   - Verify PostgreSQL is running: `docker ps`
   - Check database credentials in workspace secrets
   - Ensure migrations are up to date

3. **Authentication Issues**
   - Verify Google OAuth credentials
   - Check redirect URI configuration
   - Ensure environment variables are set correctly

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the Mozilla Public License Version 2.0 - see the LICENSE file for details.