# 🚀 GUIDE RAPIDE DE DÉPLOIEMENT - KAYEE01 VPS

## 📌 Ce Que Vous Devez Savoir

✅ **Toutes les erreurs ont été corrigées**
✅ **Le package est prêt pour le déploiement**
✅ **Installation automatique en 6 étapes**

---

## 🎯 ÉTAPE 1 : Préparer GitHub

### Sur votre ordinateur local :

```bash
# 1. Aller dans le dossier de l'application
cd /app

# 2. Initialiser Git (si pas déjà fait)
git init

# 3. Ajouter tous les fichiers
git add .

# 4. Créer le commit
git commit -m "Kayee01 - Ready for VPS deployment"

# 5. Créer la branche main
git branch -M main

# 6. Ajouter votre repository GitHub
# Remplacez VOTRE-USERNAME par votre nom d'utilisateur GitHub
git remote add origin https://github.com/VOTRE-USERNAME/kayee01.git

# 7. Pousser sur GitHub
git push -u origin main
```

**📝 Note :** Si vous n'avez pas de repository, créez-en un sur https://github.com/new

---

## 🎯 ÉTAPE 2 : Se Connecter au VPS Hostinger

```bash
# Remplacez par l'IP de votre VPS
ssh root@VOTRE-IP-VPS
```

**Mot de passe :** Utilisez le mot de passe fourni par Hostinger

---

## 🎯 ÉTAPE 3 : Installer Kayee01

### Option A : Installation Automatique (Recommandé)

```bash
# Créer le dossier
mkdir -p /opt/kayee01
cd /opt/kayee01

# Cloner votre repository
# Remplacez VOTRE-USERNAME par votre nom d'utilisateur GitHub
git clone https://github.com/VOTRE-USERNAME/kayee01.git .

# Aller dans le dossier VPS
cd hostinger-vps

# Rendre les scripts exécutables
chmod +x *.sh

# Lancer l'installation automatique
./install-vps.sh
```

### Option B : Installation Manuelle

Si vous préférez installer manuellement :

```bash
# Mise à jour du système
apt-get update && apt-get upgrade -y

# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh

# Installer Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Configurer le pare-feu
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# Cloner le repository
mkdir -p /opt/kayee01
cd /opt/kayee01
git clone https://github.com/VOTRE-USERNAME/kayee01.git .
cd hostinger-vps
chmod +x *.sh
```

---

## 🎯 ÉTAPE 4 : Configurer les Variables d'Environnement

```bash
cd /opt/kayee01/hostinger-vps

# Copier le fichier exemple
cp .env.example .env

# Éditer la configuration
nano .env
```

### Configuration MINIMALE Requise :

```env
# 1. VOTRE DOMAINE (OBLIGATOIRE)
DOMAIN_NAME=votre-domaine.com

# 2. MOT DE PASSE MONGODB (CHANGEZ-LE !)
MONGO_PASSWORD=UnMotDePasseTresFort123!@#

# 3. JWT SECRET (sera généré automatiquement)
JWT_SECRET_KEY=

# 4. SMTP (Déjà configuré, ne pas modifier)
SMTP_USER=kayicom509@gmail.com
SMTP_PASSWORD=unstcfsyowwpiuzi

# 5. STRIPE (Ajoutez votre clé réelle)
STRIPE_SECRET_KEY=sk_live_VOTRE_CLE_STRIPE

# 6. PLISIO (Ajoutez votre clé réelle)
PLISIO_API_KEY=VOTRE_CLE_PLISIO
```

**⚠️ IMPORTANT :**
- Changez `DOMAIN_NAME` par votre vrai domaine
- Utilisez un mot de passe fort pour `MONGO_PASSWORD`
- Si vous n'avez pas de clé Stripe/Plisio, laissez vide pour l'instant

**Pour sauvegarder dans nano :**
- Appuyez sur `Ctrl + X`
- Appuyez sur `Y` (pour Yes)
- Appuyez sur `Enter`

---

## 🎯 ÉTAPE 5 : Lancer l'Application

```bash
cd /opt/kayee01/hostinger-vps
./start.sh
```

**⏳ Attendez 2-3 minutes** que tous les services démarrent.

Vous verrez :
```
✅ KAYEE01 DÉMARRÉ !
Site principal: http://VOTRE-IP
Admin: http://VOTRE-IP/admin/login
API: http://VOTRE-IP/api
```

---

## 🎯 ÉTAPE 6 : Configurer SSL (HTTPS)

**⚠️ IMPORTANT :** Avant cette étape, assurez-vous que votre domaine pointe vers l'IP de votre VPS.

### Vérifier que le domaine pointe correctement :

```bash
# Remplacez par votre domaine
dig +short votre-domaine.com

# Comparez avec l'IP de votre serveur
curl -s ifconfig.me
```

Les deux IPs doivent être **identiques**.

### Configurer SSL :

```bash
cd /opt/kayee01/hostinger-vps
./setup-ssl.sh votre-domaine.com
```

Le script va :
1. Obtenir un certificat SSL gratuit de Let's Encrypt
2. Configurer Nginx pour HTTPS
3. Redémarrer les services

**✅ Terminé !** Votre site est maintenant accessible en HTTPS :
- https://votre-domaine.com
- https://votre-domaine.com/admin/login

---

## 🔍 Vérifier l'Installation

```bash
cd /opt/kayee01/hostinger-vps
./check-status.sh
```

Ce script vérifie :
- ✅ Docker et Docker Compose installés
- ✅ Fichier .env configuré
- ✅ Conteneurs en cours d'exécution
- ✅ Ports ouverts
- ✅ Accès web fonctionnel

---

## 📱 Accès à Votre Site

### URLs :
- **Site principal :** https://votre-domaine.com
- **Page admin :** https://votre-domaine.com/admin/login
- **API :** https://votre-domaine.com/api

### Identifiants Admin :
- **Email :** kayicom509@gmail.com
- **Password :** Admin123!

**⚠️ CHANGEZ LE MOT DE PASSE ADMIN IMMÉDIATEMENT APRÈS LA PREMIÈRE CONNEXION !**

---

## 🔧 Commandes Utiles

### Voir les logs en temps réel :
```bash
cd /opt/kayee01/hostinger-vps
docker-compose logs -f
```

### Logs d'un service spécifique :
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx
docker-compose logs -f mongodb
```

### Arrêter l'application :
```bash
cd /opt/kayee01/hostinger-vps
./stop.sh
```

### Redémarrer l'application :
```bash
cd /opt/kayee01/hostinger-vps
./stop.sh
./start.sh
```

### Mettre à jour le code depuis GitHub :
```bash
cd /opt/kayee01
git pull
cd hostinger-vps
./stop.sh
./start.sh
```

### Voir l'état des conteneurs :
```bash
cd /opt/kayee01/hostinger-vps
docker-compose ps
```

---

## 🐛 Dépannage

### Problème : Le site ne charge pas

**Solution 1 :** Vérifier que les conteneurs tournent
```bash
docker-compose ps
```

Tous les conteneurs doivent être "Up".

**Solution 2 :** Vérifier les logs
```bash
docker-compose logs
```

**Solution 3 :** Redémarrer
```bash
./stop.sh
./start.sh
```

---

### Problème : Erreur MongoDB

**Solution :** Vérifier le mot de passe dans `.env`
```bash
nano .env
# Vérifiez MONGO_PASSWORD
```

Puis redémarrez :
```bash
./stop.sh
./start.sh
```

---

### Problème : SSL échoue

**Causes possibles :**
1. Le domaine ne pointe pas vers le VPS
2. Les ports 80/443 ne sont pas ouverts
3. Un autre service utilise déjà le port

**Solutions :**
```bash
# Vérifier le DNS
dig +short votre-domaine.com
curl -s ifconfig.me

# Vérifier les ports
sudo ufw status

# Ouvrir les ports si nécessaire
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

---

### Problème : Les paiements ne fonctionnent pas

**Solution :** Vérifier les clés API dans `.env`
```bash
nano .env
# Vérifiez STRIPE_SECRET_KEY et PLISIO_API_KEY
```

Puis redémarrez le backend :
```bash
docker-compose restart backend
```

---

## 🔒 Sécurité

### Actions Importantes :

1. **Changez le mot de passe admin** dans l'application
2. **Utilisez un mot de passe fort** pour MongoDB
3. **Gardez vos clés API secrètes** (ne les partagez jamais)
4. **Sauvegardez régulièrement** la base de données

### Sauvegarder MongoDB :

```bash
# Créer une sauvegarde
docker exec kayee01-mongodb mongodump --out /data/backup --authenticationDatabase admin -u kayee01_admin -p VOTRE_MOT_DE_PASSE

# Copier la sauvegarde hors du conteneur
docker cp kayee01-mongodb:/data/backup ./backup-$(date +%Y%m%d)
```

### Restaurer MongoDB :

```bash
# Copier la sauvegarde dans le conteneur
docker cp ./backup kayee01-mongodb:/data/restore

# Restaurer
docker exec kayee01-mongodb mongorestore /data/restore --authenticationDatabase admin -u kayee01_admin -p VOTRE_MOT_DE_PASSE
```

---

## 📊 Performances

### Recommandations VPS :

- **Minimum :** 2 GB RAM, 1 CPU
- **Recommandé :** 4 GB RAM, 2 CPU
- **Optimal :** 8 GB RAM, 4 CPU

### Optimisation :

Si le site est lent, vous pouvez :
1. Augmenter les ressources du VPS
2. Optimiser les images des produits
3. Activer la mise en cache Nginx

---

## 🎉 Félicitations !

Votre boutique **Kayee01** est maintenant en ligne ! 🚀

### Prochaines Étapes :

1. ✅ Changez le mot de passe admin
2. ✅ Ajoutez vos produits
3. ✅ Configurez les méthodes de paiement
4. ✅ Testez le processus de commande
5. ✅ Configurez la sauvegarde automatique

---

## 📞 Support

Si vous rencontrez des problèmes :

1. **Consultez ce guide**
2. **Vérifiez les logs** : `docker-compose logs`
3. **Exécutez** : `./check-status.sh`
4. **Consultez** : `README.md` et `CORRECTIONS.md`

---

**Bonne vente ! 💰**
