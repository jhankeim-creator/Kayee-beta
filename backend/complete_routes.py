"""
Complete API routes for full e-commerce functionality
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import os
from datetime import datetime, timezone
import uuid
import shutil
from pathlib import Path

# Create router
complete_router = APIRouter(prefix="/api/v2", tags=["complete"])

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Upload directory
UPLOAD_DIR = Path("/app/backend/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ==================== MODELS ====================

class ReviewCreate(BaseModel):
    product_id: str
    user_name: str
    user_email: str
    rating: int
    comment: str
    images: List[str] = []

# ==================== MEDIA UPLOAD ====================

@complete_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload image or video"""
    # Validate file type
    allowed = ["image/jpeg", "image/png", "image/gif", "image/webp", "video/mp4"]
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Generate unique filename
    file_ext = Path(file.filename).suffix
    unique_name = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_name
    
    # Save file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Save to database
    media = {
        "id": str(uuid.uuid4()),
        "filename": unique_name,
        "original_name": file.filename,
        "url": f"/uploads/{unique_name}",
        "type": "image" if file.content_type.startswith("image") else "video",
        "size": file_path.stat().st_size,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.media.insert_one(media)
    
    return {"url": media["url"], "id": media["id"], "type": media["type"]}

@complete_router.get("/media")
async def get_media():
    """Get all uploaded media"""
    media = await db.media.find({}, {"_id": 0}).sort("created_at", -1).limit(100).to_list(100)
    return media

# ==================== CATEGORIES ====================

@complete_router.post("/categories")
async def create_category(name: str, description: str, parent_id: Optional[str] = None, image: Optional[str] = None):
    """Create category or subcategory"""
    category_data = {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": description,
        "parent_id": parent_id,
        "image": image,
        "slug": name.lower().replace(" ", "-"),
        "product_count": 0,
        "active": True,
        "display_order": 0,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.categories.insert_one(category_data)
    return category_data

@complete_router.get("/categories")
async def get_categories(parent_id: Optional[str] = None):
    """Get categories"""
    query = {}
    if parent_id is not None:
        query["parent_id"] = parent_id
    
    categories = await db.categories.find(query, {"_id": 0}).sort("display_order", 1).to_list(None)
    return categories

@complete_router.get("/categories/tree")
async def get_categories_tree():
    """Get category tree"""
    parents = await db.categories.find({"parent_id": None}, {"_id": 0}).to_list(None)
    
    result = []
    for parent in parents:
        subcategories = await db.categories.find({"parent_id": parent["id"]}, {"_id": 0}).to_list(None)
        parent["subcategories"] = subcategories
        result.append(parent)
    
    return result

@complete_router.delete("/categories/{category_id}")
async def delete_category(category_id: str):
    """Delete category"""
    result = await db.categories.delete_one({"id": category_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Deleted"}

# ==================== REVIEWS ====================

@complete_router.post("/reviews")
async def create_review(review: ReviewCreate):
    """Create review"""
    review_data = {
        "id": str(uuid.uuid4()),
        "product_id": review.product_id,
        "user_name": review.user_name,
        "user_email": review.user_email,
        "rating": review.rating,
        "comment": review.comment,
        "images": review.images,
        "status": "pending",
        "helpful_count": 0,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.reviews.insert_one(review_data)
    
    # Update product rating
    await update_product_rating(review.product_id)
    
    return review_data

@complete_router.get("/reviews/product/{product_id}")
async def get_product_reviews(product_id: str):
    """Get approved reviews for product"""
    reviews = await db.reviews.find(
        {"product_id": product_id, "status": "approved"},
        {"_id": 0}
    ).to_list(None)
    return reviews

@complete_router.get("/reviews/pending")
async def get_pending_reviews():
    """Get pending reviews"""
    reviews = await db.reviews.find({"status": "pending"}, {"_id": 0}).to_list(None)
    return reviews

@complete_router.put("/reviews/{review_id}/status")
async def update_review_status(review_id: str, status: str):
    """Update review status"""
    result = await db.reviews.update_one(
        {"id": review_id},
        {"$set": {"status": status}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review = await db.reviews.find_one({"id": review_id}, {"_id": 0})
    await update_product_rating(review["product_id"])
    
    return {"message": "Updated"}

async def update_product_rating(product_id: str):
    """Update product rating"""
    reviews = await db.reviews.find(
        {"product_id": product_id, "status": "approved"},
        {"_id": 0, "rating": 1}
    ).to_list(None)
    
    if reviews:
        avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
        reviews_count = len(reviews)
    else:
        avg_rating = 0.0
        reviews_count = 0
    
    await db.products.update_one(
        {"id": product_id},
        {"$set": {"rating": round(avg_rating, 1), "reviews_count": reviews_count}}
    )
