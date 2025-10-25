#!/bin/bash

# Configuration SSL avec Let's Encrypt

set -e

if [ -z "$1" ]; then
    echo "Usage: bash setup-ssl.sh votre-domaine.com"
    exit 1
fi

DOMAIN=$1

echo "=========================================="
echo "🔒 CONFIGURATION SSL POUR $DOMAIN"
echo "=========================================="
echo ""

# Vérifier que le domaine pointe vers ce serveur
echo "🔍 Vérification DNS..."
SERVER_IP=$(curl -s ifconfig.me)
DOMAIN_IP=$(dig +short $DOMAIN | head -1)

if [ "$SERVER_IP" != "$DOMAIN_IP" ]; then
    echo "⚠️  ATTENTION: Le domaine ne pointe pas encore vers ce serveur"
    echo "IP du serveur: $SERVER_IP"
    echo "IP du domaine: $DOMAIN_IP"
    echo ""
    read -p "Voulez-vous continuer quand même ? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "📦 Obtention du certificat SSL..."

# Obtenir le certificat
docker-compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email kayicom509@gmail.com \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN \
    -d www.$DOMAIN

if [ $? -eq 0 ]; then
    echo "✅ Certificat SSL obtenu avec succès !"
    
    # Mettre à jour nginx.conf
    echo ""
    echo "⚙️  Mise à jour de la configuration Nginx..."
    
    # Décommenter la section HTTPS dans nginx.conf
    sed -i "s/# server {/server {/g" nginx.conf
    sed -i "s/#     /    /g" nginx.conf
    sed -i "s/your-domain.com/$DOMAIN/g" nginx.conf
    sed -i "s/# return 301/return 301/g" nginx.conf
    
    # Mettre à jour .env
    sed -i "s/DOMAIN_NAME=.*/DOMAIN_NAME=$DOMAIN/" .env
    
    echo "✅ Configuration mise à jour"
    
    # Redémarrer nginx
    echo ""
    echo "🔄 Redémarrage de Nginx..."
    docker-compose restart nginx
    
    echo ""
    echo "=========================================="
    echo "✅ SSL CONFIGURÉ AVEC SUCCÈS !"
    echo "=========================================="
    echo ""
    echo "Votre site est maintenant accessible en HTTPS:"
    echo "https://$DOMAIN"
    echo ""
    echo "Le certificat sera renouvelé automatiquement."
    echo "=========================================="
else
    echo "❌ Échec de l'obtention du certificat SSL"
    echo "Vérifiez que:"
    echo "1. Le domaine pointe vers ce serveur"
    echo "2. Les ports 80 et 443 sont ouverts"
    echo "3. Nginx est en cours d'exécution"
    exit 1
fi
