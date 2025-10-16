from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import logging

from oauth_service import oauth_service

logger = logging.getLogger(__name__)

# Create router
oauth_router = APIRouter(prefix="/auth/oauth", tags=["oauth"])

# ===== MODELS =====

class GoogleAuthRequest(BaseModel):
    token: str  # Google ID token

class FacebookAuthRequest(BaseModel):
    access_token: str

class TwitterAuthRequest(BaseModel):
    oauth_token: str
    oauth_token_secret: str

# ===== GOOGLE OAUTH =====

@oauth_router.post("/google")
async def google_auth(request: GoogleAuthRequest):
    """
    Authentifier un utilisateur via Google OAuth
    
    Le frontend doit:
    1. Utiliser Google Sign-In pour obtenir le ID token
    2. Envoyer le token à cette route
    3. Recevoir un JWT pour l'authentification
    """
    user_info = await oauth_service.verify_google_token(request.token)
    
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    
    # Ici, créer ou récupérer l'utilisateur dans la base de données
    # et retourner un JWT token
    
    return {
        "success": True,
        "provider": "google",
        "user": {
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture"),
            "provider_id": user_info.get("sub")
        },
        "message": "User authenticated successfully"
    }

@oauth_router.get("/google/url")
async def get_google_auth_url(redirect_uri: str):
    """Obtenir l'URL d'authentification Google"""
    auth_url = oauth_service.get_google_auth_url(redirect_uri)
    return {"auth_url": auth_url}

# ===== FACEBOOK OAUTH =====

@oauth_router.post("/facebook")
async def facebook_auth(request: FacebookAuthRequest):
    """
    Authentifier un utilisateur via Facebook
    
    Le frontend doit:
    1. Utiliser Facebook Login pour obtenir un access token
    2. Envoyer le token à cette route
    3. Recevoir un JWT pour l'authentification
    """
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
        },
        "message": "User authenticated successfully"
    }

@oauth_router.get("/facebook/url")
async def get_facebook_auth_url(redirect_uri: str):
    """Obtenir l'URL d'authentification Facebook"""
    auth_url = oauth_service.get_facebook_auth_url(redirect_uri)
    return {"auth_url": auth_url}

# ===== TWITTER/X OAUTH =====

@oauth_router.post("/twitter")
async def twitter_auth(request: TwitterAuthRequest):
    """
    Authentifier un utilisateur via Twitter/X
    
    Note: Twitter OAuth 1.0a nécessite une implémentation plus complexe
    """
    user_info = await oauth_service.verify_twitter_token(
        request.oauth_token,
        request.oauth_token_secret
    )
    
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid Twitter token")
    
    return {
        "success": True,
        "provider": "twitter",
        "user": {
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "username": user_info.get("username"),
            "picture": user_info.get("profile_image"),
            "provider_id": user_info.get("id")
        },
        "message": "User authenticated successfully"
    }
