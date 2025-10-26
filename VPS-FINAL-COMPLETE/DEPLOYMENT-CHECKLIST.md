# ✅ KAYEE01 VPS DEPLOYMENT CHECKLIST

## 🎯 Pre-Deployment Checklist

### 1. Repository Setup
- [ ] Code pushed to GitHub
- [ ] VPS-FINAL-COMPLETE directory in repository
- [ ] All files present and validated

### 2. VPS Requirements
- [ ] Ubuntu 20.04+ VPS ready
- [ ] SSH access configured
- [ ] Domain pointing to VPS IP (93.127.217.2)
- [ ] Ports 80 and 443 accessible

### 3. Domain Configuration
- [ ] kayee01.com DNS A record → 93.127.217.2
- [ ] www.kayee01.com DNS CNAME → kayee01.com
- [ ] DNS propagation completed (check with: `dig +short kayee01.com`)

## 🚀 Deployment Steps

### Step 1: Connect to VPS
```bash
ssh root@93.127.217.2
# or
ssh your-user@93.127.217.2
```

### Step 2: Download and Run Deployment Script
```bash
# Download deployment script
wget https://raw.githubusercontent.com/YOUR-USERNAME/kayee01/main/VPS-FINAL-COMPLETE/DEPLOY.sh

# Make executable and run
chmod +x DEPLOY.sh
./DEPLOY.sh
```

### Step 3: Follow Interactive Setup
The script will ask for:
1. **GitHub Repository URL**: `https://github.com/YOUR-USERNAME/kayee01.git`
2. **Domain Name**: `kayee01.com`
3. **MongoDB Password**: Create a strong password (min 8 chars)

### Step 4: SSL Configuration (After DNS Ready)
```bash
cd /opt/kayee01/VPS-FINAL-COMPLETE
./setup-ssl.sh kayee01.com
```

## 🔧 Post-Deployment Verification

### 1. Check Services Status
```bash
cd /opt/kayee01/VPS-FINAL-COMPLETE
docker-compose ps
```
All services should show "Up".

### 2. Test Website Access
- HTTP: http://kayee01.com
- HTTPS: https://kayee01.com (after SSL setup)

### 3. Test Admin Panel
- URL: https://kayee01.com/admin/login
- Email: kayicom509@gmail.com
- Password: Admin123!

### 4. Verify API Endpoints
```bash
curl http://kayee01.com/api/products
curl http://kayee01.com/api/categories
```

## 🛡️ Security Checklist

### Immediate Actions (CRITICAL)
- [ ] Change admin password in application
- [ ] Verify MongoDB password is secure
- [ ] Confirm firewall is active: `sudo ufw status`
- [ ] SSL certificate installed and working

### Ongoing Security
- [ ] Regular system updates: `sudo apt update && sudo apt upgrade`
- [ ] Regular backups: `./backup-mongodb.sh`
- [ ] Monitor logs: `docker-compose logs -f`
- [ ] SSL certificate auto-renewal working

## 📊 Monitoring and Maintenance

### Daily Checks
```bash
cd /opt/kayee01/VPS-FINAL-COMPLETE
./monitor.sh
```

### Weekly Maintenance
```bash
# Backup database
./backup-mongodb.sh

# Check for updates
./update.sh

# Clean up Docker
docker system prune -f
```

### Monthly Tasks
- [ ] Review access logs
- [ ] Update payment gateway settings if needed
- [ ] Check SSL certificate expiration
- [ ] Review and rotate passwords

## 🆘 Troubleshooting

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| Site not loading | Check `docker-compose ps` and restart services |
| SSL certificate failed | Verify DNS and run `./setup-ssl.sh kayee01.com` |
| Database connection error | Check MongoDB password in `.env` |
| Admin login not working | Verify credentials and check backend logs |

### Emergency Commands
```bash
# Restart all services
docker-compose restart

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Start all services
docker-compose up -d

# Complete rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 📞 Support Information

### Log Locations
- Application logs: `docker-compose logs`
- Nginx logs: `docker-compose logs nginx`
- System logs: `/var/log/syslog`

### Configuration Files
- Main config: `/opt/kayee01/VPS-FINAL-COMPLETE/.env`
- Nginx config: `/opt/kayee01/VPS-FINAL-COMPLETE/nginx.conf`
- Docker config: `/opt/kayee01/VPS-FINAL-COMPLETE/docker-compose.yml`

### Backup Locations
- Database backups: `/opt/kayee01/VPS-FINAL-COMPLETE/backups/`
- SSL certificates: `/opt/kayee01/VPS-FINAL-COMPLETE/ssl/`

## ✅ Success Criteria

Your deployment is successful when:
- [ ] Website loads at https://kayee01.com
- [ ] Admin panel accessible and functional
- [ ] Products display correctly
- [ ] Payment gateways configured
- [ ] SSL certificate active
- [ ] All Docker services running
- [ ] Backups configured
- [ ] Monitoring in place

## 🎉 Final Notes

- **Admin Email**: kayicom509@gmail.com
- **Default Admin Password**: Admin123! (CHANGE IMMEDIATELY)
- **MongoDB Database**: kayee01_db
- **Application Directory**: /opt/kayee01/VPS-FINAL-COMPLETE

**Remember**: Change the default admin password immediately after first login!

---

**Deployment completed successfully! 🚀**
