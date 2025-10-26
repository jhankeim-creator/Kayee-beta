#!/bin/bash
set -e

echo "=== Kayee01 VPS Deployment ==="

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Fichye .env pa la!"
    echo "Kopi .env.example an .env epi modifye li:"
    echo "cp .env.example .env"
    exit 1
fi

echo "✓ Fichye .env jwenn"

# Stop existing containers
echo "Stopping existing containers..."
docker-compose down 2>/dev/null || true

# Build images
echo "Building Docker images..."
docker-compose build --no-cache

# Start containers
echo "Starting containers..."
docker-compose up -d

# Wait for services
echo "Waiting for services to be ready (30 seconds)..."
sleep 30

# Check status
echo ""
echo "=== Container Status ==="
docker-compose ps

echo ""
echo "=== Testing Site ==="
curl -I http://localhost 2>&1 | head -5

echo ""
echo "✅ Deplwaman fini!"
echo "Site ou a disponib sou: http://$(hostname -I | awk '{print $1}')"
echo ""
echo "Pou konfigure SSL, kouri: ./setup-ssl.sh"
