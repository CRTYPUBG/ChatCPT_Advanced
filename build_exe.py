#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatCPT Desktop Build Script
Standalone exe oluşturmak için PyInstaller script'i
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def build_exe():
    """Exe dosyasını oluştur"""
    print("🚀 ChatCPT Desktop exe oluşturuluyor...")
    
    # PyInstaller komutu
    cmd = [
        "pyinstaller",
        "--onefile",                    # Tek dosya
        "--windowed",                   # Console penceresi gösterme
        "--name=ChatCPT_Desktop",       # Exe adı
        "--icon=ui/icon.ico" if os.path.exists("ui/icon.ico") else "",
        "--add-data=server.js;.",       # Server dosyasını dahil et
        "--add-data=package.json;.",    # Package.json'ı dahil et
        "--add-data=.env;.",            # .env dosyasını dahil et
        "--add-data=ui;ui",             # UI klasörünü dahil et
        "--add-data=node_modules;node_modules" if os.path.exists("node_modules") else "",
        "--hidden-import=PyQt6.QtWebEngineWidgets",
        "--hidden-import=PyQt6.QtOpenGL",
        "--hidden-import=PyQt6.QtOpenGLWidgets", 
        "--hidden-import=requests",
        "--collect-all=PyQt6",
        "--collect-all=PyQt6.QtWebEngineWidgets",
        "--collect-all=PyQt6.QtOpenGL",
        "--collect-all=PyQt6.QtOpenGLWidgets",
        "main.py"
    ]
    
    # Boş parametreleri temizle
    cmd = [arg for arg in cmd if arg]
    
    try:
        # Build işlemini başlat
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build başarılı!")
        
        # Dist klasöründeki exe'yi ana dizine kopyala
        exe_path = Path("dist/ChatCPT_Desktop.exe")
        if exe_path.exists():
            shutil.copy2(exe_path, "ChatCPT_Desktop.exe")
            print(f"✅ Exe dosyası hazır: {os.path.abspath('ChatCPT_Desktop.exe')}")
            
            # Geçici dosyaları temizle
            if os.path.exists("build"):
                shutil.rmtree("build")
            if os.path.exists("dist"):
                shutil.rmtree("dist")
            if os.path.exists("ChatCPT_Desktop.spec"):
                os.remove("ChatCPT_Desktop.spec")
            print("🧹 Geçici dosyalar temizlendi")
        else:
            print("❌ Exe dosyası oluşturulamadı!")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build hatası: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")

def check_dependencies():
    """Gerekli bağımlılıkları kontrol et"""
    print("🔍 Bağımlılıklar kontrol ediliyor...")
    
    required_files = [
        "main.py",
        "server.js",
        "package.json",
        ".env"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Eksik dosyalar: {', '.join(missing_files)}")
        return False
    
    # Node modules kontrol et
    if not os.path.exists("node_modules"):
        print("⚠️  node_modules bulunamadı. npm install çalıştırılıyor...")
        try:
            subprocess.run(["npm", "install"], check=True)
            print("✅ npm install tamamlandı")
        except:
            print("❌ npm install başarısız. Node.js kurulu olduğundan emin olun.")
            return False
    
    print("✅ Tüm bağımlılıklar mevcut")
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("🏗️  ChatCPT Desktop Build Tool")
    print("=" * 50)
    
    if check_dependencies():
        build_exe()
    else:
        print("❌ Build işlemi iptal edildi")
        sys.exit(1)
    
    print("=" * 50)
    print("✨ Build işlemi tamamlandı!")
    print("=" * 50)