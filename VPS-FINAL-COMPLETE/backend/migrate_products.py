"""
Migration script to update existing products with new Ecwid-style fields
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def migrate_products():
    """Add new fields to existing products"""
    
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Starting product migration...")
    
    # Get all products
    products = await db.products.find({}, {"_id": 0}).to_list(None)
    print(f"Found {len(products)} products to migrate")
    
    updated_count = 0
    for product in products:
        updates = {}
        
        # Add new fields if they don't exist
        if "compare_at_price" not in product:
            updates["compare_at_price"] = None
        if "cost" not in product:
            updates["cost"] = None
        if "sku" not in product:
            updates["sku"] = None
        if "barcode" not in product:
            updates["barcode"] = None
        if "weight" not in product:
            updates["weight"] = None
        if "on_sale" not in product:
            updates["on_sale"] = False
        if "is_new" not in product:
            # Mark recent products (last 30 days) as new
            if "created_at" in product:
                created_at_str = product["created_at"]
                if isinstance(created_at_str, str):
                    created_at = datetime.fromisoformat(created_at_str)
                else:
                    created_at = created_at_str
                days_old = (datetime.now(timezone.utc) - created_at).days
                updates["is_new"] = days_old <= 30
            else:
                updates["is_new"] = False
        if "best_seller" not in product:
            updates["best_seller"] = False
        if "digital_product" not in product:
            updates["digital_product"] = False
        if "download_url" not in product:
            updates["download_url"] = None
        if "tags" not in product:
            updates["tags"] = []
        if "meta_title" not in product:
            updates["meta_title"] = None
        if "meta_description" not in product:
            updates["meta_description"] = None
        if "has_variations" not in product:
            updates["has_variations"] = False
        if "variations_count" not in product:
            updates["variations_count"] = 0
        if "rating" not in product:
            updates["rating"] = 0.0
        if "reviews_count" not in product:
            updates["reviews_count"] = 0
        if "view_count" not in product:
            updates["view_count"] = 0
        if "sales_count" not in product:
            updates["sales_count"] = 0
        if "updated_at" not in product:
            updates["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        if updates:
            await db.products.update_one(
                {"id": product["id"]},
                {"$set": updates}
            )
            updated_count += 1
    
    print(f"✅ Migration complete! Updated {updated_count} products")
    
    # Create default store settings if not exists
    settings = await db.store_settings.find_one({"id": "store_settings"})
    if not settings:
        print("Creating default store settings...")
        default_settings = {
            "id": "store_settings",
            "store_name": "LuxeBoutique",
            "store_logo": None,
            "store_description": "Luxury fashion and jewelry store",
            "primary_color": "#d4af37",
            "secondary_color": "#000000",
            "email_from": "noreply@luxeboutique.com",
            "email_notifications": True,
            "currency": "USD",
            "tax_rate": 0.0,
            "tax_included": False,
            "free_shipping_threshold": 100.0,
            "default_shipping_cost": 10.0,
            "low_stock_threshold": 5,
            "out_of_stock_behavior": "show",
            "auto_complete_orders": False,
            "order_prefix": "ORD-",
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
        await db.store_settings.insert_one(default_settings)
        print("✅ Store settings created")
    
    client.close()
    print("✅ All migrations complete!")

if __name__ == "__main__":
    asyncio.run(migrate_products())
