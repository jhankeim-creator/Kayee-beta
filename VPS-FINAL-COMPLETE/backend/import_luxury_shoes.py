"""
Import luxury shoes/sneakers with appropriate pricing
Recent 2025 models: $250-450
Older models: $200-350
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timezone
import random

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

SHOE_COLLECTIONS = {
    "nike_jordan_2025": {
        "brand": "Nike Jordan",
        "category": "fashion",
        "is_recent": True,
        "models": [
            {"name": "Air Jordan 1 Retro High OG 'Lost and Found'", "price": 389},
            {"name": "Air Jordan 4 Retro 'Midnight Navy'", "price": 429},
            {"name": "Air Jordan 11 Retro 'Cherry'", "price": 449},
            {"name": "Air Jordan 3 Retro 'White Cement'", "price": 409},
            {"name": "Nike Dunk Low 'Panda'", "price": 299},
            {"name": "Nike SB Dunk Low 'Travis Scott'", "price": 439},
            {"name": "Air Jordan 1 Low 'Mocha'", "price": 299},
            {"name": "Air Jordan 5 Retro 'UNC'", "price": 399}
        ]
    },
    "yeezy_2025": {
        "brand": "Adidas Yeezy",
        "category": "fashion",
        "is_recent": True,
        "models": [
            {"name": "Yeezy Boost 350 V2 'Onyx'", "price": 349},
            {"name": "Yeezy Slide 'Bone'", "price": 259},
            {"name": "Yeezy Foam Runner 'MXT Moon Gray'", "price": 279},
            {"name": "Yeezy 700 V3 'Fade Carbon'", "price": 389},
            {"name": "Yeezy Boost 380 'Mist'", "price": 339}
        ]
    },
    "balenciaga_2025": {
        "brand": "Balenciaga",
        "category": "fashion",
        "is_recent": True,
        "models": [
            {"name": "Triple S Clear Sole Black", "price": 449},
            {"name": "Track Trainer White", "price": 429},
            {"name": "Speed Trainer Black", "price": 389},
            {"name": "Runner Sneaker Grey", "price": 399},
            {"name": "Triple S White/Red", "price": 439}
        ]
    },
    "golden_goose_2025": {
        "brand": "Golden Goose",
        "category": "fashion",
        "is_recent": True,
        "models": [
            {"name": "Super-Star Classic White/Green", "price": 359},
            {"name": "Hi-Star Black Leather", "price": 379},
            {"name": "Ball Star White/Gold", "price": 369},
            {"name": "Mid-Star Distressed", "price": 389}
        ]
    },
    "louis_vuitton_shoes": {
        "brand": "Louis Vuitton",
        "category": "fashion",
        "is_recent": True,
        "models": [
            {"name": "LV Trainer Monogram", "price": 449},
            {"name": "Run Away Sneaker", "price": 429},
            {"name": "Rivoli Sneaker Boot", "price": 439},
            {"name": "Archlight Sneaker", "price": 449}
        ]
    },
    "gucci_shoes": {
        "brand": "Gucci",
        "category": "fashion",
        "is_recent": True,
        "models": [
            {"name": "Ace Embroidered Sneaker", "price": 399},
            {"name": "Rhyton Leather Sneaker", "price": 419},
            {"name": "Screener Leather Sneaker", "price": 429},
            {"name": "Flashtrek Sneaker", "price": 449}
        ]
    },
    "dior_shoes": {
        "brand": "Dior",
        "category": "fashion",
        "is_recent": True,
        "models": [
            {"name": "B23 High-Top Oblique", "price": 449},
            {"name": "B27 Low-Top", "price": 429},
            {"name": "B22 Sneaker White/Blue", "price": 439},
            {"name": "Walk'n'Dior Sneaker", "price": 419}
        ]
    },
    "nike_classic": {
        "brand": "Nike",
        "category": "fashion",
        "is_recent": False,
        "models": [
            {"name": "Air Force 1 Low White", "price": 249},
            {"name": "Air Max 90 OG", "price": 279},
            {"name": "Air Max 97 Silver Bullet", "price": 299},
            {"name": "Cortez Classic", "price": 229},
            {"name": "Blazer Mid '77 Vintage", "price": 259}
        ]
    },
    "new_balance": {
        "brand": "New Balance",
        "category": "fashion",
        "is_recent": False,
        "models": [
            {"name": "990v5 Grey", "price": 299},
            {"name": "550 White Green", "price": 279},
            {"name": "2002R Protection Pack", "price": 289},
            {"name": "574 Core", "price": 249}
        ]
    },
    "converse": {
        "brand": "Converse",
        "category": "fashion",
        "is_recent": False,
        "models": [
            {"name": "Chuck Taylor All Star High Top", "price": 219},
            {"name": "Chuck 70 High Top", "price": 249},
            {"name": "One Star Pro", "price": 239},
            {"name": "Run Star Hike", "price": 269}
        ]
    },
    "vans": {
        "brand": "Vans",
        "category": "fashion",
        "is_recent": False,
        "models": [
            {"name": "Old Skool Classic", "price": 229},
            {"name": "Sk8-Hi Black/White", "price": 249},
            {"name": "Authentic White", "price": 219},
            {"name": "Slip-On Checkerboard", "price": 229}
        ]
    }
}

async def import_shoes():
    """Import luxury shoes and sneakers"""
    
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("=" * 80)
    print("👟 IMPORTING LUXURY SHOES & SNEAKERS")
    print("   Recent 2025 models: $250-$450")
    print("   Classic/Older models: $200-$350")
    print("=" * 80)
    
    all_shoes = []
    
    for collection_key, collection_info in SHOE_COLLECTIONS.items():
        print(f"\n👟 {collection_info['brand']}")
        print(f"   Models: {len(collection_info['models'])}")
        print(f"   Type: {'Recent 2025' if collection_info['is_recent'] else 'Classic'}")
        
        for model_info in collection_info['models']:
            shoe_id = f"shoe_{collection_key}_{model_info['name'].replace(' ', '_').lower()}_{int(datetime.now(timezone.utc).timestamp())}"
            
            base_price = model_info['price']
            # Add some variation
            price = round(base_price + random.uniform(-20, 20), 2)
            
            # Ensure minimum $200
            price = max(price, 200.0)
            
            # Apply pricing rules
            if collection_info['is_recent']:
                # Recent: $250-450
                price = max(min(price, 450), 250)
            else:
                # Older: $200-350
                price = max(min(price, 350), 200)
            
            # Some shoes on sale
            on_sale = random.random() > 0.65
            compare_at_price = round(price * random.uniform(1.4, 1.8), 2) if on_sale else None
            
            shoe = {
                "id": shoe_id,
                "name": f"{collection_info['brand']} {model_info['name']}",
                "description": f"1:1 High-Quality Replica {collection_info['brand']} {model_info['name']}. Premium materials, perfect stitching, identical to authentic. Comes with original box and accessories.",
                "price": price,
                "compare_at_price": compare_at_price,
                "images": [
                    f"https://via.placeholder.com/600x600.png?text={collection_info['brand'].replace(' ', '+')}+{model_info['name'][:20].replace(' ', '+')}",
                    f"https://via.placeholder.com/600x600.png?text=Side+View"
                ],
                "category": "fashion",
                "stock": random.randint(5, 30),
                "sku": f"{collection_key.upper()[:4]}-{model_info['name'][:8].replace(' ', '').upper()}",
                "featured": random.random() > 0.75,
                "on_sale": on_sale,
                "is_new": collection_info['is_recent'] and random.random() > 0.5,
                "best_seller": random.random() > 0.80,
                "tags": [collection_key, "shoes", "sneakers", collection_info['brand'].lower().replace(' ', '_')],
                "rating": round(random.uniform(4.3, 5.0), 1),
                "reviews_count": random.randint(20, 180),
                "weight": 0.5,  # kg
                "meta_title": f"{collection_info['brand']} {model_info['name']} - 1:1 Replica",
                "meta_description": f"Buy {collection_info['brand']} {model_info['name']} high-quality replica shoes. Premium materials. ${price}",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            all_shoes.append(shoe)
    
    print(f"\n📊 TOTAL SHOES: {len(all_shoes)}")
    
    # Insert into database
    print(f"\n💾 Inserting shoes into database...")
    inserted_count = 0
    for shoe in all_shoes:
        existing = await db.products.find_one({"sku": shoe["sku"]})
        if not existing:
            await db.products.insert_one(shoe)
            inserted_count += 1
    
    print(f"   ✅ Inserted {inserted_count} new shoes")
    print(f"   ℹ️  Skipped {len(all_shoes) - inserted_count} duplicates")
    
    # Pricing summary
    prices = [s["price"] for s in all_shoes]
    recent_prices = [s["price"] for s in all_shoes if any(k in s["tags"] for k in ["nike_jordan_2025", "yeezy_2025", "balenciaga_2025", "golden_goose_2025", "louis_vuitton_shoes", "gucci_shoes", "dior_shoes"])]
    classic_prices = [s["price"] for s in all_shoes if s["price"] not in recent_prices]
    
    print(f"\n💰 SHOE PRICING SUMMARY:")
    print(f"   Overall Minimum: ${min(prices):.2f}")
    print(f"   Overall Maximum: ${max(prices):.2f}")
    print(f"   Overall Average: ${sum(prices)/len(prices):.2f}")
    
    if recent_prices:
        print(f"\n   Recent 2025 Models:")
        print(f"      Min: ${min(recent_prices):.2f}")
        print(f"      Max: ${max(recent_prices):.2f}")
        print(f"      Avg: ${sum(recent_prices)/len(recent_prices):.2f}")
    
    if classic_prices:
        print(f"\n   Classic Models:")
        print(f"      Min: ${min(classic_prices):.2f}")
        print(f"      Max: ${max(classic_prices):.2f}")
        print(f"      Avg: ${sum(classic_prices)/len(classic_prices):.2f}")
    
    # By brand
    print(f"\n👟 SHOES BY BRAND:")
    brands = {}
    for shoe in all_shoes:
        brand = shoe['name'].split()[0]
        brands[brand] = brands.get(brand, 0) + 1
    for brand, count in sorted(brands.items()):
        print(f"   {brand}: {count} models")
    
    client.close()
    
    print("\n" + "=" * 80)
    print("✅ SHOE IMPORT COMPLETED!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(import_shoes())
