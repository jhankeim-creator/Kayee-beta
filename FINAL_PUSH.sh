#!/bin/bash

echo "=========================================="
echo "🚀 PUSH FINAL VERS GITHUB"
echo "=========================================="
echo ""

cd /app

# Vérifier le dossier uploads
echo "📁 Vérification dossier uploads..."
if git ls-files | grep -q "backend/uploads"; then
    echo "✅ Dossier uploads dans Git:"
    git ls-files backend/uploads/ | wc -l
    echo "   fichiers trouvés"
else
    echo "❌ Dossier uploads manquant!"
    exit 1
fi

echo ""
echo "📊 Fichiers dans uploads:"
git ls-files backend/uploads/
echo ""

# Vérifier les modifications en attente
echo "🔍 Vérification des modifications..."
if git status --short | grep -q .; then
    echo "⚠️ Modifications en attente:"
    git status --short
    echo ""
    echo "💾 Ajout et commit..."
    git add -A
    git commit -m "Final commit - Uploads directory and all Render configs ready"
else
    echo "✅ Aucune modification en attente"
fi

echo ""
echo "=========================================="
echo "✅ PRÊT À POUSSER"
echo "=========================================="
echo ""
echo "Remote configuré:"
git remote -v | grep origin | head -1
echo ""
echo "Dernier commit:"
git log --oneline -1
echo ""
echo "📋 COMMANDE À EXÉCUTER:"
echo ""
echo "   git push -u origin main"
echo ""
echo "Si demandé, utilisez votre Personal Access Token"
echo ""
echo "=========================================="
