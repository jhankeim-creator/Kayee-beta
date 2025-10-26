#!/bin/bash

# ========================================
# KAYEE01 VPS DEPLOYMENT SCRIPT
# Complete automated deployment for Hostinger VPS
# ========================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
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

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    error "This script should not be run as root for security reasons."
    error "Please run as a regular user with sudo privileges."
    exit 1
fi

echo "=========================================="
echo "🚀 KAYEE01 VPS DEPLOYMENT"
echo "=========================================="
echo ""

# Step 1: System Update and Dependencies
log "Step 1: Installing system dependencies..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y \
    curl \
    wget \
    git \
    docker.io \
    docker-compose \
    nginx \
    certbot \
    python3-certbot-nginx \
    ufw \
    htop \
    unzip \
    jq

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER

log "System dependencies installed successfully"

# Step 2: Firewall Configuration
log "Step 2: Configuring firewall..."

sudo ufw --force reset
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

log "Firewall configured successfully"

# Step 3: Download Application Code
log "Step 3: Setting up application..."

# Create application directory
sudo mkdir -p /opt/kayee01
sudo chown $USER:$USER /opt/kayee01
cd /opt/kayee01

# Get GitHub repository URL from user
echo ""
echo "Please provide your GitHub repository URL:"
echo "Example: https://github.com/yourusername/kayee01.git"
read -p "GitHub Repository URL: " REPO_URL

if [[ -z "$REPO_URL" ]]; then
    error "Repository URL is required"
    exit 1
fi

# Clone repository
log "Cloning repository from $REPO_URL..."
git clone "$REPO_URL" .

# Navigate to deployment directory
if [[ ! -d "VPS-FINAL-COMPLETE" ]]; then
    error "VPS-FINAL-COMPLETE directory not found in repository"
    error "Please ensure you're using the correct repository with the deployment package"
    exit 1
fi

cd VPS-FINAL-COMPLETE

log "Application code downloaded successfully"

# Step 4: Environment Configuration
log "Step 4: Configuring environment..."

# Copy environment template
if [[ ! -f ".env.template" ]]; then
    error ".env.template file not found"
    exit 1
fi

cp .env.template .env

# Generate JWT secret
JWT_SECRET=$(openssl rand -hex 32)
sed -i "s/JWT_SECRET_KEY=/JWT_SECRET_KEY=$JWT_SECRET/" .env

echo ""
echo "=========================================="
echo "🔧 ENVIRONMENT CONFIGURATION"
echo "=========================================="
echo ""
echo "Please configure the following required settings:"
echo ""

# Get domain name
while true; do
    read -p "Enter your domain name (e.g., kayee01.com): " DOMAIN_NAME
    if [[ -n "$DOMAIN_NAME" ]]; then
        break
    fi
    error "Domain name is required"
done

# Get MongoDB password
while true; do
    read -s -p "Enter a secure MongoDB password: " MONGO_PASSWORD
    echo ""
    if [[ ${#MONGO_PASSWORD} -ge 8 ]]; then
        break
    fi
    error "MongoDB password must be at least 8 characters long"
done

# Get SMTP password
echo ""
read -s -p "Enter your SMTP password (for kayicom509@gmail.com): " SMTP_PASSWORD
echo ""

# Get Stripe key
echo ""
read -p "Enter your Stripe Secret Key (sk_live_...): " STRIPE_KEY
echo ""

# Get Plisio key
read -p "Enter your Plisio API Key: " PLISIO_KEY
echo ""

# Update .env file
sed -i "s/DOMAIN_NAME=.*/DOMAIN_NAME=$DOMAIN_NAME/" .env
sed -i "s/MONGO_PASSWORD=.*/MONGO_PASSWORD=$MONGO_PASSWORD/" .env
sed -i "s/SMTP_PASSWORD=.*/SMTP_PASSWORD=$SMTP_PASSWORD/" .env
sed -i "s/STRIPE_SECRET_KEY=.*/STRIPE_SECRET_KEY=$STRIPE_KEY/" .env
sed -i "s/PLISIO_API_KEY=.*/PLISIO_API_KEY=$PLISIO_KEY/" .env

log "Environment configured successfully"

# Step 5: Copy Application Files
log "Step 5: Preparing application files..."

# Copy backend and frontend from parent directory
if [[ -d "../backend" ]]; then
    cp -r ../backend .
    log "Backend files copied"
else
    error "Backend directory not found in repository"
    exit 1
fi

if [[ -d "../frontend" ]]; then
    cp -r ../frontend .
    log "Frontend files copied"
else
    error "Frontend directory not found in repository"
    exit 1
fi

# Create SSL directory
mkdir -p ssl

log "Application files prepared successfully"

# Step 6: Build and Start Services
log "Step 6: Building and starting services..."

# Stop any existing nginx service
sudo systemctl stop nginx 2>/dev/null || true
sudo systemctl disable nginx 2>/dev/null || true

# Build and start Docker containers
docker-compose down 2>/dev/null || true
docker-compose build --no-cache
docker-compose up -d

log "Services started successfully"

# Step 7: Wait for Services and Health Check
log "Step 7: Waiting for services to be ready..."

# Wait for services to start
sleep 30

# Check if all containers are running
CONTAINERS_RUNNING=$(docker-compose ps --services --filter "status=running" | wc -l)
TOTAL_CONTAINERS=$(docker-compose ps --services | wc -l)

if [[ $CONTAINERS_RUNNING -eq $TOTAL_CONTAINERS ]]; then
    log "All containers are running successfully"
else
    warning "Some containers may not be running properly"
    docker-compose ps
fi

# Health check
log "Performing health checks..."

# Check backend
if curl -f http://localhost:8001/api/products >/dev/null 2>&1; then
    log "✅ Backend is responding"
else
    warning "⚠️ Backend health check failed"
fi

# Check frontend
if curl -f http://localhost:3000 >/dev/null 2>&1; then
    log "✅ Frontend is responding"
else
    warning "⚠️ Frontend health check failed"
fi

# Check if site is accessible
if curl -f http://localhost >/dev/null 2>&1; then
    log "✅ Site is accessible through Nginx"
else
    warning "⚠️ Site accessibility check failed"
fi

# Step 8: DNS Verification
log "Step 8: Verifying DNS configuration..."

SERVER_IP=$(curl -s ifconfig.me)
DOMAIN_IP=$(dig +short $DOMAIN_NAME | head -1)

echo ""
echo "DNS Configuration Check:"
echo "Server IP: $SERVER_IP"
echo "Domain IP: $DOMAIN_IP"

if [[ "$SERVER_IP" == "$DOMAIN_IP" ]]; then
    log "✅ DNS is configured correctly"
    DNS_READY=true
else
    warning "⚠️ DNS is not pointing to this server yet"
    warning "Please update your domain's DNS records to point to: $SERVER_IP"
    DNS_READY=false
fi

# Step 9: SSL Setup (if DNS is ready)
if [[ "$DNS_READY" == true ]]; then
    log "Step 9: Setting up SSL certificate..."
    
    echo ""
    read -p "Do you want to set up SSL now? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./setup-ssl.sh "$DOMAIN_NAME"
    else
        info "SSL setup skipped. You can run './setup-ssl.sh $DOMAIN_NAME' later"
    fi
else
    warning "Step 9: SSL setup skipped due to DNS configuration"
    info "After DNS propagation, run: './setup-ssl.sh $DOMAIN_NAME'"
fi

# Step 10: Final Status and Instructions
echo ""
echo "=========================================="
echo "🎉 DEPLOYMENT COMPLETED!"
echo "=========================================="
echo ""

log "Deployment Summary:"
echo "• Domain: $DOMAIN_NAME"
echo "• Server IP: $SERVER_IP"
echo "• Application Directory: /opt/kayee01/VPS-FINAL-COMPLETE"
echo ""

if [[ "$DNS_READY" == true ]]; then
    log "Your site should be accessible at:"
    echo "• HTTP: http://$DOMAIN_NAME"
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "• HTTPS: https://$DOMAIN_NAME"
    fi
else
    warning "Complete DNS setup first, then access your site at:"
    echo "• HTTP: http://$DOMAIN_NAME (after DNS propagation)"
fi

echo ""
log "Admin Access:"
echo "• URL: https://$DOMAIN_NAME/admin/login"
echo "• Email: kayicom509@gmail.com"
echo "• Password: Admin123!"
echo ""

warning "IMPORTANT SECURITY STEPS:"
echo "1. Change the admin password immediately after first login"
echo "2. Keep your MongoDB password secure: $MONGO_PASSWORD"
echo "3. Regularly update your system and Docker images"
echo ""

log "Useful Commands:"
echo "• Check status: docker-compose ps"
echo "• View logs: docker-compose logs -f"
echo "• Restart services: docker-compose restart"
echo "• Stop services: docker-compose down"
echo "• Setup SSL: ./setup-ssl.sh $DOMAIN_NAME"
echo ""

log "Deployment completed successfully! 🚀"

# Create a status file
cat > deployment-status.txt << EOL
Deployment completed: $(date)
Domain: $DOMAIN_NAME
Server IP: $SERVER_IP
DNS Ready: $DNS_READY
Admin Email: kayicom509@gmail.com
MongoDB Password: [SECURE - Check .env file]
EOL

echo "Deployment status saved to: deployment-status.txt"
echo ""
echo "=========================================="
