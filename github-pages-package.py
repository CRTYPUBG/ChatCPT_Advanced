#!/usr/bin/env python3
"""
GitHub Pages Package Creator
chatcpt.github.io için dosyaları hazırlar
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_github_pages_package():
    # Hedef klasör
    package_dir = "github-pages-package"
    
    # Eski package'ı temizle
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    
    print("🚀 GitHub Pages package oluşturuluyor...")
    
    # Web dosyalarını kopyala (root seviyesine)
    web_files = [
        ("web/index.html", "index.html"),
        ("web/login.html", "login.html"),
        ("web/register.html", "register.html"),
        ("web/chat.html", "chat.html"),
        ("web/test.html", "test.html"),
    ]
    
    for src, dst in web_files:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(package_dir, dst))
            print(f"✅ {src} → {dst}")
    
    # CSS klasörünü kopyala
    css_dir = os.path.join(package_dir, "css")
    os.makedirs(css_dir, exist_ok=True)
    
    css_files = [
        ("web/css/style.css", "css/style.css"),
        ("web/css/chat.css", "css/chat.css"),
    ]
    
    for src, dst in css_files:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(package_dir, dst))
            print(f"✅ {src} → {dst}")
    
    # JS klasörünü kopyala
    js_dir = os.path.join(package_dir, "js")
    os.makedirs(js_dir, exist_ok=True)
    
    js_files = [
        ("web/js/main.js", "js/main.js"),
        ("web/js/login.js", "js/login.js"),
        ("web/js/register.js", "js/register.js"),
        ("web/js/chat.js", "js/chat.js"),
        ("web/js/security.js", "js/security.js"),
    ]
    
    for src, dst in js_files:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(package_dir, dst))
            print(f"✅ {src} → {dst}")
    
    # README.md oluştur
    readme_content = """# ChatCPT Web

Modern AI Chat Assistant - GitHub Pages

## 🌐 Live Demo
https://chatcpt.github.io

## ✨ Features
- Modern dark theme design
- Responsive mobile-friendly interface
- Advanced security protection
- Turkish language support

## 🚀 Technologies
- HTML5, CSS3, JavaScript
- Modern ES6+ features
- CSS Grid & Flexbox
- Progressive Web App ready

## 📱 Pages
- **Home**: Landing page with features
- **Login**: User authentication
- **Register**: New user registration  
- **Chat**: AI chat interface
- **Test**: API testing page

## 🔒 Security
- F12 developer tools blocking
- Right-click context menu disabled
- Console protection
- Source code protection

---
© 2025 ChatCPT Web. All rights reserved.
"""
    
    with open(os.path.join(package_dir, "README.md"), "w", encoding="utf-8") as f:
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
"""
    
    with open(os.path.join(package_dir, ".gitignore"), "w") as f:
        f.write(gitignore_content)
    print("✅ .gitignore oluşturuldu")
    
    # ZIP dosyası oluştur
    zip_filename = "chatcpt-github-pages.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arc_name)
    
    print(f"\n🎉 GitHub Pages package hazır!")
    print(f"📦 ZIP dosyası: {zip_filename}")
    print(f"📁 Klasör: {package_dir}")
    
    print("\n📋 GitHub Pages Deployment Adımları:")
    print("1. GitHub'da yeni repository oluştur: 'chatcpt.github.io'")
    print("2. Repository'yi clone et")
    print("3. Bu package'daki dosyaları repository'ye kopyala")
    print("4. Git add, commit, push yap")
    print("5. Settings → Pages → Source: Deploy from branch")
    print("6. Branch: main, Folder: / (root)")
    print("7. Save → Site hazır: https://chatcpt.github.io")
    
    print("\n⚠️  Not: Backend API çalışmayacak (sadece frontend)")
    print("💡 Tam özellik için InfinityFree kullan")

if __name__ == "__main__":
    create_github_pages_package()