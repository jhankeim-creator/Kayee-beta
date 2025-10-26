#!/bin/bash
set -e

echo "SSL Setup for Kayee01"
echo ""

source .env

if [ -z "$DOMAIN_NAME" ]; then
    echo "ERROR: DOMAIN_NAME not found in .env"
    exit 1
fi

echo "Domain: $DOMAIN_NAME"
echo ""
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
    echo ""
    echo "✓ SSL certificate obtained!"
    echo "Now update nginx.conf to enable HTTPS"
else
    echo ""
    echo "✗ SSL setup failed"
    exit 1
fi