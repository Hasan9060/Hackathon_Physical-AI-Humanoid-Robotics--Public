# RAG Chatbot for Robotics Textbook

A Retrieval-Augmented Generation (RAG) chatbot specifically designed for the Physical AI & Humanoid Robotics textbook.

## Features

- **RAG-Powered Responses**: Answers questions based on textbook content using vector search
- **Text Selection Support**: Select any text in the book and ask specific questions about it
- **FastAPI Backend**: High-performance async backend with OpenAI integration
- **Neon Serverless Postgres**: Scalable database for chat sessions and content
- **Qdrant Cloud**: Vector database for semantic search
- **OpenAI Integration**: Uses GPT-4 Turbo with embeddings for intelligent responses

## Architecture

### Backend Services

1. **FastAPI Application** (`rag-chatbot/backend/`)
   - RESTful API endpoints for chat, ingestion, and health checks
   - Async database operations with PostgreSQL
   - Vector search with Qdrant Cloud

2. **Core Components**:
   - `app/services/openai_service.py`: OpenAI API integration
   - `app/services/qdrant_service.py`: Vector database operations
   - `app/services/ingestion_service.py`: Content processing and chunking
   - `app/core/database.py`: PostgreSQL connection management

3. **API Endpoints**:
   - `/api/v1/chat/chat`: Main chat endpoint with RAG
   - `/api/v1/chat/selected-text`: Analyze selected text
   - `/api/v1/ingestion/status`: Content ingestion status
   - `/api/v1/health`: Health check for all services

### Frontend Component

- **RAGChatbot** (`src/components/RAGChatbot/`)
  - React component with TypeScript
  - Session management
  - Text selection detection
  - Source citation display

## Setup Instructions

### Prerequisites

1. **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/)
2. **Neon Database**: Create free serverless Postgres database
3. **Qdrant Cloud**: Create free vector database cluster
4. **Python 3.9+**: For running the backend

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd rag-chatbot/backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. Run the backend:
   ```bash
   python run.py
   ```

### Environment Variables

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# Neon Database Configuration
NEON_DATABASE_URL=postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/robotics_db

# Qdrant Cloud Configuration
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_URL=https://xxx-xxx.us-east-1.aws.qdrant.io:6333

# Book Content Configuration
BOOK_CONTENT_PATH=../../docs
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### Content Ingestion

1. Start the backend service
2. Trigger content ingestion via API:
   ```bash
   curl -X POST http://localhost:8000/api/v1/ingestion/start
   ```

3. Check ingestion status:
   ```bash
   curl http://localhost:8000/api/v1/ingestion/status
   ```

### Frontend Integration

The RAG chatbot is already integrated into the Docusaurus site:

```tsx
import { RAGChatbot } from '@site/src/components/RAGChatbot';

<RAGChatbot
  apiBaseUrl="http://localhost:8000/api/v1"
  onSessionChange={(sessionId) => console.log('Session:', sessionId)}
/>
```

## Usage

### Basic Chat

1. Click the "Ask RAG Assistant" button
2. Ask questions about robotics, AI, or specific topics from the textbook
3. The chatbot will provide answers with source citations

### Text Selection Feature

1. Select any text while reading the textbook
2. A popup will appear asking if you want to ask about the selected text
3. The chatbot will provide answers specifically about the selected content

### Session Management

- Chat sessions are automatically saved
- Use the clear button to start a new session
- Session IDs are preserved across page reloads

## Development

### Running Locally

1. Backend (Terminal 1):
   ```bash
   cd rag-chatbot/backend
   python run.py
   ```

2. Frontend (Terminal 2):
   ```bash
   npm run start
   ```

### API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Monitoring

- Health check: http://localhost:8000/api/v1/health
- Ingestion status: http://localhost:8000/api/v1/ingestion/status

## Deployment

### Production Environment Variables

Set `API_ENVIRONMENT=production` to disable reload and optimize for production.

### Docker Deployment

```dockerfile
# Example Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Common Issues

1. **Database Connection**: Ensure Neon database URL is correct and accessible
2. **Qdrant Connection**: Verify Qdrant cluster is running and API key is valid
3. **OpenAI API**: Check API key has sufficient credits
4. **Content Ingestion**: Ensure book content is accessible at the specified path

### Logs

Check backend logs for detailed error information:
```bash
tail -f rag-chatbot/backend/logs/app.log
```

## Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   FastAPI       │    │   External      │
│   (React)       │◄──►│   Backend       │◄──►│   Services      │
│                 │    │                 │    │                 │
│ RAGChatbot      │    │ - Chat API      │    │ - OpenAI API    │
│ Component       │    │ - Ingestion API │    │ - Qdrant Cloud  │
│                 │    │ - Health API    │    │ - Neon DB       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the Physical AI & Humanoid Robotics textbook.