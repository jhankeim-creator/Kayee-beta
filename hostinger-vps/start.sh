#!/bin/bash

# Script de démarrage Kayee01

set -e

cd "$(dirname "$0")"

echo "=========================================="
echo "🚀 DÉMARRAGE KAYEE01"
echo "=========================================="
echo ""

# Vérifier que .env existe
if [ ! -f ".env" ]; then
    echo "❌ Fichier .env manquant !"
    echo "Copiez .env.example vers .env et configurez-le"
    exit 1
fi

# Charger les variables
source .env

echo "📦 Construction des images Docker..."
docker-compose build

echo ""
echo "🚀 Démarrage des conteneurs..."
docker-compose up -d

echo ""
echo "⏳ Attente du démarrage des services (30 secondes)..."
sleep 30

echo ""
echo "📊 Statut des conteneurs:"
docker-compose ps

echo ""
echo "=========================================="
echo "✅ KAYEE01 DÉMARRÉ !"
echo "=========================================="
echo ""
echo "📋 URLs d'accès:"
echo ""
if [ "$DOMAIN_NAME" != "your-domain.com" ]; then
    echo "Site principal: http://$DOMAIN_NAME"
    echo "Admin: http://$DOMAIN_NAME/admin/login"
    echo "API: http://$DOMAIN_NAME/api"
else
    IP=$(curl -s ifconfig.me)
    echo "Site principal: http://$IP"
    echo "Admin: http://$IP/admin/login"
    echo "API: http://$IP/api"
fi
echo ""
echo "📝 Voir les logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Arrêter:"
echo "   bash stop.sh"
echo ""
echo "=========================================="
