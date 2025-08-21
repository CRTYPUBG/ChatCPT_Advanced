# 🚀 Render Deployment - Full Stack (Recommended)

## 🎯 Render Avantajları
- ✅ **Tamamen ücretsiz** - Sınırsız
- ✅ **PHP desteği** - Backend çalışır
- ✅ **PostgreSQL database** - Ücretsiz
- ✅ **Custom domain** - chatcpt.onrender.com
- ✅ **SSL sertifikası** - Otomatik HTTPS
- ✅ **GitHub entegrasyonu** - Otomatik deploy

## 📋 Render Setup

### 1. Render Hesap
1. **render.com**'a git
2. **GitHub ile giriş** yap
3. **New** → **Web Service**

### 2. Repository Connect
- **ChatCPT_Advanced** repository'sini seç
- **Connect** tıkla

### 3. Build Settings
```
Name: chatcpt
Environment: PHP
Build Command: composer install (if needed)
Start Command: (leave empty for PHP)
```

### 4. Environment Variables
```
GEMINI_API_KEY=AIzaSyDKrMLRGaRyyUoRKKTw9ywFfBloMpMpXxx1
SUPABASE_URL=https://qaepmzfqzpawaqktorlw.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 5. Database Setup
1. **New** → **PostgreSQL**
2. **Name**: chatcpt-db
3. **Connect** to web service

### 6. Custom Domain
- **Settings** → **Custom Domains**
- Add: `chatcpt.com` (if you have)

## 🌐 Final URLs
- **Site**: `https://chatcpt.onrender.com`
- **API**: `https://chatcpt.onrender.com/api/`

## 💰 Pricing
- **Free Tier**: Tamamen ücretsiz
- **Starter**: $7/month (faster)
- **Pro**: $25/month (production)