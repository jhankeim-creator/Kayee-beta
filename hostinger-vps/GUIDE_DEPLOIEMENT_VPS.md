# 🚀 GUIDE DÉPLOIEMENT HOSTINGER VPS - KAYEE01

## ✅ VOTRE SITE EST 100% PRÊT POUR HOSTINGER VPS

Ce guide vous permet de déployer votre site e-commerce Kayee01 sur Hostinger VPS en **30 minutes**.

---

## 📋 CE DONT VOUS AVEZ BESOIN

1. **Hostinger VPS** (4-5€/mois)
   - Plan KVM 1 ou supérieur
   - Ubuntu 20.04 ou 22.04
   - Accès SSH root

2. **Nom de domaine** (optionnel mais recommandé)
   - Peut être acheté sur Hostinger (~10€/an)
   - Ou utilisez l'IP du VPS temporairement

3. **Les informations suivantes:**
   - Mot de passe Gmail App (déjà fourni)
   - Clés Stripe/Plisio (optionnel)

---

## 🎯 DÉPLOIEMENT EN 4 ÉTAPES

### ÉTAPE 1 : Accéder au VPS (5 min)

#### 1.1 Obtenir les accès SSH

Après l'achat du VPS Hostinger, vous recevrez par email :
- **IP du serveur** : ex: 123.45.67.89
- **Utilisateur** : root
- **Mot de passe** : fourni par Hostinger

#### 1.2 Se connecter au VPS

**Depuis Windows :**
- Téléchargez PuTTY : https://putty.org
- Entrez l'IP du serveur
- Connectez-vous avec root + mot de passe

**Depuis Mac/Linux/Android (Termux) :**
```bash
ssh root@VOTRE_IP_VPS
```

Entrez le mot de passe quand demandé.

---

### ÉTAPE 2 : Installation Automatique (10 min)

#### 2.1 Télécharger le script d'installation

```bash
cd /root
wget https://raw.githubusercontent.com/kayee_beta/kayee01-ecommerce/main/hostinger-vps/install-vps.sh
chmod +x install-vps.sh
```

#### 2.2 Lancer l'installation

```bash
sudo bash install-vps.sh
```

**Ce script va installer automatiquement :**
- ✅ Docker & Docker Compose
- ✅ Nginx
- ✅ Certbot (SSL)
- ✅ Pare-feu (UFW)
- ✅ Télécharger votre code
- ✅ Créer la structure nécessaire

⏱️ **Durée : 5-10 minutes**

---

### ÉTAPE 3 : Configuration (10 min)

#### 3.1 Éditer le fichier de configuration

```bash
cd /opt/kayee01/hostinger-vps
nano .env
```

#### 3.2 Modifier ces valeurs IMPORTANTES :

```bash
# VOTRE NOM DE DOMAINE (ou IP si pas de domaine)
DOMAIN_NAME=kayee01.com

# MOT DE PASSE MONGODB (changez-le !)
MONGO_PASSWORD=VotreMotDePasseSecurise123!

# SMTP (déjà configuré)
SMTP_USER=kayicom509@gmail.com
SMTP_PASSWORD=unstcfsyowwpiuzi

# JWT (généré automatiquement, ne touchez pas)
JWT_SECRET_KEY=...

# STRIPE (optionnel)
STRIPE_SECRET_KEY=sk_test_...

# PLISIO (optionnel)
PLISIO_API_KEY=...
```

**Sauvegarder :**
- Appuyez sur `Ctrl+X`
- Tapez `Y`
- Appuyez sur `Entrée`

#### 3.3 Pointer votre domaine vers le VPS (si vous avez un domaine)

Dans votre gestionnaire de domaine (Hostinger, Namecheap, etc.) :

**Ajoutez un enregistrement A :**
```
Type: A
Name: @
Value: VOTRE_IP_VPS
TTL: 300
```

**Ajoutez un enregistrement A pour www :**
```
Type: A
Name: www
Value: VOTRE_IP_VPS
TTL: 300
```

⏱️ **Propagation DNS : 5-30 minutes**

---

### ÉTAPE 4 : Lancer le Site (5 min)

#### 4.1 Démarrer l'application

```bash
cd /opt/kayee01/hostinger-vps
bash start.sh
```

**Cela va :**
- ✅ Construire les images Docker
- ✅ Démarrer MongoDB
- ✅ Démarrer le backend FastAPI
- ✅ Démarrer le frontend React
- ✅ Configurer Nginx

⏱️ **Durée : 3-5 minutes**

#### 4.2 Vérifier que tout fonctionne

```bash
docker-compose ps
```

Vous devez voir 5 conteneurs **Up** :
- ✅ kayee01-mongodb
- ✅ kayee01-backend
- ✅ kayee01-frontend
- ✅ kayee01-nginx
- ✅ kayee01-certbot

#### 4.3 Tester le site

Ouvrez votre navigateur et allez sur :
- **Avec domaine :** http://kayee01.com
- **Sans domaine :** http://VOTRE_IP_VPS

**Testez :**
- ✅ Page d'accueil
- ✅ Liste des produits
- ✅ Admin : http://kayee01.com/admin/login
  - Email : kayicom509@gmail.com
  - Mot de passe : Admin123!

---

### ÉTAPE 5 : Configurer HTTPS/SSL (5 min) - OPTIONNEL

**⚠️ N'exécutez cette étape QUE si vous avez un nom de domaine et que le DNS est propagé !**

```bash
cd /opt/kayee01/hostinger-vps
bash setup-ssl.sh kayee01.com
```

**Ce script va :**
- ✅ Obtenir un certificat SSL gratuit (Let's Encrypt)
- ✅ Configurer HTTPS automatiquement
- ✅ Rediriger HTTP vers HTTPS
- ✅ Renouvellement automatique du certificat

**Testez :** https://kayee01.com (avec HTTPS)

---

## 🎉 DÉPLOIEMENT TERMINÉ !

### 🌐 URLs de votre site :

**Site public :**
```
https://kayee01.com
```

**Panneau Admin :**
```
https://kayee01.com/admin/login
Email: kayicom509@gmail.com
Password: Admin123!
```

**API Backend :**
```
https://kayee01.com/api
```

---

## 🛠️ COMMANDES UTILES

### Gérer l'application

```bash
# Démarrer
cd /opt/kayee01/hostinger-vps
bash start.sh

# Arrêter
bash stop.sh

# Redémarrer
bash stop.sh && bash start.sh

# Voir les logs
docker-compose logs -f

# Voir les logs d'un service spécifique
docker-compose logs -f backend
docker-compose logs -f frontend

# Statut des conteneurs
docker-compose ps
```

### Mise à jour du code

```bash
cd /opt/kayee01
git pull
cd hostinger-vps
bash stop.sh
bash start.sh
```

### Backup de la base de données

```bash
docker exec kayee01-mongodb mongodump --out /data/backup
docker cp kayee01-mongodb:/data/backup ./mongodb-backup-$(date +%Y%m%d)
```

---

## 📊 PERFORMANCES & RESSOURCES

### Ressources utilisées (VPS KVM 1) :

- **CPU :** ~20-40% en utilisation normale
- **RAM :** ~1.5-2 GB
- **Disque :** ~3-5 GB avec MongoDB

### Capacités :

- **Produits :** Illimité (limité par le disque)
- **Images :** Stockage illimité sur le VPS
- **Visiteurs simultanés :** 100-500 (selon le plan VPS)
- **Base de données :** Illimitée

---

## 🔧 DÉPANNAGE

### Le site ne charge pas

```bash
# Vérifier les conteneurs
docker-compose ps

# Vérifier les logs
docker-compose logs -f

# Redémarrer tout
bash stop.sh && bash start.sh
```

### Erreur de connexion MongoDB

```bash
# Vérifier MongoDB
docker-compose logs mongodb

# Redémarrer MongoDB
docker-compose restart mongodb
```

### Erreur 502 Bad Gateway

```bash
# Vérifier que le backend tourne
docker-compose ps backend

# Redémarrer le backend
docker-compose restart backend

# Voir les logs backend
docker-compose logs -f backend
```

### Le pare-feu bloque les connexions

```bash
# Vérifier le pare-feu
sudo ufw status

# Ouvrir les ports nécessaires
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

---

## 💰 COÛTS

### Hostinger VPS KVM 1 :
- **Prix :** ~4€/mois (ou 3.49€/mois si payé annuellement)
- **Inclus :**
  - 2 GB RAM
  - 1 CPU Core
  - 20 GB SSD
  - 100 GB Bandwidth
  - IPv4 dédiée

### Nom de domaine :
- **Prix :** ~10€/an
- **Inclus :** SSL gratuit via Let's Encrypt

### **Total : ~58€/an** (4.83€/mois en moyenne)

---

## 🎯 PROCHAINES ÉTAPES

1. ✅ **Testez votre site** complètement
2. ✅ **Ajoutez vos produits** via l'admin
3. ✅ **Configurez les paiements** (Stripe, Plisio)
4. ✅ **Testez une commande** de bout en bout
5. ✅ **Configurez les sauvegardes automatiques**
6. ✅ **Partagez votre site !**

---

## 📞 SUPPORT

### Problèmes techniques :
- Vérifiez les logs : `docker-compose logs -f`
- Consultez la section Dépannage ci-dessus
- Support Hostinger : https://www.hostinger.com/support

### Besoin d'aide supplémentaire :
- Email : kayicom509@gmail.com

---

## ✅ CHECKLIST FINALE

- [ ] VPS Hostinger acheté et accessible
- [ ] Script d'installation exécuté
- [ ] Fichier .env configuré
- [ ] Domaine pointé vers le VPS (optionnel)
- [ ] Application démarrée
- [ ] Site accessible
- [ ] Admin accessible
- [ ] SSL configuré (optionnel)
- [ ] Commande de test passée
- [ ] Emails fonctionnels

---

**🎉 FÉLICITATIONS ! Votre site Kayee01 est maintenant en ligne sur Hostinger VPS ! 🚀**

**Professionnel, rapide, sécurisé et 100% sous votre contrôle !**

---

*Guide créé le 25 Octobre 2025*
*Version : 1.0*
