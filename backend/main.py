"""
RAG Chatbot Backend - Real Implementation
"""

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Optional, Dict
import os
from pathlib import Path
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from openai import AsyncOpenAI
import google.generativeai as genai
from sqlalchemy.orm import Session
from database.db import get_db, init_db
from database.models import User
from services.auth_service import AuthService
from services.phr_service import PHRService, Stage
import datetime
import traceback

load_dotenv()

# Initialize DB
init_db()

app = FastAPI(
    title="Robotics Book RAG API",
    description="RAG API for Physical AI textbook",
    version="1.0.0"
)

# CORS - Allow all for development ease
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add validation error handler for debugging
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("\n" + "="*50)
    print("❌ VALIDATION ERROR (422)")
    print("="*50)
    print(f"URL: {request.url}")
    print(f"Method: {request.method}")
    print(f"Errors: {exc.errors()}")
    print(f"Body: {await request.body()}")
    print("="*50 + "\n")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": str(await request.body())}
    )

# Auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Global clients
qdrant_client = None
openai_client = None
gemini_model = None
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME", "robotics_book_embeddings")

# Models
class UserSignup(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    full_name: Optional[str] = None
    software_background: str
    hardware_background: str
    learning_goals: Optional[str] = None

    @model_validator(mode='before')
    def extract_name(cls, values):
        # Accept either 'name' or 'full_name' field
        if 'full_name' in values and values['full_name']:
            values['name'] = values['full_name']
            values.pop('full_name', None)
        elif 'name' not in values:
            raise ValueError('Either name or full_name must be provided')
        return values

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_profile: dict

class QueryRequest(BaseModel):
    question: str
    max_results: Optional[int] = 5
    selected_text: Optional[str] = None

class PHRCreateRequest(BaseModel):
    title: str
    stage: str  # constitution, spec, plan, tasks, red, green, refactor, explainer, misc, general
    prompt_text: str
    response_text: str
    surface: Optional[str] = "agent"
    model: Optional[str] = "claude-3-opus"
    feature: Optional[str] = "none"
    branch: Optional[str] = "main"
    user: Optional[str] = "user"
    command: Optional[str] = ""
    labels: Optional[List[str]] = []
    links: Optional[Dict[str, str]] = {}
    files_yaml: Optional[List[str]] = []
    tests_yaml: Optional[List[str]] = []
    outcome: Optional[str] = None
    evaluation: Optional[str] = None

class PHRSearchRequest(BaseModel):
    query: str
    stage: Optional[str] = None
    feature: Optional[str] = None
    limit: Optional[int] = 50

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = AuthService.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.on_event("startup")
async def startup_event():
    """Initialize clients on startup"""
    global qdrant_client, openai_client, gemini_model

    try:
        # Initialize Qdrant
        qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )

        # Check if collection exists to warn user if empty
        try:
            collections = qdrant_client.get_collections().collections
            collection_names = [c.name for c in collections]

            if COLLECTION_NAME not in collection_names:
                print(f"WARNING: Collection {COLLECTION_NAME} not found. Please run upload script.")
            else:
                info = qdrant_client.get_collection(COLLECTION_NAME)
                print(f"SUCCESS: Collection found: {COLLECTION_NAME} ({info.points_count} items)")
        except Exception as e:
            print(f"WARNING: Could not verify collection: {e}")

        # Initialize OpenAI (for embeddings)
        openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Initialize Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        gemini_model = genai.GenerativeModel('models/gemini-2.0-flash')

        print("SUCCESS: RAG Chatbot API initialized successfully")

    except Exception as e:
        print(f"ERROR: Startup error: {e}")

@app.get("/")
async def root():
    return {
        "status": "healthy",
        "message": "Real RAG Chatbot API is running",
        "version": "1.0.0"
    }

@app.post("/signup", response_model=Token)
async def signup(user: UserSignup, db: Session = Depends(get_db)):
    import json
    print(f"\n[Signup] Signup request received:")
    print(f"  User object: {user}")
    print(f"  User dict: {user.model_dump()}")
    print(f"  User JSON: {json.dumps(user.model_dump(), indent=2)}")
    print(f"  Email: '{user.email}' (type: {type(user.email)})")
    print(f"  Name: '{user.name}' (type: {type(user.name)})")
    print(f"  Software: '{user.software_background}' (type: {type(user.software_background)})")
    print(f"  Hardware: '{user.hardware_background}' (type: {type(user.hardware_background)})")
    print(f"  Goals: '{user.learning_goals}' (type: {type(user.learning_goals)})")

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        print(f"[ERROR] Email already registered: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    
    password_hash = AuthService.get_password_hash(user.password)
    new_user = User(
        email=user.email,
        password_hash=password_hash,
        name=user.name,
        software_background=user.software_background,
        hardware_background=user.hardware_background,
        learning_goals=user.learning_goals
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = AuthService.create_access_token(data={"sub": new_user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_profile": {
            "name": new_user.name,
            "software": new_user.software_background,
            "hardware": new_user.hardware_background
        }
    }

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not AuthService.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = AuthService.create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_profile": {
            "name": user.name,
            "software": user.software_background,
            "hardware": user.hardware_background
        }
    }

@app.post("/query")
async def query_chatbot(request: QueryRequest):
    """Query the RAG chatbot"""
    print(f"\n[Query] Received query: {request.question}")
    
    try:
        # Check for vague inputs/greetings
        vague_inputs = ['hi', 'hello', 'hey', 'ji', 'yes', 'no', 'ok', 'okay', 'thanks', 'thank you']
        if request.question.lower().strip() in vague_inputs:
            return {
                "answer": "Hello! I'm your AI assistant for the Physical AI & Humanoid Robotics Lab textbook. What would you like to learn about? You can ask me about ROS 2, Gazebo simulation, Isaac Sim, humanoid robotics, or hardware setup.",
                "sources": [],
                "confidence": 1.0
            }

        # Create embedding for question
        embedding_response = await openai_client.embeddings.create(
            model="text-embedding-3-small",
            input=request.question
        )
        question_embedding = embedding_response.data[0].embedding
        
        # Search Qdrant
        search_result_obj = qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=question_embedding,
            limit=request.max_results
        )
        search_results = search_result_obj.points
        
        # Build context
        sources = []
        context_parts = []
        
        for i, hit in enumerate(search_results, 1):
            text = hit.payload.get("text", "")
            # Add file info/module info if available
            module = hit.payload.get("module", "")
            file_name = hit.payload.get("file", "")
            source_info = f"[{module} - {file_name}]" if module else ""
            
            context_parts.append(f"[Source {i} {source_info}]: {text}")
            sources.append({
                "id": hit.id,
                "score": hit.score,
                "text": text,
                "metadata": {k: v for k, v in hit.payload.items() if k != "text"}
            })
        
        context = "\n\n".join(context_parts)
        
        if request.selected_text:
            context = f"Selected Text by User:\n{request.selected_text}\n\nRelevant Textbook Content:\n{context}"
            
        # Generate answer
        system_prompt = """You are an expert AI assistant for the Physical AI & Humanoid Robotics Lab textbook.
Your role is to help students learn about robotics, ROS 2, simulation, and AI control systems based on the textbook content.

Guidelines:
- Answer based ONLY on the provided context from the textbook.
- Be precise, technical, and educational.
- If the context doesn't contain relevant information, say: "I don't have specific information about that in the textbook. Could you ask about ROS 2, Gazebo, Isaac Sim, or hardware setup?"
- Use clear, conversational language.
- Cite specific information from the context where appropriate.
- Keep answers focused and relevant to the question."""

        user_prompt = f"""Context from the textbook:
{context}

Question: {request.question}

Please provide a detailed answer based on the context above."""

        # Generate answer using Gemini
        combined_prompt = f"{system_prompt}\n\n{user_prompt}"

        # Configure generation parameters
        generation_config = {
            "temperature": float(os.getenv("TEMPERATURE", 0.7)),
            "max_output_tokens": int(os.getenv("MAX_TOKENS", 1000)),
        }

        # Generate response
        response = gemini_model.generate_content(
            combined_prompt,
            generation_config=generation_config
        )

        answer = response.text
        avg_score = sum(s["score"] for s in sources) / len(sources) if sources else 0
        
        return {
            "answer": answer,
            "sources": sources,
            "confidence": round(avg_score, 2)
        }
        
    except Exception as e:
        error_msg = f"[ERROR] Query error: {e}\n"
        print(error_msg)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# PHR Endpoints
@app.post("/phr/create")
async def create_phr(request: PHRCreateRequest, current_user: User = Depends(get_current_user)):
    """Create a new Prompt History Record"""
    try:
        # Validate stage
        try:
            stage = Stage(request.stage.lower())
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid stage: {request.stage}")

        # Initialize PHR service
        phr_service = PHRService()

        # Create PHR
        file_path = phr_service.create_phr(
            title=request.title,
            stage=stage,
            prompt_text=request.prompt_text,
            response_text=request.response_text,
            surface=request.surface,
            model=request.model,
            feature=request.feature,
            branch=request.branch,
            user=current_user.email,
            command=request.command,
            labels=request.labels,
            links=request.links,
            files_yaml=request.files_yaml,
            tests_yaml=request.tests_yaml,
            outcome=request.outcome,
            evaluation=request.evaluation
        )

        return {
            "message": "PHR created successfully",
            "file_path": file_path,
            "stage": stage.value,
            "title": request.title
        }

    except Exception as e:
        print(f"[ERROR] PHR creation error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/phr/list")
async def list_phrs(
    stage: Optional[str] = None,
    feature: Optional[str] = None,
    limit: Optional[int] = 50,
    current_user: User = Depends(get_current_user)
):
    """List Prompt History Records with optional filtering"""
    try:
        phr_service = PHRService()

        # Convert stage string to enum if provided
        stage_enum = None
        if stage:
            try:
                stage_enum = Stage(stage.lower())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid stage: {stage}")

        phrs = phr_service.list_phrs(stage=stage_enum, feature=feature, limit=limit)

        return {
            "phrs": phrs,
            "count": len(phrs),
            "stage_filter": stage,
            "feature_filter": feature
        }

    except Exception as e:
        print(f"[ERROR] PHR list error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/phr/search")
async def search_phrs(
    request: PHRSearchRequest,
    current_user: User = Depends(get_current_user)
):
    """Search Prompt History Records by content"""
    try:
        phr_service = PHRService()

        # Convert stage string to enum if provided
        stage_enum = None
        if request.stage:
            try:
                stage_enum = Stage(request.stage.lower())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid stage: {request.stage}")

        results = phr_service.search_phrs(
            query=request.query,
            stage=stage_enum,
            feature=request.feature
        )

        return {
            "query": request.query,
            "results": results,
            "count": len(results)
        }

    except Exception as e:
        print(f"[ERROR] PHR search error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/phr/{file_path:path}")
async def get_phr(file_path: str, current_user: User = Depends(get_current_user)):
    """Get a specific PHR by file path"""
    try:
        phr_service = PHRService()
        phr = phr_service.load_phr(file_path)

        if not phr:
            raise HTTPException(status_code=404, detail="PHR not found")

        return {
            "metadata": {
                "id": phr.metadata.id,
                "title": phr.metadata.title,
                "stage": phr.metadata.stage.value,
                "date_iso": phr.metadata.date_iso,
                "surface": phr.metadata.surface,
                "model": phr.metadata.model,
                "feature": phr.metadata.feature,
                "branch": phr.metadata.branch,
                "user": phr.metadata.user,
                "command": phr.metadata.command,
                "labels": phr.metadata.labels,
                "links": phr.metadata.links,
                "files_yaml": phr.metadata.files_yaml,
                "tests_yaml": phr.metadata.tests_yaml
            },
            "content": {
                "prompt_text": phr.content.prompt_text,
                "response_text": phr.content.response_text,
                "outcome": phr.content.outcome,
                "evaluation": phr.content.evaluation
            }
        }

    except Exception as e:
        print(f"[ERROR] PHR get error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Specs Endpoints
@app.get("/specs")
async def get_specs(current_user: User = Depends(get_current_user)):
    """Get all available specs"""
    try:
        specs_dir = Path(__file__).parent.parent / "specs"
        specs = []

        if specs_dir.exists():
            for spec_dir in specs_dir.iterdir():
                if spec_dir.is_dir():
                    spec_files = {}
                    # Look for spec.md, plan.md, tasks.md
                    for file_name in ["spec.md", "plan.md", "tasks.md", "research.md", "data-model.md", "quickstart.md"]:
                        file_path = spec_dir / file_name
                        if file_path.exists():
                            with open(file_path, 'r', encoding='utf-8') as f:
                                spec_files[file_name] = f.read()

                    if spec_files:  # Only add if we found files
                        specs.append({
                            "id": spec_dir.name,
                            "name": spec_dir.name.replace("-", " ").title(),
                            "files": spec_files
                        })

        return {
            "specs": specs,
            "count": len(specs)
        }

    except Exception as e:
        print(f"[ERROR] Specs get error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/specs/{spec_id}")
async def get_spec(spec_id: str, current_user: User = Depends(get_current_user)):
    """Get a specific spec by ID"""
    try:
        spec_dir = Path(__file__).parent.parent / "specs" / spec_id

        if not spec_dir.exists():
            raise HTTPException(status_code=404, detail="Spec not found")

        spec_files = {}
        for file_name in ["spec.md", "plan.md", "tasks.md", "research.md", "data-model.md", "quickstart.md"]:
            file_path = spec_dir / file_name
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    spec_files[file_name] = f.read()

        return {
            "id": spec_id,
            "name": spec_id.replace("-", " ").title(),
            "files": spec_files
        }

    except Exception as e:
        print(f"[ERROR] Spec get error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Website Content Endpoints
@app.get("/content/docs/{file_path:path}")
async def get_doc_content(file_path: str, current_user: User = Depends(get_current_user)):
    """Get documentation content"""
    try:
        doc_path = Path(__file__).parent.parent / "docs" / file_path

        # Ensure the path doesn't go outside docs directory
        doc_path = doc_path.resolve()
        docs_root = Path(__file__).parent.parent / "docs"
        if not str(doc_path).startswith(str(docs_root.resolve())):
            raise HTTPException(status_code=403, detail="Access denied")

        if not doc_path.exists():
            raise HTTPException(status_code=404, detail="Documentation file not found")

        # Read the file content
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "path": file_path,
            "content": content,
            "type": "markdown" if file_path.endswith('.md') or file_path.endswith('.mdx') else "text"
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Doc content error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/content/docs")
async def list_docs(current_user: User = Depends(get_current_user)):
    """List all documentation files"""
    try:
        docs_path = Path(__file__).parent.parent / "docs"
        files = []

        if docs_path.exists():
            for file_path in docs_path.rglob("*.md"):
                relative_path = file_path.relative_to(docs_path)
                files.append(str(relative_path))

        return {
            "files": sorted(files),
            "count": len(files)
        }

    except Exception as e:
        print(f"[ERROR] Docs list error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/content/components/{component_path:path}")
async def get_component_content(component_path: str, current_user: User = Depends(get_current_user)):
    """Get React component content"""
    try:
        comp_path = Path(__file__).parent.parent / "src" / "components" / component_path

        # Ensure the path doesn't go outside components directory
        comp_path = comp_path.resolve()
        comp_root = Path(__file__).parent.parent / "src" / "components"
        if not str(comp_path).startswith(str(comp_root.resolve())):
            raise HTTPException(status_code=403, detail="Access denied")

        if not comp_path.exists():
            raise HTTPException(status_code=404, detail="Component file not found")

        # Read the file content
        with open(comp_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            "path": component_path,
            "content": content,
            "type": "react" if component_path.endswith('.tsx') or component_path.endswith('.jsx') else "text"
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Component content error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/content/static/{file_path:path}")
async def get_static_file(file_path: str, current_user: User = Depends(get_current_user)):
    """Get static file content"""
    try:
        static_path = Path(__file__).parent.parent / "static" / file_path

        # Ensure the path doesn't go outside static directory
        static_path = static_path.resolve()
        static_root = Path(__file__).parent.parent / "static"
        if not str(static_path).startswith(str(static_root.resolve())):
            raise HTTPException(status_code=403, detail="Access denied")

        if not static_path.exists():
            raise HTTPException(status_code=404, detail="Static file not found")

        # Check if it's an image
        image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']
        if any(file_path.lower().endswith(ext) for ext in image_extensions):
            # For images, we'll return base64 encoded content
            import base64
            with open(static_path, 'rb') as f:
                image_data = f.read()
                encoded = base64.b64encode(image_data).decode('utf-8')

            return {
                "path": file_path,
                "content": encoded,
                "type": "image",
                "encoding": "base64"
            }
        else:
            # For text files
            with open(static_path, 'r', encoding='utf-8') as f:
                content = f.read()

            return {
                "path": file_path,
                "content": content,
                "type": "static"
            }

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Static file error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/content/static")
async def list_static_files(current_user: User = Depends(get_current_user)):
    """List all static files"""
    try:
        static_path = Path(__file__).parent.parent / "static"
        files = []

        if static_path.exists():
            for file_path in static_path.rglob("*"):
                if file_path.is_file():
                    relative_path = file_path.relative_to(static_path)
                    files.append(str(relative_path))

        return {
            "files": sorted(files),
            "count": len(files)
        }

    except Exception as e:
        print(f"[ERROR] Static files list error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
