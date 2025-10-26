#!/bin/bash

# Update Script for Kayee01
# Safely update the application with zero downtime

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

echo "=========================================="
echo "🔄 KAYEE01 UPDATE SCRIPT"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [[ ! -f "docker-compose.yml" ]]; then
    error "docker-compose.yml not found. Please run this script from the deployment directory."
    exit 1
fi

# Create backup before update
log "Creating backup before update..."
if [[ -f "backup-mongodb.sh" ]]; then
    ./backup-mongodb.sh
    log "Backup completed"
else
    warning "Backup script not found, skipping backup"
fi

# Pull latest changes from Git
log "Pulling latest changes from Git..."
if git pull origin main; then
    log "Git pull successful"
else
    error "Git pull failed. Please resolve conflicts manually."
    exit 1
fi

# Check if there are any changes to Docker files
DOCKER_CHANGED=false
if git diff HEAD~1 --name-only | grep -E "(Dockerfile|docker-compose\.yml|requirements\.txt|package\.json)" >/dev/null; then
    DOCKER_CHANGED=true
    log "Docker-related files changed, will rebuild images"
fi

# Update Docker images
if [[ "$DOCKER_CHANGED" == true ]]; then
    log "Rebuilding Docker images..."
    docker-compose build --no-cache
else
    log "Pulling latest base images..."
    docker-compose pull
fi

# Rolling update with health checks
log "Performing rolling update..."

# Update backend first
log "Updating backend..."
docker-compose up -d --no-deps backend

# Wait for backend to be healthy
log "Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -f http://localhost:8001/api/products >/dev/null 2>&1; then
        log "Backend is healthy"
        break
    fi
    if [[ $i -eq 30 ]]; then
        error "Backend failed to start properly"
        exit 1
    fi
    sleep 2
done

# Update frontend
log "Updating frontend..."
docker-compose up -d --no-deps frontend

# Wait for frontend to be healthy
log "Waiting for frontend to be ready..."
for i in {1..30}; do
    if curl -f http://localhost:3000 >/dev/null 2>&1; then
        log "Frontend is healthy"
        break
    fi
    if [[ $i -eq 30 ]]; then
        error "Frontend failed to start properly"
        exit 1
    fi
    sleep 2
done

# Update nginx (if config changed)
if git diff HEAD~1 --name-only | grep "nginx.conf" >/dev/null; then
    log "Updating Nginx configuration..."
    docker-compose up -d --no-deps nginx
    sleep 5
fi

# Final health check
log "Performing final health checks..."
if curl -f http://localhost >/dev/null 2>&1; then
    log "✅ Site is accessible"
else
    error "❌ Site is not accessible"
    exit 1
fi

# Clean up old Docker images
log "Cleaning up old Docker images..."
docker image prune -f

# Show final status
log "Update completed successfully!"
echo ""
info "Service Status:"
docker-compose ps

echo ""
log "Update completed at $(date)"
echo "=========================================="
