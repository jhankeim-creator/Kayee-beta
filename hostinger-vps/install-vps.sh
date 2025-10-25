#!/bin/bash

# Kayee01 - Installation automatique sur Hostinger VPS
# Ce script installe et configure tout automatiquement

set -e

echo "=========================================="
echo "🚀 KAYEE01 - INSTALLATION HOSTINGER VPS"
echo "=========================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Vérifier que le script est exécuté en root
if [ "$EUID" -ne 0 ]; then 
  echo -e "${RED}❌ Ce script doit être exécuté en root${NC}"
  echo "Utilisez: sudo bash install-vps.sh"
  exit 1
fi

echo -e "${GREEN}✅ Exécution en root${NC}"
echo ""

# Mise à jour du système
echo "📦 Mise à jour du système..."
apt-get update -qq
apt-get upgrade -y -qq
echo -e "${GREEN}✅ Système à jour${NC}"
echo ""

# Installation Docker
echo "🐳 Installation de Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl enable docker
    systemctl start docker
    echo -e "${GREEN}✅ Docker installé${NC}"
else
    echo -e "${GREEN}✅ Docker déjà installé${NC}"
fi
echo ""

# Installation Docker Compose
echo "📦 Installation de Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✅ Docker Compose installé${NC}"
else
    echo -e "${GREEN}✅ Docker Compose déjà installé${NC}"
fi
echo ""

# Installation des outils nécessaires
echo "🔧 Installation des outils..."
apt-get install -y -qq git curl wget nano ufw
echo -e "${GREEN}✅ Outils installés${NC}"
echo ""

# Configuration du pare-feu
echo "🔥 Configuration du pare-feu..."
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
echo -e "${GREEN}✅ Pare-feu configuré${NC}"
echo ""

# Création du répertoire de l'application
echo "📁 Création du répertoire..."
mkdir -p /opt/kayee01
cd /opt/kayee01
echo -e "${GREEN}✅ Répertoire créé : /opt/kayee01${NC}"
echo ""

# Clone du repository (vous devrez remplacer par votre repo)
echo "📥 Téléchargement du code..."
if [ -d ".git" ]; then
    echo "Repository déjà cloné, mise à jour..."
    git pull
else
    echo "⚠️  Configuration du repository GitHub..."
    echo "IMPORTANT: Vous devez d'abord pousser votre code sur GitHub"
    echo "Puis remplacez l'URL ci-dessous par votre repository"
    echo ""
    read -p "Entrez l'URL de votre repository GitHub: " REPO_URL
    if [ -z "$REPO_URL" ]; then
        echo "❌ URL manquante, abandon..."
        exit 1
    fi
    git clone "$REPO_URL" .
fi
echo -e "${GREEN}✅ Code téléchargé${NC}"
echo ""

# Création du fichier .env
echo "⚙️  Configuration des variables d'environnement..."
if [ ! -f "hostinger-vps/.env" ]; then
    cat > hostinger-vps/.env << EOF
# Configuration Kayee01 VPS
DOMAIN_NAME=your-domain.com

# MongoDB
MONGO_PASSWORD=ChangeThisSecurePassword123!

# JWT
JWT_SECRET_KEY=$(openssl rand -hex 32)

# SMTP Gmail
SMTP_USER=kayicom509@gmail.com
SMTP_PASSWORD=unstcfsyowwpiuzi

# Stripe (optionnel)
STRIPE_SECRET_KEY=your_stripe_key

# Plisio (optionnel)
PLISIO_API_KEY=your_plisio_key
EOF
    echo -e "${YELLOW}⚠️  Fichier .env créé avec valeurs par défaut${NC}"
    echo -e "${YELLOW}⚠️  IMPORTANT: Éditez hostinger-vps/.env avec vos vraies valeurs !${NC}"
else
    echo -e "${GREEN}✅ Fichier .env existe déjà${NC}"
fi
echo ""

# Création des répertoires SSL
echo "🔒 Préparation SSL..."
mkdir -p hostinger-vps/ssl
echo -e "${GREEN}✅ Répertoires SSL créés${NC}"
echo ""

echo "=========================================="
echo -e "${GREEN}✅ INSTALLATION TERMINÉE !${NC}"
echo "=========================================="
echo ""
echo "📋 PROCHAINES ÉTAPES:"
echo ""
echo "1. Éditez le fichier de configuration:"
echo "   nano /opt/kayee01/hostinger-vps/.env"
echo ""
echo "2. Modifiez au minimum:"
echo "   - DOMAIN_NAME (votre nom de domaine)"
echo "   - MONGO_PASSWORD (mot de passe sécurisé)"
echo ""
echo "3. Lancez l'application:"
echo "   cd /opt/kayee01/hostinger-vps"
echo "   bash start.sh"
echo ""
echo "4. Configurez SSL:"
echo "   bash setup-ssl.sh votre-domaine.com"
echo ""
echo "=========================================="
