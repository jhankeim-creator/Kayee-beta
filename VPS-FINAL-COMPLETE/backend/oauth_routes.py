from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

from oauth_service import oauth_service

logger = logging.getLogger(__name__)

oauth_router = APIRouter(prefix="/auth/oauth", tags=["oauth"])

class GoogleAuthRequest(BaseModel):
    token: str

class FacebookAuthRequest(BaseModel):
    access_token: str

@oauth_router.post("/google")
async def google_auth(request: GoogleAuthRequest):
    user_info = await oauth_service.verify_google_token(request.token)
    
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    
    return {
        "success": True,
        "provider": "google",
        "user": {
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture"),
            "provider_id": user_info.get("sub")
        }
    }

@oauth_router.get("/google/url")
async def get_google_auth_url(redirect_uri: str):
    auth_url = oauth_service.get_google_auth_url(redirect_uri)
    return {"auth_url": auth_url}

@oauth_router.post("/facebook")
async def facebook_auth(request: FacebookAuthRequest):
    user_info = await oauth_service.verify_facebook_token(request.access_token)
    
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid Facebook token")
    
    return {
        "success": True,
        "provider": "facebook",
        "user": {
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture"),
            "provider_id": user_info.get("id")
        }
    }

@oauth_router.get("/facebook/url")
async def get_facebook_auth_url(redirect_uri: str):
    auth_url = oauth_service.get_facebook_auth_url(redirect_uri)
    return {"auth_url": auth_url}
