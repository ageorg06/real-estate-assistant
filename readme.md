
# Real Estate Assistant

An AI-powered real estate assistant built with PHIdata that helps qualify leads and match properties through natural conversation.

## Features

### 1. Lead Generation
- Capture essential contact information
  - Name
  - Email/Phone (with validation)
- Required before proceeding with property search

### 2. Property Matching
- Natural conversation flow for collecting preferences
- Property filtering based on:
  - Transaction type (Buy/Rent)
  - Property type (House/Apartment/Field)
  - Location
  - Budget range
  - Additional preferences
- Display 4 best matches in carousel format

### 3. Technical Stack
- Framework: PHIdata
- Frontend: Streamlit
- Database: PostgreSQL with pgvector
- Container: Docker

## Project Structure

tree -L 3
.
├── Dockerfile
├── LICENSE
├── README.md
├── agents
│   ├── __init__.py
│   ├── example.py
│   ├── settings.py
│   └── test
│       ├── __init__.py
│       └── example_agent.py
├── api
│   ├── __init__.py
│   ├── main.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── health.py
│   │   ├── playground.py
│   │   └── v1_router.py
│   └── settings.py
├── app
│   ├── Home.py
│   └── __init__.py
├── db
│   ├── README.md
│   ├── __init__.py
│   ├── alembic.ini
│   ├── migrations
│   │   ├── README
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   ├── session.py
│   ├── settings.py
│   └── tables
│       ├── __init__.py
│       └── base.py
├── example.env
├── pyproject.toml
├── requirements.txt
├── scripts
│   ├── _utils.sh
│   ├── auth_ecr.sh
│   ├── build_dev_image.sh
│   ├── build_prd_image.sh
│   ├── entrypoint.sh
│   ├── format.sh
│   ├── generate_requirements.sh
│   ├── install.sh
│   ├── test.sh
│   └── validate.sh
├── tests
│   ├── __init__.py
│   └── evals
│       └── test_haiku.py
├── utils
│   ├── __init__.py
│   ├── dttm.py
│   └── log.py
└── workspace
    ├── __init__.py
    ├── __pycache__
    │   └── settings.cpython-313.pyc
    ├── dev_resources.py
    ├── example_secrets
    │   ├── dev_app_secrets.yml
    │   ├── prd_app_secrets.yml
    │   └── prd_db_secrets.yml
    ├── prd_resources.py
    ├── secrets
    │   ├── dev_app_secrets.yml
    │   ├── prd_app_secrets.yml
    │   └── prd_db_secrets.yml
    └── settings.py

18 directories, 56 files

## Setup Instructions

1. **Create Virtual Environment**
```bash
python3 -m venv ~/.venvs/aienv
source ~/.venvs/aienv/activate
```

2. **Install Dependencies**
```bash
pip install -U phidata openai pgvector streamlit "psycopg[binary]" sqlalchemy
```

3. **Run Database**
```bash
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -p 5532:5432 \
  --name pgvector \
  phidata/pgvector:16
```

4. **Set OpenAI API Key**
```bash
export OPENAI_API_KEY=your-key-here
```

5. **Run Application**
```bash
streamlit run app/main.py
```

## Development Guidelines
- Follow PEP 8 standards
- Add docstrings for functions/classes
- Test conversation flows thoroughly
```

# PRD.md
```markdown
# Real Estate Assistant PRD

## 1. Overview

### Purpose
Create an AI-powered real estate assistant that captures leads and helps users find suitable properties through natural conversation.

### MVP Scope
- Lead capture system
- Natural language property search
- Basic property matching
- Property display interface

## 2. Functional Requirements

### 2.1 Lead Capture (Priority: High)
- **Required Fields:**
  - Name
  - Contact (email or phone)
- **Validation:**
  - Standard email format
  - Standard phone number format
- **Flow:**
  - Must complete before property search
  - Simple form interface
  - Validation feedback

### 2.2 Property Search (Priority: High)
- **Conversation Flow:**
  - Natural language interaction
  - Progressive information gathering
  - Flexible order of questions
- **Search Criteria:**
  - Transaction type (buy/rent)
  - Property type (house/apartment/field)
  - Location
  - Budget range
  - Number of bedrooms (optional)

### 2.3 Results Display (Priority: High)
- **Format:**
  - Carousel display
  - 4 properties maximum
  - Responsive design
- **Property Card:**
  - Primary image
  - Price
  - Location
  - Key features
  - Square footage
  - Bedrooms/bathrooms

## 3. Technical Requirements

### 3.1 Database Schema
```sql
-- Properties Table
CREATE TABLE properties (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    type VARCHAR(50),
    transaction_type VARCHAR(20),
    price DECIMAL(12,2),
    location VARCHAR(255),
    bedrooms INTEGER,
    bathrooms INTEGER,
    square_feet DECIMAL(10,2),
    description TEXT,
    image_url VARCHAR(255),
    features JSONB
);

-- Leads Table
CREATE TABLE leads (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    contact VARCHAR(255),
    contact_type VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3.2 Performance Requirements
- Response time < 3 seconds
- Support for concurrent users
- Graceful error handling

## 4. MVP Development Phases

### Phase 1: Setup (Week 1)
- [ ] Environment configuration
- [ ] Database setup
- [ ] Basic Streamlit interface

### Phase 2: Lead Capture (Week 1)
- [ ] Contact form implementation
- [ ] Validation logic
- [ ] Lead storage system

### Phase 3: Property Search (Week 2)
- [ ] Conversation flow
- [ ] Property matching logic
- [ ] Results display

### Phase 4: Testing (Week 2)
- [ ] Unit testing
- [ ] Conversation flow testing
- [ ] UI/UX refinement
```
