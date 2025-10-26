import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
import uuid
from datetime import datetime, timezone

# Watch images for ReplicaRolex theme
WATCH_IMAGES = [
    "https://images.unsplash.com/photo-1523275335684-37898b6baf30?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwxfHx3YXRjaHxlbnwwfHx8fDE3NjA0ODc2ODl8MA&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1594534475808-b18fc33b045e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwyfHx3YXRjaHxlbnwwfHx8fDE3NjA0ODc2ODl8MA&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1548181622-6ac4ac7b5b5d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwzfHx3YXRjaHxlbnwwfHx8fDE3NjA0ODc2ODl8MA&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1606859065739-36aa4e4f4b83?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHw0fHx3YXRjaHxlbnwwfHx8fDE3NjA0ODc2ODl8MA&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHw1fHx3YXRjaHxlbnwwfHx8fDE3NjA0ODc2ODl8MA&ixlib=rb-4.1.0&q=85"
]

async def add_watch_products():
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'test_database')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("Adding watch products for ReplicaRolex theme...")
    
    # Add Watches category
    watches_category = {
        'id': str(uuid.uuid4()),
        'name': 'Watches',
        'slug': 'watches',
        'description': 'Luxury replica watches - highest quality 1:1 superclones',
        'image': WATCH_IMAGES[0],
        'created_at': datetime.now(timezone.utc).isoformat()
    }
    await db.categories.insert_one(watches_category)
    print(f"✓ Created Watches category")
    
    # Create watch products with ReplicaRolex theme
    watch_products = [
        {
            'id': str(uuid.uuid4()),
            'name': 'Rolex Submariner 1:1 Superclone',
            'description': 'Perfect 1:1 replica of the iconic Rolex Submariner. Swiss movement, ceramic bezel, and waterproof construction. Indistinguishable from the original.',
            'price': 450.00,
            'compare_at_price': 599.00,
            'images': [WATCH_IMAGES[0], WATCH_IMAGES[1]],
            'category': 'watches',
            'stock': 25,
            'featured': True,
            'on_sale': True,
            'best_seller': True,
            'tags': ['rolex', 'submariner', 'diving', 'luxury'],
            'meta_title': 'Rolex Submariner Replica - 1:1 Superclone Watch',
            'meta_description': 'High-quality Rolex Submariner replica with Swiss movement and ceramic bezel.',
            'rating': 4.8,
            'reviews_count': 127,
            'created_at': datetime.now(timezone.utc).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Rolex Daytona Cosmograph Replica',
            'description': 'Stunning replica of the legendary Rolex Daytona. Chronograph function, tachymeter bezel, and premium steel construction.',
            'price': 520.00,
            'compare_at_price': 699.00,
            'images': [WATCH_IMAGES[1], WATCH_IMAGES[2]],
            'category': 'watches',
            'stock': 18,
            'featured': True,
            'on_sale': True,
            'is_new': True,
            'tags': ['rolex', 'daytona', 'chronograph', 'racing'],
            'meta_title': 'Rolex Daytona Replica - Racing Chronograph Watch',
            'meta_description': 'Premium Rolex Daytona replica with working chronograph and tachymeter.',
            'rating': 4.9,
            'reviews_count': 89,
            'created_at': datetime.now(timezone.utc).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Rolex GMT-Master II Superclone',
            'description': 'Exceptional GMT-Master II replica with dual time zone function. Perfect for travelers and watch enthusiasts.',
            'price': 480.00,
            'images': [WATCH_IMAGES[2], WATCH_IMAGES[3]],
            'category': 'watches',
            'stock': 22,
            'featured': True,
            'is_new': True,
            'tags': ['rolex', 'gmt', 'travel', 'pilot'],
            'meta_title': 'Rolex GMT-Master II Replica - Dual Time Zone Watch',
            'meta_description': 'High-end GMT-Master II replica with working GMT function.',
            'rating': 4.7,
            'reviews_count': 156,
            'created_at': datetime.now(timezone.utc).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Omega Speedmaster Professional',
            'description': 'Legendary Omega Speedmaster "Moonwatch" replica. Manual wind chronograph with hesalite crystal.',
            'price': 380.00,
            'compare_at_price': 499.00,
            'images': [WATCH_IMAGES[3], WATCH_IMAGES[4]],
            'category': 'watches',
            'stock': 30,
            'featured': True,
            'on_sale': True,
            'tags': ['omega', 'speedmaster', 'moonwatch', 'chronograph'],
            'meta_title': 'Omega Speedmaster Replica - Moonwatch Professional',
            'meta_description': 'Authentic Omega Speedmaster replica with manual chronograph movement.',
            'rating': 4.6,
            'reviews_count': 203,
            'created_at': datetime.now(timezone.utc).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Audemars Piguet Royal Oak',
            'description': 'Iconic Royal Oak replica with octagonal bezel and "Tapisserie" dial. A masterpiece of horological design.',
            'price': 650.00,
            'images': [WATCH_IMAGES[4], WATCH_IMAGES[0]],
            'category': 'watches',
            'stock': 12,
            'featured': True,
            'best_seller': True,
            'tags': ['audemars piguet', 'royal oak', 'luxury', 'steel'],
            'meta_title': 'Audemars Piguet Royal Oak Replica - Luxury Steel Watch',
            'meta_description': 'Premium Royal Oak replica with signature octagonal bezel design.',
            'rating': 4.9,
            'reviews_count': 78,
            'created_at': datetime.now(timezone.utc).isoformat()
        }
    ]
    
    await db.products.insert_many(watch_products)
    print(f"✓ Created {len(watch_products)} watch products")
    
    # Update existing products to have badges for testing
    await db.products.update_many(
        {'category': 'fashion'},
        {'$set': {'is_new': True}}
    )
    
    await db.products.update_many(
        {'category': 'jewelry'},
        {'$set': {'best_seller': True}}
    )
    
    print("✓ Updated existing products with badges")
    
    print("\n✅ Watch products added successfully!")
    print("ReplicaRolex theme is now ready!")
    
    client.close()

if __name__ == '__main__':
    asyncio.run(add_watch_products())