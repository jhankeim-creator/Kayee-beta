"""
Update product images with real luxury fashion images
Using Unsplash API for high-quality images
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import random

load_dotenv()

# Real luxury fashion images organized by category/brand
LUXURY_IMAGES = {
    # T-shirts and casual wear
    "tshirt": [
        "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab",
        "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a",
        "https://images.unsplash.com/photo-1503341504253-dff4815485f1",
        "https://images.unsplash.com/photo-1576566588028-4147f3842f27",
        "https://images.unsplash.com/photo-1622445275576-721325763afe"
    ],
    # Jackets and outerwear
    "jacket": [
        "https://images.unsplash.com/photo-1551028719-00167b16eac5",
        "https://images.unsplash.com/photo-1539533018447-63fcce2678e3",
        "https://images.unsplash.com/photo-1591047139829-d91aecb6caea",
        "https://images.unsplash.com/photo-1578932750355-5eb30ece2a82",
        "https://images.unsplash.com/photo-1544022613-e87ca75a784a"
    ],
    # Dresses
    "dress": [
        "https://images.unsplash.com/photo-1595777457583-95e059d581b8",
        "https://images.unsplash.com/photo-1566174053879-31528523f8ae",
        "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1",
        "https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03",
        "https://images.unsplash.com/photo-1611312449408-fcece27cdbb7"
    ],
    # Luxury brands - generic luxury clothing
    "luxury": [
        "https://images.unsplash.com/photo-1490481651871-ab68de25d43d",
        "https://images.unsplash.com/photo-1483985988355-763728e1935b",
        "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f",
        "https://images.unsplash.com/photo-1467043153537-a4fba2cd39ef",
        "https://images.unsplash.com/photo-1558769132-cb1aea9c9b27"
    ],
    # Shoes and sneakers
    "shoes": [
        "https://images.unsplash.com/photo-1549298916-b41d501d3772",
        "https://images.unsplash.com/photo-1460353581641-37baddab0fa2",
        "https://images.unsplash.com/photo-1542291026-7eec264c27ff",
        "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a",
        "https://images.unsplash.com/photo-1605348532760-6753d2c43329"
    ],
    # Watches
    "watch": [
        "https://images.unsplash.com/photo-1523275335684-37898b6baf30",
        "https://images.unsplash.com/photo-1524805444758-089113d48a6d",
        "https://images.unsplash.com/photo-1587836374828-4dbafa94cf0e",
        "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1",
        "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd"
    ],
    # Default/Generic
    "default": [
        "https://images.unsplash.com/photo-1441986300917-64674bd600d8",
        "https://images.unsplash.com/photo-1469334031218-e382a71b716b",
        "https://images.unsplash.com/photo-1441984904996-e0b6ba687e04",
        "https://images.unsplash.com/photo-1445205170230-053b83016050",
        "https://images.unsplash.com/photo-1472851294608-062f824d29cc"
    ]
}

def get_image_category(product_name, tags):
    """Determine which image category to use based on product info"""
    name_lower = product_name.lower()
    tags_lower = [t.lower() for t in tags] if tags else []
    
    # Check for watches
    if any(brand in name_lower for brand in ["rolex", "patek", "audemars", "omega", "cartier", "tag", "hublot", "iwc"]):
        return "watch"
    
    # Check for shoes
    if any(word in name_lower for word in ["shoe", "sneaker", "jordan", "yeezy", "nike", "adidas"]):
        return "shoes"
    if any(word in tags_lower for word in ["shoes", "sneakers"]):
        return "shoes"
    
    # Check for specific clothing types
    if "dress" in name_lower or "dress" in tags_lower:
        return "dress"
    if any(word in name_lower for word in ["jacket", "coat", "parka"]):
        return "jacket"
    if "tshirt" in name_lower or "t-shirt" in name_lower or "tshirt" in tags_lower:
        return "tshirt"
    
    # Check for luxury brands
    if any(brand in name_lower for brand in ["gucci", "louis vuitton", "dior", "balenciaga", "versace", "prada"]):
        return "luxury"
    
    return "default"

async def update_product_images():
    """Update all products with real images"""
    
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    print("=" * 80)
    print("🖼️  UPDATING PRODUCT IMAGES")
    print("=" * 80)
    
    # Get all products
    products = await db.products.find({}, {"_id": 0}).to_list(None)
    print(f"\n📦 Found {len(products)} products to update")
    
    updated_count = 0
    
    for product in products:
        # Skip if already has real images (not placeholder)
        if product.get("images") and "placeholder" not in product["images"][0]:
            continue
        
        # Determine image category
        category = get_image_category(product.get("name", ""), product.get("tags", []))
        
        # Get random images from that category
        available_images = LUXURY_IMAGES.get(category, LUXURY_IMAGES["default"])
        
        # Select 2-3 random images with different parameters for variety
        num_images = random.randint(2, 3)
        selected_images = []
        
        for i in range(num_images):
            base_url = random.choice(available_images)
            # Add Unsplash parameters for different views/crops
            params = [
                "?w=800&h=800&fit=crop",
                "?w=800&h=800&fit=crop&crop=faces",
                "?w=800&h=800&fit=crop&q=80"
            ]
            image_url = base_url + params[i % len(params)]
            selected_images.append(image_url)
        
        # Update product
        await db.products.update_one(
            {"id": product["id"]},
            {"$set": {"images": selected_images}}
        )
        
        updated_count += 1
        
        if updated_count % 100 == 0:
            print(f"   ✅ Updated {updated_count} products...")
    
    print(f"\n✅ Total products updated: {updated_count}")
    
    # Summary by category
    print(f"\n📊 IMAGE DISTRIBUTION:")
    categories = {}
    for product in products:
        cat = get_image_category(product.get("name", ""), product.get("tags", []))
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat, count in sorted(categories.items()):
        print(f"   {cat}: {count} products")
    
    client.close()
    
    print("\n" + "=" * 80)
    print("✅ IMAGE UPDATE COMPLETED!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(update_product_images())
