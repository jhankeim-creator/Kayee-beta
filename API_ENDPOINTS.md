# 📚 API ENDPOINTS - LuxeBoutique E-Commerce

**Base URL:** `https://replica-store-1.preview.emergentagent.com/api`

---

## 🔐 AUTHENTIFICATION

### Inscription
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

### Connexion
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

### Profil utilisateur
```http
GET /api/auth/me
Authorization: Bearer {token}
```

---

## 🔐 AUTHENTIFICATION SOCIALE (OAuth)

### Google OAuth
```http
POST /api/auth/oauth/google
Content-Type: application/json

{
  "token": "google_id_token_here"
}
```

**Obtenir l'URL d'authentification:**
```http
GET /api/auth/oauth/google/url?redirect_uri=https://your-domain.com/callback
```

### Facebook OAuth
```http
POST /api/auth/oauth/facebook
Content-Type: application/json

{
  "access_token": "facebook_access_token_here"
}
```

**Obtenir l'URL d'authentification:**
```http
GET /api/auth/oauth/facebook/url?redirect_uri=https://your-domain.com/callback
```

---

## 💳 PAIEMENTS

### 1. Stripe (Cartes Bancaires)

**Créer un lien de paiement:**
```http
POST /api/payments/stripe/create
Content-Type: application/json

{
  "order_id": "ORD-12345",
  "amount": 99.99,
  "currency": "USD",
  "description": "Order #12345",
  "customer_email": "customer@example.com"
}
```

**Réponse:**
```json
{
  "success": true,
  "payment_id": "pi_xxxxx",
  "payment_url": "https://checkout.stripe.com/pay/xxxxx",
  "amount": 99.99,
  "currency": "USD",
  "status": "pending"
}
```

**Webhook (configuré automatiquement):**
```http
POST /api/payments/stripe/webhook
Stripe-Signature: {signature}
```

---

### 2. PayPal

**Créer une commande:**
```http
POST /api/payments/paypal/create
Content-Type: application/json

{
  "order_id": "ORD-12345",
  "amount": 99.99,
  "currency": "USD",
  "description": "Order #12345"
}
```

**Réponse:**
```json
{
  "success": true,
  "order_id": "8VF52814937998046",
  "approval_url": "https://www.paypal.com/checkoutnow?token=xxxxx",
  "amount": 99.99,
  "currency": "USD",
  "status": "created"
}
```

**Capturer le paiement:**
```http
POST /api/payments/paypal/capture/{order_id}
```

---

### 3. CoinPal.io (Crypto)

**Créer un paiement:**
```http
POST /api/payments/coinpal/create
Content-Type: application/json

{
  "order_id": "ORD-12345",
  "amount": 99.99,
  "currency": "USD",
  "description": "Order #12345",
  "customer_email": "customer@example.com"
}
```

**Réponse:**
```json
{
  "success": true,
  "payment_id": "coinpal_xxxxx",
  "payment_url": "https://coinpal.io/pay/xxxxx",
  "qr_code": "https://coinpal.io/qr/xxxxx",
  "amount": 99.99,
  "currency": "USD",
  "status": "pending",
  "expires_at": 1234567890
}
```

**Vérifier le statut:**
```http
GET /api/payments/coinpal/status/{payment_id}
```

**Webhook:**
```http
POST /api/payments/coinpal/webhook
X-Signature: {signature}
```

---

### 4. Plisio (Multi-Crypto)

**Créer une facture:**
```http
POST /api/payments/plisio/create
Content-Type: application/json

{
  "order_id": "ORD-12345",
  "amount": 99.99,
  "currency": "USD",
  "description": "Order #12345",
  "customer_email": "customer@example.com"
}
```

**Réponse:**
```json
{
  "success": true,
  "invoice_id": "txn_xxxxx",
  "invoice_url": "https://plisio.net/invoice/xxxxx",
  "wallet_hash": "bc1qxxxxx",
  "amount": 99.99,
  "currency": "BTC",
  "qr_code": "https://plisio.net/qr/xxxxx",
  "status": "new"
}
```

**Vérifier le statut:**
```http
GET /api/payments/plisio/status/{invoice_id}
```

**Webhook:**
```http
POST /api/payments/plisio/webhook
```

---

### 5. Binance Pay (Crypto Binance)

**Créer une commande:**
```http
POST /api/payments/binance/create
Content-Type: application/json

{
  "order_id": "ORD-12345",
  "amount": 99.99,
  "currency": "USDT",
  "description": "Order #12345",
  "customer_email": "customer@example.com"
}
```

**Réponse:**
```json
{
  "success": true,
  "order_id": "29383937493038367292",
  "checkout_url": "https://pay.binance.com/checkout/xxxxx",
  "qr_code": "https://qr.binance.com/xxxxx",
  "amount": 99.99,
  "currency": "USDT",
  "status": "INITIAL",
  "universal_url": {
    "qrContent": "binance://pay/xxxxx",
    "qrcodeLink": "https://qr.binance.com/xxxxx"
  }
}
```

**Vérifier le statut:**
```http
GET /api/payments/binance/status/{order_id}
```

**Webhook:**
```http
POST /api/payments/binance/webhook
BinancePay-Signature: {signature}
```

---

## 🛍️ PRODUITS

### Lister les produits (avec pagination)
```http
GET /api/products?skip=0&limit=20&category=fashion&featured=true
```

**Paramètres:**
- `skip`: Nombre de produits à sauter (pagination)
- `limit`: Nombre maximum de produits à retourner
- `category`: Filtrer par catégorie (fashion, jewelry)
- `featured`: Filtrer les produits en vedette (true/false)

### Compter les produits
```http
GET /api/products/count?category=fashion
```

### Détails d'un produit
```http
GET /api/products/{product_id}
```

### Créer un produit (Admin)
```http
POST /api/products
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "name": "Designer Dress",
  "description": "Beautiful evening dress",
  "price": 299.99,
  "images": ["https://image1.jpg", "https://image2.jpg"],
  "category": "fashion",
  "stock": 10,
  "featured": true
}
```

### Modifier un produit (Admin)
```http
PUT /api/products/{product_id}
Authorization: Bearer {admin_token}
```

### Supprimer un produit (Admin)
```http
DELETE /api/products/{product_id}
Authorization: Bearer {admin_token}
```

---

## 📦 COMMANDES

### Créer une commande
```http
POST /api/orders
Content-Type: application/json

{
  "user_email": "customer@example.com",
  "user_name": "John Doe",
  "items": [
    {
      "product_id": "uuid",
      "name": "Product Name",
      "price": 99.99,
      "quantity": 2,
      "image": "https://image.jpg"
    }
  ],
  "total": 199.98,
  "payment_method": "stripe",
  "shipping_address": {
    "address": "123 Main St",
    "city": "Paris",
    "postal_code": "75001",
    "country": "France"
  },
  "phone": "+33123456789",
  "notes": "Please deliver before 5pm"
}
```

### Lister toutes les commandes (Admin)
```http
GET /api/orders
Authorization: Bearer {admin_token}
```

### Mes commandes (Client)
```http
GET /api/orders/my
Authorization: Bearer {token}
```

### Détails d'une commande
```http
GET /api/orders/{order_id}
```

### Suivre une commande
```http
GET /api/orders/track/{order_number}
```

**Exemple:** `GET /api/orders/track/ORD-12345678`

### Mettre à jour le statut (Admin)
```http
PUT /api/orders/{order_id}/status?status=shipped&payment_status=confirmed
Authorization: Bearer {admin_token}
```

**Statuts disponibles:**
- `pending`, `processing`, `shipped`, `delivered`, `cancelled`

**Statuts de paiement:**
- `pending`, `confirmed`, `failed`

---

## 📊 CATÉGORIES

### Lister les catégories
```http
GET /api/categories
```

### Créer une catégorie (Admin)
```http
POST /api/categories
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "name": "Summer Collection",
  "slug": "summer-collection",
  "description": "Hot summer styles",
  "image": "https://image.jpg"
}
```

### Modifier une catégorie (Admin)
```http
PUT /api/categories/{category_id}
Authorization: Bearer {admin_token}
```

### Supprimer une catégorie (Admin)
```http
DELETE /api/categories/{category_id}
Authorization: Bearer {admin_token}
```

---

## 📈 STATISTIQUES (Admin)

### Tableau de bord
```http
GET /api/admin/stats
Authorization: Bearer {admin_token}
```

**Réponse:**
```json
{
  "total_products": 1500,
  "total_orders": 150,
  "pending_orders": 25,
  "total_users": 500,
  "total_revenue": 45000.00
}
```

---

## 🔔 NOTIFICATIONS

Les notifications sont envoyées automatiquement par email lors de:

1. **Création de commande** → Email de confirmation
2. **Paiement confirmé** → Email de confirmation de paiement
3. **Changement de statut** → Email de mise à jour:
   - Commande en traitement
   - Commande expédiée
   - Commande livrée
   - Commande annulée

**Configuration dans `.env`:**
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@luxeboutique.com
FROM_NAME=LuxeBoutique
```

---

## 🧪 MODE DÉMO

**Tous les endpoints fonctionnent en mode démo sans configuration !**

Quand les clés API ne sont pas configurées, le système retourne des données de démonstration:
- Les paiements retournent des URLs de test
- Les emails sont loggés dans la console
- L'OAuth fonctionne avec des utilisateurs de test

---

## 🔒 SÉCURITÉ

### Headers requis pour les routes protégées:
```http
Authorization: Bearer {jwt_token}
```

### Webhooks
Tous les webhooks vérifient les signatures pour garantir l'authenticité:
- Stripe: `Stripe-Signature`
- CoinPal: `X-Signature`
- Binance: `BinancePay-Signature`

---

## 📝 CODES D'ERREUR

- `200` - Succès
- `201` - Créé avec succès
- `400` - Requête invalide
- `401` - Non autorisé (token invalide)
- `403` - Interdit (accès admin requis)
- `404` - Ressource non trouvée
- `500` - Erreur serveur

---

## 🚀 EXEMPLES CURL

### Créer une commande
```bash
curl -X POST https://replica-store-1.preview.emergentagent.com/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_email": "test@example.com",
    "user_name": "Test User",
    "items": [{"product_id": "123", "name": "Test", "price": 99.99, "quantity": 1, "image": "img.jpg"}],
    "total": 99.99,
    "payment_method": "stripe",
    "shipping_address": {"address": "123 St", "city": "Paris", "postal_code": "75001", "country": "France"},
    "phone": "+33123456789"
  }'
```

### Créer un paiement Stripe
```bash
curl -X POST https://replica-store-1.preview.emergentagent.com/api/payments/stripe/create \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "ORD-12345",
    "amount": 99.99,
    "currency": "USD",
    "customer_email": "test@example.com"
  }'
```

### Lister les produits
```bash
curl https://replica-store-1.preview.emergentagent.com/api/products?skip=0&limit=10
```

---

**🎉 Votre API e-commerce complète est prête !**
