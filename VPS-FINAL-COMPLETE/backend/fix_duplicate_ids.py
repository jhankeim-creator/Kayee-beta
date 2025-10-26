"""
Fix duplicate admin IDs
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
import uuid

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

async def fix_duplicate_ids():
    # Find admins with duplicate IDs
    admins = await db.users.find({'role': 'admin'}, {'_id': 0}).to_list(length=10)
    
    for admin in admins:
        if admin.get('id') == 'admin-001':
            new_id = str(uuid.uuid4())
            result = await db.users.update_one(
                {'email': admin['email']},
                {'$set': {'id': new_id}}
            )
            print(f"✅ Updated {admin['email']} with new ID: {new_id}")
    
    # Show all admins after fix
    print("\n📋 All admins after fix:")
    admins = await db.users.find({'role': 'admin'}, {'_id': 0, 'password': 0}).to_list(length=10)
    for admin in admins:
        print(f"  - {admin.get('email')} - ID: {admin.get('id')}")

if __name__ == "__main__":
    asyncio.run(fix_duplicate_ids())
