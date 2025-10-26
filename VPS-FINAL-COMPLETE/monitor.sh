#!/bin/bash

# System Monitoring Script for Kayee01
# Check system health and service status

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

echo "=========================================="
echo "🔍 KAYEE01 SYSTEM MONITOR"
echo "=========================================="
echo ""

# System Information
info "System Information:"
echo "Date: $(date)"
echo "Uptime: $(uptime -p)"
echo "Load: $(uptime | awk -F'load average:' '{print $2}')"
echo ""

# Disk Usage
info "Disk Usage:"
df -h / | tail -1 | awk '{print "Root: " $3 "/" $2 " (" $5 " used)"}'
if [[ -d "/opt/kayee01" ]]; then
    du -sh /opt/kayee01 | awk '{print "Application: " $1}'
fi
echo ""

# Memory Usage
info "Memory Usage:"
free -h | grep Mem | awk '{print "Memory: " $3 "/" $2 " (" int($3/$2*100) "% used)"}'
echo ""

# Docker Services Status
info "Docker Services:"
if command -v docker-compose >/dev/null 2>&1; then
    if [[ -f "docker-compose.yml" ]]; then
        SERVICES=$(docker-compose ps --services)
        for service in $SERVICES; do
            STATUS=$(docker-compose ps $service | tail -1 | awk '{print $4}')
            if [[ "$STATUS" == "Up" ]]; then
                log "$service: Running"
            else
                error "$service: $STATUS"
            fi
        done
    else
        warning "docker-compose.yml not found"
    fi
else
    error "Docker Compose not installed"
fi
echo ""

# Network Connectivity
info "Network Tests:"
if curl -f http://localhost >/dev/null 2>&1; then
    log "HTTP (port 80): Accessible"
else
    error "HTTP (port 80): Not accessible"
fi

if curl -f http://localhost:8001/api/products >/dev/null 2>&1; then
    log "Backend API: Responding"
else
    error "Backend API: Not responding"
fi

if curl -f http://localhost:3000 >/dev/null 2>&1; then
    log "Frontend: Responding"
else
    error "Frontend: Not responding"
fi
echo ""

# SSL Certificate Status (if domain configured)
if [[ -f ".env" ]]; then
    source .env
    if [[ -n "$DOMAIN_NAME" ]]; then
        info "SSL Certificate Status for $DOMAIN_NAME:"
        if command -v openssl >/dev/null 2>&1; then
            CERT_INFO=$(echo | openssl s_client -servername $DOMAIN_NAME -connect $DOMAIN_NAME:443 2>/dev/null | openssl x509 -noout -dates 2>/dev/null)
            if [[ $? -eq 0 ]]; then
                echo "$CERT_INFO"
                
                # Check expiration
                EXPIRY=$(echo "$CERT_INFO" | grep "notAfter" | cut -d= -f2)
                EXPIRY_TIMESTAMP=$(date -d "$EXPIRY" +%s 2>/dev/null)
                CURRENT_TIMESTAMP=$(date +%s)
                DAYS_LEFT=$(( (EXPIRY_TIMESTAMP - CURRENT_TIMESTAMP) / 86400 ))
                
                if [[ $DAYS_LEFT -gt 30 ]]; then
                    log "Certificate expires in $DAYS_LEFT days"
                elif [[ $DAYS_LEFT -gt 7 ]]; then
                    warning "Certificate expires in $DAYS_LEFT days"
                else
                    error "Certificate expires in $DAYS_LEFT days - RENEWAL NEEDED"
                fi
            else
                error "Could not retrieve SSL certificate information"
            fi
        fi
    fi
fi
echo ""

# Recent Logs (last 10 lines)
info "Recent Application Logs:"
if [[ -f "docker-compose.yml" ]]; then
    echo "Backend logs:"
    docker-compose logs --tail=5 backend 2>/dev/null | tail -5 || echo "No backend logs available"
    echo ""
    echo "Nginx logs:"
    docker-compose logs --tail=5 nginx 2>/dev/null | tail -5 || echo "No nginx logs available"
fi
echo ""

# Resource Usage by Container
info "Container Resource Usage:"
if command -v docker >/dev/null 2>&1; then
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | head -10
fi

echo ""
echo "=========================================="
echo "Monitor completed at $(date)"
echo "=========================================="
