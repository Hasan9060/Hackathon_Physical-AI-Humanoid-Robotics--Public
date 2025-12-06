# Backend API Documentation

## Overview

This backend serves the Physical AI & Humanoid Robotics Textbook with the following features:
- RAG-powered chatbot for textbook Q&A
- User authentication
- Prompt History Records (PHR) management
- Specifications (specs) management
- Website content serving (docs, components, static files)

## Base URL

```
http://localhost:8000
```

## Authentication

All endpoints (except `/signup` and `/login`) require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## API Endpoints

### Authentication

#### POST /signup
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "User Name",
  "software_background": "Your software experience",
  "hardware_background": "Your hardware experience",
  "learning_goals": "What you want to learn (optional)"
}
```

**Response:**
```json
{
  "access_token": "jwt-token",
  "token_type": "bearer",
  "user_profile": {
    "name": "User Name",
    "software": "Software background",
    "hardware": "Hardware background"
  }
}
```

#### POST /login
Login with existing credentials.

**Request Body (Form Data):**
- username: Email address
- password: Password

**Response:**
```json
{
  "access_token": "jwt-token",
  "token_type": "bearer",
  "user_profile": {
    "name": "User Name",
    "software": "Software background",
    "hardware": "Hardware background"
  }
}
```

### Chatbot

#### POST /query
Query the RAG-powered chatbot.

**Request Body:**
```json
{
  "question": "What is ROS 2?",
  "max_results": 5,
  "selected_text": "Optional selected text from document"
}
```

**Response:**
```json
{
  "answer": "ROS 2 is a Robot Operating System...",
  "sources": [
    {
      "id": "point-id",
      "score": 0.95,
      "text": "Relevant content",
      "metadata": {}
    }
  ],
  "confidence": 0.95
}
```

### Prompt History Records (PHR)

#### POST /phr/create
Create a new Prompt History Record.

**Request Body:**
```json
{
  "title": "PHR Title",
  "stage": "spec|plan|tasks|red|green|refactor|explainer|misc|general",
  "prompt_text": "The user's prompt",
  "response_text": "The AI's response",
  "surface": "agent",
  "model": "claude-3-opus",
  "feature": "feature-name",
  "branch": "main",
  "command": "slash-command",
  "labels": ["tag1", "tag2"],
  "links": {
    "spec": "url",
    "ticket": "url",
    "adr": "url",
    "pr": "url"
  },
  "files_yaml": ["file1.js", "file2.ts"],
  "tests_yaml": ["test1.js"],
  "outcome": "Result outcome",
  "evaluation": "Evaluation notes"
}
```

#### GET /phr/list
List PHRs with optional filtering.

**Query Parameters:**
- stage: Filter by stage (optional)
- feature: Filter by feature (optional)
- limit: Maximum number of results (default: 50)

**Response:**
```json
{
  "phrs": [
    {
      "id": "0001",
      "title": "PHR Title",
      "stage": "spec",
      "date_iso": "2024-01-01T00:00:00",
      "feature": "feature-name",
      "file_path": "path/to/phr",
      "preview": "First 100 characters..."
    }
  ],
  "count": 1,
  "stage_filter": "spec",
  "feature_filter": "feature-name"
}
```

#### POST /phr/search
Search PHRs by content.

**Request Body:**
```json
{
  "query": "search term",
  "stage": "spec (optional)",
  "feature": "feature-name (optional)",
  "limit": 50
}
```

#### GET /phr/{file_path}
Get a specific PHR by file path.

**Response:**
```json
{
  "metadata": {
    "id": "0001",
    "title": "PHR Title",
    "stage": "spec",
    "date_iso": "2024-01-01T00:00:00",
    "surface": "agent",
    "model": "claude-3-opus",
    "feature": "feature-name",
    "branch": "main",
    "user": "user@example.com",
    "command": "command",
    "labels": ["tag1"],
    "links": {},
    "files_yaml": ["file.js"],
    "tests_yaml": ["test.js"]
  },
  "content": {
    "prompt_text": "The prompt",
    "response_text": "The response",
    "outcome": "Result",
    "evaluation": "Notes"
  }
}
```

### Specifications (Specs)

#### GET /specs
Get all available specifications.

**Response:**
```json
{
  "specs": [
    {
      "id": "001-robotics-lab-guide",
      "name": "001 Robotics Lab Guide",
      "files": {
        "spec.md": "Specification content",
        "plan.md": "Plan content",
        "tasks.md": "Tasks content"
      }
    }
  ],
  "count": 1
}
```

#### GET /specs/{spec_id}
Get a specific specification by ID.

**Response:**
```json
{
  "id": "001-robotics-lab-guide",
  "name": "001 Robotics Lab Guide",
  "files": {
    "spec.md": "Content...",
    "plan.md": "Content...",
    "tasks.md": "Content..."
  }
}
```

### Website Content

#### GET /content/docs
List all documentation files.

**Response:**
```json
{
  "files": [
    "00-intro/overview.mdx",
    "01-ros2/fundamentals.mdx"
  ],
  "count": 2
}
```

#### GET /content/docs/{file_path}
Get documentation content.

**Response:**
```json
{
  "path": "00-intro/overview.mdx",
  "content": "Document content",
  "type": "markdown"
}
```

#### GET /content/components/{component_path}
Get React component content.

**Response:**
```json
{
  "path": "HomepageFeatures/index.tsx",
  "content": "Component code",
  "type": "react"
}
```

#### GET /content/static
List all static files.

**Response:**
```json
{
  "files": [
    "img/logo.svg",
    "css/custom.css"
  ],
  "count": 2
}
```

#### GET /content/static/{file_path}
Get static file content.

**For images:**
```json
{
  "path": "img/logo.svg",
  "content": "base64-encoded-image",
  "type": "image",
  "encoding": "base64"
}
```

**For text files:**
```json
{
  "path": "css/custom.css",
  "content": "CSS content",
  "type": "static"
}
```

## Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=sqlite:///./database.db

# JWT
SECRET_KEY=your-secret-key

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# Google Gemini
GEMINI_API_KEY=your-gemini-api-key

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION_NAME=robotics_book_embeddings

# Generation Settings
TEMPERATURE=0.7
MAX_TOKENS=1000
```

## Running the Backend

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up environment variables (see above)

3. Run the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, you can view the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`