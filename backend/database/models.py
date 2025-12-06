"""
Database models for storing metadata about text chunks and queries
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, JSON
from sqlalchemy.sql import func
from database.db import Base

class TextChunkMetadata(Base):
    """Store metadata about uploaded text chunks"""
    __tablename__ = "text_chunks"
    
    id = Column(String, primary_key=True)
    doc_id = Column(String, index=True)
    content = Column(Text)
    chunk_metadata = Column(JSON)  # Renamed from 'metadata' to avoid conflict
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class User(Base):
    """User account with personalization profile"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)  # Changed from full_name to match DB schema
    password_hash = Column(String, nullable=False)  # Fixed to match actual DB column name

    # Personalization Profile
    software_background = Column(String)  # e.g., "Expert", "Beginner", "Python dev"
    hardware_background = Column(String)  # e.g., "None", "Arduino hobbyist", "EE Engineer"
    learning_goals = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class QueryLog(Base):
    """Log user queries for analytics"""
    __tablename__ = "query_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text)
    answer = Column(Text)
    confidence = Column(Integer)
    sources_count = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
