# KAYEE01 VPS DEPLOYMENT - FINAL PACKAGE

## 📦 KONTNI

- `docker-compose.yml` - Docker services (MongoDB, Backend, Frontend, Nginx)
- `Dockerfile.backend` - Backend Python/FastAPI
- `Dockerfile.frontend` - Frontend React (Node 20)
- `nginx.conf` - Nginx reverse proxy
- `.env.template` - Environment variables template
- `DEPLOY.sh` - Automatic deployment script
- `setup-ssl.sh` - SSL/HTTPS setup

## 🚀 DEPLOYMENT RAPID

### 1. Upload fichye yo sou VPS

Sou VPS ou a (93.127.217.2):

```bash
cd /opt/kayee01
mkdir deployment-final
cd deployment-final
```

Apre sa, upload TOUT fichye yo nan dosye `DEPLOY-VPS-FINAL/` sou ordinatè ou a vè VPS la.

### 2. Kopi kòd sous la

```bash
cd /opt/kayee01/deployment-final
cp -r ../backend .
cp -r ../frontend .
```

### 3. Deploy

```bash
chmod +x DEPLOY.sh
./DEPLOY.sh
```

### 4. SSL (apre sit la mache)

```bash
chmod +x setup-ssl.sh
./setup-ssl.sh
```

## ✅ VERIFICATION

```bash
# Check containers
docker-compose ps

# Check logs
docker-compose logs -f

# Test site
curl -I http://localhost
```

## 🔧 TROUBLESHOOTING

Si gen pwoblèm:

```bash
# Restart tout
docker-compose down
docker-compose up -d

# Check logs
docker-compose logs nginx
docker-compose logs backend
docker-compose logs frontend
```