# 🚀 Railway Deployment - Full Stack

## 🎯 Railway Avantajları
- ✅ **PHP desteği** - Backend çalışır
- ✅ **MySQL database** - Ücretsiz
- ✅ **Custom domain** - chatcpt.up.railway.app
- ✅ **SSL sertifikası** - Otomatik HTTPS
- ✅ **GitHub entegrasyonu** - Otomatik deploy

## 📋 Railway Setup

### 1. Railway Hesap
1. **railway.app**'e git
2. **GitHub ile giriş** yap
3. **New Project** → **Deploy from GitHub repo**

### 2. Repository Seç
- **ChatCPT_Advanced** repository'sini seç
- **Deploy** tıkla

### 3. Environment Variables
Railway dashboard'da:
```
GEMINI_API_KEY=AIzaSyDKrMLRGaRyyUoRKKTw9ywFfBloMpMpXxx1
SUPABASE_URL=https://qaepmzfqzpawaqktorlw.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 4. Database Setup
1. **Add Service** → **MySQL**
2. **Connect** to your app
3. Database URL otomatik eklenir

### 5. Custom Domain (Opsiyonel)
- **Settings** → **Domains**
- **Custom Domain** ekle: `chatcpt.com`

## 🌐 Final URL
- **Site**: `https://chatcpt.up.railway.app`
- **API**: `https://chatcpt.up.railway.app/api/`

## 💰 Pricing
- **Ücretsiz**: $5 credit/month
- **Hobby**: $5/month unlimited
- **Pro**: $20/month