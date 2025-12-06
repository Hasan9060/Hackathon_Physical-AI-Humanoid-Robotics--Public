"""
Fix user schema - Add 'name' column mapping to 'full_name'
This script updates the User model to match the actual PostgreSQL schema
"""

from sqlalchemy import text
from database.db import engine, get_db
import os

def fix_schema():
    """Check and fix the user table schema"""
    
    with engine.connect() as conn:
        # Check if 'name' column exists
        result = conn.execute(text("""
            SELECT column_name, is_nullable, data_type
            FROM information_schema.columns
            WHERE table_name = 'users'
            ORDER BY ordinal_position;
        """))
        
        columns = result.fetchall()
        print("Current columns in 'users' table:")
        for col in columns:
            print(f"  - {col[0]} ({col[2]}, nullable={col[1]})")
        
        column_names = [col[0] for col in columns]
        
        # If 'name' exists but 'full_name' doesn't, we need to add full_name or rename
        if 'name' in column_names and 'full_name' not in column_names:
            print("\n⚠️  Found 'name' column but not 'full_name'")
            print("Adding 'full_name' column as alias...")
            
            # Add full_name column
            conn.execute(text("""
                ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name VARCHAR;
            """))
            
            # Copy data from name to full_name
            conn.execute(text("""
                UPDATE users SET full_name = name WHERE full_name IS NULL;
            """))
            
            conn.commit()
            print("✅ Added 'full_name' column and copied data from 'name'")
            
        elif 'full_name' in column_names and 'name' not in column_names:
            print("\n✅ Schema is correct - 'full_name' exists")
            
        elif 'name' in column_names and 'full_name' in column_names:
            print("\n✅ Both columns exist - syncing data...")
            # Sync data
            conn.execute(text("""
                UPDATE users SET full_name = name WHERE full_name IS NULL AND name IS NOT NULL;
            """))
            conn.execute(text("""
                UPDATE users SET name = full_name WHERE name IS NULL AND full_name IS NOT NULL;
            """))
            conn.commit()
            print("✅ Data synced between 'name' and 'full_name'")
        else:
            print("\n⚠️  Neither 'name' nor 'full_name' found!")

if __name__ == "__main__":
    print("🔧 Checking user table schema...\n")
    
    if not os.getenv("DATABASE_URL"):
        print("❌ DATABASE_URL not set in environment")
        exit(1)
    
    try:
        fix_schema()
        print("\n✅ Schema check complete!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
