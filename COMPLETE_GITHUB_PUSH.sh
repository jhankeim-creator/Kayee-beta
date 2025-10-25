#!/bin/bash
echo "=========================================="
echo "🚀 CONFIGURATION COMPLÈTE GITHUB"
echo "=========================================="
echo ""

# Configurer le remote
echo "📡 Configuration du remote GitHub..."
git remote add origin https://github.com/kayee_beta/kayee01-ecommerce.git 2>/dev/null || echo "Remote déjà configuré"

# Vérifier
echo "✅ Remote configuré:"
git remote -v | grep origin | head -1
echo ""

# Ajouter tous les fichiers
echo "📦 Ajout de tous les fichiers..."
git add -A

# Commit si nécessaire
if ! git diff --staged --quiet; then
    echo "💾 Création du commit..."
    git commit -m "Add Render deployment config and fix uploads directory" || echo "Commit déjà fait"
else
    echo "✅ Aucun changement à commiter"
fi

echo ""
echo "=========================================="
echo "✅ TOUT EST PRÊT"
echo "=========================================="
echo ""
echo "📋 COMMANDES À EXÉCUTER:"
echo ""
echo "cd /app"
echo "git push -u origin main"
echo ""
echo "Si demandé, utilisez votre Personal Access Token GitHub"
echo "=========================================="
