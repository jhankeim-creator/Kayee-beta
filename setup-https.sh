#!/bin/bash

###############################################################################
# KAYEE01 E-COMMERCE - HTTPS SETUP SCRIPT FOR HOSTINGER VPS
# This script will configure NGINX with SSL/TLS using Let's Encrypt (Certbot)
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration variables
DOMAIN="yourdomain.com"  # CHANGE THIS to your actual domain
WWW_DOMAIN="www.yourdomain.com"
EMAIL="admin@yourdomain.com"  # CHANGE THIS to your email
APP_DIR="/app"
NGINX_CONF="/etc/nginx/sites-available/kayee01"
NGINX_ENABLED="/etc/nginx/sites-enabled/kayee01"

###############################################################################
# Functions
###############################################################################

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root (use sudo)"
        exit 1
    fi
}

###############################################################################
# Main Script
###############################################################################

print_header "KAYEE01 E-COMMERCE - HTTPS CONFIGURATION"

# Check if running as root
check_root

# Prompt for domain if not changed
if [[ "$DOMAIN" == "yourdomain.com" ]]; then
    print_warning "Please enter your domain name (e.g., kayee01.com):"
    read -r DOMAIN
    WWW_DOMAIN="www.$DOMAIN"
fi

# Prompt for email if not changed
if [[ "$EMAIL" == "admin@yourdomain.com" ]]; then
    print_warning "Please enter your email address for Let's Encrypt:"
    read -r EMAIL
fi

print_success "Domain: $DOMAIN"
print_success "WWW Domain: $WWW_DOMAIN"
print_success "Email: $EMAIL"

# Confirm before proceeding
read -p "Continue with these settings? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_error "Installation cancelled"
    exit 1
fi

###############################################################################
# Step 1: Update system and install dependencies
###############################################################################

print_header "Step 1: Installing Dependencies"

apt-get update
apt-get install -y nginx certbot python3-certbot-nginx

print_success "Dependencies installed"

###############################################################################
# Step 2: Build React Frontend
###############################################################################

print_header "Step 2: Building React Frontend"

cd $APP_DIR/frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    print_warning "Installing frontend dependencies..."
    yarn install
fi

# Build production version
print_warning "Building production build..."
yarn build

print_success "Frontend built successfully"

###############################################################################
# Step 3: Stop any existing services
###############################################################################

print_header "Step 3: Preparing Services"

# Stop supervisor services temporarily
supervisorctl stop frontend 2>/dev/null || true
supervisorctl stop nginx-code-proxy 2>/dev/null || true

print_success "Services stopped"

###############################################################################
# Step 4: Configure NGINX
###############################################################################

print_header "Step 4: Configuring NGINX"

# Create NGINX configuration
cat > $NGINX_CONF << EOF
# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN $WWW_DOMAIN;
    
    # Allow Certbot ACME challenge
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        allow all;
    }
    
    # Redirect to HTTPS
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name $DOMAIN $WWW_DOMAIN;
    
    # SSL Certificate paths
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Gzip Compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;
    
    client_max_body_size 50M;
    
    # Frontend
    root $APP_DIR/frontend/build;
    index index.html;
    
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
    
    # Block sensitive files
    location ~ /\. {
        deny all;
    }
    
    location ~ /\.env {
        deny all;
    }
    
    access_log /var/log/nginx/kayee01_access.log;
    error_log /var/log/nginx/kayee01_error.log;
}
EOF

# Enable site
ln -sf $NGINX_CONF $NGINX_ENABLED

# Remove default NGINX config
rm -f /etc/nginx/sites-enabled/default

print_success "NGINX configured"

###############################################################################
# Step 5: Create directory for Certbot challenges
###############################################################################

print_header "Step 5: Preparing Certbot"

mkdir -p /var/www/certbot
chown -R www-data:www-data /var/www/certbot

print_success "Certbot directory created"

###############################################################################
# Step 6: Test NGINX configuration
###############################################################################

print_header "Step 6: Testing NGINX Configuration"

nginx -t

if [ $? -eq 0 ]; then
    print_success "NGINX configuration is valid"
else
    print_error "NGINX configuration has errors"
    exit 1
fi

###############################################################################
# Step 7: Reload NGINX
###############################################################################

print_header "Step 7: Reloading NGINX"

systemctl reload nginx
systemctl enable nginx

print_success "NGINX reloaded"

###############################################################################
# Step 8: Obtain SSL Certificate
###############################################################################

print_header "Step 8: Obtaining SSL Certificate"

print_warning "Obtaining SSL certificate from Let's Encrypt..."

certbot certonly \
    --nginx \
    --non-interactive \
    --agree-tos \
    --email $EMAIL \
    -d $DOMAIN \
    -d $WWW_DOMAIN

if [ $? -eq 0 ]; then
    print_success "SSL certificate obtained successfully!"
else
    print_error "Failed to obtain SSL certificate"
    print_warning "Make sure:"
    print_warning "1. Your domain DNS points to this server's IP"
    print_warning "2. Port 80 and 443 are open in firewall"
    print_warning "3. No other service is using port 80/443"
    exit 1
fi

###############################################################################
# Step 9: Setup Auto-renewal
###############################################################################

print_header "Step 9: Setting up Auto-renewal"

# Test renewal
certbot renew --dry-run

if [ $? -eq 0 ]; then
    print_success "Auto-renewal configured successfully"
else
    print_warning "Auto-renewal test failed, but certificate is installed"
fi

###############################################################################
# Step 10: Reload NGINX with SSL
###############################################################################

print_header "Step 10: Final NGINX Reload"

nginx -t && systemctl reload nginx

print_success "NGINX reloaded with SSL"

###############################################################################
# Step 11: Restart Backend
###############################################################################

print_header "Step 11: Restarting Backend"

supervisorctl restart backend

print_success "Backend restarted"

###############################################################################
# Completion
###############################################################################

print_header "HTTPS SETUP COMPLETED SUCCESSFULLY!"

echo -e "${GREEN}"
echo "=========================================="
echo "  HTTPS is now configured!"
echo "=========================================="
echo -e "${NC}"
echo ""
echo -e "${GREEN}Your site is now accessible at:${NC}"
echo -e "${BLUE}  https://$DOMAIN${NC}"
echo -e "${BLUE}  https://$WWW_DOMAIN${NC}"
echo ""
echo -e "${GREEN}Certificate Details:${NC}"
echo -e "  Location: /etc/letsencrypt/live/$DOMAIN/"
echo -e "  Expires: ~90 days (auto-renews)"
echo ""
echo -e "${YELLOW}Important Notes:${NC}"
echo "1. HTTP traffic is automatically redirected to HTTPS"
echo "2. Certificate will auto-renew via cron job"
echo "3. Check certificate status: certbot certificates"
echo "4. Manual renewal: certbot renew"
echo "5. NGINX config: $NGINX_CONF"
echo ""
echo -e "${GREEN}Next Steps:${NC}"
echo "1. Test your site: https://$DOMAIN"
echo "2. Check SSL rating: https://www.ssllabs.com/ssltest/"
echo "3. Update frontend .env REACT_APP_BACKEND_URL to https://$DOMAIN"
echo ""
print_success "Setup complete!"
