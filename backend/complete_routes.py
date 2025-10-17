"""
Complete API routes for categories, subcategories, reviews, and media uploads
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime, timezone
import uuid
import shutil
from pathlib import Path
from models_complete import (
    CategoryExtended, CategoryCreate,
    Review, ReviewCreate, ReviewUpdate,
    MediaUpload,
    ProductComplete, ProductCreateComplete
)

# Create router
complete_router = APIRouter(prefix="/api/v2", tags=["complete"])

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Media upload directory
UPLOAD_DIR = Path("/app/backend/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# ==================== CATEGORIES ====================

@complete_router.post("/categories", response_model=CategoryExtended)
async def create_category(category: CategoryCreate):
    """Create a new category or subcategory"""
    category_data = category.model_dump()
    category_data["id"] = str(uuid.uuid4())
    
    # Auto-generate slug if not provided
    if not category_data.get("slug"):
        category_data["slug"] = category_data["name"].lower().replace(" ", "-").replace("/", "-")
    
    category_data["product_count"] = 0
    category_data["active"] = True
    category_data["created_at"] = datetime.now(timezone.utc).isoformat()
    
    await db.categories.insert_one(category_data)
    return CategoryExtended(**category_data)

@complete_router.get("/categories", response_model=List[CategoryExtended])
async def get_categories(parent_id: Optional[str] = None, active_only: bool = True):
    """Get all categories, optionally filtered by parent_id"""
    query = {}
    if parent_id is not None:
        query["parent_id"] = parent_id
    if active_only:
        query["active"] = True
    
    categories = await db.categories.find(query, {"_id": 0}).sort("display_order", 1).to_list(None)
    return [CategoryExtended(**cat) for cat in categories]

@complete_router.get("/categories/tree")
async def get_categories_tree():
    """Get categories in tree structure (parents with their subcategories)"""
    # Get all parent categories
    parents = await db.categories.find(
        {"parent_id": None, "active": True},
        {"_id": 0}
    ).sort("display_order", 1).to_list(None)
    
    result = []
    for parent in parents:
        # Get subcategories for this parent
        subcategories = await db.categories.find(
            {"parent_id": parent["id"], "active": True},
            {"_id": 0}
        ).sort("display_order", 1).to_list(None)
        
        parent["subcategories"] = subcategories
        result.append(parent)
    
    return result

@complete_router.put("/categories/{category_id}", response_model=CategoryExtended)
async def update_category(category_id: str, updates: dict):
    """Update a category"""
    if not updates:
        raise HTTPException(status_code=400, detail="No updates provided")
    
    result = await db.categories.update_one(
        {"id": category_id},
        {"$set": updates}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category = await db.categories.find_one({"id": category_id}, {"_id": 0})
    return CategoryExtended(**category)

@complete_router.delete("/categories/{category_id}")
async def delete_category(category_id: str):
    """Delete a category"""
    # Check if category has products
    product_count = await db.products.count_documents({"category_id": category_id})
    if product_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete category with {product_count} products"
        )
    
    # Check if category has subcategories
    subcat_count = await db.categories.count_documents({"parent_id": category_id})
    if subcat_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete category with {subcat_count} subcategories"
        )
    
    result = await db.categories.delete_one({"id": category_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return {"message": "Category deleted successfully"}

# ==================== MEDIA UPLOADS ====================

@complete_router.post("/media/upload")
async def upload_media(file: UploadFile = File(...)):
    """Upload image or video"""
    
    # Validate file type
    allowed_types = {
        "image/jpeg", "image/png", "image/gif", "image/webp",
        "video/mp4", "video/quicktime", "video/x-msvideo"
    }
    
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Generate unique filename
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Determine file type
    file_type = "image" if file.content_type.startswith("image") else "video"
    
    # Create media record
    media_data = {
        "id": str(uuid.uuid4()),
        "filename": unique_filename,
        "original_filename": file.filename,
        "file_path": str(file_path),
        "file_url": f"/uploads/{unique_filename}",
        "file_type": file_type,
        "mime_type": file.content_type,
        "file_size": file_path.stat().st_size,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    await db.media.insert_one(media_data)
    
    return {
        "id": media_data["id"],
        "url": media_data["file_url"],
        "type": file_type
    }

@complete_router.get("/media")
async def get_media(file_type: Optional[str] = None, limit: int = 100):
    """Get uploaded media files"""
    query = {}
    if file_type:
        query["file_type"] = file_type
    
    media = await db.media.find(query, {"_id": 0}).sort("created_at", -1).limit(limit).to_list(limit)
    return media

# ==================== REVIEWS ====================

@complete_router.post("/reviews", response_model=Review)
async def create_review(review: ReviewCreate):
    """Create a product review"""
    review_data = review.model_dump()
    review_data["id"] = str(uuid.uuid4())
    review_data["verified_purchase"] = False
    review_data["helpful_count"] = 0
    review_data["status"] = "pending"
    review_data["created_at"] = datetime.now(timezone.utc).isoformat()
    review_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    await db.reviews.insert_one(review_data)
    
    # Update product rating
    await update_product_rating(review_data["product_id"])
    
    return Review(**review_data)

@complete_router.get("/reviews/product/{product_id}", response_model=List[Review])
async def get_product_reviews(product_id: str, status: str = "approved"):
    """Get all reviews for a product"""
    query = {"product_id": product_id}
    if status:
        query["status"] = status
    
    reviews = await db.reviews.find(query, {"_id": 0}).sort("created_at", -1).to_list(None)
    return [Review(**r) for r in reviews]

@complete_router.get("/reviews/pending", response_model=List[Review])
async def get_pending_reviews():
    """Get all pending reviews for admin moderation"""
    reviews = await db.reviews.find(
        {"status": "pending"},
        {"_id": 0}
    ).sort("created_at", -1).to_list(None)
    return [Review(**r) for r in reviews]

@complete_router.put("/reviews/{review_id}")
async def update_review(review_id: str, updates: ReviewUpdate):
    """Update review (for admin moderation)"""
    update_data = {k: v for k, v in updates.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    result = await db.reviews.update_one(
        {"id": review_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # If status changed, update product rating
    if "status" in update_data:
        review = await db.reviews.find_one({"id": review_id}, {"_id": 0})
        if review:
            await update_product_rating(review["product_id"])
    
    return {"message": "Review updated successfully"}

@complete_router.delete("/reviews/{review_id}")
async def delete_review(review_id: str):
    """Delete a review"""
    review = await db.reviews.find_one({"id": review_id}, {"_id": 0})
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    result = await db.reviews.delete_one({"id": review_id})
    
    # Update product rating
    await update_product_rating(review["product_id"])
    
    return {"message": "Review deleted successfully"}

async def update_product_rating(product_id: str):
    """Recalculate and update product rating"""
    # Get all approved reviews for this product
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
        {"$set": {
            "rating": round(avg_rating, 1),
            "reviews_count": reviews_count
        }}
    )

# ==================== ENHANCED PRODUCTS ====================

@complete_router.post("/products", response_model=ProductComplete)
async def create_product_complete(product: ProductCreateComplete):
    """Create a product with all features"""
    product_data = product.model_dump()
    product_data["id"] = str(uuid.uuid4())
    
    # Auto-generate slug if not provided
    if not product_data.get("slug"):
        product_data["slug"] = product_data["name"].lower().replace(" ", "-")[:100]
    
    # Initialize stats
    product_data["rating"] = 0.0
    product_data["reviews_count"] = 0
    product_data["view_count"] = 0
    product_data["sales_count"] = 0
    product_data["active"] = True
    
    # Timestamps
    product_data["created_at"] = datetime.now(timezone.utc).isoformat()
    product_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    await db.products.insert_one(product_data)
    
    # Update category product count
    await db.categories.update_one(
        {"id": product_data["category_id"]},
        {"$inc": {"product_count": 1}}
    )
    
    return ProductComplete(**product_data)

@complete_router.get("/products/{product_id}/full", response_model=ProductComplete)
async def get_product_complete(product_id: str):
    """Get complete product with all details"""
    product = await db.products.find_one({"id": product_id}, {"_id": 0})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Increment view count
    await db.products.update_one(
        {"id": product_id},
        {"$inc": {"view_count": 1}}
    )
    
    return ProductComplete(**product)
