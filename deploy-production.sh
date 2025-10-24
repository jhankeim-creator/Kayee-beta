#!/bin/bash

################################################################################
# KAYEE01 E-COMMERCE - PRODUCTION DEPLOYMENT WITH HTTPS
# Complete production setup for Hostinger VPS
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

################################################################################
# CONFIGURATION - EDIT THESE VALUES
################################################################################

# Domain configuration
DOMAIN="yourdomain.com"
WWW_DOMAIN="www.yourdomain.com"
EMAIL="admin@yourdomain.com"

# Paths
APP_DIR="/var/www/kayee01"
BACKEND_PORT="8001"

# Database
DB_NAME="kayee01_db"

################################################################################
# Functions
################################################################################

print_header() {
    echo -e "\n${BLUE}================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================${NC}\n"
}

print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }

check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root"
        exit 1
    fi
}

################################################################################
# MAIN DEPLOYMENT
################################################################################

print_header "KAYEE01 E-COMMERCE - PRODUCTION DEPLOYMENT"

check_root

# Prompt for configuration
if [[ "$DOMAIN" == "yourdomain.com" ]]; then
    echo -e "${YELLOW}Enter your domain name (e.g., kayee01.com):${NC}"
    read -r DOMAIN
    WWW_DOMAIN="www.$DOMAIN"
fi

if [[ "$EMAIL" == "admin@yourdomain.com" ]]; then
    echo -e "${YELLOW}Enter your email for SSL certificate:${NC}"
    read -r EMAIL
fi

print_success "Domain: $DOMAIN"
print_success "Email: $EMAIL"

read -p "Continue with deployment? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

################################################################################
# STEP 1: System Update & Dependencies
################################################################################

print_header "Step 1: Installing System Dependencies"

apt-get update
apt-get upgrade -y
apt-get install -y \
    nginx \
    certbot \
    python3-certbot-nginx \
    python3-pip \
    python3-venv \
    mongodb \
    supervisor \
    git \
    curl \
    wget

# Install Node.js and Yarn
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt-get install -y nodejs
npm install -g yarn

print_success "Dependencies installed"

################################################################################
# STEP 2: Create Application Directory
################################################################################

print_header "Step 2: Setting Up Application Directory"

mkdir -p $APP_DIR
cd $APP_DIR

print_success "Application directory created"

################################################################################
# STEP 3: Clone/Copy Application Files
################################################################################

print_header "Step 3: Application Files"

# If files already exist, skip
if [ ! -d "$APP_DIR/backend" ]; then
    print_warning "Copy your application files to $APP_DIR"
    print_warning "Expected structure:"
    echo "  $APP_DIR/"
    echo "    ├── backend/"
    echo "    └── frontend/"
    read -p "Press Enter when files are ready..."
fi

print_success "Application files ready"

################################################################################
# STEP 4: Setup MongoDB
################################################################################

print_header "Step 4: Configuring MongoDB"

systemctl start mongodb
systemctl enable mongodb

# Create database and user
mongo <<EOF
use $DB_NAME
db.createUser({
    user: "kayee01_user",
    pwd: "$(openssl rand -base64 32)",
    roles: ["readWrite"]
})
EOF

print_success "MongoDB configured"

################################################################################
# STEP 5: Setup Backend (FastAPI)
################################################################################

print_header "Step 5: Setting Up Backend"

cd $APP_DIR/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create production .env
cat > .env << EOF
MONGO_URL=mongodb://localhost:27017
DB_NAME=$DB_NAME
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
ADMIN_EMAIL=admin@$DOMAIN
STRIPE_SECRET_KEY=your_stripe_secret_key
PLISIO_SECRET_KEY=your_plisio_secret_key
EOF

print_success "Backend configured"

################################################################################
# STEP 6: Setup Frontend (React)
################################################################################

print_header "Step 6: Building Frontend"

cd $APP_DIR/frontend

# Install dependencies
yarn install

# Create production .env
cat > .env << EOF
REACT_APP_BACKEND_URL=https://$DOMAIN
EOF

# Build production version
yarn build

print_success "Frontend built"

################################################################################
# STEP 7: Configure Supervisor (Backend Process Manager)
################################################################################

print_header "Step 7: Configuring Supervisor"

cat > /etc/supervisor/conf.d/kayee01-backend.conf << EOF
[program:kayee01-backend]
directory=$APP_DIR/backend
command=$APP_DIR/backend/venv/bin/uvicorn server:app --host 0.0.0.0 --port $BACKEND_PORT
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/kayee01-backend.err.log
stdout_logfile=/var/log/supervisor/kayee01-backend.out.log
environment=PATH="$APP_DIR/backend/venv/bin"
EOF

supervisorctl reread
supervisorctl update
supervisorctl start kayee01-backend

print_success "Backend service configured"

################################################################################
# STEP 8: Configure NGINX (Pre-SSL)
################################################################################

print_header "Step 8: Configuring NGINX (Pre-SSL)"

cat > /etc/nginx/sites-available/kayee01 << 'EOFNGINX'
server {
    listen 80;
    listen [::]:80;
    server_name DOMAIN_PLACEHOLDER WWW_DOMAIN_PLACEHOLDER;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}
EOFNGINX

# Replace placeholders
sed -i "s/DOMAIN_PLACEHOLDER/$DOMAIN/g" /etc/nginx/sites-available/kayee01
sed -i "s/WWW_DOMAIN_PLACEHOLDER/$WWW_DOMAIN/g" /etc/nginx/sites-available/kayee01

# Enable site
ln -sf /etc/nginx/sites-available/kayee01 /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Create certbot directory
mkdir -p /var/www/certbot

nginx -t && systemctl reload nginx

print_success "NGINX configured (HTTP only)"

################################################################################
# STEP 9: Obtain SSL Certificate
################################################################################

print_header "Step 9: Obtaining SSL Certificate"

certbot certonly \
    --nginx \
    --non-interactive \
    --agree-tos \
    --email $EMAIL \
    -d $DOMAIN \
    -d $WWW_DOMAIN

if [ $? -ne 0 ]; then
    print_error "SSL certificate failed. Check DNS and firewall."
    exit 1
fi

print_success "SSL certificate obtained"

################################################################################
# STEP 10: Configure NGINX (Full HTTPS)
################################################################################

print_header "Step 10: Configuring NGINX (Full HTTPS)"

cat > /etc/nginx/sites-available/kayee01 << 'EOFNGINX'
# HTTP to HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name DOMAIN_PLACEHOLDER WWW_DOMAIN_PLACEHOLDER;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS Server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name DOMAIN_PLACEHOLDER WWW_DOMAIN_PLACEHOLDER;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/DOMAIN_PLACEHOLDER/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/DOMAIN_PLACEHOLDER/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_stapling on;
    ssl_stapling_verify on;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # Compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;
    
    client_max_body_size 50M;
    
    # Frontend
    root APP_DIR_PLACEHOLDER/frontend/build;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API
    location /api/ {
        proxy_pass http://localhost:BACKEND_PORT_PLACEHOLDER;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
    }
    
    # Block sensitive files
    location ~ /\.(git|env|htaccess) {
        deny all;
    }
    
    location ~ ~$ {
        deny all;
    }
    
    # Logs
    access_log /var/log/nginx/kayee01_access.log;
    error_log /var/log/nginx/kayee01_error.log;
}
EOFNGINX

# Replace placeholders
sed -i "s|DOMAIN_PLACEHOLDER|$DOMAIN|g" /etc/nginx/sites-available/kayee01
sed -i "s|WWW_DOMAIN_PLACEHOLDER|$WWW_DOMAIN|g" /etc/nginx/sites-available/kayee01
sed -i "s|APP_DIR_PLACEHOLDER|$APP_DIR|g" /etc/nginx/sites-available/kayee01
sed -i "s|BACKEND_PORT_PLACEHOLDER|$BACKEND_PORT|g" /etc/nginx/sites-available/kayee01

nginx -t && systemctl reload nginx

print_success "NGINX configured with HTTPS"

################################################################################
# STEP 11: Setup SSL Auto-Renewal
################################################################################

print_header "Step 11: Configuring SSL Auto-Renewal"

# Test renewal
certbot renew --dry-run

# Create renewal hook
cat > /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh << 'EOF'
#!/bin/bash
systemctl reload nginx
EOF

chmod +x /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh

print_success "SSL auto-renewal configured"

################################################################################
# STEP 12: Configure Firewall
################################################################################

print_header "Step 12: Configuring Firewall"

# Install and configure UFW
apt-get install -y ufw

ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

print_success "Firewall configured"

################################################################################
# STEP 13: Final Checks
################################################################################

print_header "Step 13: Running Final Checks"

# Check services
systemctl status nginx --no-pager
supervisorctl status kayee01-backend

# Check SSL
curl -I https://$DOMAIN 2>&1 | head -n 1

print_success "All checks passed"

################################################################################
# COMPLETION
################################################################################

print_header "DEPLOYMENT COMPLETED SUCCESSFULLY!"

echo -e "${GREEN}"
echo "=========================================="
echo "  KAYEE01 E-COMMERCE IS NOW LIVE!"
echo "=========================================="
echo -e "${NC}"
echo ""
echo -e "${GREEN}Your site is accessible at:${NC}"
echo -e "${BLUE}  https://$DOMAIN${NC}"
echo -e "${BLUE}  https://$WWW_DOMAIN${NC}"
echo ""
echo -e "${GREEN}Important Information:${NC}"
echo "  App Directory: $APP_DIR"
echo "  Backend Port: $BACKEND_PORT"
echo "  Database: $DB_NAME"
echo "  SSL Certificate: /etc/letsencrypt/live/$DOMAIN/"
echo ""
echo -e "${GREEN}Service Management:${NC}"
echo "  Backend: supervisorctl restart kayee01-backend"
echo "  NGINX: systemctl reload nginx"
echo "  Logs Backend: tail -f /var/log/supervisor/kayee01-backend.err.log"
echo "  Logs NGINX: tail -f /var/log/nginx/kayee01_error.log"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Update backend .env with real API keys (Stripe, SMTP, etc.)"
echo "2. Test all pages: https://$DOMAIN"
echo "3. Test payments and emails"
echo "4. Check SSL grade: https://www.ssllabs.com/ssltest/"
echo "5. Setup monitoring and backups"
echo ""
echo -e "${GREEN}API Keys to Configure:${NC}"
echo "  Edit: $APP_DIR/backend/.env"
echo "  - STRIPE_SECRET_KEY"
echo "  - PLISIO_SECRET_KEY"
echo "  - SMTP_USERNAME & SMTP_PASSWORD"
echo ""
echo -e "${GREEN}Congratulations! Your e-commerce site is production-ready! 🎉${NC}"
