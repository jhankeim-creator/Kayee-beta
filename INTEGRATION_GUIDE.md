# 🚀 Guide Complet d'Intégration - LuxeBoutique E-Commerce

## 📋 Table des Matières
1. [Paiements Automatiques](#paiements-automatiques)
2. [Authentification Sociale (OAuth)](#authentification-sociale)
3. [Notifications Email & SMS](#notifications)
4. [Configuration](#configuration)
5. [Tests](#tests)

---

## 💳 PAIEMENTS AUTOMATIQUES

### 1. **Stripe** (Cartes Bancaires)
**Documentation:** https://docs.stripe.com/payment-links/api

**Configuration:**
```env
STRIPE_SECRET_KEY=sk_test_xxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxx
```

**Obtenir les clés:**
1. Créez un compte sur https://dashboard.stripe.com
2. Allez dans "Developers" → "API keys"
3. Copiez vos clés de test ou production

**Fonctionnalités:**
- ✅ Création automatique de liens de paiement
- ✅ Webhooks pour confirmation automatique
- ✅ Paiements par carte bancaire
- ✅ Support 135+ devises

**Endpoint API:** `/api/payments/stripe/create`

---

### 2. **PayPal** (Paiement en ligne)
**Documentation:** https://developer.paypal.com/studio/checkout/payment-links-and-buttons

**Configuration:**
```env
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_client_secret
PAYPAL_MODE=sandbox  # ou "live" pour production
```

**Obtenir les clés:**
1. Créez un compte sur https://developer.paypal.com
2. Créez une application REST API
3. Copiez Client ID et Secret

**Fonctionnalités:**
- ✅ Création automatique de commandes
- ✅ Capture automatique des paiements
- ✅ Support mondial
- ✅ Protection acheteur/vendeur

**Endpoint API:** `/api/payments/paypal/create`

---

### 3. **CoinPal.io** (Crypto Multi-devises)
**Documentation:** https://docs.coinpal.io/

**Configuration:**
```env
COINPAL_API_KEY=your_api_key
COINPAL_API_SECRET=your_api_secret
COINPAL_WEBHOOK_SECRET=your_webhook_secret
```

**Obtenir les clés:**
1. Créez un compte marchand sur https://coinpal.io
2. Allez dans API Settings
3. Générez vos clés API

**Fonctionnalités:**
- ✅ Support BTC, ETH, USDT, BNB, et 50+ cryptos
- ✅ QR Code automatique
- ✅ Webhooks pour confirmation
- ✅ Conversion automatique en fiat

**Endpoint API:** `/api/payments/coinpal/create`

---

### 4. **Plisio** (Crypto Multi-devises)
**Documentation:** https://plisio.net/documentation/

**Configuration:**
```env
PLISIO_API_KEY=your_api_key
```

**Obtenir la clé:**
1. Créez un compte sur https://plisio.net
2. Allez dans Settings → API
3. Copiez votre API Key

**Fonctionnalités:**
- ✅ Support 100+ cryptomonnaies
- ✅ Factures automatiques
- ✅ Callbacks pour notifications
- ✅ Faibles frais de transaction

**Endpoint API:** `/api/payments/plisio/create`

---

### 5. **Binance Pay** (Crypto via Binance)
**Documentation:** https://developers.binance.com/docs/binance-pay/introduction

**Configuration:**
```env
BINANCE_PAY_API_KEY=your_api_key
BINANCE_PAY_API_SECRET=your_api_secret
```

**Obtenir les clés:**
1. Connectez-vous à Binance Merchant
2. Créez un certificat API
3. Téléchargez votre clé privée

**Fonctionnalités:**
- ✅ 0% de frais
- ✅ Confirmation instantanée
- ✅ QR Code Binance Pay
- ✅ Support multi-crypto

**Endpoint API:** `/api/payments/binance/create`

---

## 🔐 AUTHENTIFICATION SOCIALE (OAuth)

### 1. **Google OAuth**
**Documentation:** https://developers.google.com/identity/protocols/oauth2

**Configuration:**
```env
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret
```

**Configuration:**
1. Allez sur https://console.cloud.google.com
2. Créez un projet
3. Activez "Google+ API"
4. Créez des identifiants OAuth 2.0
5. Ajoutez les URL de redirection autorisées:
   - `https://your-domain.com/auth/google/callback`

**Fonctionnalités:**
- ✅ Connexion en un clic
- ✅ Récupération automatique du profil
- ✅ Email vérifié automatiquement

**Endpoint API:** `/api/auth/google`

---

### 2. **Facebook Login**
**Documentation:** https://developers.facebook.com/docs/facebook-login

**Configuration:**
```env
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
```

**Configuration:**
1. Allez sur https://developers.facebook.com
2. Créez une application
3. Ajoutez "Facebook Login"
4. Configurez les URL de redirection OAuth

**Fonctionnalités:**
- ✅ Connexion rapide
- ✅ Accès au profil Facebook
- ✅ Permissions personnalisables

**Endpoint API:** `/api/auth/facebook`

---

### 3. **Twitter/X OAuth**
**Documentation:** https://developer.twitter.com/en/docs/authentication

**Configuration:**
```env
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
```

**Configuration:**
1. Allez sur https://developer.twitter.com
2. Créez une application
3. Générez vos clés API
4. Activez OAuth 1.0a

**Fonctionnalités:**
- ✅ Connexion avec X/Twitter
- ✅ Récupération du profil
- ✅ OAuth 1.0a sécurisé

**Endpoint API:** `/api/auth/twitter`

---

## 📧 NOTIFICATIONS EMAIL & SMS

### Email (SMTP)
**Configuration Gmail:**
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@luxeboutique.com
FROM_NAME=LuxeBoutique
```

**Obtenir le mot de passe d'application Gmail:**
1. Activez la vérification en 2 étapes
2. Allez dans Sécurité → Mots de passe des applications
3. Générez un mot de passe pour "Mail"

**Types d'emails automatiques:**
- ✅ Confirmation de commande
- ✅ Confirmation de paiement
- ✅ Commande expédiée
- ✅ Commande livrée
- ✅ Commande annulée

---

### SMS (Twilio - Optionnel)
**Configuration:**
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

**Configuration:**
1. Créez un compte sur https://www.twilio.com
2. Achetez un numéro de téléphone
3. Copiez vos identifiants

---

## ⚙️ CONFIGURATION RAPIDE

### Mode Démo
**Tous les services fonctionnent en mode démo sans configuration !**
- Les paiements retournent des URLs de démonstration
- Les emails sont loggés dans la console
- L'OAuth fonctionne avec des données de test

### Mode Production

**Étape 1: Configurer les paiements**
```bash
# Éditez /app/backend/.env
STRIPE_SECRET_KEY=sk_live_xxxxx
PAYPAL_CLIENT_ID=xxxxx
COINPAL_API_KEY=xxxxx
PLISIO_API_KEY=xxxxx
BINANCE_PAY_API_KEY=xxxxx
```

**Étape 2: Configurer OAuth**
```bash
GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
FACEBOOK_APP_ID=xxxxx
TWITTER_API_KEY=xxxxx
```

**Étape 3: Configurer les notifications**
```bash
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

**Étape 4: Redémarrer**
```bash
sudo supervisorctl restart backend
```

---

## 🧪 TESTS

### Tester un paiement (Mode Démo)
```bash
curl -X POST https://your-domain.com/api/payments/stripe/create \
  -H "Content-Type: application/json" \
  -d '{"order_id": "test123", "amount": 99.99}'
```

### Tester OAuth Google
1. Allez sur `/admin/login`
2. Cliquez sur "Se connecter avec Google"
3. Autorisez l'application

### Vérifier les emails
```bash
# Les emails en mode démo sont loggés ici:
tail -f /var/log/supervisor/backend.out.log | grep "EMAIL"
```

---

## 🔗 LIENS UTILES

### Documentation des APIs
- **CoinPal:** https://docs.coinpal.io/
- **Plisio:** https://plisio.net/documentation/
- **Binance Pay:** https://developers.binance.com/docs/binance-pay/introduction
- **Stripe:** https://docs.stripe.com/payment-links/api
- **PayPal:** https://developer.paypal.com/studio/checkout/payment-links-and-buttons
- **Google OAuth:** https://developers.google.com/identity
- **Facebook Login:** https://developers.facebook.com/docs/facebook-login
- **Twitter OAuth:** https://developer.twitter.com/en/docs/authentication

### Support
- **Email:** support@luxeboutique.com
- **WhatsApp:** +1234567890
- **Documentation:** /app/STORE_INSTRUCTIONS.md

---

## 🎯 CHECKLIST DE DÉPLOIEMENT

**Avant de passer en production:**

- [ ] Configurer toutes les clés API (production)
- [ ] Tester chaque méthode de paiement
- [ ] Configurer les webhooks pour chaque service
- [ ] Tester l'authentification sociale
- [ ] Configurer l'envoi d'emails SMTP
- [ ] Activer HTTPS
- [ ] Changer les mots de passe par défaut
- [ ] Configurer les sauvegardes MongoDB
- [ ] Tester le workflow complet (commande → paiement → email)
- [ ] Vérifier les logs d'erreur

---

**💪 Votre boutique est maintenant équipée d'un système de paiement professionnel complet !**
