#!/bin/bash

# MongoDB Backup Script for Kayee01
# Run this script regularly to backup your database

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

# Load environment variables
if [[ -f .env ]]; then
    source .env
else
    error ".env file not found"
    exit 1
fi

# Create backup directory
BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

log "Starting MongoDB backup..."

# Backup MongoDB
docker exec kayee01-mongodb mongodump \
    --out /data/backup \
    --authenticationDatabase admin \
    --username kayee01_admin \
    --password "$MONGO_PASSWORD" \
    --db kayee01_db

# Copy backup from container
docker cp kayee01-mongodb:/data/backup "$BACKUP_DIR/"

# Backup uploads
if [[ -d "uploads" ]]; then
    cp -r uploads "$BACKUP_DIR/"
    log "Uploads backed up"
fi

# Backup environment file (without sensitive data)
cp .env "$BACKUP_DIR/.env.backup"
sed -i 's/MONGO_PASSWORD=.*/MONGO_PASSWORD=***HIDDEN***/' "$BACKUP_DIR/.env.backup"
sed -i 's/JWT_SECRET_KEY=.*/JWT_SECRET_KEY=***HIDDEN***/' "$BACKUP_DIR/.env.backup"

# Create backup info
cat > "$BACKUP_DIR/backup-info.txt" << EOL
Backup created: $(date)
Domain: $DOMAIN_NAME
Database: kayee01_db
Backup size: $(du -sh "$BACKUP_DIR" | cut -f1)
EOL

# Compress backup
cd backups
tar -czf "$(basename $BACKUP_DIR).tar.gz" "$(basename $BACKUP_DIR)"
rm -rf "$(basename $BACKUP_DIR)"
cd ..

log "Backup completed: backups/$(basename $BACKUP_DIR).tar.gz"

# Clean old backups (keep last 7 days)
find ./backups -name "*.tar.gz" -mtime +7 -delete 2>/dev/null || true

log "MongoDB backup completed successfully"
