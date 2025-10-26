"""
Delete imported products and keep only originals
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def delete_imported_products():
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    print("🗑️  Deleting imported products...")
    
    # Count before
    before = await db.products.count_documents({})
    print(f'📊 Products before deletion: {before}')
    
    # Delete products with SKUs starting with specific patterns
    result = await db.products.delete_many({
        "$or": [
            {"sku": {"$regex": "^QQ-"}},
            {"sku": {"$regex": "^ROLEX"}},
            {"sku": {"$regex": "^PATEK"}},
            {"sku": {"$regex": "^AUDEM"}},
            {"sku": {"$regex": "^OMEGA"}},
            {"sku": {"$regex": "^CARTI"}},
            {"sku": {"$regex": "^TAG_H"}},
            {"sku": {"$regex": "^HUBLO"}},
            {"sku": {"$regex": "^IWC-"}},
            {"sku": {"$regex": "^NIKE_"}},
            {"sku": {"$regex": "^YEEZY"}},
            {"sku": {"$regex": "^BALEN"}},
            {"sku": {"$regex": "^GOLDE"}},
            {"sku": {"$regex": "^LOUIS"}},
            {"sku": {"$regex": "^GUCCI"}},
            {"sku": {"$regex": "^DIOR_"}},
            {"sku": {"$regex": "^NEW_B"}},
            {"sku": {"$regex": "^CONVE"}},
            {"sku": {"$regex": "^VANS"}}
        ]
    })
    
    print(f'✅ Deleted {result.deleted_count} imported products')
    
    # Count after
    after = await db.products.count_documents({})
    print(f'📊 Products remaining: {after}')
    
    client.close()

if __name__ == "__main__":
    asyncio.run(delete_imported_products())
