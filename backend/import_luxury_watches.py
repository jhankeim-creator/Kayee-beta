"""
Import luxury watch replicas with pricing from unitedluxury.net
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

# Watch models with realistic pricing based on unitedluxury.net
WATCH_COLLECTIONS = {
    "rolex": {
        "category": "jewelry",
        "brand": "Rolex",
        "models": [
            {"name": "Submariner Date 126610LN", "price": 1299, "tags": ["dive", "steel"]},
            {"name": "Daytona Gold 40mm", "price": 1599, "tags": ["chronograph", "gold"]},
            {"name": "GMT-Master II Batman", "price": 1399, "tags": ["gmt", "blue/black"]},
            {"name": "Datejust 36mm Steel/Gold", "price": 1199, "tags": ["classic", "twotone"]},
            {"name": "Yacht-Master 42mm", "price": 1449, "tags": ["sport", "platinum"]},
            {"name": "Explorer II Polar", "price": 1249, "tags": ["explorer", "white"]},
            {"name": "Sea-Dweller 43mm", "price": 1499, "tags": ["dive", "professional"]},
            {"name": "Sky-Dweller Rose Gold", "price": 1699, "tags": ["complication", "rose gold"]},
            {"name": "Day-Date 40 President", "price": 1649, "tags": ["presidential", "gold"]},
            {"name": "Air-King Black Dial", "price": 999, "tags": ["pilot", "steel"]},
            {"name": "Milgauss Green Crystal", "price": 1299, "tags": ["antimagnetic", "green"]},
            {"name": "Oyster Perpetual 41mm", "price": 899, "tags": ["classic", "colorful"]},
            {"name": "Submariner Hulk Green", "price": 1399, "tags": ["dive", "green", "hulk"]},
            {"name": "Submariner Smurf Blue", "price": 1399, "tags": ["dive", "blue", "smurf"]},
            {"name": "Daytona Panda White", "price": 1549, "tags": ["chronograph", "panda"]}
        ]
    },
    "patek_philippe": {
        "category": "jewelry",
        "brand": "Patek Philippe",
        "models": [
            {"name": "Nautilus 5711/1A Blue", "price": 1599, "tags": ["sport", "blue"]},
            {"name": "Nautilus 5719/10G Iced Out", "price": 1750, "tags": ["luxury", "diamonds"]},
            {"name": "Aquanaut 5167A Black", "price": 1399, "tags": ["sport", "rubber"]},
            {"name": "Calatrava 5196G White Gold", "price": 1499, "tags": ["dress", "classic"]},
            {"name": "Complications Annual Calendar", "price": 1699, "tags": ["complication", "moon"]},
            {"name": "Nautilus 5726A Blue", "price": 1649, "tags": ["annual calendar", "sport"]},
            {"name": "Aquanaut 5168G Blue", "price": 1549, "tags": ["large", "rubber"]},
            {"name": "Grand Complications", "price": 1899, "tags": ["perpetual", "tourbillon"]}
        ]
    },
    "audemars_piguet": {
        "category": "jewelry",
        "brand": "Audemars Piguet",
        "models": [
            {"name": "Royal Oak 15400ST Blue", "price": 1549, "tags": ["iconic", "blue"]},
            {"name": "Royal Oak Offshore Chrono", "price": 1699, "tags": ["chronograph", "large"]},
            {"name": "Royal Oak Iced Out", "price": 1899, "tags": ["diamonds", "luxury"]},
            {"name": "Royal Oak Perpetual Calendar", "price": 1850, "tags": ["complication", "moon"]},
            {"name": "Royal Oak Jumbo Extra-Thin", "price": 1649, "tags": ["thin", "classic"]},
            {"name": "Code 11.59 Chronograph", "price": 1599, "tags": ["modern", "chronograph"]},
            {"name": "Royal Oak Offshore Diver", "price": 1749, "tags": ["dive", "sport"]}
        ]
    },
    "omega": {
        "category": "jewelry",
        "brand": "Omega",
        "models": [
            {"name": "Seamaster Diver 300M Blue", "price": 899, "tags": ["dive", "blue", "007"]},
            {"name": "Speedmaster Moonwatch", "price": 999, "tags": ["chronograph", "moon"]},
            {"name": "Seamaster Aqua Terra", "price": 849, "tags": ["dress", "sport"]},
            {"name": "Speedmaster Racing", "price": 949, "tags": ["chronograph", "racing"]},
            {"name": "Seamaster Planet Ocean", "price": 999, "tags": ["dive", "orange"]},
            {"name": "Constellation Manhattan", "price": 799, "tags": ["dress", "star"]},
            {"name": "Seamaster 007 Edition", "price": 1099, "tags": ["limited", "007"]}
        ]
    },
    "cartier": {
        "category": "jewelry",
        "brand": "Cartier",
        "models": [
            {"name": "Santos de Cartier Large", "price": 1199, "tags": ["pilot", "square"]},
            {"name": "Tank Solo Steel", "price": 899, "tags": ["rectangular", "dress"]},
            {"name": "Ballon Bleu 42mm Blue", "price": 1099, "tags": ["blue", "round"]},
            {"name": "Drive de Cartier", "price": 1049, "tags": ["cushion", "elegant"]},
            {"name": "Pasha de Cartier", "price": 1149, "tags": ["crown", "sport"]},
            {"name": "Tank Française", "price": 999, "tags": ["bracelet", "integrated"]}
        ]
    },
    "tag_heuer": {
        "category": "jewelry",
        "brand": "TAG Heuer",
        "models": [
            {"name": "Monaco Chronograph", "price": 799, "tags": ["square", "racing"]},
            {"name": "Carrera Calibre 16", "price": 749, "tags": ["chronograph", "sport"]},
            {"name": "Aquaracer 300M", "price": 699, "tags": ["dive", "professional"]},
            {"name": "Formula 1 Chronograph", "price": 649, "tags": ["racing", "colorful"]},
            {"name": "Autavia Chronograph", "price": 849, "tags": ["vintage", "pilot"]}
        ]
    },
    "hublot": {
        "category": "jewelry",
        "brand": "Hublot",
        "models": [
            {"name": "Big Bang Classic Fusion", "price": 1399, "tags": ["modern", "skeleton"]},
            {"name": "Big Bang Unico Titanium", "price": 1499, "tags": ["chronograph", "titanium"]},
            {"name": "Classic Fusion Black Magic", "price": 1299, "tags": ["ceramic", "black"]},
            {"name": "Spirit of Big Bang", "price": 1549, "tags": ["tonneau", "skeleton"]}
        ]
    },
    "iwc": {
        "category": "jewelry",
        "brand": "IWC",
        "models": [
            {"name": "Portuguese Chronograph", "price": 1199, "tags": ["chronograph", "classic"]},
            {"name": "Pilot's Watch Mark XVIII", "price": 999, "tags": ["pilot", "military"]},
            {"name": "Aquatimer Automatic", "price": 1099, "tags": ["dive", "professional"]},
            {"name": "Portofino Automatic", "price": 949, "tags": ["dress", "elegant"]}
        ]
    }
}

async def import_watches():
    """Import luxury watch replicas"""
    
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("=" * 80)
    print("⌚ IMPORTING LUXURY WATCH REPLICAS")
    print("   Pricing based on unitedluxury.net 2024-2025")
    print("=" * 80)
    
    all_watches = []
    
    for brand_key, brand_info in WATCH_COLLECTIONS.items():
        print(f"\n⌚ {brand_info['brand']}")
        print(f"   Models: {len(brand_info['models'])}")
        
        for model_info in brand_info['models']:
            watch_id = f"watch_{brand_key}_{model_info['name'].replace(' ', '_').lower()}_{int(datetime.now(timezone.utc).timestamp())}"
            
            base_price = model_info['price']
            # Add some variation
            price = round(base_price + random.uniform(-50, 50), 2)
            # Ensure minimum $200
            price = max(price, 200.0)
            
            # Some watches on sale
            on_sale = random.random() > 0.7
            compare_at_price = round(price * random.uniform(1.5, 2.0), 2) if on_sale else None
            
            watch = {
                "id": watch_id,
                "name": f"{brand_info['brand']} {model_info['name']}",
                "description": f"1:1 Superclone {brand_info['brand']} {model_info['name']} - Swiss movement, sapphire crystal, 904L stainless steel. Water resistant. Comes with branded box and papers (optional). Identical to authentic model.",
                "price": price,
                "compare_at_price": compare_at_price,
                "images": [
                    f"https://via.placeholder.com/600x600.png?text={brand_info['brand']}+{model_info['name'].replace(' ', '+')}",
                    f"https://via.placeholder.com/600x600.png?text={brand_info['brand']}+back"
                ],
                "category": "jewelry",
                "stock": random.randint(3, 15),
                "sku": f"{brand_key.upper()}-{model_info['name'][:10].replace(' ', '').upper()}",
                "featured": random.random() > 0.7,
                "on_sale": on_sale,
                "is_new": random.random() > 0.6,
                "best_seller": random.random() > 0.75,
                "tags": [brand_key, "watch", "luxury", "superclone"] + model_info["tags"],
                "rating": round(random.uniform(4.5, 5.0), 1),
                "reviews_count": random.randint(15, 150),
                "weight": 0.2,  # kg
                "meta_title": f"{brand_info['brand']} {model_info['name']} - 1:1 Superclone",
                "meta_description": f"Buy {brand_info['brand']} {model_info['name']} superclone replica watch. Swiss movement, sapphire crystal. ${price}",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            all_watches.append(watch)
    
    print(f"\n📊 TOTAL WATCHES: {len(all_watches)}")
    
    # Insert into database
    print(f"\n💾 Inserting watches into database...")
    inserted_count = 0
    for watch in all_watches:
        existing = await db.products.find_one({"sku": watch["sku"]})
        if not existing:
            await db.products.insert_one(watch)
            inserted_count += 1
    
    print(f"   ✅ Inserted {inserted_count} new watches")
    print(f"   ℹ️  Skipped {len(all_watches) - inserted_count} duplicates")
    
    # Pricing summary
    prices = [w["price"] for w in all_watches]
    print(f"\n💰 WATCH PRICING SUMMARY:")
    print(f"   Minimum: ${min(prices):.2f}")
    print(f"   Maximum: ${max(prices):.2f}")
    print(f"   Average: ${sum(prices)/len(prices):.2f}")
    
    # By brand
    print(f"\n⌚ WATCHES BY BRAND:")
    for brand_key, brand_info in WATCH_COLLECTIONS.items():
        count = len(brand_info['models'])
        avg_price = sum(m['price'] for m in brand_info['models']) / count
        print(f"   {brand_info['brand']}: {count} models (avg ${avg_price:.0f})")
    
    client.close()
    
    print("\n" + "=" * 80)
    print("✅ WATCH IMPORT COMPLETED!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(import_watches())
