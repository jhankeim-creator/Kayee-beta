#!/bin/bash
set -e

echo "=== Kayee01 VPS Deployment FINAL ==="

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Fichye .env pa la!"
    echo "Kopi .env-COMPLETE an .env epi modifye JWT_SECRET:"
    echo "cp .env-COMPLETE .env"
    echo "Apre sa, kouri: ./DEPLOY-FINAL.sh"
    exit 1
fi

echo "✓ Fichye .env jwenn"

# Generate JWT if needed
if grep -q "your-secret-key-change-in-production" .env; then
    echo "Generating random JWT_SECRET..."
    JWT_KEY=$(openssl rand -base64 32)
    sed -i "s|JWT_SECRET=your-secret-key-change-in-production|JWT_SECRET=$JWT_KEY|" .env
    echo "✓ JWT_SECRET generated"
fi

# Stop existing containers
echo "Stopping existing containers..."
docker-compose -f docker-compose-FINAL.yml down 2>/dev/null || true

# Build images
echo "Building Docker images (this will take 3-5 minutes)..."
docker-compose -f docker-compose-FINAL.yml build --no-cache

# Start containers
echo "Starting containers..."
docker-compose -f docker-compose-FINAL.yml up -d

# Wait for services
echo "Waiting for services to be healthy (40 seconds)..."
sleep 40

# Check status
echo ""
echo "=== Container Status ==="
docker-compose -f docker-compose-FINAL.yml ps

echo ""
echo "=== Testing Site ==="
curl -I http://localhost 2>&1 | head -10

echo ""
echo "✅ Deplwaman fini!"
echo "Site ou a disponib sou: http://$(hostname -I | awk '{print $1}')"
echo ""
echo "Pou konfigure SSL, kouri: ./setup-ssl.sh"
