# 🚀 Package de Déploiement Kayee01 pour Hostinger VPS

Ce package contient tout ce dont vous avez besoin pour déployer votre boutique e-commerce Kayee01 sur un VPS Hostinger avec Docker.

## 📋 Contenu du Package

```
hostinger-vps/
├── docker-compose.yml          # Configuration Docker Compose
├── Dockerfile.backend          # Image Docker pour FastAPI
├── Dockerfile.frontend         # Image Docker pour React
├── nginx.conf                  # Configuration Nginx (reverse proxy)
├── nginx-frontend.conf         # Configuration Nginx (frontend)
├── .env.example               # Exemple de configuration
├── install-vps.sh             # Script d'installation automatique
├── start.sh                   # Script de démarrage
├── stop.sh                    # Script d'arrêt
├── setup-ssl.sh               # Configuration SSL automatique
├── check-status.sh            # Vérification de l'état
├── GUIDE_DEPLOIEMENT_VPS.md   # Guide détaillé en français
└── README.md                  # Ce fichier
```

## 🎯 Prérequis

### Sur votre ordinateur local :
- Git installé
- Accès à votre repository GitHub (ou créez-en un nouveau)

### Sur le VPS Hostinger :
- VPS Ubuntu 20.04 ou 22.04
- Accès SSH root
- Minimum 2GB RAM recommandé
- Nom de domaine pointant vers votre VPS

## 📦 Installation Rapide

### Étape 1 : Pousser votre code sur GitHub

Si ce n'est pas déjà fait, créez un repository GitHub et poussez votre code :

```bash
# Sur votre ordinateur local, dans le dossier /app
cd /app
git init
git add .
git commit -m "Initial commit - Kayee01 e-commerce"
git branch -M main
git remote add origin https://github.com/VOTRE-USERNAME/kayee01.git
git push -u origin main
```

### Étape 2 : Se connecter au VPS

```bash
ssh root@votre-ip-vps
```

### Étape 3 : Installer Kayee01

```bash
# Télécharger et exécuter le script d'installation
wget https://raw.githubusercontent.com/VOTRE-USERNAME/kayee01/main/hostinger-vps/install-vps.sh
sudo bash install-vps.sh
```

**OU** si vous clonez manuellement :

```bash
# Créer le dossier
mkdir -p /opt/kayee01
cd /opt/kayee01

# Cloner votre repository
git clone https://github.com/VOTRE-USERNAME/kayee01.git .

# Rendre les scripts exécutables
cd hostinger-vps
chmod +x *.sh
```

### Étape 4 : Configurer les variables d'environnement

```bash
cd /opt/kayee01/hostinger-vps

# Copier le fichier exemple
cp .env.example .env

# Éditer la configuration
nano .env
```

**Configuration minimale requise :**

```env
# Votre nom de domaine
DOMAIN_NAME=votre-domaine.com

# Mot de passe MongoDB (changez-le !)
MONGO_PASSWORD=VotreMotDePasseSecurise123!

# JWT Secret (sera généré automatiquement)
JWT_SECRET_KEY=

# SMTP Gmail (déjà configuré)
SMTP_USER=kayicom509@gmail.com
SMTP_PASSWORD=unstcfsyowwpiuzi

# Stripe (ajoutez vos clés)
STRIPE_SECRET_KEY=sk_live_...

# Plisio (ajoutez votre clé)
PLISIO_API_KEY=votre_cle_plisio
```

### Étape 5 : Lancer l'application

```bash
cd /opt/kayee01/hostinger-vps
bash start.sh
```

Attendez environ 2-3 minutes que tous les services démarrent.

### Étape 6 : Configurer SSL (HTTPS)

**Important :** Assurez-vous que votre domaine pointe vers l'IP de votre VPS avant cette étape.

```bash
cd /opt/kayee01/hostinger-vps
bash setup-ssl.sh votre-domaine.com
```

## ✅ Vérification de l'Installation

```bash
cd /opt/kayee01/hostinger-vps
bash check-status.sh
```

## 🌐 Accès à votre Site

- **Site principal :** https://votre-domaine.com
- **Page admin :** https://votre-domaine.com/admin/login
- **API :** https://votre-domaine.com/api

### Identifiants Admin :
- **Email :** kayicom509@gmail.com
- **Mot de passe :** Admin123!

## 🔧 Commandes Utiles

### Démarrer l'application :
```bash
cd /opt/kayee01/hostinger-vps
bash start.sh
```

### Arrêter l'application :
```bash
cd /opt/kayee01/hostinger-vps
bash stop.sh
```

### Voir les logs :
```bash
cd /opt/kayee01/hostinger-vps
docker-compose logs -f
```

### Logs d'un service spécifique :
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f mongodb
```

### Redémarrer un service :
```bash
docker-compose restart backend
docker-compose restart frontend
docker-compose restart nginx
```

### Mettre à jour le code :
```bash
cd /opt/kayee01
git pull
cd hostinger-vps
bash stop.sh
bash start.sh
```

## 🐛 Dépannage

### Le site ne charge pas

1. Vérifier que les conteneurs tournent :
```bash
docker-compose ps
```

2. Vérifier les logs :
```bash
docker-compose logs
```

3. Vérifier que le domaine pointe vers le bon IP :
```bash
dig +short votre-domaine.com
curl -s ifconfig.me
```

### Erreur de connexion MongoDB

Vérifiez que le mot de passe dans `.env` est correct et que MongoDB est démarré :
```bash
docker-compose logs mongodb
```

### Problème SSL

Assurez-vous que :
- Le domaine pointe vers votre VPS
- Les ports 80 et 443 sont ouverts
- Nginx est en cours d'exécution

```bash
sudo ufw status
docker-compose ps nginx
```

## 🔒 Sécurité

### Changements obligatoires après installation :

1. **Mot de passe MongoDB** dans `.env`
2. **JWT_SECRET_KEY** dans `.env`
3. **Mot de passe admin** de l'application

### Recommandations :

- Utilisez des mots de passe forts
- Activez le pare-feu (UFW)
- Gardez Docker et le système à jour
- Sauvegardez régulièrement la base de données

### Sauvegarder MongoDB :

```bash
docker exec kayee01-mongodb mongodump --out /data/backup --authenticationDatabase admin -u kayee01_admin -p VOTRE_MOT_DE_PASSE
```

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│         Internet (Port 443/80)          │
└────────────────┬────────────────────────┘
                 │
         ┌───────▼────────┐
         │  Nginx Proxy   │ (Reverse Proxy + SSL)
         └───────┬────────┘
                 │
     ┌───────────┴───────────┐
     │                       │
┌────▼─────┐          ┌─────▼──────┐
│ Frontend │          │  Backend   │
│  React   │          │  FastAPI   │
│ (Port 80)│          │ (Port 8001)│
└──────────┘          └─────┬──────┘
                            │
                      ┌─────▼──────┐
                      │  MongoDB   │
                      │(Port 27017)│
                      └────────────┘
```

## 🆘 Support

Si vous rencontrez des problèmes :

1. Consultez le fichier `GUIDE_DEPLOIEMENT_VPS.md`
2. Vérifiez les logs : `docker-compose logs`
3. Exécutez : `bash check-status.sh`
4. Vérifiez que tous les ports sont ouverts

## 📝 Notes Importantes

- **Première connexion :** Il peut falloir 2-3 minutes pour que tous les services démarrent
- **MongoDB :** Les données sont persistées dans des volumes Docker
- **Uploads :** Les images uploadées sont sauvegardées dans un volume dédié
- **SSL :** Le certificat se renouvelle automatiquement tous les 90 jours
- **Logs :** Les logs Nginx sont dans `/var/log/nginx/` du conteneur

## 🎉 Félicitations !

Votre boutique Kayee01 est maintenant déployée sur Hostinger VPS avec Docker et SSL ! 🚀

Pour toute question, consultez la documentation complète dans `GUIDE_DEPLOIEMENT_VPS.md`.
