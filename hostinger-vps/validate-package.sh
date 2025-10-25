#!/bin/bash

# Script de validation du package VPS avant déploiement
# Ce script vérifie que tous les fichiers sont corrects

echo "=========================================="
echo "🔍 VALIDATION DU PACKAGE VPS KAYEE01"
echo "=========================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

# Vérifier qu'on est dans le bon dossier
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ Erreur: Ce script doit être exécuté depuis /app/hostinger-vps/${NC}"
    exit 1
fi

cd "$(dirname "$0")"

echo "📁 Vérification de la structure des fichiers..."
echo ""

# Fonction de vérification de fichier
check_file() {
    if [ -f "$1" ]; then
        echo -e "   ${GREEN}✅${NC} $1"
    else
        echo -e "   ${RED}❌${NC} $1 (MANQUANT)"
        ((ERRORS++))
    fi
}

# Fonction de vérification de permission exécutable
check_executable() {
    if [ -x "$1" ]; then
        echo -e "   ${GREEN}✅${NC} $1 (exécutable)"
    else
        echo -e "   ${YELLOW}⚠️${NC}  $1 (pas exécutable - correction possible avec chmod +x)"
        ((WARNINGS++))
    fi
}

# Vérification des fichiers Docker
echo "1. Fichiers Docker:"
check_file "docker-compose.yml"
check_file "Dockerfile.backend"
check_file "Dockerfile.frontend"
check_file "nginx.conf"
check_file "nginx-frontend.conf"
echo ""

# Vérification des scripts
echo "2. Scripts shell:"
check_file "install-vps.sh"
check_executable "install-vps.sh"
check_file "start.sh"
check_executable "start.sh"
check_file "stop.sh"
check_executable "stop.sh"
check_file "setup-ssl.sh"
check_executable "setup-ssl.sh"
check_file "check-status.sh"
check_executable "check-status.sh"
echo ""

# Vérification de la documentation
echo "3. Documentation:"
check_file "README.md"
check_file "QUICK_START.md"
check_file "CORRECTIONS.md"
check_file "DEPLOY_STATUS.md"
check_file "GUIDE_DEPLOIEMENT_VPS.md"
check_file ".env.example"
echo ""

# Vérification de la syntaxe des scripts
echo "4. Validation de la syntaxe bash:"
for script in *.sh; do
    if bash -n "$script" 2>/dev/null; then
        echo -e "   ${GREEN}✅${NC} $script (syntaxe correcte)"
    else
        echo -e "   ${RED}❌${NC} $script (ERREUR DE SYNTAXE)"
        ((ERRORS++))
    fi
done
echo ""

# Vérification de la syntaxe docker-compose
echo "5. Validation docker-compose.yml:"
if command -v docker-compose &> /dev/null; then
    if docker-compose config > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅${NC} Syntaxe docker-compose valide"
    else
        echo -e "   ${RED}❌${NC} Erreur de syntaxe docker-compose"
        ((ERRORS++))
    fi
else
    echo -e "   ${YELLOW}⚠️${NC}  docker-compose non installé (impossible de valider)"
    ((WARNINGS++))
fi
echo ""

# Vérification du fichier .env.example
echo "6. Validation .env.example:"
if grep -q "DOMAIN_NAME=" .env.example && \
   grep -q "MONGO_PASSWORD=" .env.example && \
   grep -q "JWT_SECRET_KEY=" .env.example && \
   grep -q "SMTP_USER=" .env.example; then
    echo -e "   ${GREEN}✅${NC} Toutes les variables essentielles présentes"
else
    echo -e "   ${RED}❌${NC} Variables manquantes dans .env.example"
    ((ERRORS++))
fi
echo ""

# Vérification des Dockerfiles
echo "7. Validation des Dockerfiles:"

# Backend
if grep -q "COPY backend/" Dockerfile.backend; then
    echo -e "   ${GREEN}✅${NC} Dockerfile.backend - chemins corrects"
else
    echo -e "   ${RED}❌${NC} Dockerfile.backend - chemins incorrects"
    ((ERRORS++))
fi

# Frontend
if grep -q "COPY frontend/" Dockerfile.frontend && \
   grep -q "COPY hostinger-vps/nginx-frontend.conf" Dockerfile.frontend; then
    echo -e "   ${GREEN}✅${NC} Dockerfile.frontend - chemins corrects"
else
    echo -e "   ${RED}❌${NC} Dockerfile.frontend - chemins incorrects"
    ((ERRORS++))
fi
echo ""

# Vérification des codes couleurs dans les scripts
echo "8. Validation des codes couleurs bash:"
if grep -q "GREEN='\\033\\[0;32m'" install-vps.sh && \
   grep -q "GREEN='\\033\\[0;32m'" check-status.sh; then
    echo -e "   ${GREEN}✅${NC} Codes couleurs corrects"
else
    echo -e "   ${RED}❌${NC} Codes couleurs incorrects (manque l'échappement)"
    ((ERRORS++))
fi
echo ""

# Vérification que les fichiers parent existent
echo "9. Vérification des dossiers parent:"
if [ -d "../backend" ]; then
    echo -e "   ${GREEN}✅${NC} ../backend existe"
    if [ -f "../backend/requirements.txt" ]; then
        echo -e "   ${GREEN}✅${NC} ../backend/requirements.txt existe"
    else
        echo -e "   ${RED}❌${NC} ../backend/requirements.txt manquant"
        ((ERRORS++))
    fi
else
    echo -e "   ${RED}❌${NC} ../backend n'existe pas"
    ((ERRORS++))
fi

if [ -d "../frontend" ]; then
    echo -e "   ${GREEN}✅${NC} ../frontend existe"
    if [ -f "../frontend/package.json" ]; then
        echo -e "   ${GREEN}✅${NC} ../frontend/package.json existe"
    else
        echo -e "   ${RED}❌${NC} ../frontend/package.json manquant"
        ((ERRORS++))
    fi
else
    echo -e "   ${RED}❌${NC} ../frontend n'existe pas"
    ((ERRORS++))
fi
echo ""

# Résumé
echo "=========================================="
echo "📊 RÉSULTAT DE LA VALIDATION"
echo "=========================================="
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}🎉 SUCCÈS COMPLET !${NC}"
    echo ""
    echo "✅ Tous les fichiers sont présents et corrects"
    echo "✅ Aucune erreur détectée"
    echo "✅ Le package est prêt pour le déploiement"
    echo ""
    echo "Prochaine étape: Pousser sur GitHub puis déployer sur VPS"
    echo "Consultez QUICK_START.md pour les instructions"
    EXIT_CODE=0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  VALIDATION RÉUSSIE AVEC AVERTISSEMENTS${NC}"
    echo ""
    echo "✅ Tous les fichiers sont présents"
    echo -e "⚠️  ${WARNINGS} avertissement(s) détecté(s)"
    echo ""
    echo "Les avertissements n'empêchent pas le déploiement,"
    echo "mais il est recommandé de les corriger."
    EXIT_CODE=0
else
    echo -e "${RED}❌ ÉCHEC DE LA VALIDATION${NC}"
    echo ""
    echo -e "${RED}${ERRORS} erreur(s) détectée(s)${NC}"
    echo -e "${YELLOW}${WARNINGS} avertissement(s)${NC}"
    echo ""
    echo "Corrigez les erreurs avant de déployer."
    echo "Consultez CORRECTIONS.md pour plus d'informations."
    EXIT_CODE=1
fi

echo ""
echo "=========================================="

exit $EXIT_CODE
