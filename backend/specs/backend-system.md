---
title: Backend System Specification
description: Complete backend API specification for Physical AI & Humanoid Robotics Textbook
stage: spec
surface: backend
model: claude-3-opus-20250215
user: hasanrafay
branch: main
labels: ["backend", "api", "spec-driven", "authentication", "rag", "phr", "specs"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
---

# Backend System Specification

## 1. Overview

The backend system provides a comprehensive API for the Physical AI & Humanoid Robotics Textbook, featuring RAG-powered chatbot, user authentication, prompt history management, and content serving capabilities.

### 1.1 Key Components

- **FastAPI Application**: High-performance async web framework
- **Authentication System**: JWT-based user authentication with SQLAlchemy
- **RAG Chatbot**: Qdrant + OpenAI embeddings + Gemini generation
- **PHR Service**: Prompt History Records management with YAML persistence
- **Content Management**: Serve website content (docs, components, static files)
- **Specifications Storage**: Access to project specifications

## 2. Architecture

### 2.1 Technology Stack

```python
# Core Framework
FastAPI 0.104+
Python 3.12+

# Database
SQLAlchemy 2.0+
SQLite (development), PostgreSQL (production)

# Authentication
python-jose (JWT)
python-multipart
passlib (bcrypt)

# Vector Database & AI
qdrant-client
openai
google-generativeai

# Additional Libraries
pydantic
python-dotenv
uvicorn
```

### 2.2 Directory Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── auth_server.py          # Alternative auth server
├── database/
│   ├── db.py              # Database connection and session management
│   ├── models.py          # SQLAlchemy models
│   └── __init__.py
├── services/
│   ├── auth_service.py    # Authentication business logic
│   ├── rag_service.py     # RAG chatbot logic
│   ├── embedding_service.py # Text embedding service
│   └── phr_service.py     # Prompt History Records management
├── src/                   # Copied website source code
│   └── components/
├── docs/                  # Copied documentation
├── static/                # Copied static files
├── specs/                 # Project specifications
│   └── 001-robotics-lab-guide/
├── history/
│   └── prompts/           # Prompt History Records
│       ├── constitution/
│       ├── 001-robotics-lab-guide/
│       └── general/
├── requirements.txt       # Python dependencies
├── package.json          # Node.js dependencies (for TypeScript)
└── README.md             # API documentation
```

## 3. API Endpoints Specification

### 3.1 Authentication Endpoints

#### POST /signup
- **Purpose**: Register new user account
- **Authentication**: None
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securePassword123",
    "name": "Full Name",
    "software_background": "Description of software experience",
    "hardware_background": "Description of hardware experience",
    "learning_goals": "Optional learning objectives"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "jwt-token-string",
    "token_type": "bearer",
    "user_profile": {
      "name": "User's name",
      "software": "Software background",
      "hardware": "Hardware background"
    }
  }
  ```
- **Error Codes**:
  - 400: Email already registered
  - 422: Validation error

#### POST /login
- **Purpose**: Authenticate existing user
- **Authentication**: None
- **Request Body** (form-data):
  - username: Email address
  - password: Plain text password
- **Response**: Same as /signup
- **Error Codes**:
  - 401: Invalid credentials

### 3.2 Chatbot Endpoints

#### POST /query
- **Purpose**: Query RAG-powered chatbot
- **Authentication**: Required (Bearer token)
- **Request Body**:
  ```json
  {
    "question": "What is ROS 2?",
    "max_results": 5,
    "selected_text": "Optional highlighted text"
  }
  ```
- **Response**:
  ```json
  {
    "answer": "Generated answer based on context",
    "sources": [
      {
        "id": "vector-id",
        "score": 0.95,
        "text": "Relevant textbook content",
        "metadata": {
          "module": "ROS 2 Fundamentals",
          "file": "fundamentals.mdx"
        }
      }
    ],
    "confidence": 0.92
  }
  ```
- **Features**:
  - Handles vague inputs (greetings, etc.)
  - Context-aware responses
  - Source citation
  - Confidence scoring

### 3.3 Prompt History Records (PHR)

#### POST /phr/create
- **Purpose**: Create new PHR entry
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "title": "Implementation of Feature X",
    "stage": "spec|plan|tasks|red|green|refactor|explainer|misc|general",
    "prompt_text": "User's complete prompt",
    "response_text": "AI's complete response",
    "surface": "agent",
    "model": "claude-3-opus",
    "feature": "feature-name",
    "branch": "main",
    "user": "user@example.com",
    "command": "/slash-command",
    "labels": ["tag1", "tag2"],
    "links": {
      "spec": "spec-url",
      "ticket": "ticket-url",
      "adr": "adr-url",
      "pr": "pr-url"
    },
    "files_yaml": ["src/file1.js", "src/file2.ts"],
    "tests_yaml": ["tests/test1.js"],
    "outcome": "Implementation completed successfully",
    "evaluation": "Performance improvements observed"
  }
  ```
- **Response**:
  ```json
  {
    "message": "PHR created successfully",
    "file_path": "history/prompts/feature/0001-title.stage.prompt.md",
    "stage": "spec",
    "title": "Implementation of Feature X"
  }
  ```

#### GET /phr/list
- **Purpose**: List PHR entries
- **Authentication**: Required
- **Query Parameters**:
  - stage: Filter by stage (optional)
  - feature: Filter by feature (optional)
  - limit: Max results (default: 50)
- **Response**:
  ```json
  {
    "phrs": [
      {
        "id": "0001",
        "title": "PHR Title",
        "stage": "spec",
        "date_iso": "2024-01-15T10:30:00",
        "feature": "feature-name",
        "file_path": "path/to/phr",
        "preview": "First 100 characters of prompt..."
      }
    ],
    "count": 1,
    "stage_filter": "spec",
    "feature_filter": "feature-name"
  }
  ```

#### POST /phr/search
- **Purpose**: Search PHR content
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "query": "search terms",
    "stage": "spec",
    "feature": "feature-name",
    "limit": 50
  }
  ```
- **Response**:
  ```json
  {
    "query": "search terms",
    "results": [/* PHR objects matching query */],
    "count": 5
  }
  ```

### 3.4 Specifications Management

#### GET /specs
- **Purpose**: List all project specifications
- **Authentication**: Required
- **Response**:
  ```json
  {
    "specs": [
      {
        "id": "001-robotics-lab-guide",
        "name": "Robotics Lab Guide",
        "files": {
          "spec.md": "Specification content",
          "plan.md": "Implementation plan",
          "tasks.md": "Task list",
          "research.md": "Research notes",
          "data-model.md": "Data model definition",
          "quickstart.md": "Quick start guide"
        }
      }
    ],
    "count": 1
  }
  ```

#### GET /specs/{spec_id}
- **Purpose**: Get specific specification
- **Authentication**: Required
- **Response**: Individual spec object with all files

### 3.5 Content Serving

#### GET /content/docs/{file_path}
- **Purpose**: Serve documentation content
- **Authentication**: Required
- **Security**: Path traversal protection
- **Response**:
  ```json
  {
    "path": "00-intro/overview.mdx",
    "content": "Markdown content",
    "type": "markdown"
  }
  ```

#### GET /content/components/{component_path}
- **Purpose**: Serve React component code
- **Authentication**: Required
- **Security**: Path traversal protection
- **Response**:
  ```json
  {
    "path": "HomepageFeatures/index.tsx",
    "content": "TypeScript/React code",
    "type": "react"
  }
  ```

#### GET /content/static/{file_path}
- **Purpose**: Serve static files
- **Authentication**: Required
- **Features**:
  - Base64 encoding for images
  - Text content for other files
- **Security**: Path traversal protection

## 4. Data Models

### 4.1 Database Models

#### User (SQLAlchemy)
```python
class User:
    id: int (Primary Key)
    email: str (Unique)
    password_hash: str
    name: str
    software_background: str
    hardware_background: str
    learning_goals: Optional[str]
    created_at: datetime
    updated_at: datetime
```

### 4.2 PHR Data Structure

#### PHR Metadata
```yaml
ID: "0001"
TITLE: "PHR Title"
STAGE: "spec"
DATE_ISO: "2024-01-15T10:30:00"
SURFACE: "agent"
MODEL: "claude-3-opus"
FEATURE: "feature-name"
BRANCH: "main"
USER: "user@example.com"
COMMAND: "/command"
LABELS: ["tag1", "tag2"]
LINKS:
  SPEC: "url"
  TICKET: "url"
  ADR: "url"
  PR: "url"
FILES_YAML:
  - file1.js
  - file2.ts
TESTS_YAML:
  - test1.js
  - test2.js
```

#### PHR Content
```yaml
PROMPT_TEXT: "Complete user prompt"
RESPONSE_TEXT: "Complete AI response"
OUTCOME: "Result description"
EVALUATION: "Evaluation notes"
```

## 5. Security Considerations

### 5.1 Authentication
- JWT tokens with expiration
- Password hashing with bcrypt
- Token validation middleware

### 5.2 Input Validation
- Pydantic models for request validation
- Path traversal protection for file access
- SQL injection prevention through SQLAlchemy

### 5.3 CORS Configuration
- Configurable for development/production
- Currently allows all origins (adjustable for production)

## 6. Performance Considerations

### 6.1 Database
- Connection pooling
- Efficient queries with indexes

### 6.2 RAG System
- Vector similarity search
- Caching considerations
- Batch processing for embeddings

### 6.3 File Serving
- Efficient file reading
- Base64 encoding for images
- Static file optimization

## 7. Environment Configuration

### 7.1 Required Environment Variables
```env
# Database
DATABASE_URL=sqlite:///./database.db

# Authentication
SECRET_KEY=your-secret-key-here

# AI Services
OPENAI_API_KEY=your-openai-key
GEMINI_API_KEY=your-gemini-key

# Vector Database
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your-qdrant-key
QDRANT_COLLECTION_NAME=robotics_book_embeddings

# Generation Settings
TEMPERATURE=0.7
MAX_TOKENS=1000
```

## 8. Error Handling

### 8.1 HTTP Status Codes
- 200: Success
- 400: Bad Request (validation)
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 422: Unprocessable Entity
- 500: Internal Server Error

### 8.2 Error Response Format
```json
{
  "detail": "Error description",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-15T10:30:00"
}
```

## 9. Testing Strategy

### 9.1 Unit Tests
- Service layer testing
- Model validation
- Utility functions

### 9.2 Integration Tests
- API endpoint testing
- Database operations
- Authentication flow

### 9.3 End-to-End Tests
- Complete user flows
- RAG functionality
- PHR lifecycle

## 10. Deployment

### 10.1 Development
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 10.2 Production
- Use Gunicorn/Uvicorn
- PostgreSQL database
- Redis for caching
- Docker containerization
- Environment-specific configuration

## 11. Monitoring and Logging

### 11.1 Logging Levels
- INFO: General operation
- WARNING: Non-critical issues
- ERROR: Errors requiring attention
- DEBUG: Detailed debugging

### 11.2 Metrics
- Request latency
- Error rates
- User activity
- RAG performance

## 12. Future Enhancements

### 12.1 Planned Features
- Real-time notifications
- WebSocket support
- Advanced search filters
- Export functionality
- API versioning
- Rate limiting

### 12.2 Scaling Considerations
- Microservices architecture
- Load balancing
- Database sharding
- CDN integration