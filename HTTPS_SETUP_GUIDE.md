# 🔐 GUIDE COMPLET - CONFIGURATION HTTPS POUR KAYEE01 SUR HOSTINGER VPS

## 📋 PRÉ-REQUIS

Avant de commencer, assurez-vous que :

1. ✅ **Nom de domaine configuré** (ex: kayee01.com)
2. ✅ **DNS pointant vers votre VPS** 
   - Enregistrement A : `kayee01.com` → `VOTRE_IP_VPS`
   - Enregistrement A : `www.kayee01.com` → `VOTRE_IP_VPS`
3. ✅ **Ports ouverts dans le firewall**:
   - Port 80 (HTTP)
   - Port 443 (HTTPS)
4. ✅ **Accès root au VPS**

---

## 🚀 ÉTAPE 1 : VÉRIFIER LE DNS

```bash
# Vérifier que le DNS pointe vers votre serveur
ping kayee01.com
ping www.kayee01.com

# Ou utilisez :
nslookup kayee01.com
```

**Résultat attendu :** L'IP retournée doit être celle de votre VPS.

---

## 🚀 ÉTAPE 2 : OUVRIR LES PORTS (Hostinger)

Sur Hostinger VPS, les ports sont généralement ouverts par défaut. Vérifiez avec :

```bash
# Vérifier le firewall UFW (si utilisé)
sudo ufw status

# Si UFW est actif, ouvrir les ports :
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
```

---

## 🚀 ÉTAPE 3 : EXÉCUTER LE SCRIPT D'INSTALLATION

```bash
# Se connecter au VPS via SSH
ssh root@VOTRE_IP_VPS

# Aller dans le dossier de l'application
cd /app

# Rendre le script exécutable (déjà fait)
chmod +x setup-https.sh

# Exécuter le script
sudo ./setup-https.sh
```

### 📝 Le script vous demandera :

1. **Votre nom de domaine** (ex: `kayee01.com`)
2. **Votre email** (pour Let's Encrypt, ex: `admin@kayee01.com`)
3. **Confirmation** pour continuer

### ⚙️ Le script va automatiquement :

1. ✅ Installer NGINX et Certbot
2. ✅ Construire le frontend React (production build)
3. ✅ Configurer NGINX avec redirection HTTP → HTTPS
4. ✅ Obtenir le certificat SSL de Let's Encrypt
5. ✅ Configurer le renouvellement automatique
6. ✅ Ajouter les headers de sécurité
7. ✅ Bloquer l'accès aux fichiers sensibles
8. ✅ Redémarrer tous les services

---

## 🚀 ÉTAPE 4 : METTRE À JOUR LES VARIABLES D'ENVIRONNEMENT

Après l'installation HTTPS, mettez à jour le fichier `.env` du frontend :

```bash
cd /app/frontend
nano .env
```

Modifiez :
```env
REACT_APP_BACKEND_URL=https://kayee01.com
```

Puis rebuilder :
```bash
yarn build
sudo systemctl reload nginx
```

---

## 🚀 ÉTAPE 5 : VÉRIFIER L'INSTALLATION

### 1. Tester le site

Ouvrez votre navigateur :
- `http://kayee01.com` → **Doit rediriger vers** `https://kayee01.com`
- `https://kayee01.com` → **Doit afficher votre site avec cadenas vert** 🔒

### 2. Vérifier le certificat SSL

```bash
# Voir les certificats installés
sudo certbot certificates

# Tester le renouvellement automatique
sudo certbot renew --dry-run
```

### 3. Tester la sécurité SSL

Visitez : https://www.ssllabs.com/ssltest/

Entrez votre domaine et vérifiez que vous obtenez **A ou A+**

---

## 🔄 RENOUVELLEMENT AUTOMATIQUE

Le certificat SSL expire après **90 jours**, mais Certbot configure un **renouvellement automatique** via cron.

### Vérifier le cron job :

```bash
sudo systemctl status certbot.timer
```

### Renouveler manuellement (si nécessaire) :

```bash
sudo certbot renew
sudo systemctl reload nginx
```

---

## 📂 FICHIERS DE CONFIGURATION

### NGINX Configuration
```bash
/etc/nginx/sites-available/kayee01
/etc/nginx/sites-enabled/kayee01
```

### Certificats SSL
```bash
/etc/letsencrypt/live/kayee01.com/fullchain.pem
/etc/letsencrypt/live/kayee01.com/privkey.pem
```

### Logs
```bash
/var/log/nginx/kayee01_access.log
/var/log/nginx/kayee01_error.log
```

---

## 🛠️ COMMANDES UTILES

```bash
# Tester la configuration NGINX
sudo nginx -t

# Recharger NGINX
sudo systemctl reload nginx

# Redémarrer NGINX
sudo systemctl restart nginx

# Voir l'état de NGINX
sudo systemctl status nginx

# Voir les logs en temps réel
sudo tail -f /var/log/nginx/kayee01_error.log

# Forcer le renouvellement SSL
sudo certbot renew --force-renewal

# Voir tous les certificats
sudo certbot certificates
```

---

## 🔒 HEADERS DE SÉCURITÉ AJOUTÉS

Le script configure automatiquement les headers de sécurité suivants :

1. **HSTS** (Strict-Transport-Security) - Force HTTPS
2. **X-Frame-Options** - Protection contre clickjacking
3. **X-Content-Type-Options** - Protection contre MIME sniffing
4. **X-XSS-Protection** - Protection XSS
5. **Referrer-Policy** - Contrôle des informations de référence

---

## ❌ DÉPANNAGE

### Problème 1 : "Failed to obtain SSL certificate"

**Causes possibles :**
- DNS ne pointe pas vers le serveur
- Ports 80/443 fermés
- Autre service utilise le port 80

**Solutions :**
```bash
# Vérifier DNS
nslookup kayee01.com

# Vérifier ports
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443

# Arrêter Apache si installé
sudo systemctl stop apache2
```

### Problème 2 : "502 Bad Gateway"

**Cause :** Backend FastAPI n'est pas démarré

**Solution :**
```bash
sudo supervisorctl status
sudo supervisorctl restart backend
```

### Problème 3 : "Site inaccessible"

**Solutions :**
```bash
# Vérifier NGINX
sudo systemctl status nginx

# Vérifier les logs
sudo tail -f /var/log/nginx/kayee01_error.log

# Vérifier la configuration
sudo nginx -t
```

---

## 📱 TESTER TOUTES LES PAGES

Après l'installation, testez :

1. ✅ Homepage : `https://kayee01.com`
2. ✅ Shop : `https://kayee01.com/shop`
3. ✅ Product : `https://kayee01.com/product/[id]`
4. ✅ Cart : `https://kayee01.com/cart`
5. ✅ Checkout : `https://kayee01.com/checkout`
6. ✅ Login : `https://kayee01.com/login`
7. ✅ Account : `https://kayee01.com/account`
8. ✅ Admin : `https://kayee01.com/admin/login`
9. ✅ Track Order : `https://kayee01.com/track-order`
10. ✅ API : `https://kayee01.com/api/products`

---

## 🎉 FÉLICITATIONS !

Votre site Kayee01 est maintenant sécurisé avec HTTPS ! 🔐

**Prochaines étapes :**
1. Tester tous les paiements (Stripe, Crypto, etc.)
2. Vérifier les emails de confirmation
3. Configurer le monitoring
4. Faire des backups réguliers

---

## 📞 SUPPORT

En cas de problème, vérifiez :
1. Les logs NGINX : `/var/log/nginx/kayee01_error.log`
2. Les logs backend : `/var/log/supervisor/backend.err.log`
3. L'état des services : `sudo supervisorctl status`

**Bonne chance ! 🚀**
