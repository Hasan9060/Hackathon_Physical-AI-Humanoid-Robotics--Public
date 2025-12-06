"""
Script to check the actual database schema
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set in .env file")
    exit(1)

# Create engine
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Get column info for users table
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'users'
            ORDER BY ordinal_position
        """))

        columns = result.fetchall()

        print("Users table schema:")
        print("-" * 50)
        for col in columns:
            print(f"Column: {col[0]:<20} Type: {col[1]:<20} Nullable: {col[2]}")

except Exception as e:
    print(f"Error: {e}")
    exit(1)