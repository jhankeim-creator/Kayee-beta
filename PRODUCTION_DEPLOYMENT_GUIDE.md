# 🚀 GUIDE COMPLET - DÉPLOIEMENT PRODUCTION AVEC HTTPS

## 📋 APERÇU

Ce guide vous permettra de déployer votre site Kayee01 E-commerce en production sur un VPS Hostinger avec HTTPS complet, SSL/TLS sécurisé, et toutes les bonnes pratiques.

---

## 🎯 CE QUI SERA INSTALLÉ

✅ **NGINX** - Serveur web reverse proxy
✅ **Let's Encrypt SSL** - Certificat HTTPS gratuit
✅ **FastAPI Backend** - API Python sur port 8001
✅ **React Frontend** - Build production optimisé
✅ **MongoDB** - Base de données
✅ **Supervisor** - Gestionnaire de processus backend
✅ **UFW Firewall** - Sécurité réseau
✅ **Auto-renewal SSL** - Renouvellement automatique tous les 90 jours

---

## 📦 PRÉ-REQUIS OBLIGATOIRES

### 1. VPS Hostinger
- **Minimum**: 2 CPU, 4GB RAM, 50GB Storage
- **OS**: Ubuntu 20.04 ou 22.04 LTS
- **Accès**: SSH root

### 2. Nom de Domaine
- Domaine acheté (ex: kayee01.com)
- **DNS configuré** (IMPORTANT !) :
  ```
  Type A: kayee01.com → VOTRE_IP_VPS
  Type A: www.kayee01.com → VOTRE_IP_VPS
  ```

### 3. Ports Ouverts
- Port 22 (SSH)
- Port 80 (HTTP)
- Port 443 (HTTPS)

### 4. Fichiers de l'Application
- Tout le code source dans `/app` (backend + frontend)

---

## 🚀 DÉPLOIEMENT EN 1 COMMANDE

### Étape 1: Préparer les Fichiers

Sur votre machine locale ou Emergent :

```bash
# Créer une archive du projet
cd /app
tar -czf kayee01-app.tar.gz backend/ frontend/

# Transférer vers le VPS
scp kayee01-app.tar.gz root@VOTRE_IP_VPS:/tmp/
```

### Étape 2: Sur le VPS

```bash
# Se connecter en SSH
ssh root@VOTRE_IP_VPS

# Extraire les fichiers
cd /var/www
tar -xzf /tmp/kayee01-app.tar.gz
mv backend frontend kayee01/

# Télécharger le script de déploiement
cd /var/www/kayee01
wget https://raw.githubusercontent.com/votre-repo/deploy-production.sh
# OU copiez le fichier /app/deploy-production.sh

chmod +x deploy-production.sh

# LANCER LE DÉPLOIEMENT
sudo ./deploy-production.sh
```

### Étape 3: Suivre les Instructions

Le script vous demandera :
1. **Nom de domaine** : `kayee01.com`
2. **Email** : `admin@kayee01.com`
3. **Confirmation** : `y`

Ensuite, il installera tout automatiquement (10-20 minutes).

---

## 📝 CONFIGURATION MANUELLE DES API KEYS

Après le déploiement automatique, configurez vos clés API :

```bash
# Éditer le fichier .env backend
nano /var/www/kayee01/backend/.env
```

**Modifiez ces valeurs :**

```env
# Email (SMTP)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=votre_email@gmail.com
SMTP_PASSWORD=votre_app_password_gmail

# Stripe
STRIPE_SECRET_KEY=sk_live_VOTRE_CLE_STRIPE

# Plisio (Crypto)
PLISIO_SECRET_KEY=votre_cle_plisio

# Admin Email
ADMIN_EMAIL=admin@kayee01.com
```

Puis redémarrez le backend :

```bash
supervisorctl restart kayee01-backend
```

---

## 🔒 VÉRIFICATIONS DE SÉCURITÉ

### 1. Vérifier HTTPS

```bash
# Test basique
curl -I https://kayee01.com

# Vérifier le certificat
openssl s_client -connect kayee01.com:443 -servername kayee01.com
```

### 2. Vérifier la Redirection HTTP → HTTPS

```bash
curl -I http://kayee01.com
# Doit retourner: 301 Moved Permanently
# Location: https://kayee01.com
```

### 3. Test SSL Grade

Visitez : https://www.ssllabs.com/ssltest/

Entrez votre domaine et visez **A+**

### 4. Vérifier les Headers de Sécurité

```bash
curl -I https://kayee01.com | grep -i "strict-transport\|x-frame\|x-content"
```

Doit afficher :
- `Strict-Transport-Security: max-age=31536000`
- `X-Frame-Options: SAMEORIGIN`
- `X-Content-Type-Options: nosniff`

---

## 🧪 TESTS COMPLETS

### Test 1: Frontend

```bash
curl https://kayee01.com
# Doit retourner le HTML React
```

### Test 2: Backend API

```bash
curl https://kayee01.com/api/products?featured=true
# Doit retourner un JSON avec les produits
```

### Test 3: Pages Principales

Testez dans votre navigateur :
- ✅ https://kayee01.com (Homepage)
- ✅ https://kayee01.com/shop (Shop)
- ✅ https://kayee01.com/login (Login)
- ✅ https://kayee01.com/cart (Cart)
- ✅ https://kayee01.com/admin/login (Admin)

### Test 4: Paiements

- ✅ Stripe : Mode test puis live
- ✅ Crypto (Plisio) : Adresse générée
- ✅ Paiements manuels

---

## 📊 SURVEILLANCE & LOGS

### Logs Backend (FastAPI)

```bash
# Voir les logs en temps réel
tail -f /var/log/supervisor/kayee01-backend.err.log
tail -f /var/log/supervisor/kayee01-backend.out.log

# Rechercher erreurs
grep -i error /var/log/supervisor/kayee01-backend.err.log
```

### Logs NGINX

```bash
# Access logs
tail -f /var/log/nginx/kayee01_access.log

# Error logs
tail -f /var/log/nginx/kayee01_error.log
```

### Logs MongoDB

```bash
tail -f /var/log/mongodb/mongod.log
```

### État des Services

```bash
# Backend
supervisorctl status kayee01-backend

# NGINX
systemctl status nginx

# MongoDB
systemctl status mongodb

# Certificat SSL
certbot certificates
```

---

## 🔄 GESTION DU SSL

### Renouvellement Manuel

```bash
sudo certbot renew
sudo systemctl reload nginx
```

### Vérifier l'Auto-Renewal

```bash
# Test de renouvellement (dry run)
sudo certbot renew --dry-run

# Voir le cron job
systemctl list-timers | grep certbot
```

### Ajouter un Nouveau Domaine

```bash
sudo certbot --nginx -d nouveaudomaine.com -d www.nouveaudomaine.com
```

---

## 🔧 COMMANDES DE MAINTENANCE

### Redémarrer Services

```bash
# Backend seulement
supervisorctl restart kayee01-backend

# NGINX seulement
systemctl reload nginx

# Tout redémarrer
supervisorctl restart all
systemctl restart nginx
```

### Mettre à Jour le Code

```bash
cd /var/www/kayee01

# Backend
cd backend
git pull  # Si vous utilisez Git
supervisorctl restart kayee01-backend

# Frontend
cd ../frontend
git pull
yarn build
systemctl reload nginx
```

### Backup Base de Données

```bash
# Créer un backup
mongodump --db kayee01_db --out /backup/mongo-$(date +%Y%m%d)

# Restaurer un backup
mongorestore --db kayee01_db /backup/mongo-20231023/kayee01_db
```

---

## ⚠️ DÉPANNAGE

### Problème 1: Certificat SSL non obtenu

**Symptômes:**
- `certbot certonly` échoue
- "Challenge failed"

**Solutions:**
```bash
# Vérifier DNS
nslookup kayee01.com

# Vérifier que NGINX écoute sur port 80
netstat -tulpn | grep :80

# Vérifier les logs Certbot
tail -f /var/log/letsencrypt/letsencrypt.log

# Essayer manuellement
certbot certonly --standalone -d kayee01.com
```

### Problème 2: 502 Bad Gateway

**Cause:** Backend non démarré

**Solutions:**
```bash
# Vérifier backend
supervisorctl status kayee01-backend

# Voir logs d'erreur
tail -f /var/log/supervisor/kayee01-backend.err.log

# Redémarrer
supervisorctl restart kayee01-backend
```

### Problème 3: API ne répond pas

**Solutions:**
```bash
# Tester directement le backend
curl http://localhost:8001/api/products

# Vérifier proxy NGINX
tail -f /var/log/nginx/kayee01_error.log

# Tester config NGINX
nginx -t
```

### Problème 4: Site lent

**Solutions:**
```bash
# Activer cache NGINX (ajouter dans config)
# Optimiser MongoDB indexes
# Vérifier charge serveur
htop

# Analyser logs
tail -f /var/log/nginx/kayee01_access.log | grep -v "GET /static"
```

---

## 🔐 SÉCURITÉ RENFORCÉE (Optionnel)

### 1. Fail2Ban (Protection SSH)

```bash
apt-get install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban
```

### 2. Désactiver Root Login SSH

```bash
nano /etc/ssh/sshd_config
# Modifier: PermitRootLogin no
systemctl restart sshd
```

### 3. Mise à Jour Automatique de Sécurité

```bash
apt-get install -y unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades
```

### 4. Monitoring (Optionnel)

Installez **Netdata** pour monitoring en temps réel :

```bash
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
```

Accès : https://kayee01.com:19999

---

## 📈 OPTIMISATIONS PERFORMANCE

### 1. Compression Gzip (Déjà configuré)

Vérifié dans NGINX config.

### 2. Cache Navigateur

Déjà configuré pour fichiers statiques (1 an).

### 3. CDN (Optionnel)

Utilisez Cloudflare pour CDN gratuit :
- Ajoutez votre site sur Cloudflare
- Changez les nameservers
- Activez proxy orange (CDN)

---

## 📋 CHECKLIST POST-DÉPLOIEMENT

- [ ] Site accessible en HTTPS
- [ ] Certificat SSL valide (cadenas vert)
- [ ] Redirection HTTP → HTTPS fonctionne
- [ ] Backend API répond (`/api/products`)
- [ ] Login/Register fonctionnels
- [ ] Admin login accessible
- [ ] Paiements Stripe testés
- [ ] Emails envoyés correctement
- [ ] SSL Grade A+ sur SSLLabs
- [ ] Logs backend sans erreurs
- [ ] Logs NGINX sans erreurs
- [ ] Firewall UFW actif
- [ ] Auto-renewal SSL configuré
- [ ] Backup MongoDB planifié
- [ ] Monitoring en place

---

## 🎉 FÉLICITATIONS !

Votre site Kayee01 E-commerce est maintenant :

✅ **Déployé en production**
✅ **Sécurisé avec HTTPS**
✅ **Optimisé pour performance**
✅ **Prêt à accepter des commandes**

**URL Finale:** https://kayee01.com

---

## 📞 SUPPORT

Pour toute aide :
1. Vérifiez les logs (`/var/log/`)
2. Consultez ce guide
3. Contactez le support Hostinger si problème serveur

**Bonne chance avec votre e-commerce ! 🚀💰**
