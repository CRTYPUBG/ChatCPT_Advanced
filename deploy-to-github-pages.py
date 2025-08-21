#!/usr/bin/env python3
"""
ChatCPT GitHub Pages Deployment Script
chatcpt.github.io repository'sine dosyaları hazırlar
"""

import os
import shutil
import subprocess
from pathlib import Path

def deploy_to_github_pages():
    print("🚀 ChatCPT GitHub Pages deployment başlıyor...")
    
    # GitHub Pages için dosyaları hazırla
    pages_dir = "chatcpt-github-pages"
    
    # Eski klasörü temizle
    if os.path.exists(pages_dir):
        shutil.rmtree(pages_dir)
    
    os.makedirs(pages_dir)
    
    print("📁 Dosyalar kopyalanıyor...")
    
    # Web dosyalarını root seviyesine kopyala
    files_to_copy = [
        # HTML files
        ("web/index.html", "index.html"),
        ("web/login.html", "login.html"),
        ("web/register.html", "register.html"),
        ("web/chat.html", "chat.html"),
        ("web/test.html", "test.html"),
        
        # Config file
        ("web/js/config.js", "js/config.js"),
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            dst_path = os.path.join(pages_dir, dst)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src, dst_path)
            print(f"✅ {src} → {dst}")
    
    # CSS klasörünü kopyala
    css_src = "web/css"
    css_dst = os.path.join(pages_dir, "css")
    if os.path.exists(css_src):
        shutil.copytree(css_src, css_dst)
        print("✅ CSS klasörü kopyalandı")
    
    # JS klasörünü kopyala
    js_src = "web/js"
    js_dst = os.path.join(pages_dir, "js")
    if os.path.exists(js_src):
        if os.path.exists(js_dst):
            shutil.rmtree(js_dst)
        shutil.copytree(js_src, js_dst)
        print("✅ JS klasörü kopyalandı")
    
    # README.md oluştur
    readme_content = """# ChatCPT Web

🤖 Modern AI Chat Assistant

## 🌐 Live Demo
**https://chatcpt.github.io**

## ✨ Features
- 🎨 Modern dark theme design
- 📱 Responsive mobile-friendly interface
- 🔒 Advanced security protection
- 🇹🇷 Turkish language support
- 🤖 AI-powered chat assistant
- 👤 User authentication system

## 🚀 Technologies
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Backend API**: PHP (hosted separately)
- **Database**: MySQL
- **Hosting**: GitHub Pages + InfinityFree API
- **Security**: F12 blocking, right-click protection

## 📱 Pages
- **Home** (`/`): Landing page with features
- **Login** (`/login.html`): User authentication
- **Register** (`/register.html`): New user registration  
- **Chat** (`/chat.html`): AI chat interface
- **Test** (`/test.html`): API testing page

## 🔒 Security Features
- F12 developer tools blocking
- Right-click context menu disabled
- Console protection and warnings
- Source code protection
- Input validation and sanitization

## 🌐 API Integration
- **Frontend**: GitHub Pages (Static hosting)
- **Backend**: InfinityFree PHP API
- **CORS**: Configured for cross-origin requests
- **Authentication**: JWT token-based

## 📊 Performance
- ⚡ Fast loading with GitHub Pages CDN
- 📱 Mobile-optimized responsive design
- 🔄 Progressive Web App features
- 🎯 SEO optimized

## 🛠️ Development
```bash
# Clone repository
git clone https://github.com/CRTYPUBG/chatcpt.github.io.git

# Open in browser
open index.html
```

## 📞 Support
- 🐛 **Issues**: [GitHub Issues](https://github.com/CRTYPUBG/chatcpt.github.io/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/CRTYPUBG/chatcpt.github.io/discussions)

---

**© 2025 ChatCPT Web. All rights reserved.**

Built with ❤️ by CRTY Apps
"""
    
    with open(os.path.join(pages_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("✅ README.md oluşturuldu")
    
    # .gitignore oluştur
    gitignore_content = """# Dependencies
node_modules/
*.log

# Build files
dist/
build/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp

# Local development
.env
database.sqlite
"""
    
    with open(os.path.join(pages_dir, ".gitignore"), "w") as f:
        f.write(gitignore_content)
    print("✅ .gitignore oluşturuldu")
    
    # CNAME dosyası oluştur (custom domain için)
    # with open(os.path.join(pages_dir, "CNAME"), "w") as f:
    #     f.write("chatcpt.com")
    # print("✅ CNAME oluşturuldu")
    
    print(f"\n🎉 GitHub Pages dosyaları hazır!")
    print(f"📁 Klasör: {pages_dir}")
    
    print("\n📋 Deployment Adımları:")
    print("1. Terminal'de şu komutları çalıştır:")
    print(f"   cd {pages_dir}")
    print("   git init")
    print("   git add .")
    print('   git commit -m "Initial commit - ChatCPT Web"')
    print("   git branch -M main")
    print("   git remote add origin https://github.com/CRTYPUBG/chatcpt.github.io.git")
    print("   git push -u origin main")
    print("\n2. GitHub'da Settings → Pages → Source: Deploy from branch")
    print("3. Branch: main, Folder: / (root)")
    print("4. Save → Site hazır: https://chatcpt.github.io")
    
    print("\n🔧 API Setup (InfinityFree):")
    print("1. infinityfree.net'te hesap oluştur")
    print("2. Subdomain: chatcpt-api.epizy.com")
    print("3. api/ klasörünü yükle")
    print("4. MySQL database oluştur")
    print("5. config.php'de database bilgilerini güncelle")

if __name__ == "__main__":
    deploy_to_github_pages()