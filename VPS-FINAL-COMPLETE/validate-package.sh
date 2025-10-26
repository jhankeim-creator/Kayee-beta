#!/bin/bash

# Package Validation Script
# Validates all files and configurations before deployment

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${GREEN}✅ $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

ERRORS=0
WARNINGS=0

check_file() {
    if [[ -f "$1" ]]; then
        log "File exists: $1"
    else
        error "Missing file: $1"
        ((ERRORS++))
    fi
}

check_directory() {
    if [[ -d "$1" ]]; then
        log "Directory exists: $1"
    else
        error "Missing directory: $1"
        ((ERRORS++))
    fi
}

check_executable() {
    if [[ -x "$1" ]]; then
        log "Executable: $1"
    else
        error "Not executable: $1"
        ((ERRORS++))
    fi
}

echo "=========================================="
echo "🔍 KAYEE01 PACKAGE VALIDATION"
echo "=========================================="
echo ""

# Check core files
info "Checking core deployment files..."
check_file "docker-compose.yml"
check_file "Dockerfile.backend"
check_file "Dockerfile.frontend"
check_file "nginx.conf"
check_file "nginx-frontend.conf"
check_file ".env.template"
check_file "README.md"

# Check scripts
info "Checking deployment scripts..."
check_file "DEPLOY.sh"
check_file "setup-ssl.sh"
check_file "backup-mongodb.sh"
check_file "monitor.sh"
check_file "update.sh"
check_file "validate-package.sh"

# Check script permissions
info "Checking script permissions..."
check_executable "DEPLOY.sh"
check_executable "setup-ssl.sh"
check_executable "backup-mongodb.sh"
check_executable "monitor.sh"
check_executable "update.sh"
check_executable "validate-package.sh"

# Check application directories
info "Checking application directories..."
check_directory "backend"
check_directory "frontend"

# Check backend files
info "Checking backend files..."
check_file "backend/server.py"
check_file "backend/requirements.txt"
check_file "backend/models.py"

# Check frontend files
info "Checking frontend files..."
check_file "frontend/package.json"
check_file "frontend/src/App.js"
check_directory "frontend/src"
check_directory "frontend/public"

# Validate Docker Compose syntax
info "Validating Docker Compose syntax..."
if command -v docker-compose >/dev/null 2>&1; then
    if docker-compose config >/dev/null 2>&1; then
        log "docker-compose.yml syntax is valid"
    else
        error "docker-compose.yml syntax error"
        ((ERRORS++))
    fi
else
    warning "Docker Compose not installed, skipping syntax check"
    ((WARNINGS++))
fi

# Validate Nginx configuration syntax
info "Validating Nginx configuration..."
if command -v nginx >/dev/null 2>&1; then
    if nginx -t -c "$(pwd)/nginx.conf" >/dev/null 2>&1; then
        log "nginx.conf syntax is valid"
    else
        error "nginx.conf syntax error"
        ((ERRORS++))
    fi
else
    warning "Nginx not installed, skipping syntax check"
    ((WARNINGS++))
fi

# Check environment template
info "Checking environment template..."
if [[ -f ".env.template" ]]; then
    if grep -q "DOMAIN_NAME=" .env.template && grep -q "MONGO_PASSWORD=" .env.template; then
        log "Environment template contains required variables"
    else
        error "Environment template missing required variables"
        ((ERRORS++))
    fi
fi

# Check for hardcoded URLs in backend
info "Checking for hardcoded URLs in backend..."
if grep -r "preview\.emergentagent\.com" backend/ >/dev/null 2>&1; then
    error "Found hardcoded preview URLs in backend"
    ((ERRORS++))
else
    log "No hardcoded preview URLs found in backend"
fi

# Check for hardcoded URLs in frontend
info "Checking for hardcoded URLs in frontend..."
if grep -r "preview\.emergentagent\.com" frontend/src/ >/dev/null 2>&1; then
    error "Found hardcoded preview URLs in frontend"
    ((ERRORS++))
else
    log "No hardcoded preview URLs found in frontend"
fi

# Check backend requirements
info "Checking backend requirements..."
if [[ -f "backend/requirements.txt" ]]; then
    REQUIRED_PACKAGES=("fastapi" "uvicorn" "motor" "pymongo" "python-dotenv")
    for package in "${REQUIRED_PACKAGES[@]}"; do
        if grep -q "$package" backend/requirements.txt; then
            log "Required package found: $package"
        else
            error "Missing required package: $package"
            ((ERRORS++))
        fi
    done
fi

# Check frontend dependencies
info "Checking frontend dependencies..."
if [[ -f "frontend/package.json" ]]; then
    REQUIRED_DEPS=("react" "axios")
    for dep in "${REQUIRED_DEPS[@]}"; do
        if grep -q "\"$dep\"" frontend/package.json; then
            log "Required dependency found: $dep"
        else
            error "Missing required dependency: $dep"
            ((ERRORS++))
        fi
    done
fi

# Check file sizes (warn if too large)
info "Checking file sizes..."
if [[ -d "backend" ]]; then
    BACKEND_SIZE=$(du -sm backend | cut -f1)
    if [[ $BACKEND_SIZE -gt 100 ]]; then
        warning "Backend directory is large: ${BACKEND_SIZE}MB"
        ((WARNINGS++))
    fi
fi

if [[ -d "frontend" ]]; then
    FRONTEND_SIZE=$(du -sm frontend | cut -f1)
    if [[ $FRONTEND_SIZE -gt 500 ]]; then
        warning "Frontend directory is large: ${FRONTEND_SIZE}MB"
        ((WARNINGS++))
    fi
fi

# Summary
echo ""
echo "=========================================="
echo "📊 VALIDATION SUMMARY"
echo "=========================================="

if [[ $ERRORS -eq 0 ]]; then
    log "✅ VALIDATION PASSED"
    echo ""
    log "Package is ready for deployment!"
    if [[ $WARNINGS -gt 0 ]]; then
        warning "$WARNINGS warnings found (non-critical)"
    fi
else
    error "❌ VALIDATION FAILED"
    echo ""
    error "$ERRORS critical errors found"
    if [[ $WARNINGS -gt 0 ]]; then
        warning "$WARNINGS warnings found"
    fi
    echo ""
    error "Please fix the errors before deployment"
    exit 1
fi

echo ""
info "Next steps:"
echo "1. Push code to GitHub"
echo "2. Run DEPLOY.sh on your VPS"
echo "3. Configure SSL with setup-ssl.sh"
echo ""
echo "=========================================="
