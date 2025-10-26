"""
Update existing admin to be super admin with full permissions
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def update_admin_to_super():
    # Update all existing admins to have is_super_admin and permissions
    result = await db.users.update_many(
        {"role": "admin"},
        {
            "$set": {
                "is_super_admin": True,
                "permissions": {
                    "manage_products": True,
                    "manage_orders": True,
                    "manage_customers": True,
                    "manage_coupons": True,
                    "manage_settings": True,
                    "manage_team": True
                },
                "is_active": True
            }
        }
    )
    
    print(f"✅ Updated {result.modified_count} admin user(s) to super admin with full permissions")
    
    # Show updated admin
    admin = await db.users.find_one({"role": "admin"}, {"_id": 0, "password": 0, "password_hash": 0})
    if admin:
        print(f"✅ Admin user: {admin['email']}")
        print(f"   - Super Admin: {admin.get('is_super_admin', False)}")
        print(f"   - Permissions: {admin.get('permissions', {})}")

if __name__ == "__main__":
    asyncio.run(update_admin_to_super())
