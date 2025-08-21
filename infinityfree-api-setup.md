# 🚀 InfinityFree API Setup

## 📋 Adım Adım Kurulum

### 1. InfinityFree Hesap Oluştur
1. **infinityfree.net** adresine git
2. **"Create Account"** tıkla
3. Email ile kayıt ol
4. Email'ini doğrula

### 2. Website Oluştur
1. **"Create Account"** → **"Create Website"**
2. **Subdomain seç**: `chatcpt-api` (chatcpt-api.epizy.com olacak)
3. **Create Account** tıkla

### 3. File Manager'a Git
1. **Control Panel** → **File Manager**
2. **htdocs** klasörüne git
3. Varsayılan dosyaları sil (index.html, etc.)

### 4. API Dosyalarını Yükle
`chatcpt-infinityfree.zip` dosyasından sadece `api/` klasörünü yükle:

```
htdocs/
├── api/
│   ├── config.php
│   ├── auth.php
│   ├── chat.php
│   ├── health.php
│   ├── index.php
│   └── .htaccess
└── index.html (API ana sayfası)
```

### 5. MySQL Database Oluştur
1. **Control Panel** → **MySQL Databases**
2. **Create Database**: `chatcpt_db`
3. **Create User**: `chatcpt_user`
4. **Password**: Güçlü şifre oluştur
5. **Add User to Database** → **All Privileges**

### 6. Database Bilgilerini Güncelle
`api/config.php` dosyasını düzenle:

```php
$DB_HOST = 'sql200.epizy.com';  // InfinityFree MySQL host
$DB_NAME = 'epiz_xxxxx_chatcpt'; // Senin database adın
$DB_USER = 'epiz_xxxxx';         // Senin database kullanıcın
$DB_PASS = 'senin_sifren';       // Senin database şifren
```

### 7. CORS Ayarları
`api/config.php`'de CORS'u GitHub Pages için ayarla:

```php
header('Access-Control-Allow-Origin: https://chatcpt.github.io');
```

### 8. Test Et
1. **API Health**: `https://chatcpt-api.epizy.com/api/health.php`
2. **Test sayfası**: `https://chatcpt.github.io/test.html`

## 🔧 Troubleshooting

### API 500 Error
- Database bilgilerini kontrol et
- PHP syntax hatalarını kontrol et
- Error logs'u incele

### CORS Error
- `config.php`'de CORS headers'ı kontrol et
- GitHub Pages domain'ini doğru yazdığından emin ol

### Database Connection Error
- MySQL host, database adı, kullanıcı adı, şifre kontrol et
- Database user'ın tüm yetkilerinin olduğundan emin ol

## 🎯 Final Test
1. **Frontend**: https://chatcpt.github.io
2. **API**: https://chatcpt-api.epizy.com/api/health.php
3. **Register**: Yeni kullanıcı oluştur
4. **Login**: Giriş yap
5. **Chat**: AI ile sohbet et

---

**🎉 Tamamlandığında tam özellikli ChatCPT Web uygulaması hazır olacak!**