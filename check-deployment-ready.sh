#!/bin/bash

echo "=========================================="
echo "🧪 KAYEE01 - PRE-DEPLOYMENT CHECKLIST"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_count=0
pass_count=0

# Function to check
check() {
    ((check_count++))
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
        ((pass_count++))
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

echo "📦 Checking Files..."
echo ""

# Check render.yaml
[ -f "/app/render.yaml" ]
check $? "render.yaml exists"

# Check build script
[ -f "/app/build-backend.sh" ]
check $? "build-backend.sh exists"

# Check backend requirements
[ -f "/app/backend/requirements.txt" ]
check $? "backend/requirements.txt exists"

# Check frontend package.json
[ -f "/app/frontend/package.json" ]
check $? "frontend/package.json exists"

# Check .gitignore
[ -f "/app/.gitignore" ]
check $? ".gitignore exists"

# Check README
[ -f "/app/README.md" ]
check $? "README.md exists"

# Check deployment guides
[ -f "/app/RENDER_DEPLOYMENT_GUIDE.md" ]
check $? "RENDER_DEPLOYMENT_GUIDE.md exists"

[ -f "/app/QUICK_START_RENDER.md" ]
check $? "QUICK_START_RENDER.md exists"

echo ""
echo "🔍 Checking Backend..."
echo ""

# Check backend server
[ -f "/app/backend/server.py" ]
check $? "backend/server.py exists"

# Check email service
[ -f "/app/backend/email_service.py" ]
check $? "backend/email_service.py exists"

# Check payment services
[ -f "/app/backend/stripe_service.py" ]
check $? "backend/stripe_service.py exists"

[ -f "/app/backend/plisio_service.py" ]
check $? "backend/plisio_service.py exists"

echo ""
echo "🎨 Checking Frontend..."
echo ""

# Check frontend files
[ -f "/app/frontend/src/App.js" ]
check $? "frontend/src/App.js exists"

[ -f "/app/frontend/public/index.html" ]
check $? "frontend/public/index.html exists"

[ -f "/app/frontend/.env.production" ]
check $? "frontend/.env.production exists"

echo ""
echo "📊 Results:"
echo "=========================================="
echo -e "Total Checks: ${check_count}"
echo -e "Passed: ${GREEN}${pass_count}${NC}"
echo -e "Failed: ${RED}$((check_count - pass_count))${NC}"
echo ""

if [ $pass_count -eq $check_count ]; then
    echo -e "${GREEN}🎉 All checks passed! Ready for deployment!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Push to GitHub"
    echo "2. Connect to Render"
    echo "3. Deploy!"
    echo ""
    echo "Run: bash prepare-render-deployment.sh"
else
    echo -e "${RED}⚠️  Some checks failed. Please review.${NC}"
fi

echo ""
