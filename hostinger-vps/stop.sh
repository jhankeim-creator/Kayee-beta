#!/bin/bash

# Script d'arrêt Kayee01

cd "$(dirname "$0")"

echo "=========================================="
echo "🛑 ARRÊT KAYEE01"
echo "=========================================="
echo ""

docker-compose down

echo ""
echo "✅ Kayee01 arrêté"
echo ""
echo "Pour redémarrer: bash start.sh"
echo "=========================================="
