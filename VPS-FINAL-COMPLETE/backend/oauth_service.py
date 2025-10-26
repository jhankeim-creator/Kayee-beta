import os
import requests
import logging
from typing import Dict, Optional
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

logger = logging.getLogger(__name__)

class OAuthService:
    """
    Service d'authentification OAuth pour Google, Facebook, Twitter/X
    """
    
    def __init__(self):
        # Google OAuth
        self.google_client_id = os.environ.get('GOOGLE_CLIENT_ID', 'your_google_client_id')
        self.google_client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', 'your_google_client_secret')
        
        # Facebook OAuth
        self.facebook_app_id = os.environ.get('FACEBOOK_APP_ID', 'your_facebook_app_id')
        self.facebook_app_secret = os.environ.get('FACEBOOK_APP_SECRET', 'your_facebook_app_secret')
        
        # Twitter/X OAuth
        self.twitter_api_key = os.environ.get('TWITTER_API_KEY', 'your_twitter_api_key')
        self.twitter_api_secret = os.environ.get('TWITTER_API_SECRET', 'your_twitter_api_secret')
        
        self.is_demo = self.google_client_id == 'your_google_client_id'
    
    async def verify_google_token(self, token: str) -> Optional[Dict]:
        """
        Vérifier et décoder un token Google OAuth
        
        Documentation: https://developers.google.com/identity/sign-in/web/backend-auth
        """
        
        if self.is_demo:
            logger.info("🔐 Google OAuth Demo Mode")
            return {
                "email": "demo@gmail.com",
                "name": "Demo User",
                "picture": "https://via.placeholder.com/150",
                "sub": "demo_google_id_123",
                "email_verified": True
            }
        
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                self.google_client_id
            )
            
            # Vérifier que le token est pour notre application
            if idinfo['aud'] != self.google_client_id:
                raise ValueError('Invalid audience')
            
            return {
                "email": idinfo.get("email"),
                "name": idinfo.get("name"),
                "picture": idinfo.get("picture"),
                "sub": idinfo.get("sub"),
                "email_verified": idinfo.get("email_verified", False)
            }
        except Exception as e:
            logger.error(f"Google token verification failed: {str(e)}")
            return None
    
    async def verify_facebook_token(self, access_token: str) -> Optional[Dict]:
        """
        Vérifier un token Facebook et récupérer les infos utilisateur
        
        Documentation: https://developers.facebook.com/docs/facebook-login/guides/access-tokens/
        """
        
        if self.is_demo:
            logger.info("🔐 Facebook OAuth Demo Mode")
            return {
                "email": "demo@facebook.com",
                "name": "Demo User",
                "picture": "https://via.placeholder.com/150",
                "id": "demo_facebook_id_123"
            }
        
        try:
            # Vérifier le token
            verify_url = f"https://graph.facebook.com/debug_token"
            params = {
                "input_token": access_token,
                "access_token": f"{self.facebook_app_id}|{self.facebook_app_secret}"
            }
            
            verify_response = requests.get(verify_url, params=params, timeout=30)
            
            if verify_response.status_code != 200:
                return None
            
            verify_data = verify_response.json()
            
            if not verify_data.get("data", {}).get("is_valid"):
                return None
            
            # Récupérer les infos utilisateur
            user_url = "https://graph.facebook.com/me"
            user_params = {
                "fields": "id,name,email,picture",
                "access_token": access_token
            }
            
            user_response = requests.get(user_url, params=user_params, timeout=30)
            
            if user_response.status_code == 200:
                user_data = user_response.json()
                return {
                    "email": user_data.get("email"),
                    "name": user_data.get("name"),
                    "picture": user_data.get("picture", {}).get("data", {}).get("url"),
                    "id": user_data.get("id")
                }
            
            return None
        except Exception as e:
            logger.error(f"Facebook token verification failed: {str(e)}")
            return None
    
    async def verify_twitter_token(self, access_token: str, access_token_secret: str) -> Optional[Dict]:
        """
        Vérifier un token Twitter/X et récupérer les infos utilisateur
        
        Documentation: https://developer.twitter.com/en/docs/authentication/oauth-1-0a
        """
        
        if self.is_demo:
            logger.info("🔐 Twitter/X OAuth Demo Mode")
            return {
                "email": "demo@twitter.com",
                "name": "Demo User",
                "username": "demo_user",
                "profile_image": "https://via.placeholder.com/150",
                "id": "demo_twitter_id_123"
            }
        
        try:
            # Note: Twitter OAuth 1.0a nécessite une implémentation plus complexe
            # avec des signatures HMAC-SHA1
            # Pour simplifier, on utiliserait une bibliothèque comme tweepy
            
            # Pour l'instant, retourner None en mode production
            # L'implémentation complète nécessiterait tweepy ou requests-oauthlib
            
            logger.warning("Twitter OAuth not fully implemented - use demo mode or implement with tweepy")
            return None
            
        except Exception as e:
            logger.error(f"Twitter token verification failed: {str(e)}")
            return None
    
    def get_google_auth_url(self, redirect_uri: str) -> str:
        """
        Générer l'URL d'authentification Google
        """
        if self.is_demo:
            return "https://accounts.google.com/o/oauth2/v2/auth?demo=true"
        
        from urllib.parse import urlencode
        
        params = {
            "client_id": self.google_client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent"
        }
        
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    
    def get_facebook_auth_url(self, redirect_uri: str) -> str:
        """
        Générer l'URL d'authentification Facebook
        """
        if self.is_demo:
            return "https://www.facebook.com/v12.0/dialog/oauth?demo=true"
        
        from urllib.parse import urlencode
        
        params = {
            "client_id": self.facebook_app_id,
            "redirect_uri": redirect_uri,
            "scope": "email,public_profile",
            "response_type": "code"
        }
        
        return f"https://www.facebook.com/v12.0/dialog/oauth?{urlencode(params)}"

oauth_service = OAuthService()
