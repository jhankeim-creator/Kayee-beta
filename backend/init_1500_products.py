import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import uuid
from datetime import datetime, timezone
import random

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Sample images from vision_expert_agent
FASHION_IMAGES = [
    "https://images.unsplash.com/photo-1613909671501-f9678ffc1d33?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwxfHxsdXh1cnklMjBmYXNoaW9ufGVufDB8fHx8MTc2MDQ4NzY4OXww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1591884807235-1dc6c2e148b1?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwyfHxsdXh1cnklMjBmYXNoaW9ufGVufDB8fHx8MTc2MDQ4NzY4OXww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1589363358751-ab05797e5629?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHw0fHxsdXh1cnklMjBmYXNoaW9ufGVufDB8fHx8MTc2MDQ4NzY4OXww&ixlib=rb-4.1.0&q=85",
    "https://images.pexels.com/photos/135620/pexels-photo-135620.jpeg",
    "https://images.pexels.com/photos/336372/pexels-photo-336372.jpeg",
    "https://images.unsplash.com/photo-1591348278863-a8fb3887e2aa?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwzfHxsdXh1cnklMjBmYXNoaW9ufGVufDB8fHx8MTc2MDQ4NzY4OXww&ixlib=rb-4.1.0&q=85"
]

JEWELRY_IMAGES = [
    "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxsdXh1cnklMjBqZXdlbHJ5fGVufDB8fHx8MTc2MDUwNTkzOXww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1606623546924-a4f3ae5ea3e8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwyfHxsdXh1cnklMjBqZXdlbHJ5fGVufDB8fHx8MTc2MDUwNTkzOXww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1616837874254-8d5aaa63e273?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxsdXh1cnklMjBqZXdlbHJ5fGVufDB8fHx8MTc2MDUwNTkzOXww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1727784892059-c85b4d9f763c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHw0fHxsdXh1cnklMjBqZXdlbHJ5fGVufDB8fHx8MTc2MDUwNTkzOXww&ixlib=rb-4.1.0&q=85",
    "https://images.pexels.com/photos/34299107/pexels-photo-34299107.jpeg",
    "https://images.pexels.com/photos/34253028/pexels-photo-34253028.jpeg"
]

# Product name templates
FASHION_NAMES = [
    "Designer Evening Gown", "Luxury Handbag Collection", "Classic Leather Bag", "Designer Accessories Set",
    "Silk Dress", "Cashmere Sweater", "Leather Jacket", "Designer Jeans", "Evening Clutch", "Designer Sunglasses",
    "Wool Coat", "Linen Shirt", "Satin Blouse", "Designer Belt", "Leather Boots", "High Heels", "Sneakers",
    "Trench Coat", "Blazer", "Suit", "Tie", "Scarf", "Hat", "Gloves", "Wallet", "Backpack", "Tote Bag",
    "Crossbody Bag", "Travel Bag", "Business Bag", "Evening Dress", "Cocktail Dress", "Summer Dress",
    "Winter Coat", "Spring Jacket", "Autumn Cardigan", "Formal Shirt", "Casual Shirt", "T-Shirt",
    "Polo Shirt", "Hoodie", "Sweatshirt", "Cardigan", "Pullover", "Vest", "Tank Top", "Shorts",
    "Skirt", "Pants", "Leggings", "Joggers"
]

JEWELRY_NAMES = [
    "Pearl Necklace Deluxe", "Gemstone Cocktail Ring", "Gold Statement Necklace", "Diamond Stud Earrings",
    "Vintage Jewelry Collection", "Silver Bracelet", "Gold Chain", "Diamond Ring", "Emerald Ring",
    "Sapphire Necklace", "Ruby Earrings", "Platinum Band", "Tennis Bracelet", "Charm Bracelet",
    "Pendant Necklace", "Hoop Earrings", "Drop Earrings", "Chandelier Earrings", "Stud Earrings",
    "Gold Bangle", "Silver Bangle", "Cuff Bracelet", "Link Bracelet", "Beaded Bracelet",
    "Statement Ring", "Engagement Ring", "Wedding Band", "Eternity Ring", "Signet Ring",
    "Cocktail Ring", "Fashion Ring", "Midi Ring", "Pinky Ring", "Toe Ring",
    "Anklet", "Body Chain", "Brooch", "Cufflinks", "Tie Pin", "Lapel Pin",
    "Hair Clip", "Hair Pin", "Tiara", "Crown", "Choker", "Locket",
    "Cross Pendant", "Heart Pendant", "Initial Pendant", "Gemstone Pendant"
]

DESCRIPTIONS = [
    "Stunning piece perfect for special occasions. Made from premium materials with elegant detailing.",
    "Premium quality with exquisite craftsmanship. Spacious and functional design.",
    "Timeless design in rich tones. Perfect for everyday elegance and professional settings.",
    "Complete set of luxury items. Make a statement with this curated collection.",
    "Elegant and sophisticated piece. Features high-quality materials and modern styling.",
    "Classic design with contemporary twist. Versatile piece for any wardrobe.",
    "Luxurious and comfortable. Crafted with attention to detail and quality.",
    "Bold and eye-catching design. Perfect for making a fashion statement.",
    "Minimalist and refined style. Ideal for both casual and formal occasions.",
    "Artisan-crafted with precision. Unique piece that showcases exceptional quality."
]

async def init_database():
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'test_database')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("Initializing database with 1500 products...")
    
    # Clear existing data
    await db.categories.delete_many({})
    await db.products.delete_many({})
    await db.users.delete_many({})
    
    # Create admin user
    admin_user = {
        'id': str(uuid.uuid4()),
        'email': 'admin@luxeboutique.com',
        'name': 'Admin User',
        'role': 'admin',
        'password_hash': pwd_context.hash('admin123'),
        'created_at': datetime.now(timezone.utc).isoformat()
    }
    await db.users.insert_one(admin_user)
    print(f"✓ Created admin user: {admin_user['email']} / admin123")
    
    # Create categories
    categories = [
        {
            'id': str(uuid.uuid4()),
            'name': 'Fashion',
            'slug': 'fashion',
            'description': 'Elegant fashion pieces for every occasion',
            'image': FASHION_IMAGES[0],
            'created_at': datetime.now(timezone.utc).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Jewelry',
            'slug': 'jewelry',
            'description': 'Exquisite jewelry to complete your look',
            'image': JEWELRY_IMAGES[0],
            'created_at': datetime.now(timezone.utc).isoformat()
        }
    ]
    await db.categories.insert_many(categories)
    print(f"✓ Created {len(categories)} categories")
    
    # Create 1500 products
    products = []
    batch_size = 100
    
    for i in range(1500):
        # Alternate between fashion and jewelry
        is_fashion = i % 2 == 0
        category = 'fashion' if is_fashion else 'jewelry'
        
        if is_fashion:
            name = random.choice(FASHION_NAMES)
            images = [random.choice(FASHION_IMAGES) for _ in range(random.randint(1, 3))]
        else:
            name = random.choice(JEWELRY_NAMES)
            images = [random.choice(JEWELRY_IMAGES) for _ in range(random.randint(1, 3))]
        
        # Add number to name for uniqueness
        name = f"{name} #{i+1}"
        
        product = {
            'id': str(uuid.uuid4()),
            'name': name,
            'description': random.choice(DESCRIPTIONS),
            'price': round(random.uniform(49.99, 1999.99), 2),
            'images': images,
            'category': category,
            'stock': random.randint(0, 50),
            'featured': i < 50,  # First 50 products are featured
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        products.append(product)
        
        # Insert in batches for better performance
        if len(products) >= batch_size:
            await db.products.insert_many(products)
            print(f"✓ Created {i+1} products...")
            products = []
    
    # Insert remaining products
    if products:
        await db.products.insert_many(products)
    
    print(f"\n✅ Database initialized successfully with 1500 products!")
    print("\nAdmin credentials:")
    print("Email: admin@luxeboutique.com")
    print("Password: admin123")
    
    # Show stats
    fashion_count = await db.products.count_documents({'category': 'fashion'})
    jewelry_count = await db.products.count_documents({'category': 'jewelry'})
    featured_count = await db.products.count_documents({'featured': True})
    
    print(f"\nProduct Statistics:")
    print(f"- Fashion items: {fashion_count}")
    print(f"- Jewelry items: {jewelry_count}")
    print(f"- Featured products: {featured_count}")
    
    client.close()

if __name__ == '__main__':
    asyncio.run(init_database())
