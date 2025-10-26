#!/bin/bash

echo "======================================"
echo "🚀 KAYEE01 - RENDER DEPLOYMENT SCRIPT"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Step 1: Initializing Git Repository${NC}"
cd /app
git init
git add .
git commit -m "Initial commit - Kayee01 ready for Render deployment"
echo -e "${GREEN}✅ Git repository initialized${NC}"
echo ""

echo -e "${BLUE}Step 2: Repository Information${NC}"
echo "================================================"
echo "Your repository is ready to be pushed to GitHub"
echo "================================================"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   - Go to: https://github.com/new"
echo "   - Name: kayee01-ecommerce"
echo "   - Type: Private (recommended)"
echo "   - Don't initialize with README"
echo ""
echo "2. Push your code (replace YOUR_USERNAME):"
echo "   git remote add origin https://github.com/YOUR_USERNAME/kayee01-ecommerce.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Deploy on Render:"
echo "   - Go to: https://dashboard.render.com"
echo "   - Click: New + → Blueprint"
echo "   - Connect your kayee01-ecommerce repository"
echo "   - Render will auto-detect render.yaml"
echo ""
echo "4. Add these environment variables in Render:"
echo "   MONGO_URL=mongodb+srv://user:pass@cluster.mongodb.net/kayee01_db"
echo "   SMTP_PASSWORD=your_gmail_app_password"
echo "   (Stripe/Plisio keys are optional for testing)"
echo ""
echo -e "${GREEN}✅ Deployment preparation complete!${NC}"
echo ""
echo "📖 Full guide: Read RENDER_DEPLOYMENT_GUIDE.md"
echo ""
