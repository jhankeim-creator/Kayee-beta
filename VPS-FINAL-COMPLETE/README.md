# 🚀 KAYEE01 - Pakèt Konplè pou Hostinger VPS

## 📋 Sa ki nan pakèt la

Pakèt sa a gen tout bagay ou bezwen pou mete boutik Kayee01 ou a sou Hostinger VPS ou an.

### 🎯 Karakteristik yo
- ✅ **FastAPI Backend** - API rapid ak Python
- ✅ **React Frontend** - Entèfas modèn ak responsive
- ✅ **MongoDB Database** - Base done ki solid
- ✅ **Nginx Reverse Proxy** - Jesyon trafik ak SSL
- ✅ **SSL Otomatik** - Sètifika HTTPS gratis ak Let's Encrypt
- ✅ **Docker Containers** - Jesyon sèvis ki fasil
- ✅ **Sistèm Peman** - Stripe ak Plisio (crypto)
- ✅ **Admin Panel** - Jesyon pwodwi ak kòmand yo

## 🛠️ Kondisyon yo

### VPS Requirements
- **Sistèm**: Ubuntu 20.04 oswa 22.04
- **RAM**: Minimòm 2GB (4GB pi bon)
- **Depo**: Minimòm 20GB
- **Aksè**: SSH root oswa sudo
- **Domèn**: Ki ap pwente nan IP VPS la

### Kont yo ou bezwen
- Kont GitHub (pou kòd la)
- Domèn ki konfigire (kayee01.com)
- Aksè SSH nan VPS ou an

## 🚀 Enstalasyon Rapid (5 minit)

### Etap 1: Prepare kòd la
```bash
# Sou òdinatè ou an
cd /app
git add VPS-FINAL-COMPLETE/
git commit -m "Complete VPS deployment package"
git push origin main
```

### Etap 2: Konekte ak VPS ou an
```bash
ssh root@93.127.217.2
# Oswa ak user ki gen sudo
ssh your-user@93.127.217.2
```

### Etap 3: Telechaje ak kouri script la
```bash
# Telechaje script enstalasyon an
wget https://raw.githubusercontent.com/YOUR-USERNAME/kayee01/main/VPS-FINAL-COMPLETE/DEPLOY.sh

# Bay pèmi ak kouri li
chmod +x DEPLOY.sh
./DEPLOY.sh
```

### Etap 4: Swiv enstriksyon yo
Script la ap mande ou:
1. **URL GitHub ou an** - Kote kòd ou an ye
2. **Non domèn ou an** - kayee01.com
3. **Modpas MongoDB** - Yon modpas ki solid

### Etap 5: Konfigire SSL (si DNS pare)
```bash
# Si domèn ou an ap pwente nan VPS la
./setup-ssl.sh kayee01.com
```

## 📁 Fichye yo ki enpòtan

| Fichye | Deskripsyon |
|---------|-------------|
| `DEPLOY.sh` | Script enstalasyon otomatik |
| `docker-compose.yml` | Konfigirasyon sèvis yo |
| `nginx.conf` | Konfigirasyon proxy ak SSL |
| `.env.template` | Egzanp konfigirasyon |
| `setup-ssl.sh` | Script SSL otomatik |

## ⚙️ Konfigirasyon Anviwonman

Nan fichye `.env` ou an, ou dwe konfigire:

```env
# OBLIGATWA - Non domèn ou an
DOMAIN_NAME=kayee01.com

# OBLIGATWA - Modpas MongoDB (chanje li!)
MONGO_PASSWORD=YourSecurePassword123!

# Otomatik - JWT secret
JWT_SECRET_KEY=auto-generated

# Pre-konfigire - Email
SMTP_USER=kayicom509@gmail.com
SMTP_PASSWORD=remxlraghtscsvgo

# Opsyonèl - Kle peman yo
STRIPE_SECRET_KEY=sk_live_...
PLISIO_API_KEY=...
```

## 🔧 Kòmand Itil yo

### Jesyon Sèvis yo
```bash
# Gade estati sèvis yo
docker-compose ps

# Gade log yo
docker-compose logs -f

# Rèkòmanse sèvis yo
docker-compose restart

# Rete sèvis yo
docker-compose down

# Kòmanse sèvis yo
docker-compose up -d
```

### Jesyon SSL
```bash
# Konfigire SSL
./setup-ssl.sh kayee01.com

# Verifye sètifika a
./check-ssl-renewal.sh kayee01.com
```

### Jesyon Base Done
```bash
# Antre nan MongoDB
docker exec -it kayee01-mongodb mongosh -u kayee01_admin -p

# Backup base done an
docker exec kayee01-mongodb mongodump --out /data/backup \
  --authenticationDatabase admin -u kayee01_admin -p YOUR_PASSWORD

# Kopye backup la
docker cp kayee01-mongodb:/data/backup ./backup-$(date +%Y%m%d)
```

## 🏗️ Achitèk Sistèm nan

```
Internet (HTTPS/HTTP)
         │
         ↓
    Nginx Proxy (Port 80/443)
         │
         ├──→ Frontend React (Port 3000)
         │    └─ Nginx Alpine
         │
         └──→ Backend FastAPI (Port 8001)
              └─ MongoDB (Port 27017)
```

## 🔍 Verifye Apre Enstalasyon

### 1. Verifye sèvis yo ap mache
```bash
docker-compose ps
```
Tout sèvis yo dwe "Up".

### 2. Verifye aksè web la
```bash
curl -I http://kayee01.com
```
Li dwe retounen "HTTP/1.1 200 OK".

### 3. Teste admin an
- Ale nan: https://kayee01.com/admin/login
- Email: kayicom509@gmail.com
- Modpas: Admin123!

## 🛡️ Sekirite

### Aksyon Obligatwa Apre Enstalasyon
1. ✅ Chanje modpas admin an nan aplikasyon an
2. ✅ Verifye MONGO_PASSWORD solid
3. ✅ Konfigire backup otomatik
4. ✅ Aktive firewall (deja fèt pa script la)

### Backup Regilyè
```bash
# Backup MongoDB chak semèn
crontab -e
# Ajoute: 0 2 * * 0 /opt/kayee01/VPS-FINAL-COMPLETE/backup-mongodb.sh
```

## 🆘 Rezoud Pwoblèm yo

### Pwoblèm Komen yo

| Pwoblèm | Solisyon |
|---------|----------|
| Sit la pa chaje | `docker-compose ps` pou verifye sèvis yo |
| Erè MongoDB | Verifye MONGO_PASSWORD nan `.env` |
| SSL echwe | Verifye domèn an ap pwente nan VPS la |
| Port deja itilize | Rete sèvis ki nan konfli yo |

### Kòmand Depanaj
```bash
# Netwaye Docker
docker system prune -a

# Rebati imaj yo
docker-compose build --no-cache

# Gade log erè yo
docker-compose logs backend
docker-compose logs frontend
docker-compose logs nginx
```

## 📞 Sipò

### Si ou gen pwoblèm:
1. Gade log yo: `docker-compose logs -f`
2. Verifye DNS: `dig +short kayee01.com`
3. Verifye firewall: `sudo ufw status`
4. Rèkòmanse sèvis yo: `docker-compose restart`

### Fichye Referans yo
- **Script Enstalasyon**: `DEPLOY.sh`
- **Konfigirasyon SSL**: `setup-ssl.sh`
- **Egzanp Anviwonman**: `.env.template`

## 🎉 Rezime

✅ **Pakèt VPS konplètman teste ak fonksyonèl**
✅ **Backend verifye ak fonksyonèl**
✅ **Dokimantasyon konplè nan Kreyòl**
✅ **Script enstalasyon otomatik pare**
✅ **Achitèk Docker optimize**
✅ **Pare pou enstalasyon nan pwodiksyon**

---

## 🚀 Pwochen Etap yo

1. **Kounye a**: Pouse kòd la sou GitHub
2. **Apre sa**: Swiv script `DEPLOY.sh`
3. **Apre enstalasyon**: Teste tout fonksyon yo (kòmand, peman)
4. **Finalman**: Konfigire backup otomatik

---

**🎯 ESTATI FINAL: PARE POU ENSTALASYON** ✅

Tout bagay pare! Swiv script `DEPLOY.sh` pou mete boutik Kayee01 ou a sou Hostinger VPS ou an.

**Bon enstalasyon! 🚀**
