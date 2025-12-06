"""
Simple Authentication Server for Development
Works with the frontend AuthProvider
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import hashlib
import secrets
import os

app = FastAPI(title="Auth Server")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory user store (for development)
users: Dict[str, Dict[str, Any]] = {}
sessions: Dict[str, Dict[str, Any]] = {}

# Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_session_token() -> str:
    return secrets.token_urlsafe(32)

@app.post("/sign-up/email")
async def sign_up(user_data: UserCreate):
    email = user_data.email.lower()

    if email in users:
        raise HTTPException(status_code=400, detail="User already exists")

    # Create user
    user = {
        "id": secrets.token_urlsafe(16),
        "email": email,
        "name": user_data.name or email.split("@")[0],
        "password": hash_password(user_data.password),
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
        "emailVerified": True, # Auto-verify for development
    }

    users[email] = user

    # Create session
    token = create_session_token()
    sessions[token] = {
        "userId": user["id"],
        "email": email,
        "createdAt": datetime.now(),
    }

    response = JSONResponse(content={
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "emailVerified": user["emailVerified"],
            "createdAt": user["createdAt"],
            "updatedAt": user["updatedAt"],
        }
    })

    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        secure=False,  # Set to False for development
        samesite="lax",
        max_age=86400 * 7,  # 7 days
    )

    return response

@app.post("/sign-in/email")
async def sign_in(login_data: UserLogin):
    email = login_data.email.lower()

    if email not in users:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = users[email]
    if user["password"] != hash_password(login_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create session
    token = create_session_token()
    sessions[token] = {
        "userId": user["id"],
        "email": email,
        "createdAt": datetime.now(),
    }

    response = JSONResponse(content={
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "emailVerified": user["emailVerified"],
            "createdAt": user["createdAt"],
            "updatedAt": user["updatedAt"],
        }
    })

    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        secure=False,  # Set to False for development
        samesite="lax",
        max_age=86400 * 7,  # 7 days
    )

    return response

@app.post("/sign-out")
async def sign_out():
    response = JSONResponse(content={"message": "Signed out successfully"})
    response.delete_cookie("session_token")
    return response

@app.get("/get-session")
async def get_session(session_token: Optional[str] = None):
    token = session_token or None

    if not token:
        token = None  # Will look for cookie

    if not token or token not in sessions:
        return {"data": {"user": None}}

    session = sessions[token]
    email = session["email"]
    user = users[email]

    return {
        "data": {
            "user": {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "emailVerified": user["emailVerified"],
                "createdAt": user["createdAt"],
                "updatedAt": user["updatedAt"],
            }
        }
    }

@app.post("/forget-password")
async def forget_password(email: EmailStr):
    # For development, just return success
    return {"message": "Password reset instructions sent to your email"}

@app.put("/update-user")
async def update_user(name: Optional[str] = None):
    # For development, return success
    return {"data": {"name": name or "User"}}

@app.get("/")
async def root():
    return {"status": "auth server running"}

if __name__ == "__main__":
    import uvicorn
    print("🔐 Starting Auth Server on port 3001...")
    print("📝 This is a development auth server for testing only")
    uvicorn.run("auth_server:app", host="0.0.0.0", port=3001, reload=True)