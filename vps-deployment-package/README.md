# Kayee01 VPS Deployment Package

## 📦 Kontni Pakèt la

- `docker-compose.yml` - Konfigirasyon Docker ak healthchecks
- `nginx.conf` - Nginx config ak variables dinamik (PA gen upstream blocks)
- `Dockerfile.backend` - Backend Python/FastAPI
- `Dockerfile.frontend` - Frontend React
- `.env.example` - Egzanp konfigirasyon
- `DEPLOY.sh` - Script deployment otomatik
- `setup-ssl.sh` - Script konfigirasyon SSL

## 🚀 Enstale Rapid

### 1. Clone repo ou a sou VPS:
```bash
cd /opt
git clone https://github.com/jhankeim-creator/Kayee-beta.git kayee01
cd kayee01
```

### 2. Kopi fichye deployment yo:
```bash
cp -r vps-deployment-package/* .
```

### 3. Konfigure .env:
```bash
cp .env.example .env
nano .env  # Modifye DOMAIN_NAME, MONGO_PASSWORD, elatriye
```

### 4. Deploy:
```bash
chmod +x DEPLOY.sh
./DEPLOY.sh
```

### 5. Konfigure SSL:
```bash
chmod +x setup-ssl.sh
./setup-ssl.sh
```

## ✅ Solisyon Pwoblèm yo

### Pwoblèm: "host not found in upstream backend"
**Solisyon**: Nou itilize **variables dinamik** (`set $backend_upstream`) olye de `upstream` blocks estatik.

### Pwoblèm: Containers ap redémarre
**Solisyon**: Nou ajoute **healthchecks** pou chak sèvis ak `depends_on: condition: service_healthy`

### Pwoblèm: SSL pa travay
**Solisyon**: Nginx gen konfigirasyon pou `/.well-known/acme-challenge/` ak volim `certbot_data` monte kòrèkteman

## 📋 Verifye Status

```bash
docker-compose ps
docker-compose logs nginx
curl -I http://localhost
```

## 🔧 Troubleshooting

Si gen pwoblèm:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
docker-compose logs -f
```
