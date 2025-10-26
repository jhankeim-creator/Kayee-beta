#!/bin/bash
echo "=========================================="
echo "🚀 PUSH VERS GITHUB - FICHIERS MANQUANTS"
echo "=========================================="
echo ""

# Vérifier si remote existe
if ! git remote | grep -q origin; then
    echo "❌ Pas de remote 'origin' configuré"
    echo ""
    echo "Ajoutez d'abord le remote avec:"
    echo "git remote add origin https://github.com/kayee_beta/kayee01-ecommerce.git"
    exit 1
fi

echo "✅ Remote configuré:"
git remote -v | grep origin | head -1
echo ""

# Ajouter tous les fichiers
echo "📦 Ajout des fichiers modifiés..."
git add -A

# Vérifier ce qui va être commité
echo ""
echo "📋 Fichiers qui seront ajoutés/modifiés:"
git diff --staged --name-status | head -20
echo ""

# Commit
echo "💾 Création du commit..."
git commit -m "Add Render deployment files and fix uploads directory issue"

# Afficher le statut
echo ""
echo "📊 Statut:"
git status

echo ""
echo "=========================================="
echo "✅ PRÊT À POUSSER"
echo "=========================================="
echo ""
echo "Pour pousser vers GitHub, exécutez:"
echo "git push origin main"
echo ""
echo "Ou si première fois:"
echo "git push -u origin main"
echo ""
