"""
Create/Reset admin account
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from passlib.context import CryptContext
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_admin():
    """Create or update admin account"""
    
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    admin_email = "kayicom509@gmail.com"
    admin_password = "Admin123!"
    
    print(f"Creating/Updating admin account...")
    print(f"Email: {admin_email}")
    print(f"Password: {admin_password}")
    
    # Check if admin exists
    existing_admin = await db.users.find_one({"email": admin_email})
    
    hashed_password = pwd_context.hash(admin_password)
    
    if existing_admin:
        # Update existing admin
        await db.users.update_one(
            {"email": admin_email},
            {"$set": {
                "password": hashed_password,
                "role": "admin",
                "name": "Admin User"
            }}
        )
        print(f"✅ Admin account updated!")
    else:
        # Create new admin
        admin_user = {
            "id": "admin-001",
            "email": admin_email,
            "password": hashed_password,
            "name": "Admin User",
            "role": "admin",
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        await db.users.insert_one(admin_user)
        print(f"✅ Admin account created!")
    
    print(f"\n📋 ADMIN CREDENTIALS:")
    print(f"   Email: {admin_email}")
    print(f"   Password: {admin_password}")
    print(f"\n🔗 Login URL: http://localhost:3000/admin/login")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin())
