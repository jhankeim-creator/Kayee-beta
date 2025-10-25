# 🚀 GUIDE RAPIDE - Déploiement Render.com

## ⏱️ Temps estimé : 20 minutes

---

## 📋 CE QU'IL VOUS FAUT

1. **Compte GitHub** (gratuit) - https://github.com/join
2. **Compte Render** (gratuit) - https://render.com
3. **Compte MongoDB Atlas** (gratuit) - https://www.mongodb.com/cloud/atlas/register

---

## 🎯 ÉTAPES RAPIDES

### ÉTAPE 1 : MongoDB Atlas (5 min)

1. Allez sur https://www.mongodb.com/cloud/atlas/register
2. Créez un compte gratuit
3. Créez un cluster **M0 Sandbox** (GRATUIT)
4. Région : **Frankfurt** ou plus proche
5. Créez un utilisateur de base de données :
   - Username: `kayee01_user`
   - Password: `votre_mot_de_passe` (NOTEZ-LE !)
6. Whitelist IP : Cliquez **"Allow Access from Anywhere"** (0.0.0.0/0)
7. Copiez la connection string :
   ```
   mongodb+srv://kayee01_user:MOT_DE_PASSE@cluster.xxxxx.mongodb.net/kayee01_db
   ```

✅ **MongoDB prêt !**

---

### ÉTAPE 2 : GitHub (5 min)

1. Allez sur https://github.com/new
2. Nom du repo : `kayee01-ecommerce`
3. Type : **Private**
4. NE cochez PAS "Initialize with README"
5. Cliquez **Create repository**

6. Dans votre terminal Emergent, exécutez :
```bash
cd /app
git remote add origin https://github.com/VOTRE_USERNAME/kayee01-ecommerce.git
git branch -M main
git push -u origin main
```

✅ **Code sur GitHub !**

---

### ÉTAPE 3 : Render.com (10 min)

1. Allez sur https://dashboard.render.com
2. Inscrivez-vous avec GitHub
3. Cliquez **New +** → **Blueprint**
4. Sélectionnez votre repo **kayee01-ecommerce**
5. Cliquez **Apply**

6. **Configurez les variables d'environnement :**

#### Pour le service `kayee01-backend` :

Cliquez sur le service backend → Environment → Ajoutez :

```
MONGO_URL=mongodb+srv://kayee01_user:MOT_DE_PASSE@cluster.xxxxx.mongodb.net/kayee01_db

SMTP_PASSWORD=votre_mot_de_passe_gmail_app
```

**Pour Gmail App Password :**
- Allez sur https://myaccount.google.com/apppasswords
- Générez un mot de passe pour "Mail"
- Utilisez ce mot de passe

7. Cliquez **Save Changes**

8. Render va déployer automatiquement (5-10 min)

✅ **Site déployé !**

---

## 🎉 VOTRE SITE EST EN LIGNE !

### URLs :

**Site principal :**
```
https://kayee01-frontend.onrender.com
```

**Admin :**
```
https://kayee01-frontend.onrender.com/admin/login

Email: kayicom509@gmail.com
Password: Admin123!
```

**Backend API :**
```
https://kayee01-backend.onrender.com/api
```

---

## 🔧 AJOUTER DES PRODUITS

1. Connectez-vous à l'admin
2. Allez dans **Products**
3. Cliquez **Add Product**
4. Remplissez les informations
5. Uploadez une image
6. Sauvegardez

Ou utilisez le Shell Render pour importer des données de test :
```bash
cd backend
python create_sample_data.py
```

---

## 💳 CONFIGURER LES PAIEMENTS (Optionnel)

### Stripe (cartes bancaires)

1. Allez sur https://dashboard.stripe.com/test/apikeys
2. Copiez vos clés de test
3. Dans Render → Backend → Environment :
   ```
   STRIPE_SECRET_KEY=sk_test_xxxxx
   STRIPE_PUBLISHABLE_KEY=pk_test_xxxxx
   ```
4. Redémarrez le backend

### Plisio (crypto)

1. Inscrivez-vous sur https://plisio.net
2. Obtenez votre API key
3. Dans Render → Backend → Environment :
   ```
   PLISIO_API_KEY=votre_clé
   ```
4. Redémarrez le backend

---

## 🔄 METTRE À JOUR VOTRE SITE

Chaque fois que vous faites des changements :

```bash
cd /app
git add .
git commit -m "Description des changements"
git push
```

Render redéploiera automatiquement en 2-5 minutes !

---

## ❓ PROBLÈMES COURANTS

### Backend ne démarre pas

**Solution :** Vérifiez les logs dans Render Dashboard → Backend → Logs

Causes communes :
- MongoDB connection string incorrect
- Variables d'environnement manquantes

### Frontend ne charge pas

**Solution :** 
- Attendez 5-10 min après le déploiement initial
- Vérifiez que REACT_APP_BACKEND_URL pointe vers le bon backend

### Emails ne s'envoient pas

**Solution :**
- Utilisez un App Password Gmail (pas votre mot de passe normal)
- Vérifiez SMTP_PASSWORD dans les variables d'environnement

---

## 💰 COÛTS

**Tout est GRATUIT avec :**
- ✅ Render Free Tier (750h/mois)
- ✅ MongoDB Atlas M0 (512MB gratuit)
- ✅ SSL/HTTPS inclus

Si vous dépassez :
- Render : ~$7/mois
- MongoDB : $9/mois pour 2GB

---

## 📞 SUPPORT

Besoin d'aide ? Contactez :
- kayicom509@gmail.com

---

## 🎯 PROCHAINES ÉTAPES

1. ✅ Testez votre site
2. ✅ Ajoutez vos produits
3. ✅ Configurez les paiements
4. ✅ Testez une commande
5. ✅ Partagez votre site !

**Optionnel :**
- Achetez un nom de domaine (kayee01.com - ~10€/an)
- Connectez-le à Render (guide dans Settings → Custom Domain)

---

**Félicitations ! Votre site e-commerce est en ligne ! 🎉**

---

Pour plus de détails, consultez **RENDER_DEPLOYMENT_GUIDE.md**
