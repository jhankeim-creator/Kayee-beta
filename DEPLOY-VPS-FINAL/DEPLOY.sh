#!/bin/bash
set -e

echo "========================================"
echo "  KAYEE01 DEPLOYMENT FINAL"
echo "========================================"
echo ""

# Generate JWT if needed
if [ ! -f .env ]; then
    echo "Creating .env file..."
    JWT_KEY=$(openssl rand -base64 32)
    cp .env.template .env
    sed -i "s|JWT_SECRET=WILL_BE_GENERATED|JWT_SECRET=$JWT_KEY|" .env
    echo "✓ .env created with random JWT_SECRET"
else
    echo "✓ .env already exists"
fi

echo ""
echo "Stopping old containers..."
docker-compose down 2>/dev/null || true

echo ""
echo "Building images (this takes 3-5 minutes)..."
docker-compose build --no-cache

echo ""
echo "Starting containers..."
docker-compose up -d

echo ""
echo "Waiting 30 seconds for services to start..."
sleep 30

echo ""
echo "========================================"
echo "  DEPLOYMENT STATUS"
echo "========================================"
docker-compose ps

echo ""
echo "Testing site..."
curl -I http://localhost 2>&1 | head -5

echo ""
echo "========================================"
echo "✓ DEPLOYMENT COMPLETE!"
echo "========================================"
echo ""
echo "Your site: http://$(hostname -I | awk '{print $1}')"
echo ""
echo "To setup SSL: ./setup-ssl.sh"
echo ""