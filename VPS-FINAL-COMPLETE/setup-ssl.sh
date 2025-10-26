#!/bin/bash

# ========================================
# SSL SETUP SCRIPT FOR KAYEE01
# Automated SSL certificate setup with Let's Encrypt
# ========================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

if [ -z "$1" ]; then
    error "Usage: ./setup-ssl.sh your-domain.com"
    exit 1
fi

DOMAIN=$1

echo "=========================================="
echo "🔒 SSL SETUP FOR $DOMAIN"
echo "=========================================="
echo ""

# Verify domain points to this server
log "Verifying DNS configuration..."
SERVER_IP=$(curl -s ifconfig.me)
DOMAIN_IP=$(dig +short $DOMAIN | head -1)

echo "Server IP: $SERVER_IP"
echo "Domain IP: $DOMAIN_IP"

if [ "$SERVER_IP" != "$DOMAIN_IP" ]; then
    warning "Domain does not point to this server yet"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if containers are running
log "Checking if services are running..."
if ! docker-compose ps | grep -q "Up"; then
    error "Docker services are not running. Please start them first with: docker-compose up -d"
    exit 1
fi

# Test HTTP access
log "Testing HTTP access..."
if ! curl -f http://localhost/.well-known/acme-challenge/ >/dev/null 2>&1; then
    info "Setting up HTTP access for certificate validation..."
fi

# Obtain SSL certificate
log "Obtaining SSL certificate for $DOMAIN and www.$DOMAIN..."

docker-compose run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email kayicom509@gmail.com \
    --agree-tos \
    --no-eff-email \
    --force-renewal \
    -d $DOMAIN \
    -d www.$DOMAIN

if [ $? -eq 0 ]; then
    log "✅ SSL certificate obtained successfully!"
    
    # Update nginx configuration
    log "Updating Nginx configuration..."
    
    # Create backup of current config
    cp nginx.conf nginx.conf.backup
    
    # Enable HTTPS section and update domain
    sed -i 's/# server {/server {/g' nginx.conf
    sed -i 's/#     /    /g' nginx.conf
    sed -i "s/DOMAIN_PLACEHOLDER/$DOMAIN/g" nginx.conf
    
    # Enable HTTP to HTTPS redirect
    sed -i 's/# return 301/return 301/g' nginx.conf
    
    # Update .env file
    sed -i "s/DOMAIN_NAME=.*/DOMAIN_NAME=$DOMAIN/" .env
    
    log "✅ Nginx configuration updated"
    
    # Test nginx configuration
    log "Testing Nginx configuration..."
    if docker-compose exec nginx nginx -t; then
        log "✅ Nginx configuration is valid"
        
        # Reload nginx
        log "Reloading Nginx..."
        docker-compose restart nginx
        
        # Wait for nginx to restart
        sleep 5
        
        # Test HTTPS access
        log "Testing HTTPS access..."
        if curl -f https://$DOMAIN >/dev/null 2>&1; then
            log "✅ HTTPS is working correctly"
        else
            warning "⚠️ HTTPS test failed, but certificate was installed"
        fi
        
        echo ""
        echo "=========================================="
        echo "✅ SSL SETUP COMPLETED SUCCESSFULLY!"
        echo "=========================================="
        echo ""
        log "Your site is now accessible at:"
        echo "• https://$DOMAIN"
        echo "• https://www.$DOMAIN"
        echo ""
        log "HTTP traffic will automatically redirect to HTTPS"
        echo ""
        log "Certificate will auto-renew every 12 hours"
        echo "=========================================="
        
    else
        error "Nginx configuration test failed"
        log "Restoring backup configuration..."
        cp nginx.conf.backup nginx.conf
        docker-compose restart nginx
        exit 1
    fi
    
else
    error "Failed to obtain SSL certificate"
    echo ""
    error "Common issues:"
    echo "1. Domain does not point to this server"
    echo "2. Ports 80 and 443 are not accessible"
    echo "3. Another web server is running"
    echo "4. Firewall is blocking connections"
    echo ""
    error "Please check the following:"
    echo "• DNS: dig +short $DOMAIN"
    echo "• Firewall: sudo ufw status"
    echo "• Services: docker-compose ps"
    echo "• Logs: docker-compose logs nginx"
    exit 1
fi

# Create SSL renewal check script
cat > check-ssl-renewal.sh << 'EOL'
#!/bin/bash
# Check SSL certificate expiration
DOMAIN=$1
if [ -z "$DOMAIN" ]; then
    echo "Usage: ./check-ssl-renewal.sh domain.com"
    exit 1
fi

echo "Checking SSL certificate for $DOMAIN..."
echo | openssl s_client -servername $DOMAIN -connect $DOMAIN:443 2>/dev/null | openssl x509 -noout -dates
EOL

chmod +x check-ssl-renewal.sh

log "SSL renewal check script created: ./check-ssl-renewal.sh"
echo ""
log "SSL setup completed successfully! 🔒✅"
