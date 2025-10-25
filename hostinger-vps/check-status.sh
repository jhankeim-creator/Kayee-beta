#!/bin/bash

# Vérification de l'installation Kayee01

echo "=========================================="
echo "🔍 VÉRIFICATION KAYEE01"
echo "=========================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

cd "$(dirname "$0")"

# Vérifier Docker
echo "1. Docker:"
if command -v docker &> /dev/null; then
    echo -e "   ${GREEN}✅ Installé${NC}"
    docker --version
else
    echo -e "   ${RED}❌ Non installé${NC}"
fi
echo ""

# Vérifier Docker Compose
echo "2. Docker Compose:"
if command -v docker-compose &> /dev/null; then
    echo -e "   ${GREEN}✅ Installé${NC}"
    docker-compose --version
else
    echo -e "   ${RED}❌ Non installé${NC}"
fi
echo ""

# Vérifier le fichier .env
echo "3. Configuration (.env):"
if [ -f ".env" ]; then
    echo -e "   ${GREEN}✅ Fichier .env existe${NC}"
    
    source .env
    
    if [ "$DOMAIN_NAME" == "your-domain.com" ]; then
        echo -e "   ${YELLOW}⚠️  Domaine par défaut - à changer${NC}"
    else
        echo -e "   ${GREEN}✅ Domaine: $DOMAIN_NAME${NC}"
    fi
    
    if [ "$MONGO_PASSWORD" == "ChangeThisSecurePassword123!" ]; then
        echo -e "   ${YELLOW}⚠️  Mot de passe MongoDB par défaut - à changer${NC}"
    else
        echo -e "   ${GREEN}✅ Mot de passe MongoDB configuré${NC}"
    fi
else
    echo -e "   ${RED}❌ Fichier .env manquant${NC}"
fi
echo ""

# Vérifier les conteneurs
echo "4. Conteneurs Docker:"
if docker-compose ps | grep -q "Up"; then
    echo -e "   ${GREEN}✅ Conteneurs en cours d'exécution${NC}"
    docker-compose ps
else
    echo -e "   ${YELLOW}⚠️  Aucun conteneur en cours d'exécution${NC}"
    echo "   Lancez: bash start.sh"
fi
echo ""

# Vérifier les ports
echo "5. Ports:"
if netstat -tuln | grep -q ":80 "; then
    echo -e "   ${GREEN}✅ Port 80 (HTTP) ouvert${NC}"
else
    echo -e "   ${RED}❌ Port 80 fermé${NC}"
fi

if netstat -tuln | grep -q ":443 "; then
    echo -e "   ${GREEN}✅ Port 443 (HTTPS) ouvert${NC}"
else
    echo -e "   ${YELLOW}⚠️  Port 443 fermé (normal si SSL pas configuré)${NC}"
fi
echo ""

# Vérifier l'accès web
echo "6. Accès web:"
IP=$(curl -s ifconfig.me)
echo "   IP du serveur: $IP"

if curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -q "200\|301\|302"; then
    echo -e "   ${GREEN}✅ Site accessible localement${NC}"
else
    echo -e "   ${RED}❌ Site non accessible${NC}"
fi
echo ""

echo "=========================================="
echo "📋 RÉSUMÉ"
echo "=========================================="
echo ""
echo "URLs d'accès:"
if [ -f ".env" ]; then
    source .env
    if [ "$DOMAIN_NAME" != "your-domain.com" ]; then
        echo "   http://$DOMAIN_NAME"
        echo "   http://$DOMAIN_NAME/admin/login"
    else
        echo "   http://$IP"
        echo "   http://$IP/admin/login"
    fi
else
    echo "   http://$IP"
    echo "   http://$IP/admin/login"
fi
echo ""
echo "Identifiants Admin:"
echo "   Email: kayicom509@gmail.com"
echo "   Password: Admin123!"
echo ""
echo "=========================================="
