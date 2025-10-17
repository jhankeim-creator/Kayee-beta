"""
Update products with REAL images from qiqiyg.com
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import random

load_dotenv()

# Real product images from qiqiyg.com
REAL_QIQIYG_IMAGES = [
    "https://uspic.qiqiyg.com/upfile/category/322504.jpg",
    "https://uspic.qiqiyg.com/upfile/category/322393.jpg",
    "https://uspic.qiqiyg.com/upfile/category/322388.jpg",
    "https://uspic.qiqiyg.com/upfile/category/322391.jpg",
    "https://uspic.qiqiyg.com/upfile/category/322390.jpg",
    "https://uspic.qiqiyg.com/upfile/category/322387.jpg",
    "https://uspic.qiqiyg.com/upfile/category/322069.jpg",
    "https://uspic.qiqiyg.com/upfile/category/322068.jpg",
    "https://uspic.qiqiyg.com/upfile/category/321874.jpg",
    "https://uspic.qiqiyg.com/upfile/category/321857.jpg",
    "https://uspic.qiqiyg.com/upfile/category/321650.jpg",
    "https://uspic.qiqiyg.com/upfile/category/321648.jpg",
    "https://uspic.qiqiyg.com/upfile/category/321649.jpg",
    "https://uspic.qiqiyg.com/upfile/category/321187.jpg",
    "https://uspic.qiqiyg.com/upfile/category/321186.jpg",
    "https://uspic.qiqiyg.com/upfile/category/321182.jpg",
    "https://uspic.qiqiyg.com/upfile/category/320846.jpg",
    "https://uspic.qiqiyg.com/upfile/category/320782.jpg",
    "https://uspic.qiqiyg.com/upfile/category/320769.jpg",
    "https://uspic.qiqiyg.com/upfile/category/320679.jpg",
    "https://uspic.qiqiyg.com/upfile/category/320521.jpg",
    "https://uspic.qiqiyg.com/upfile/category/320520.jpg",
    "https://uspic.qiqiyg.com/upfile/category/320519.jpg",
    "https://uspic.qiqiyg.com/upfile/category/Arcteryx%20XS-L%20attr54%20(5)_4134360.jpg",
    "https://uspic.qiqiyg.com/upfile/category/320167.jpg",
    "https://uspic.qiqiyg.com/upfile/category/320162.jpg",
    "https://uspic.qiqiyg.com/upfile/category/320129.jpg",
    "https://uspic.qiqiyg.com/upfile/category/320122.jpg",
    "https://uspic.qiqiyg.com/upfile/category/319827.jpg",
    "https://uspic.qiqiyg.com/upfile/category/319811.jpg",
    "https://uspic.qiqiyg.com/upfile/category/Balmain%20S-XL%20%20(2)_4119437.jpg",
    "https://uspic.qiqiyg.com/upfile/category/MiuMiu%20S-XL%20%20(1)_4115526.JPG",
    "https://uspic.qiqiyg.com/upfile/category/Chanel%20S-XL_4111469.jpg",
    "https://uspic.qiqiyg.com/upfile/category/318710.jpg",
    "https://uspic.qiqiyg.com/upfile/category/318632.jpg",
    "https://uspic.qiqiyg.com/upfile/category/318592.jpg",
    "https://uspic.qiqiyg.com/upfile/category/318588.jpg",
    "https://uspic.qiqiyg.com/upfile/category/Supreme%20S-2XL%20thtxS192%20(10)_4108305.jpg",
    "https://uspic.qiqiyg.com/upfile/category/318566.jpg",
    "https://uspic.qiqiyg.com/upfile/category/318554.jpg",
    "https://uspic.qiqiyg.com/upfile/category/318219.jpg",
    "https://uspic.qiqiyg.com/upfile/category/318218.jpg",
    "https://uspic.qiqiyg.com/upfile/category/318217.jpg",
    "https://uspic.qiqiyg.com/upfile/category/318206.jpg",
    "https://uspic.qiqiyg.com/upfile/category/317796.jpg",
    "https://uspic.qiqiyg.com/upfile/category/317795.jpg",
    "https://uspic.qiqiyg.com/upfile/category/317751.jpg",
    "https://uspic.qiqiyg.com/upfile/category/317740.jpg",
    "https://uspic.qiqiyg.com/upfile/category/317301.jpg",
    "https://uspic.qiqiyg.com/upfile/category/317272.jpg",
    "https://uspic.qiqiyg.com/upfile/category/317263.jpg",
    "https://uspic.qiqiyg.com/upfile/category/317226.jpg",
    "https://uspic.qiqiyg.com/upfile/category/317010.jpg",
    "https://uspic.qiqiyg.com/upfile/category/Burberry%20M-4XL%2011Lr53%20(3)_4077618.jpg",
    "https://uspic.qiqiyg.com/upfile/category/316962.jpg",
    "https://uspic.qiqiyg.com/upfile/category/316946.jpg",
    "https://uspic.qiqiyg.com/upfile/category/Godspeed%20S-XL%20brtx5526%20(3)_4076271.jpg",
    "https://uspic.qiqiyg.com/upfile/category/316528.jpg",
    "https://uspic.qiqiyg.com/upfile/category/316523.jpg",
    "https://uspic.qiqiyg.com/upfile/category/316406.jpg",
    "https://uspic.qiqiyg.com/upfile/category/316400.jpg",
    "https://uspic.qiqiyg.com/upfile/category/316132.jpg",
    "https://uspic.qiqiyg.com/upfile/category/315941.jpg",
    "https://uspic.qiqiyg.com/upfile/category/315908.jpg",
    "https://uspic.qiqiyg.com/upfile/category/315786.jpg",
    "https://uspic.qiqiyg.com/upfile/category/315785.jpg",
    "https://uspic.qiqiyg.com/upfile/category/315779.jpg",
    "https://uspic.qiqiyg.com/upfile/category/315710.jpg",
    "https://uspic.qiqiyg.com/upfile/category/315697.jpg",
    "https://uspic.qiqiyg.com/upfile/category/315178.jpg",
    "https://uspic.qiqiyg.com/upfile/category/315130.JPG",
    "https://uspic.qiqiyg.com/upfile/category/314887.jpg",
    "https://uspic.qiqiyg.com/upfile/category/314877.jpg",
    "https://uspic.qiqiyg.com/upfile/category/314866.jpg",
    "https://uspic.qiqiyg.com/upfile/category/314851.jpg",
    "https://uspic.qiqiyg.com/upfile/category/314849.jpg",
    "https://uspic.qiqiyg.com/upfile/category/314522.jpg",
    "https://uspic.qiqiyg.com/upfile/category/314401.jpg",
    "https://uspic.qiqiyg.com/upfile/category/314370.jpg",
    "https://uspic.qiqiyg.com/upfile/category/314288.jpg",
    "https://uspic.qiqiyg.com/upfile/category/314123.jpg",
    "https://uspic.qiqiyg.com/upfile/category/314121.jpg",
    "https://uspic.qiqiyg.com/upfile/category/Gucci%20sz66%2073%2080%2090%20100%20110%20(1)_4026441.jpg",
    "https://uspic.qiqiyg.com/upfile/category/313797.jpg",
    "https://uspic.qiqiyg.com/upfile/category/313796.jpg",
    "https://uspic.qiqiyg.com/upfile/category/313495.JPG",
    "https://uspic.qiqiyg.com/upfile/category/313499.jpg",
    "https://uspic.qiqiyg.com/upfile/category/313483.jpg",
    "https://uspic.qiqiyg.com/upfile/category/313430.jpg",
    "https://uspic.qiqiyg.com/upfile/category/313114.jpg",
    "https://uspic.qiqiyg.com/upfile/category/312938.jpg",
    "https://uspic.qiqiyg.com/upfile/category/312846.jpg",
    "https://uspic.qiqiyg.com/upfile/category/312845.jpg",
    "https://uspic.qiqiyg.com/upfile/category/312812.jpg",
    "https://uspic.qiqiyg.com/upfile/category/312808.jpg",
    "https://uspic.qiqiyg.com/upfile/category/312469.jpg",
    "https://uspic.qiqiyg.com/upfile/category/312316.jpg",
    "https://uspic.qiqiyg.com/upfile/category/312228.jpg",
    "https://uspic.qiqiyg.com/upfile/category/312221.jpg",
    "https://uspic.qiqiyg.com/upfile/category/312214.jpg",
]

# Add more categories of images
JACKET_IMAGES = [
    "https://uspic.qiqiyg.com/upfile/category/Stone%20Island%20S-2XL%20xetr26%20(1)_3993109.jpg",
    "https://uspic.qiqiyg.com/upfile/category/312086.jpg",
    "https://uspic.qiqiyg.com/upfile/category/311755.jpg",
    "https://uspic.qiqiyg.com/upfile/category/Arcteryx%20M-5XL%20kdtr08%20(1)_3908811.jpg",
    "https://uspic.qiqiyg.com/upfile/category/Balenciaga%20M-3XL%2012yr40%20(2)_3891811.jpg",
    "https://uspic.qiqiyg.com/upfile/category/Burberry%20M-3XL%2012yr118%20(5)_3891375.jpg",
]

DRESS_IMAGES = [
    "https://uspic.qiqiyg.com/upfile/category/Balmain%20S-XL%20%20(2)_4119437.jpg",
    "https://uspic.qiqiyg.com/upfile/category/MiuMiu%20S-XL%20%20(1)_4115526.JPG",
    "https://uspic.qiqiyg.com/upfile/category/Chanel%20S-XL_4111469.jpg",
    "https://uspic.qiqiyg.com/upfile/category/308178.jpg",
    "https://uspic.qiqiyg.com/upfile/category/307745.jpg",
    "https://uspic.qiqiyg.com/upfile/category/307428.jpg",
]

# Combine all images
ALL_IMAGES = REAL_QIQIYG_IMAGES + JACKET_IMAGES + DRESS_IMAGES

async def update_all_products_with_real_images():
    """Update all products with real qiqiyg images"""
    
    client = AsyncIOMotorClient(os.environ['MONGO_URL'])
    db = client[os.environ['DB_NAME']]
    
    print("=" * 80)
    print("🖼️  UPDATING ALL PRODUCTS WITH REAL QIQIYG.COM IMAGES")
    print("=" * 80)
    
    # Get all products
    products = await db.products.find({}, {"_id": 0, "id": 1, "name": 1}).to_list(None)
    print(f"\n📦 Found {len(products)} products")
    print(f"📸 Available {len(ALL_IMAGES)} real images from qiqiyg.com")
    
    updated_count = 0
    
    for product in products:
        # Select 2-3 random real images for each product
        num_images = random.randint(2, 3)
        selected_images = random.sample(ALL_IMAGES, min(num_images, len(ALL_IMAGES)))
        
        # Update product
        await db.products.update_one(
            {"id": product["id"]},
            {"$set": {"images": selected_images}}
        )
        
        updated_count += 1
        
        if updated_count % 200 == 0:
            print(f"   ✅ Updated {updated_count} products...")
    
    print(f"\n✅ Total products updated: {updated_count}")
    print(f"📸 All products now have real images from qiqiyg.com!")
    
    client.close()
    
    print("\n" + "=" * 80)
    print("✅ REAL IMAGES UPDATE COMPLETED!")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(update_all_products_with_real_images())
