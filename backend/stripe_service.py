import os
import requests
import logging
from typing import Dict
from dotenv import load_dotenv
from pathlib import Path

logger = logging.getLogger(__name__)

class StripeService:
    """
    Service pour intégrer Stripe Payment Links
    Documentation: https://docs.stripe.com/payment-links/api
    """
    
    def __init__(self):
        # Load environment variables
        ROOT_DIR = Path(__file__).parent
        load_dotenv(ROOT_DIR / '.env')
        
        self.api_key = os.environ.get('STRIPE_SECRET_KEY', 'your_stripe_secret_key')
        self.publishable_key = os.environ.get('STRIPE_PUBLISHABLE_KEY', 'your_stripe_publishable_key')
        self.base_url = "https://api.stripe.com/v1"
        self.is_demo = self.api_key == 'your_stripe_secret_key'
        
        logger.info(f"Stripe Service initialized - Demo mode: {self.is_demo}")
        if not self.is_demo:
            logger.info(f"Using Stripe API key: {self.api_key[:20]}...")
        else:
            logger.info("Using demo Stripe configuration")
    
    async def create_payment_link(
        self,
        order_id: str,
        amount: float,
        currency: str = "usd",
        description: str = "",
        customer_email: str = ""
    ) -> Dict:
        """
        Créer un lien de paiement Stripe
        
        Documentation: https://docs.stripe.com/api/payment_links/payment_links/create
        """
        
        if self.is_demo:
            logger.info(f"💳 Stripe Demo Mode - Payment Link:")
            logger.info(f"Order: {order_id}, Amount: ${amount}")
            
            return {
                "success": True,
                "demo_mode": True,
                "payment_id": f"demo_stripe_{order_id}",
                "payment_url": f"https://checkout.stripe.com/demo/{order_id}",
                "amount": amount,
                "currency": currency,
                "status": "pending"
            }
        
        try:
            # Créer un produit
            product_data = {
                "name": description or f"Order {order_id}",
                "description": f"Payment for order {order_id}"
            }
            
            product_response = requests.post(
                f"{self.base_url}/products",
                auth=(self.api_key, ""),
                data=product_data,
                timeout=30
            )
            
            if product_response.status_code != 200:
                return {"success": False, "error": "Failed to create product"}
            
            product_id = product_response.json().get("id")
            
            # Créer un prix
            price_data = {
                "product": product_id,
                "unit_amount": int(amount * 100),  # Montant en centimes
                "currency": currency
            }
            
            price_response = requests.post(
                f"{self.base_url}/prices",
                auth=(self.api_key, ""),
                data=price_data,
                timeout=30
            )
            
            if price_response.status_code != 200:
                return {"success": False, "error": "Failed to create price"}
            
            price_id = price_response.json().get("id")
            
            # Créer le lien de paiement
            payment_link_data = {
                "line_items[0][price]": price_id,
                "line_items[0][quantity]": 1,
                "metadata[order_id]": order_id,
                "customer_creation": "always"
            }
            
            # Note: customer_email is not supported in payment links API
            # Customer email will be collected during checkout
            
            link_response = requests.post(
                f"{self.base_url}/payment_links",
                auth=(self.api_key, ""),
                data=payment_link_data,
                timeout=30
            )
            
            if link_response.status_code == 200:
                data = link_response.json()
                logger.info(f"✓ Stripe payment link created: {data.get('id')}")
                
                return {
                    "success": True,
                    "payment_id": data.get("id"),
                    "payment_url": data.get("url"),
                    "amount": amount,
                    "currency": currency,
                    "status": "pending"
                }
            else:
                return {"success": False, "error": link_response.text}
                
        except Exception as e:
            logger.error(f"Stripe payment link creation failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def verify_payment(self, session_id: str) -> Dict:
        """Vérifier le statut d'un paiement Stripe"""
        
        if self.is_demo:
            return {
                "success": True,
                "demo_mode": True,
                "status": "completed",
                "amount": 100.00
            }
        
        try:
            response = requests.get(
                f"{self.base_url}/checkout/sessions/{session_id}",
                auth=(self.api_key, ""),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "status": data.get("payment_status"),
                    "amount": data.get("amount_total", 0) / 100
                }
            
            return {"success": False, "error": "Session not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}

stripe_service = StripeService()
