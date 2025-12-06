from services.auth_service import AuthService
import hashlib

print("Testing AuthService locally...")
long_password = "a" * 100
print(f"Password length: {len(long_password)}")

try:
    print("Hashing...")
    hashed = AuthService.get_password_hash(long_password)
    print(f"Hashed: {hashed[:10]}... (len={len(hashed)})")
    
    print("Verifying...")
    valid = AuthService.verify_password(long_password, hashed)
    print(f"Valid: {valid}")
    
except Exception as e:
    print(f"❌ Error: {e}")
