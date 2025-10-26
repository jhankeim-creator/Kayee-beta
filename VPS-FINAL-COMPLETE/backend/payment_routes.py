from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
import logging

# Import services
from stripe_service import stripe_service
from paypal_service import paypal_service
from coinpal_service import coinpal_service
from plisio_service import plisio_service
from binance_service import binance_service

logger = logging.getLogger(__name__)

# Create router
payment_router = APIRouter(prefix="/payments", tags=["payments"])

# ===== MODELS =====

class PaymentRequest(BaseModel):
    order_id: str
    amount: float
    currency: str = "USD"
    description: Optional[str] = None
    customer_email: Optional[str] = None

# ===== STRIPE ROUTES =====

@payment_router.post("/stripe/create")
async def create_stripe_payment(request: PaymentRequest):
    """Créer un lien de paiement Stripe"""
    result = await stripe_service.create_payment_link(
        order_id=request.order_id,
        amount=request.amount,
        currency=request.currency.lower(),
        description=request.description or f"Order {request.order_id}",
        customer_email=request.customer_email
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Payment creation failed"))
    
    return result

@payment_router.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    """Webhook Stripe pour confirmation de paiement"""
    try:
        payload = await request.body()
        sig_header = request.headers.get('stripe-signature')
        
        # Ici, vous devez vérifier la signature avec votre webhook secret
        # Pour l'instant, on log simplement
        logger.info(f"Stripe webhook received: {payload[:100]}")
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Stripe webhook error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# ===== PAYPAL ROUTES =====

@payment_router.post("/paypal/create")
async def create_paypal_payment(request: PaymentRequest):
    """Créer une commande PayPal"""
    result = await paypal_service.create_order(
        order_id=request.order_id,
        amount=request.amount,
        currency=request.currency,
        description=request.description or f"Order {request.order_id}"
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Payment creation failed"))
    
    return result

@payment_router.post("/paypal/capture/{order_id}")
async def capture_paypal_payment(order_id: str):
    """Capturer un paiement PayPal approuvé"""
    result = await paypal_service.capture_order(order_id)
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Capture failed"))
    
    return result

# ===== COINPAL ROUTES =====

@payment_router.post("/coinpal/create")
async def create_coinpal_payment(request: PaymentRequest):
    """Créer un paiement CoinPal"""
    result = await coinpal_service.create_payment(
        order_id=request.order_id,
        amount=request.amount,
        currency=request.currency,
        description=request.description or f"Order {request.order_id}",
        customer_email=request.customer_email or ""
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Payment creation failed"))
    
    return result

@payment_router.get("/coinpal/status/{payment_id}")
async def check_coinpal_status(payment_id: str):
    """Vérifier le statut d'un paiement CoinPal"""
    return await coinpal_service.check_payment_status(payment_id)

@payment_router.post("/coinpal/webhook")
async def coinpal_webhook(request: Request):
    """Webhook CoinPal"""
    try:
        body = await request.body()
        signature = request.headers.get("X-Signature", "")
        
        # Vérifier la signature
        if not coinpal_service.verify_webhook_signature(body.decode(), signature):
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        data = await request.json()
        logger.info(f"CoinPal webhook: {data}")
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"CoinPal webhook error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# ===== PLISIO ROUTES =====

@payment_router.post("/plisio/create")
async def create_plisio_payment(request: PaymentRequest):
    """Créer une facture Plisio"""
    result = await plisio_service.create_invoice(
        order_number=request.order_id,
        amount=request.amount,
        source_currency=request.currency,
        description=request.description or f"Order {request.order_id}",
        email=request.customer_email or ""
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Invoice creation failed"))
    
    return result

@payment_router.get("/plisio/status/{invoice_id}")
async def check_plisio_status(invoice_id: str):
    """Vérifier le statut d'une facture Plisio"""
    return await plisio_service.get_invoice_status(invoice_id)

@payment_router.post("/plisio/webhook")
async def plisio_webhook(request: Request):
    """Webhook Plisio"""
    try:
        data = await request.json()
        logger.info(f"Plisio webhook: {data}")
        
        # Traiter le callback
        # Vérifier le statut et mettre à jour la commande
        
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Plisio webhook error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# ===== BINANCE PAY ROUTES =====

@payment_router.post("/binance/create")
async def create_binance_payment(request: PaymentRequest):
    """Créer une commande Binance Pay"""
    result = await binance_service.create_order(
        merchant_order_no=request.order_id,
        total_amount=request.amount,
        currency=request.currency,
        description=request.description or f"Order {request.order_id}",
        buyer_email=request.customer_email or ""
    )
    
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Order creation failed"))
    
    return result

@payment_router.get("/binance/status/{order_id}")
async def check_binance_status(order_id: str):
    """Vérifier le statut d'une commande Binance Pay"""
    return await binance_service.query_order(order_id)

@payment_router.post("/binance/webhook")
async def binance_webhook(request: Request):
    """Webhook Binance Pay"""
    try:
        data = await request.json()
        logger.info(f"Binance Pay webhook: {data}")
        
        # Vérifier la signature Binance
        # Traiter le callback
        
        return {"returnCode": "SUCCESS", "returnMessage": None}
    except Exception as e:
        logger.error(f"Binance webhook error: {str(e)}")
        return {"returnCode": "FAIL", "returnMessage": str(e)}
