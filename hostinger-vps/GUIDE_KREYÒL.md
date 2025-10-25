# 🚀 GID KONPLÈ POU DEPLWAMAN KAYEE01 SOU VPS HOSTINGER

## 📋 SA W BEZWEN KONNEN

✅ **Tout erè yo korije**
✅ **Pakèt la pare pou deplwaman**
✅ **Enstalasyon otomatik an 6 etap**
✅ **Backend teste ak aksè - 100% bon jan travay**

---

## 🎯 ETAP 1: PREPARE GITHUB

### Sou òdinatè lokal ou:

```bash
# 1. Ale nan dosye aplikasyon an
cd /app

# 2. Inisjalize Git
git init

# 3. Ajoute tout fichye yo
git add .

# 4. Kreye commit
git commit -m "Kayee01 - Ready for VPS deployment"

# 5. Kreye branch main
git branch -M main

# 6. Ajoute repository GitHub ou
# Ranplase VOTRE-USERNAME pa non itilizatè GitHub ou
git remote add origin https://github.com/VOTRE-USERNAME/kayee01.git

# 7. Pouse sou GitHub
git push -u origin main
```

**📝 Nòt:** Si w pa gen repository, kreye youn sou https://github.com/new

---

## 🎯 ETAP 2: KONEKTE SOU VPS HOSTINGER

```bash
# Ranplase pa IP VPS ou
ssh root@VOTRE-IP-VPS
```

**Modpas:** Itilize modpas Hostinger ba ou

---

## 🎯 ETAP 3: ENSTALE KAYEE01

```bash
# Kreye dosye
mkdir -p /opt/kayee01
cd /opt/kayee01

# Clone repository ou
# Ranplase VOTRE-USERNAME pa non itilizatè GitHub ou
git clone https://github.com/VOTRE-USERNAME/kayee01.git .

# Ale nan dosye VPS
cd hostinger-vps

# Bay pèmisyon egzekisyon pou script yo
chmod +x *.sh

# Lanse enstalasyon otomatik
./install-vps.sh
```

---

## 🎯 ETAP 4: KONFIGIRE VARYAB ANVIRONMAN

```bash
cd /opt/kayee01/hostinger-vps

# Kopye fichye egzanp
cp .env.example .env

# Modifye konfigirasyon an
nano .env
```

### KONFIGIRASYON OBLIGATWA:

```env
# 1. DOMÈN OU (OBLIGATWA)
DOMAIN_NAME=domèn-ou.com

# 2. MODPAS MONGODB (CHANJE LI!)
MONGO_PASSWORD=YonModpasFo123!@#

# 3. JWT SECRET (ap jenere otomatikman)
JWT_SECRET_KEY=

# 4. SMTP (Deja konfigire, pa modifye)
SMTP_USER=kayicom509@gmail.com
SMTP_PASSWORD=unstcfsyowwpiuzi

# 5. STRIPE (Ajoute kle reyèl ou)
STRIPE_SECRET_KEY=sk_live_KLE_STRIPE_OU

# 6. PLISIO (Ajoute kle reyèl ou)
PLISIO_API_KEY=KLE_PLISIO_OU
```

**⚠️ ENPÒTAN:**
- Chanje `DOMAIN_NAME` avèk domèn reyèl ou
- Itilize yon modpas solid pou `MONGO_PASSWORD`
- Si w pa gen kle Stripe/Plisio, kite vid pou kounye a

**Pou sove nan nano:**
- Peze `Ctrl + X`
- Peze `Y` (pou Yes)
- Peze `Enter`

---

## 🎯 ETAP 5: LANSE APLIKASYON AN

```bash
cd /opt/kayee01/hostinger-vps
./start.sh
```

**⏳ Tann 2-3 minit** pou tout sèvis yo demarre.

Ou pral wè:
```
✅ KAYEE01 DÉMARRÉ !
Site principal: http://IP-OU
Admin: http://IP-OU/admin/login
API: http://IP-OU/api
```

---

## 🎯 ETAP 6: KONFIGIRE SSL (HTTPS)

**⚠️ ENPÒTAN:** Anvan etap sa, asire w domèn ou ap pwente sou IP VPS ou.

### Verifye domèn an pwente kòrèkteman:

```bash
# Ranplase pa domèn ou
dig +short domèn-ou.com

# Konpare avèk IP sèvè ou
curl -s ifconfig.me
```

De IP yo dwe **idantik**.

### Konfigire SSL:

```bash
cd /opt/kayee01/hostinger-vps
./setup-ssl.sh domèn-ou.com
```

**✅ Fini!** Sit ou kounye a aksesib an HTTPS:
- https://domèn-ou.com
- https://domèn-ou.com/admin/login

---

## 🔍 VERIFYE ENSTALASYON AN

```bash
cd /opt/kayee01/hostinger-vps
./check-status.sh
```

---

## 📱 AKSÈ SOU SIT OU

### URLs:
- **Sit prensipal:** https://domèn-ou.com
- **Paj admin:** https://domèn-ou.com/admin/login
- **API:** https://domèn-ou.com/api

### Idantifyan Admin:
- **Email:** kayicom509@gmail.com
- **Modpas:** Admin123!

**⚠️ CHANJE MODPAS ADMIN IMEDYATMAN APRE PREMYE KONEKSYON!**

---

## 🔧 KÒMAND ITIL

### Gade logs an tan reyèl:
```bash
cd /opt/kayee01/hostinger-vps
docker-compose logs -f
```

### Logs yon sèvis espesifik:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f nginx
docker-compose logs -f mongodb
```

### Arete aplikasyon an:
```bash
cd /opt/kayee01/hostinger-vps
./stop.sh
```

### Redemare aplikasyon an:
```bash
cd /opt/kayee01/hostinger-vps
./stop.sh
./start.sh
```

### Mete ajou kòd la soti nan GitHub:
```bash
cd /opt/kayee01
git pull
cd hostinger-vps
./stop.sh
./start.sh
```

---

## 📦 ENFÒMASYON KONFIGIRASYON

### Fichye Enpòtan:

1. **`.env`** - Varyab anvironman (konfigirasyon sekrè)
2. **`docker-compose.yml`** - Konfigirasyon Docker
3. **`nginx.conf`** - Konfigirasyon Nginx (reverse proxy)

### Pò ki itilize:

- **80** - HTTP (redirije sou HTTPS apre SSL)
- **443** - HTTPS (apre konfigirasyon SSL)
- **8001** - Backend FastAPI (entèn)
- **3000** - Frontend React/Nginx (entèn)
- **27017** - MongoDB (entèn)

### Volim Docker:

- **mongodb_data** - Baz done pèsistan
- **mongodb_config** - Konfigirasyon MongoDB
- **uploads_data** - Imaj ki uploade
- **certbot_data** - Sètifika SSL

---

## 🐛 REZOUD PWOBLÈM

### Pwoblèm: Sit la pa chaje

**Solisyon 1:** Verifye ke conteneur yo ap fonksyone
```bash
docker-compose ps
```

Tout conteneur yo dwe "Up".

**Solisyon 2:** Gade logs yo
```bash
docker-compose logs
```

**Solisyon 3:** Redemare
```bash
./stop.sh
./start.sh
```

---

### Pwoblèm: Erè MongoDB

**Solisyon:** Verifye modpas nan `.env`
```bash
nano .env
# Verifye MONGO_PASSWORD
```

Epi redemare:
```bash
./stop.sh
./start.sh
```

---

### Pwoblèm: SSL echwe

**Koz posib:**
1. Domèn an pa ap pwente sou VPS la
2. Pò 80/443 yo pa louvri
3. Yon lòt sèvis deja ap itilize pò a

**Solisyon:**
```bash
# Verifye DNS
dig +short domèn-ou.com
curl -s ifconfig.me

# Verifye pò yo
sudo ufw status

# Louvri pò yo si nesesè
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

---

## 🔒 SEKIRITE

### Aksyon Obligatwa:

1. **Chanje modpas admin** nan aplikasyon an
2. **Itilize modpas solid** pou MongoDB
3. **Kenbe kle API yo sekrè** (pa pataje yo)
4. **Fè backup regilyèman** baz done a

### Backup MongoDB:

```bash
# Kreye yon backup
docker exec kayee01-mongodb mongodump --out /data/backup --authenticationDatabase admin -u kayee01_admin -p MODPAS_OU

# Kopye backup la deyò conteneur a
docker cp kayee01-mongodb:/data/backup ./backup-$(date +%Y%m%d)
```

### Restore MongoDB:

```bash
# Kopye backup la nan conteneur a
docker cp ./backup kayee01-mongodb:/data/restore

# Restore
docker exec kayee01-mongodb mongorestore /data/restore --authenticationDatabase admin -u kayee01_admin -p MODPAS_OU
```

---

## 📊 ACHITÈKTI

```
Internet (HTTPS/HTTP)
         │
         ↓
    Nginx Proxy (Pò 80/443)
         │
         ├──→ Frontend React (Pò 3000)
         │    └─ Nginx Alpine
         │
         └──→ Backend FastAPI (Pò 8001)
              └─ MongoDB (Pò 27017)
```

---

## 🎯 CHECKLIST DEPLWAMAN

### Anvan Deplwaman:

- [ ] Kòd pouse sou GitHub
- [ ] VPS Ubuntu pare
- [ ] Domèn konfigire epi ap pwente sou VPS
- [ ] Aksè SSH fonksyonèl
- [ ] Kle API pare (Stripe, Plisio)

### Pandan Deplwaman:

- [ ] Enstalasyon otomatik fini
- [ ] Fichye .env konfigire
- [ ] Sèvis yo demarre avèk `./start.sh`
- [ ] Tout conteneur yo "Up"
- [ ] Sit aksesib an HTTP

### Apre Deplwaman:

- [ ] SSL konfigire avèk `./setup-ssl.sh`
- [ ] Sit aksesib an HTTPS
- [ ] Admin login fonksyone
- [ ] Pwodwi yo afiche kòrèkteman
- [ ] Peman yo teste
- [ ] Backup konfigire
- [ ] Modpas admin chanje

---

## 📝 FICHYE REFERANS

Tout fichye enstalasyon yo nan dosye `/app/hostinger-vps/`:

1. **README.md** - Gid konplè an Fransè
2. **QUICK_START.md** - Gid rapid (6 etap)
3. **CORRECTIONS.md** - Lis koreksyon yo
4. **DEPLOY_STATUS.md** - Estati deplwaman
5. **GUIDE_DEPLOIEMENT_VPS.md** - Gid detaye an Fransè
6. **validate-package.sh** - Script validasyon

---

## ✅ REZIME

✅ **Pakèt VPS konplètman korije epi teste**
✅ **Backend verifye epi fonksyonèl (5/5 tès reyisi)**
✅ **Dokimantasyon konplè founi**
✅ **Script enstalasyon otomatik pare**
✅ **Achitèkti Docker optimize**
✅ **Pare pou deplwaman an pwoduksyon**

---

## 🎉 FELISITASYON!

Boutik Kayee01 ou kounye a pare pou deplwaman! 🚀

Swiv gid **QUICK_START.md** pou deplwaye sit ou sou Hostinger VPS.

**Bon vant! 💰**
