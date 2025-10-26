# Kayee01 E-commerce - Deployment Guide for Render.com

## 🚀 Complete Deployment Guide

This guide will help you deploy your Kayee01 e-commerce site completely on Render.com for FREE.

---

## 📋 Prerequisites

1. **GitHub Account** (free)
2. **Render Account** (free) - Sign up at https://render.com
3. **MongoDB Atlas Account** (free) - Sign up at https://www.mongodb.com/cloud/atlas/register

---

## 🗄️ Step 1: Setup MongoDB Atlas (5 minutes)

### 1.1 Create MongoDB Cluster

1. Go to https://www.mongodb.com/cloud/atlas/register
2. Sign up with Google or Email
3. Create a **FREE** cluster:
   - Choose **M0 Sandbox** (FREE forever)
   - Region: **Frankfurt** or closest to you
   - Cluster Name: `kayee01-cluster`
4. Click **Create Cluster** (takes 1-3 minutes)

### 1.2 Create Database User

1. Click **Database Access** (left menu)
2. Click **Add New Database User**
3. Username: `kayee01_user`
4. Password: Generate a secure password (SAVE IT!)
5. Database User Privileges: **Read and write to any database**
6. Click **Add User**

### 1.3 Whitelist IP Addresses

1. Click **Network Access** (left menu)
2. Click **Add IP Address**
3. Click **Allow Access from Anywhere** (0.0.0.0/0)
4. Click **Confirm**

### 1.4 Get Connection String

1. Click **Database** (left menu)
2. Click **Connect** on your cluster
3. Choose **Connect your application**
4. Copy the connection string:
   ```
   mongodb+srv://kayee01_user:<password>@kayee01-cluster.xxxxx.mongodb.net/kayee01_db?retryWrites=true&w=majority
   ```
5. Replace `<password>` with your actual password
6. **SAVE THIS STRING** - You'll need it for Render

---

## 🐙 Step 2: Push Code to GitHub (10 minutes)

### 2.1 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `kayee01-ecommerce`
3. **Private** repository (recommended)
4. Don't initialize with README
5. Click **Create repository**

### 2.2 Push Your Code

I've prepared everything. You just need to run these commands:

```bash
cd /app
git init
git add .
git commit -m "Initial commit - Kayee01 e-commerce ready for Render"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/kayee01-ecommerce.git
git push -u origin main
```

**Replace `YOUR_USERNAME` with your GitHub username**

---

## 🎨 Step 3: Deploy on Render (15 minutes)

### 3.1 Connect GitHub to Render

1. Go to https://dashboard.render.com
2. Click **New +** → **Blueprint**
3. Click **Connect GitHub**
4. Authorize Render to access your GitHub
5. Select **kayee01-ecommerce** repository

### 3.2 Configure Environment Variables

Render will auto-detect the `render.yaml` file. Now add these environment variables:

#### For Backend Service:

1. Click on **kayee01-backend** service
2. Go to **Environment** tab
3. Add these variables:

```
MONGO_URL=mongodb+srv://kayee01_user:YOUR_PASSWORD@kayee01-cluster.xxxxx.mongodb.net/kayee01_db?retryWrites=true&w=majority

SMTP_USER=kayee01.shop@gmail.com
SMTP_PASSWORD=your_gmail_app_password

STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key

PLISIO_API_KEY=your_plisio_api_key
```

**Note:** 
- Replace MongoDB URL with your actual connection string from Step 1
- For Gmail: Use App Password (not regular password)
  - Go to: https://myaccount.google.com/apppasswords
  - Generate app password for "Mail"
- Stripe/Plisio keys are optional initially (add later when ready)

### 3.3 Deploy

1. Click **Apply** or **Create Blueprint**
2. Render will:
   - ✅ Install dependencies
   - ✅ Build frontend
   - ✅ Start backend
   - ✅ Assign HTTPS URLs

**Deployment takes 5-10 minutes on first run.**

---

## 🎉 Step 4: Access Your Site

### Your URLs will be:

**Frontend (Main Site):**
```
https://kayee01-frontend.onrender.com
```

**Backend API:**
```
https://kayee01-backend.onrender.com
```

### Test Your Site:

1. Visit your frontend URL
2. Browse products
3. Add to cart
4. Test checkout (use Stripe test card: 4242 4242 4242 4242)

### Admin Access:

```
URL: https://kayee01-frontend.onrender.com/admin/login
Email: kayicom509@gmail.com
Password: Admin123!
```

---

## 🔧 Step 5: Import Initial Data

### 5.1 Seed Products (if database is empty)

1. Go to Render Dashboard
2. Click **kayee01-backend** service
3. Go to **Shell** tab
4. Run:

```bash
cd backend
python create_sample_data.py
```

This will create:
- Sample products
- Categories
- Admin user

---

## ⚙️ Configuration

### Gmail SMTP Setup (for emails)

1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification**
3. Go to https://myaccount.google.com/apppasswords
4. Generate password for "Mail"
5. Use this password in `SMTP_PASSWORD` env var

### Stripe Setup

1. Get your keys from https://dashboard.stripe.com/test/apikeys
2. Add to Render environment variables
3. Restart backend service

### Plisio Setup (Crypto payments)

1. Sign up at https://plisio.net
2. Get API key from dashboard
3. Add to Render environment variables

---

## 🔄 Updates and Maintenance

### To Update Your Site:

1. Make changes in your code
2. Commit and push to GitHub:
```bash
git add .
git commit -m "Your update message"
git push
```
3. Render will **auto-deploy** in 2-5 minutes!

### View Logs:

1. Go to Render Dashboard
2. Click on your service
3. Go to **Logs** tab

---

## 💰 Pricing

### Current Setup (FREE):

- ✅ Frontend hosting: **FREE**
- ✅ Backend hosting: **FREE** (750 hours/month)
- ✅ MongoDB Atlas: **FREE** (512MB storage)
- ✅ SSL/HTTPS: **FREE**
- ✅ Custom domain support: **FREE**

### If You Exceed Free Limits:

**Render charges only if you exceed:**
- 750 hours/month (your site runs 24/7 = 720 hours)
- Overages: ~$0.02/hour (~$7/month if constantly active)

**MongoDB Atlas:**
- Free tier: 512MB storage
- Paid tier: $9/month for 2GB

**For most e-commerce sites starting out, FREE tier is sufficient!**

---

## 🌐 Add Custom Domain (Optional)

### To use kayee01.com instead of .onrender.com:

1. Buy domain from Namecheap/Hostinger (~$10/year)
2. In Render Dashboard:
   - Click **kayee01-frontend** service
   - Go to **Settings** → **Custom Domain**
   - Add `kayee01.com`
3. Update DNS records (Render will show instructions)
4. SSL certificate automatically generated

---

## 📞 Support

### Common Issues:

**Build Failed:**
- Check logs in Render dashboard
- Verify all dependencies in requirements.txt and package.json

**Database Connection Error:**
- Verify MongoDB connection string
- Check database user permissions
- Ensure IP whitelist includes 0.0.0.0/0

**Email Not Sending:**
- Verify Gmail App Password (not regular password)
- Check SMTP settings

**Payment Not Working:**
- Add Stripe/Plisio API keys
- Use test keys for testing

---

## ✅ Checklist

- [ ] MongoDB Atlas cluster created
- [ ] Database user created
- [ ] Connection string saved
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Services deployed on Render
- [ ] Environment variables configured
- [ ] Frontend accessible
- [ ] Backend API responding
- [ ] Admin login working
- [ ] Test order placed
- [ ] Emails sending

---

## 🎯 Next Steps

1. **Test everything thoroughly**
2. **Add real products** via admin panel
3. **Configure payment gateways** (Stripe, Plisio)
4. **Setup email templates** if needed
5. **Consider custom domain** when ready

---

**Your site is now live at:**
- **Frontend:** https://kayee01-frontend.onrender.com
- **Admin:** https://kayee01-frontend.onrender.com/admin/login

**Congratulations! Your e-commerce site is deployed! 🎉**

---

## 📧 Need Help?

Contact me if you encounter any issues during deployment.

**Built with ❤️ for Kayee01**
