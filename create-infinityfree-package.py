#!/usr/bin/env python3
"""
InfinityFree Deployment Package Creator
Bu script InfinityFree'ye yüklenecek dosyaları hazırlar
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_infinityfree_package():
    # Hedef klasör
    package_dir = "infinityfree-package"
    
    # Eski package'ı temizle
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    
    print("🚀 InfinityFree package oluşturuluyor...")
    
    # Web dosyalarını kopyala
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
    
    # API klasörünü kopyala
    api_dir = os.path.join(package_dir, "api")
    os.makedirs(api_dir, exist_ok=True)
    
    api_files = [
        ("api/config.php", "api/config.php"),
        ("api/auth.php", "api/auth.php"),
        ("api/chat.php", "api/chat.php"),
        ("api/health.php", "api/health.php"),
        ("api/index.php", "api/index.php"),
        ("api/.htaccess", "api/.htaccess"),
    ]
    
    for src, dst in api_files:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(package_dir, dst))
            print(f"✅ {src} → {dst}")
    
    # ZIP dosyası oluştur
    zip_filename = "chatcpt-infinityfree.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arc_name)
    
    print(f"\n🎉 Package hazır!")
    print(f"📦 ZIP dosyası: {zip_filename}")
    print(f"📁 Klasör: {package_dir}")
    
    print("\n📋 InfinityFree Deployment Adımları:")
    print("1. infinityfree.net'te hesap oluştur")
    print("2. Yeni website oluştur")
    print("3. File Manager'a git")
    print("4. htdocs klasörüne ZIP'i yükle ve çıkart")
    print("5. MySQL database oluştur")
    print("6. api/config.php'de database bilgilerini güncelle")
    print("7. Test et: https://yoursite.epizy.com/test.html")

if __name__ == "__main__":
    create_infinityfree_package()