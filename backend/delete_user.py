"""
Delete a user by email from the database
"""

from database.db import get_db
from database.models import User
import sys

def delete_user(email: str):
    """Delete a user by email"""
    db = next(get_db())
    
    try:
        user = db.query(User).filter(User.email == email).first()
        
        if user:
            db.delete(user)
            db.commit()
            print(f"✅ User deleted: {email}")
            return True
        else:
            print(f"❌ User not found: {email}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python delete_user.py <email>")
        print("Example: python delete_user.py user@example.com")
        sys.exit(1)
    
    email = sys.argv[1]
    delete_user(email)
