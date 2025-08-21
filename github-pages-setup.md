# 🌐 GitHub Pages Deployment Rehberi

## 🚀 Hızlı GitHub Pages Kurulumu

### 1. Repository Ayarları
1. GitHub'da repository'ne git: `ChatCPT_Advanced`
2. **Settings** → **Pages**
3. **Source**: Deploy from a branch
4. **Branch**: `main`
5. **Folder**: `/ (root)` veya `/web`

### 2. Web Klasörünü Root'a Taşı
```bash
# Web dosyalarını root'a kopyala
git checkout -b gh-pages
cp -r web/* .
git add .
git commit -m "Setup GitHub Pages"
git push origin gh-pages
```

### 3. GitHub Pages Branch Seç
- **Settings** → **Pages**
- **Branch**: `gh-pages`
- **Save**

### 4. Site URL'i
- `https://crtypubg.github.io/ChatCPT_Advanced/`

## ⚠️ Sınırlamalar
- ❌ PHP çalışmaz (sadece static HTML/CSS/JS)
- ❌ Backend API yok
- ❌ Database yok
- ✅ Frontend tamamen çalışır
- ✅ Ücretsiz ve hızlı

## 🔧 Alternatif: GitHub Pages + External API
1. **Frontend**: GitHub Pages
2. **Backend**: InfinityFree PHP API
3. **CORS**: API'de ayarla

---

**🎯 Önerilen Çözüm: InfinityFree**
- ✅ Tam PHP desteği
- ✅ MySQL database
- ✅ Ücretsiz hosting
- ✅ Kolay kurulum