#!/bin/bash
set -e

echo "=== SSL Setup pou Kayee01 ==="

# Load domain from .env
source .env

if [ -z "$DOMAIN_NAME" ]; then
    echo "❌ DOMAIN_NAME pa defini nan .env!"
    exit 1
fi

echo "✓ Domain: $DOMAIN_NAME"

# Request certificate
echo "Requesting SSL certificate..."
docker run -it --rm \
  -v $(pwd)/ssl:/etc/letsencrypt \
  -v $(pwd)/certbot_data:/var/www/certbot \
  certbot/certbot certonly --webroot \
  -w /var/www/certbot \
  -d $DOMAIN_NAME \
  -d www.$DOMAIN_NAME \
  --email kayicom509@gmail.com \
  --agree-tos \
  --no-eff-email

if [ $? -eq 0 ]; then
    echo "✅ SSL certificate obtained!"
    echo "Now updating nginx config for HTTPS..."
    # Here you would update nginx.conf to add HTTPS server block
    echo "Please update nginx.conf manually to enable HTTPS"
else
    echo "❌ SSL setup failed!"
    exit 1
fi
