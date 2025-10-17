"""
Add test categories and 5 sample products
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
import uuid

load_dotenv()

async def add_test_data():
    """Add categories and products"""
    
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    print("=" * 80)
    print("📦 ADDING TEST DATA")
    print("=" * 80)
    
    # Create categories
    categories = [
        {
            "id": "cat-watches",
            "name": "Watches",
            "description": "Luxury replica watches",
            "slug": "watches",
            "parent_id": None,
            "product_count": 0,
            "display_order": 1,
            "active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "cat-bags",
            "name": "Bags",
            "description": "Designer replica bags",
            "slug": "bags",
            "parent_id": None,
            "product_count": 0,
            "display_order": 2,
            "active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "cat-jewelry",
            "name": "Jewelry",
            "description": "Luxury replica jewelry",
            "slug": "jewelry",
            "parent_id": None,
            "product_count": 0,
            "display_order": 3,
            "active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Insert categories
    for cat in categories:
        existing = await db.categories.find_one({"slug": cat["slug"]})
        if not existing:
            await db.categories.insert_one(cat)
            print(f"✅ Category created: {cat['name']}")
    
    # Subcategories for Watches
    watch_subcategories = [
        {
            "id": "subcat-rolex",
            "name": "Rolex",
            "description": "Rolex replica watches",
            "slug": "rolex",
            "parent_id": "cat-watches",
            "product_count": 0,
            "display_order": 1,
            "active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "subcat-omega",
            "name": "Omega",
            "description": "Omega replica watches",
            "slug": "omega",
            "parent_id": "cat-watches",
            "product_count": 0,
            "display_order": 2,
            "active": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    for subcat in watch_subcategories:
        existing = await db.categories.find_one({"slug": subcat["slug"]})
        if not existing:
            await db.categories.insert_one(subcat)
            print(f"✅ Subcategory created: {subcat['name']}")
    
    # 5 Test Products
    products = [
        {
            "id": str(uuid.uuid4()),
            "name": "Rolex Submariner Date 126610LN",
            "description": "The Rolex Submariner Date 126610LN is an iconic dive watch featuring a 41mm case in 904L stainless steel, black Cerachrom bezel, and the reliable Caliber 3235 movement. Water-resistant to 300m, this timepiece combines legendary design with cutting-edge technology. Perfect 1:1 superclone replica with Swiss movement.",
            "price": 1299.00,
            "compare_at_price": 1899.00,
            "images": [
                "https://images.unsplash.com/photo-1523275335684-37898b6baf30",
                "https://images.unsplash.com/photo-1524805444758-089113d48a6d"
            ],
            "videos": [],
            "category_id": "cat-watches",
            "subcategory_id": "subcat-rolex",
            "stock": 15,
            "sku": "ROLEX-SUB-001",
            "meta_title": "Rolex Submariner 126610LN Replica - 1:1 Superclone",
            "meta_description": "Buy Rolex Submariner Date 126610LN replica watch. Swiss movement, 904L steel, sapphire crystal. Perfect 1:1 clone.",
            "tags": ["rolex", "submariner", "dive watch", "luxury"],
            "featured": True,
            "on_sale": True,
            "is_new": True,
            "best_seller": True,
            "rating": 4.9,
            "reviews_count": 156,
            "view_count": 2341,
            "sales_count": 89,
            "active": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Rolex Daytona 116500LN White Dial",
            "description": "The Rolex Cosmograph Daytona 116500LN features a stunning white dial with black subdials, housed in a 40mm Oystersteel case. Powered by the Caliber 4130 chronograph movement. This superclone replica captures every detail of the authentic model.",
            "price": 1599.00,
            "compare_at_price": None,
            "images": [
                "https://images.unsplash.com/photo-1587836374828-4dbafa94cf0e",
                "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd"
            ],
            "videos": [],
            "category_id": "cat-watches",
            "subcategory_id": "subcat-rolex",
            "stock": 8,
            "sku": "ROLEX-DAY-002",
            "meta_title": "Rolex Daytona 116500LN White Dial Replica",
            "meta_description": "Rolex Daytona 116500LN superclone with white panda dial. Swiss chronograph movement.",
            "tags": ["rolex", "daytona", "chronograph", "white dial"],
            "featured": True,
            "on_sale": False,
            "is_new": True,
            "best_seller": True,
            "rating": 4.8,
            "reviews_count": 203,
            "view_count": 3102,
            "sales_count": 124,
            "active": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Omega Seamaster Diver 300M Blue",
            "description": "The Omega Seamaster Diver 300M in blue is a professional diving watch with a 42mm case, ceramic bezel, and the Co-Axial Master Chronometer movement. Features wave-pattern dial and helium escape valve. Superclone quality replica.",
            "price": 899.00,
            "compare_at_price": 1299.00,
            "images": [
                "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1",
                "https://images.unsplash.com/photo-1523275335684-37898b6baf30"
            ],
            "videos": [],
            "category_id": "cat-watches",
            "subcategory_id": "subcat-omega",
            "stock": 12,
            "sku": "OMEGA-SEA-003",
            "meta_title": "Omega Seamaster 300M Blue Replica Watch",
            "meta_description": "Omega Seamaster Diver 300M blue dial replica. Swiss movement, ceramic bezel.",
            "tags": ["omega", "seamaster", "dive watch", "blue"],
            "featured": True,
            "on_sale": True,
            "is_new": False,
            "best_seller": True,
            "rating": 4.7,
            "reviews_count": 178,
            "view_count": 1876,
            "sales_count": 92,
            "active": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Louis Vuitton Neverfull MM Monogram",
            "description": "The iconic Louis Vuitton Neverfull MM in classic monogram canvas. This versatile tote features natural cowhide leather trim, golden hardware, and spacious interior. Perfect for everyday use. High-quality 1:1 replica with authentic details.",
            "price": 549.00,
            "compare_at_price": None,
            "images": [
                "https://images.unsplash.com/photo-1590874103328-eac38a683ce7",
                "https://images.unsplash.com/photo-1566150905458-1bf1fc113f0d"
            ],
            "videos": [],
            "category_id": "cat-bags",
            "stock": 20,
            "sku": "LV-NEV-004",
            "meta_title": "Louis Vuitton Neverfull MM Replica",
            "meta_description": "LV Neverfull MM monogram replica bag. High quality leather, authentic details.",
            "tags": ["louis vuitton", "neverfull", "tote", "monogram"],
            "featured": True,
            "on_sale": False,
            "is_new": True,
            "best_seller": True,
            "rating": 4.9,
            "reviews_count": 267,
            "view_count": 4512,
            "sales_count": 203,
            "active": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Cartier Love Bracelet 18K Gold",
            "description": "The iconic Cartier Love Bracelet in 18K yellow gold with screw motif. This timeless piece symbolizes eternal love and commitment. Comes with screwdriver. High-quality replica with solid construction and authentic weight.",
            "price": 799.00,
            "compare_at_price": 1199.00,
            "images": [
                "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338",
                "https://images.unsplash.com/photo-1611591437281-460bfbe1220a"
            ],
            "videos": [],
            "category_id": "cat-jewelry",
            "stock": 18,
            "sku": "CART-LOVE-005",
            "meta_title": "Cartier Love Bracelet Gold Replica",
            "meta_description": "Cartier Love Bracelet 18K gold replica. Authentic design, solid construction.",
            "tags": ["cartier", "love bracelet", "gold", "jewelry"],
            "featured": True,
            "on_sale": True,
            "is_new": False,
            "best_seller": True,
            "rating": 4.8,
            "reviews_count": 189,
            "view_count": 2890,
            "sales_count": 145,
            "active": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Insert products
    for product in products:
        existing = await db.products.find_one({"sku": product["sku"]})
        if not existing:
            await db.products.insert_one(product)
            print(f"✅ Product created: {product['name']}")
            
            # Update category count
            await db.categories.update_one(
                {"id": product["category_id"]},
                {"$inc": {"product_count": 1}}
            )
    
    print(f"\n✅ Test data created successfully!")
    print(f"   - 3 Categories")
    print(f"   - 2 Subcategories")
    print(f"   - 5 Products")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_test_data())
