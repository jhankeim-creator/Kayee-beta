import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import uuid
from datetime import datetime, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Sample images from vision_expert_agent
FASHION_IMAGES = [
    "https://images.unsplash.com/photo-1613909671501-f9678ffc1d33?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwxfHxsdXh1cnklMjBmYXNoaW9ufGVufDB8fHx8MTc2MDQ4NzY4OXww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1591884807235-1dc6c2e148b1?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwyfHxsdXh1cnklMjBmYXNoaW9ufGVufDB8fHx8MTc2MDQ4NzY4OXww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1589363358751-ab05797e5629?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHw0fHxsdXh1cnklMjBmYXNoaW9ufGVufDB8fHx8MTc2MDQ4NzY4OXww&ixlib=rb-4.1.0&q=85",
    "https://images.pexels.com/photos/135620/pexels-photo-135620.jpeg",
    "https://images.pexels.com/photos/336372/pexels-photo-336372.jpeg"
]

JEWELRY_IMAGES = [
    "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxsdXh1cnklMjBqZXdlbHJ5fGVufDB8fHx8MTc2MDUwNTkzOXww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1606623546924-a4f3ae5ea3e8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwyfHxsdXh1cnklMjBqZXdlbHJ5fGVufDB8fHx8MTc2MDUwNTkzOXww&ixlib=rb-4.1.0&q=85",
    "https://images.unsplash.com/photo-1616837874254-8d5aaa63e273?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxsdXh1cnklMjBqZXdlbHJ5fGVufDB8fHx8MTc2MDUwNTkzOXww&ixlib=rb-4.1.0&q=85",
    "https://images.pexels.com/photos/34299107/pexels-photo-34299107.jpeg",
    "https://images.pexels.com/photos/34253028/pexels-photo-34253028.jpeg"
]

async def init_database():
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.environ.get('DB_NAME', 'test_database')
    
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    print("Initializing database...")
    
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
    
    # Create sample products
    products = [
        # Fashion Products
        {
            'id': str(uuid.uuid4()),
            'name': 'Designer Evening Gown',
            'description': 'Stunning white evening gown perfect for special occasions. Made from premium silk with elegant draping.',
            'price': 299.99,
            'images': [FASHION_IMAGES[0], FASHION_IMAGES[1]],
            'category': 'fashion',
            'stock': 15,
            'featured': True,
            'created_at': datetime.now(timezone.utc).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Luxury Handbag Collection',
            'description': 'Premium leather handbag with gold-tone hardware. Spacious interior with multiple compartments.',
            'price': 449.99,
            'images': [FASHION_IMAGES[2], FASHION_IMAGES[3]],
            'category': 'fashion',
            'stock': 8,
            'featured': True,
            'created_at': datetime.now(timezone.utc).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Classic Leather Bag',
            'description': 'Timeless leather bag in rich brown tone. Perfect for everyday elegance and professional settings.',
            'price': 189.99,
            'images': [FASHION_IMAGES[3]],
            'category': 'fashion',
            'stock': 20,
            'featured': False,
            'created_at': datetime.now(timezone.utc).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Designer Accessories Set',
            'description': 'Complete set of luxury accessories including designer bag and heels. Make a statement with this curated collection.',
            'price': 599.99,
            'images': [FASHION_IMAGES[1]],
            'category': 'fashion',
            'stock': 5,
            'featured': False,
            'created_at': datetime.now(timezone.utc).isoformat()
        },
        # Jewelry Products
        {
            'id': str(uuid.uuid4()),
            'name': 'Pearl Necklace Deluxe',
            'description': 'Elegant pearl necklace in luxury presentation box. Premium quality pearls with 18k gold clasp.',
            'price': 899.99,
            'images': [JEWELRY_IMAGES[0], JEWELRY_IMAGES[1]],
            'category': 'jewelry',
            'stock': 10,
            'featured': True,
            'created_at': datetime.now(timezone.utc).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Gemstone Cocktail Ring',
            'description': 'Stunning cocktail ring featuring premium gemstones. Set in 18k white gold with intricate detailing.',
            'price': 1299.99,
            'images': [JEWELRY_IMAGES[1]],
            'category': 'jewelry',
            'stock': 6,
            'featured': True,
            'created_at': datetime.now(timezone.utc).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Gold Statement Necklace',
            'description': 'Bold gold necklace that makes a statement. Perfect for evening wear and special occasions.',
            'price': 749.99,
            'images': [JEWELRY_IMAGES[2]],
            'category': 'jewelry',
            'stock': 12,
            'featured': False,
            'created_at': datetime.now(timezone.utc).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Diamond Stud Earrings',
            'description': 'Classic diamond stud earrings in platinum setting. Timeless elegance for everyday luxury.',
            'price': 1599.99,
            'images': [JEWELRY_IMAGES[3]],
            'category': 'jewelry',
            'stock': 8,
            'featured': False,
            'created_at': datetime.now(timezone.utc).isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Vintage Jewelry Collection',
            'description': 'Curated collection of vintage-inspired jewelry pieces. Each piece tells a story of timeless beauty.',
            'price': 499.99,
            'images': [JEWELRY_IMAGES[4]],
            'category': 'jewelry',
            'stock': 15,
            'featured': False,
            'created_at': datetime.now(timezone.utc).isoformat()
        },
    ]
    await db.products.insert_many(products)
    print(f"✓ Created {len(products)} products")
    
    print("\n✅ Database initialized successfully!")
    print("\nAdmin credentials:")
    print("Email: admin@luxeboutique.com")
    print("Password: admin123")
    
    client.close()

if __name__ == '__main__':
    asyncio.run(init_database())