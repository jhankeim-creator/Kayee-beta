"""
Create sample data for new Ecwid features (coupons, customers)
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timezone, timedelta
import random

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def create_sample_data():
    """Create sample coupons and customers"""
    
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Creating sample data...")
    
    # Create sample coupons
    coupons = [
        {
            "id": "coupon-1",
            "code": "WELCOME10",
            "discount_type": "percentage",
            "discount_value": 10.0,
            "minimum_purchase": 50.0,
            "max_uses": None,
            "uses_count": 5,
            "active": True,
            "valid_from": datetime.now(timezone.utc).isoformat(),
            "valid_until": (datetime.now(timezone.utc) + timedelta(days=90)).isoformat(),
            "applicable_categories": [],
            "applicable_products": [],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "coupon-2",
            "code": "SUMMER20",
            "discount_type": "percentage",
            "discount_value": 20.0,
            "minimum_purchase": 100.0,
            "max_uses": 100,
            "uses_count": 23,
            "active": True,
            "valid_from": datetime.now(timezone.utc).isoformat(),
            "valid_until": (datetime.now(timezone.utc) + timedelta(days=60)).isoformat(),
            "applicable_categories": ["fashion"],
            "applicable_products": [],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "coupon-3",
            "code": "FREESHIP",
            "discount_type": "fixed",
            "discount_value": 10.0,
            "minimum_purchase": 0.0,
            "max_uses": None,
            "uses_count": 45,
            "active": True,
            "valid_from": datetime.now(timezone.utc).isoformat(),
            "valid_until": None,
            "applicable_categories": [],
            "applicable_products": [],
            "created_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "coupon-4",
            "code": "VIP50",
            "discount_type": "fixed",
            "discount_value": 50.0,
            "minimum_purchase": 200.0,
            "max_uses": 50,
            "uses_count": 12,
            "active": True,
            "valid_from": datetime.now(timezone.utc).isoformat(),
            "valid_until": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
            "applicable_categories": ["jewelry"],
            "applicable_products": [],
            "created_at": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    # Check if coupons already exist
    existing_coupons = await db.coupons.count_documents({})
    if existing_coupons == 0:
        await db.coupons.insert_many(coupons)
        print(f"✅ Created {len(coupons)} sample coupons")
    else:
        print(f"ℹ️  {existing_coupons} coupons already exist")
    
    # Create sample customers from existing orders
    orders = await db.orders.find({}, {"_id": 0, "user_email": 1, "user_name": 1, "total": 1, "created_at": 1, "phone": 1}).to_list(None)
    
    # Group orders by email
    customer_orders = {}
    for order in orders:
        email = order.get("user_email")
        if email not in customer_orders:
            customer_orders[email] = []
        customer_orders[email].append(order)
    
    customers = []
    customer_groups = ["regular", "vip", "wholesale"]
    
    for email, user_orders in customer_orders.items():
        total_spent = sum(o.get("total", 0) for o in user_orders)
        
        # Determine customer group
        if total_spent > 1000:
            group = "vip"
        elif total_spent > 500:
            group = "wholesale"
        else:
            group = "regular"
        
        # Get most recent order date
        order_dates = [o.get("created_at") for o in user_orders if o.get("created_at")]
        last_order_date = max(order_dates) if order_dates else None
        
        customer = {
            "id": f"customer-{email.replace('@', '-').replace('.', '-')}",
            "email": email,
            "name": user_orders[0].get("user_name", "Customer"),
            "phone": user_orders[0].get("phone"),
            "total_orders": len(user_orders),
            "total_spent": total_spent,
            "customer_group": group,
            "notes": None,
            "addresses": [],
            "tags": [group],
            "created_at": user_orders[0].get("created_at", datetime.now(timezone.utc).isoformat()),
            "last_order_date": last_order_date
        }
        customers.append(customer)
    
    # Check if customers already exist
    existing_customers = await db.customers.count_documents({})
    if existing_customers == 0 and customers:
        await db.customers.insert_many(customers)
        print(f"✅ Created {len(customers)} customers from existing orders")
    else:
        print(f"ℹ️  {existing_customers} customers already exist")
    
    # Mark some products as "on_sale", "is_new", "best_seller"
    products = await db.products.find({}, {"_id": 0, "id": 1}).to_list(None)
    
    # Mark 20% as on sale
    sale_count = int(len(products) * 0.2)
    sale_products = random.sample(products, sale_count)
    for prod in sale_products:
        orig_product = await db.products.find_one({"id": prod["id"]}, {"_id": 0})
        if orig_product:
            compare_price = orig_product["price"] * random.uniform(1.2, 1.5)
            await db.products.update_one(
                {"id": prod["id"]},
                {"$set": {
                    "on_sale": True,
                    "compare_at_price": round(compare_price, 2)
                }}
            )
    print(f"✅ Marked {sale_count} products as on sale")
    
    # Mark 15% as new
    new_count = int(len(products) * 0.15)
    new_products = random.sample(products, new_count)
    for prod in new_products:
        await db.products.update_one(
            {"id": prod["id"]},
            {"$set": {"is_new": True}}
        )
    print(f"✅ Marked {new_count} products as new")
    
    # Mark 10% as best sellers
    bestseller_count = int(len(products) * 0.1)
    bestseller_products = random.sample(products, bestseller_count)
    for prod in bestseller_products:
        sales_count = random.randint(50, 200)
        await db.products.update_one(
            {"id": prod["id"]},
            {"$set": {
                "best_seller": True,
                "sales_count": sales_count
            }}
        )
    print(f"✅ Marked {bestseller_count} products as best sellers")
    
    client.close()
    print("✅ Sample data creation complete!")

if __name__ == "__main__":
    asyncio.run(create_sample_data())
