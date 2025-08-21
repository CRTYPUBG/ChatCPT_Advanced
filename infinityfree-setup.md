# 🌐 InfinityFree Deployment Rehberi

## 1. InfinityFree Hesap Oluştur
1. **infinityfree.net** adresine git
2. **"Create Account"** tıkla
3. Email ile kayıt ol
4. **"Create Account"** → **"Create Website"**

## 2. Domain Seç
- **Subdomain**: `chatcpt.epizy.com` (ücretsiz)
- Veya kendi domain'ini bağla

## 3. Dosyaları Yükle

### A. htdocs Klasörüne Yüklenecek Dosyalar:
```
htdocs/
├── index.html          (web/index.html)
├── login.html          (web/login.html)  
├── register.html       (web/register.html)
├── chat.html           (web/chat.html)
├── test.html           (web/test.html)
├── css/
│   ├── style.css       (web/css/style.css)
│   └── chat.css        (web/css/chat.css)
├── js/
│   ├── main.js         (web/js/main.js)
│   ├── login.js        (web/js/login.js)
│   ├── register.js     (web/js/register.js)
│   ├── chat.js         (web/js/chat.js)
│   └── security.js     (web/js/security.js)
└── api/
    ├── config.php      (api/config.php)
    ├── auth.php        (api/auth.php)
    ├── chat.php        (api/chat.php)
    ├── health.php      (api/health.php)
    └── index.php       (api/index.php)
```

## 4. Database Kurulum
1. **Control Panel** → **MySQL Databases**
2. **Create Database**: `chatcpt_db`
3. **Create User**: `chatcpt_user`
4. Database bilgilerini `config.php`'ye ekle

## 5. Test Et
- Ana sayfa: `https://chatcpt.epizy.com`
- API test: `https://chatcpt.epizy.com/test.html`
- Login: `https://chatcpt.epizy.com/login.html`

## 6. SSL Sertifikası
InfinityFree otomatik SSL verir, 24 saat içinde aktif olur.

---

**🎯 Avantajlar:**
- ✅ Tamamen ücretsiz
- ✅ PHP + MySQL destekli  
- ✅ Kolay kurulum
- ✅ Stabil hosting
- ✅ SSL sertifikası