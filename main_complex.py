#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ChatCPT Desktop Application
Windows için optimize edilmiş PyQt6 masaüstü uygulaması
"""

import sys
import os
import json
import subprocess
import threading
import time
import requests
import webbrowser
from pathlib import Path

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QPushButton, QLabel, QTextEdit, QLineEdit,
                            QMessageBox, QSystemTrayIcon, QMenu, QSplashScreen,
                            QProgressBar, QFrame, QScrollArea, QTabWidget, QGraphicsDropShadowEffect,
                            QGraphicsBlurEffect, QGraphicsColorizeEffect, QGraphicsOpacityEffect)
from PyQt6.QtCore import (QThread, pyqtSignal, QTimer, Qt, QSize, QUrl, QPropertyAnimation, 
                         QEasingCurve, QRect, QSequentialAnimationGroup, QParallelAnimationGroup,
                         QVariantAnimation, QAbstractAnimation)
from PyQt6.QtGui import QIcon, QPixmap, QFont, QPalette, QColor, QDesktopServices
from PyQt6.QtWebEngineWidgets import QWebEngineView

class ServerThread(QThread):
    """Node.js server'ını arka planda çalıştıran thread"""
    server_started = pyqtSignal()
    server_error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.server_process = None
        self.running = False
        
    def run(self):
        try:
            # Node.js server'ını başlat
            node_path = self.find_node()
            if not node_path:
                self.server_error.emit("Node.js bulunamadı!")
                return
                
            # Server'ı başlat
            cmd = [node_path, "server.js"]
            self.server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.getcwd(),
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            
            self.running = True
            
            # Server'ın başlamasını bekle
            time.sleep(3)
            
            # Server'ın çalışıp çalışmadığını kontrol et
            if self.check_server():
                self.server_started.emit()
            else:
                self.server_error.emit("Server başlatılamadı!")
                
        except Exception as e:
            self.server_error.emit(f"Server hatası: {str(e)}")
    
    def find_node(self):
        """Node.js executable'ını bul"""
        # Önce bundled node'u kontrol et
        if getattr(sys, 'frozen', False):
            # PyInstaller ile paketlenmiş
            bundle_dir = sys._MEIPASS
            node_path = os.path.join(bundle_dir, 'node', 'node.exe')
            if os.path.exists(node_path):
                return node_path
        
        # Sistem PATH'inde node'u ara
        import shutil
        return shutil.which('node')
    
    def check_server(self):
        """Server'ın çalışıp çalışmadığını kontrol et"""
        try:
            response = requests.get('http://localhost:3000', timeout=5)
            return True
        except:
            return False
    
    def stop_server(self):
        """Server'ı durdur"""
        if self.server_process:
            self.server_process.terminate()
            self.running = False

class ChatCPTApp(QMainWindow):
    """Ana uygulama penceresi"""
    
    def __init__(self):
        super().__init__()
        self.server_thread = None
        self.init_ui()
        self.setup_tray()
        self.start_server()
        
    def init_ui(self):
        """UI'ı başlat"""
        self.setWindowTitle("ChatCPT Desktop")
        self.setGeometry(100, 100, 1200, 800)
        
        # Icon ayarla
        if os.path.exists("ui/icon.ico"):
            self.setWindowIcon(QIcon("ui/icon.ico"))
        
        # Ana widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Başlık
        title_label = QLabel("🚀 ChatCPT Desktop")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Başlığa gelişmiş efektler ekle
        QTimer.singleShot(500, lambda: self.add_pulse_animation(title_label))
        QTimer.singleShot(1000, lambda: self.add_typewriter_effect(title_label, "🚀 ChatCPT Desktop", 150))
        QTimer.singleShot(2000, lambda: self.add_advanced_glow_effect(title_label, QColor(0, 255, 204)))
        
        # Tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Web view tab
        self.web_view = QWebEngineView()
        self.tab_widget.addTab(self.web_view, "Web Arayüz")
        
        # Kontrol paneli tab
        control_panel = self.create_control_panel()
        self.tab_widget.addTab(control_panel, "Kontrol Paneli")
        
        # Status bar
        self.statusBar().showMessage("Server başlatılıyor...")
        
        # Dark theme uygula
        self.apply_dark_theme()
        
        # Ana pencereye fade-in efekti
        self.add_fade_effect(central_widget, 500)
        
        # GPU hızlandırmayı etkinleştir
        self.enable_gpu_acceleration()
        
        # Özel durumlarda gökkuşağı efekti (server başarıyla başlatıldığında aktif olacak)
        self.rainbow_mode = False
        
    def create_control_panel(self):
        """Modern kontrol paneli oluştur"""
        widget = QWidget()
        widget.setObjectName("control_panel")
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Server durumu kartı
        status_frame = QFrame()
        status_frame.setFrameStyle(QFrame.Shape.Box)
        status_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(69, 123, 157, 0.2), stop:1 rgba(29, 53, 87, 0.3));
                border: 2px solid #457b9d;
                border-radius: 12px;
                padding: 16px;
                margin: 8px;
            }
        """)
        status_layout = QVBoxLayout(status_frame)
        
        status_title = QLabel("🖥️ Server Durumu")
        status_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #a8dadc; margin-bottom: 8px;")
        status_layout.addWidget(status_title)
        
        self.server_status = QLabel("⏳ Başlatılıyor...")
        self.server_status.setObjectName("status")
        self.server_status.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(255, 193, 7, 0.2), stop:1 rgba(255, 152, 0, 0.2));
            color: #ffc107;
            border: 1px solid #ffc107;
        """)
        status_layout.addWidget(self.server_status)
        
        # Server durumuna nefes alma efekti ekle
        QTimer.singleShot(1000, lambda: self.add_breathing_animation(self.server_status))
        
        layout.addWidget(status_frame)
        
        # Kontrol butonları
        button_frame = QFrame()
        button_frame.setFrameStyle(QFrame.Shape.Box)
        button_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(69, 123, 157, 0.2), stop:1 rgba(29, 53, 87, 0.3));
                border: 2px solid #457b9d;
                border-radius: 12px;
                padding: 16px;
                margin: 8px;
            }
        """)
        button_layout_main = QVBoxLayout(button_frame)
        
        button_title = QLabel("🎮 Kontroller")
        button_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #a8dadc; margin-bottom: 12px;")
        button_layout_main.addWidget(button_title)
        
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.start_btn = QPushButton("▶️ Başlat")
        self.start_btn.setObjectName("start_btn")
        self.start_btn.clicked.connect(self.start_server)
        self.start_btn.setEnabled(False)
        self.add_button_effects(self.start_btn)
        self.add_size_hover_animation(self.start_btn)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ Durdur")
        self.stop_btn.clicked.connect(self.stop_server)
        self.add_button_effects(self.stop_btn)
        self.add_size_hover_animation(self.stop_btn)
        button_layout.addWidget(self.stop_btn)
        
        self.browser_btn = QPushButton("🌐 Tarayıcı")
        self.browser_btn.setObjectName("browser_btn")
        self.browser_btn.clicked.connect(self.open_in_browser)
        self.browser_btn.setEnabled(False)
        self.add_button_effects(self.browser_btn)
        self.add_size_hover_animation(self.browser_btn)
        button_layout.addWidget(self.browser_btn)
        
        button_layout_main.addLayout(button_layout)
        layout.addWidget(button_frame)
        
        # Log alanı
        log_frame = QFrame()
        log_frame.setFrameStyle(QFrame.Shape.Box)
        log_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(69, 123, 157, 0.2), stop:1 rgba(29, 53, 87, 0.3));
                border: 2px solid #457b9d;
                border-radius: 12px;
                padding: 16px;
                margin: 8px;
            }
        """)
        log_layout = QVBoxLayout(log_frame)
        
        log_title = QLabel("📋 Sistem Logları")
        log_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #a8dadc; margin-bottom: 8px;")
        log_layout.addWidget(log_title)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(180)
        self.log_text.setPlaceholderText("Sistem logları burada görünecek...")
        log_layout.addWidget(self.log_text)
        
        # Log alanına hafif blur efekti (boşken)
        QTimer.singleShot(2000, lambda: self.add_progressive_blur(self.log_text, 3))
        
        layout.addWidget(log_frame)
        layout.addStretch()
        
        return widget
    
    def apply_dark_theme(self):
        """Modern dark theme uygula"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 #1a1a2e, stop:1 #16213e);
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QTabWidget {
                background: transparent;
                border: none;
            }
            
            QTabWidget::pane {
                border: 2px solid #3d5a80;
                border-radius: 12px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(29, 53, 87, 0.9), stop:1 rgba(69, 123, 157, 0.8));
                margin-top: -2px;
            }
            
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #457b9d, stop:1 #1d3557);
                color: #ffffff;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                font-weight: 600;
                font-size: 11px;
                min-width: 120px;
                border: 2px solid #3d5a80;
                border-bottom: none;
            }
            
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f1faee, stop:1 #a8dadc);
                color: #1d3557;
                font-weight: bold;
                border-color: #a8dadc;
            }
            
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c9bd1, stop:1 #457b9d);
            }
            
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:1 #d62828);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 12px;
                font-weight: bold;
                font-size: 11px;
                min-height: 20px;
                box-shadow: 0 4px 15px rgba(230, 57, 70, 0.3);
                transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
            }
            
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f77f00, stop:1 #e63946);
                transform: translateY(-3px) scale(1.02);
                box-shadow: 0 8px 25px rgba(247, 127, 0, 0.4);
                border: 2px solid rgba(247, 127, 0, 0.5);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d62828, stop:1 #ba181b);
                transform: translateY(1px) scale(0.98);
                box-shadow: 0 2px 8px rgba(214, 40, 40, 0.6);
                transition: all 0.1s ease;
            }
            
            QPushButton:focus {
                outline: none;
                border: 2px solid #0078d4;
                box-shadow: 0 0 0 3px rgba(0, 120, 212, 0.3);
            }
            
            QPushButton:disabled {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c757d, stop:1 #495057);
                color: #adb5bd;
            }
            
            QPushButton#start_btn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d6a4f, stop:1 #1b4332);
            }
            
            QPushButton#start_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #40916c, stop:1 #2d6a4f);
            }
            
            QPushButton#browser_btn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3a86ff, stop:1 #1e6091);
            }
            
            QPushButton#browser_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5aa3ff, stop:1 #3a86ff);
            }
            
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(13, 27, 42, 0.9), stop:1 rgba(27, 38, 59, 0.9));
                color: #f8f9fa;
                border: 2px solid #457b9d;
                border-radius: 12px;
                padding: 12px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10px;
                selection-background-color: #457b9d;
                transition: all 0.3s ease;
            }
            
            QTextEdit:focus {
                border: 2px solid #0078d4;
                box-shadow: 0 0 0 3px rgba(0, 120, 212, 0.2);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 120, 212, 0.1), stop:1 rgba(27, 38, 59, 0.9));
            }
            
            QTextEdit:hover {
                border: 2px solid #6c9bd1;
                box-shadow: 0 4px 12px rgba(108, 155, 209, 0.2);
            }
            
            QLabel {
                color: #f8f9fa;
                font-weight: 500;
            }
            
            QLabel#title {
                color: #f1faee;
                font-size: 28px;
                font-weight: bold;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                margin: 20px;
                padding: 10px;
            }
            
            QLabel#status {
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1d3557, stop:1 #457b9d);
                color: #f8f9fa;
                border-top: 2px solid #3d5a80;
                font-weight: 500;
            }
            
            QWidget#control_panel {
                background: transparent;
                border-radius: 8px;
                padding: 16px;
            }
            
            QScrollArea {
                border: none;
                background: transparent;
            }
            
            QScrollBar:vertical {
                background: rgba(69, 123, 157, 0.3);
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #457b9d, stop:1 #1d3557);
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6c9bd1, stop:1 #457b9d);
            }
        """)
        
        # Görsel efektleri uygula
        self.apply_visual_effects()
    
    def apply_visual_effects(self):
        """Modern görsel efektler uygula"""
        # Ana pencereye gölge efekti
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(20)
        shadow_effect.setXOffset(0)
        shadow_effect.setYOffset(10)
        shadow_effect.setColor(QColor(0, 0, 0, 80))
        
        # Tab widget'a gölge efekti
        if hasattr(self, 'tab_widget'):
            tab_shadow = QGraphicsDropShadowEffect()
            tab_shadow.setBlurRadius(15)
            tab_shadow.setXOffset(0)
            tab_shadow.setYOffset(5)
            tab_shadow.setColor(QColor(0, 0, 0, 60))
            self.tab_widget.setGraphicsEffect(tab_shadow)
    
    def add_button_effects(self, button):
        """Butonlara hover efektleri ekle"""
        # Gölge efekti
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 40))
        button.setGraphicsEffect(shadow)
        
        # Hover animasyonu için opacity efekti hazırla
        self.setup_button_animation(button)
    
    def setup_button_animation(self, button):
        """Gelişmiş buton animasyonları ve efektleri"""
        # Hover animasyonu için property animation
        self.setup_hover_animation(button)
        
        # Mouse enter/leave olayları
        original_enter = button.enterEvent
        original_leave = button.leaveEvent
        
        def enhanced_enter(event):
            # Hover efekti - yumuşak renk geçişi ve büyütme
            self.animate_button_hover(button, True)
            original_enter(event)
        
        def enhanced_leave(event):
            # Normal duruma dön
            self.animate_button_hover(button, False)
            original_leave(event)
        
        button.enterEvent = enhanced_enter
        button.leaveEvent = enhanced_leave
    
    def setup_hover_animation(self, button):
        """Hover animasyonu ayarla"""
        # Buton için özel hover stilleri
        button.setStyleSheet(button.styleSheet() + """
            QPushButton {
                transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
                transform-origin: center;
            }
            QPushButton:hover {
                transform: scale(1.05) translateY(-2px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }
            QPushButton:pressed {
                transform: scale(0.98) translateY(1px);
                transition: all 0.1s ease;
            }
        """)
    
    def animate_button_hover(self, button, hover_in):
        """Buton hover animasyonu"""
        if hover_in:
            # Hover efekti - parıltı efekti
            glow_effect = QGraphicsDropShadowEffect()
            glow_effect.setBlurRadius(20)
            glow_effect.setXOffset(0)
            glow_effect.setYOffset(0)
            glow_effect.setColor(QColor(0, 120, 212, 100))
            button.setGraphicsEffect(glow_effect)
        else:
            # Normal gölge efektine dön
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(10)
            shadow.setXOffset(0)
            shadow.setYOffset(4)
            shadow.setColor(QColor(0, 0, 0, 40))
            button.setGraphicsEffect(shadow)
    
    def add_fade_effect(self, widget, duration=300):
        """Widget'a fade in efekti ekle"""
        opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(opacity_effect)
        
        self.fade_animation = QPropertyAnimation(opacity_effect, b"opacity")
        self.fade_animation.setDuration(duration)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_animation.start()
    
    def add_success_effect(self, widget):
        """Başarı efekti - yeşil parıltı"""
        # Geçici renklendirme efekti
        colorize_effect = QGraphicsColorizeEffect()
        colorize_effect.setColor(QColor(45, 106, 79))
        colorize_effect.setStrength(0.3)
        widget.setGraphicsEffect(colorize_effect)
        
        # 2 saniye sonra efekti kaldır
        QTimer.singleShot(2000, lambda: widget.setGraphicsEffect(None))
    
    def add_error_effect(self, widget):
        """Hata efekti - kırmızı parıltı"""
        colorize_effect = QGraphicsColorizeEffect()
        colorize_effect.setColor(QColor(220, 53, 69))
        colorize_effect.setStrength(0.4)
        widget.setGraphicsEffect(colorize_effect)
        
        # 3 saniye sonra efekti kaldır
        QTimer.singleShot(3000, lambda: widget.setGraphicsEffect(None))
    
    def add_loading_blur(self, widget):
        """Yükleme sırasında bulanıklaştırma efekti"""
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(5)
        widget.setGraphicsEffect(blur_effect)
        return blur_effect
    
    def add_pulse_animation(self, widget):
        """Nabız efekti animasyonu"""
        # Opacity animasyonu
        self.pulse_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.pulse_effect)
        
        self.pulse_animation = QPropertyAnimation(self.pulse_effect, b"opacity")
        self.pulse_animation.setDuration(1000)
        self.pulse_animation.setStartValue(0.5)
        self.pulse_animation.setEndValue(1.0)
        self.pulse_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.pulse_animation.setLoopCount(-1)  # Sonsuz döngü
        self.pulse_animation.start()
    
    def add_slide_in_animation(self, widget, direction="left"):
        """Kaydırarak giriş animasyonu"""
        # Widget'ın orijinal pozisyonunu kaydet
        original_pos = widget.pos()
        
        # Başlangıç pozisyonu ayarla
        if direction == "left":
            start_pos = original_pos - widget.rect().topLeft() - widget.rect().bottomRight()
        elif direction == "right":
            start_pos = original_pos + widget.rect().bottomRight()
        elif direction == "top":
            start_pos = original_pos - widget.rect().bottomLeft()
        else:  # bottom
            start_pos = original_pos + widget.rect().bottomLeft()
        
        widget.move(start_pos)
        
        # Animasyon oluştur
        self.slide_animation = QPropertyAnimation(widget, b"pos")
        self.slide_animation.setDuration(500)
        self.slide_animation.setStartValue(start_pos)
        self.slide_animation.setEndValue(original_pos)
        self.slide_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.slide_animation.start()
    
    def add_bounce_effect(self, widget):
        """Zıplama efekti"""
        original_geometry = widget.geometry()
        
        # Bounce animasyonu
        self.bounce_animation = QPropertyAnimation(widget, b"geometry")
        self.bounce_animation.setDuration(600)
        self.bounce_animation.setStartValue(original_geometry)
        
        # Zıplama noktaları
        bounce_geometry = original_geometry.adjusted(0, -20, 0, -20)
        self.bounce_animation.setKeyValueAt(0.5, bounce_geometry)
        self.bounce_animation.setEndValue(original_geometry)
        self.bounce_animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        self.bounce_animation.start()
    
    def add_rotate_animation(self, widget, angle=360):
        """Döndürme animasyonu"""
        # Transform efekti (PyQt'de sınırlı)
        self.rotation_timer = QTimer()
        self.rotation_angle = 0
        
        def rotate_step():
            self.rotation_angle += 10
            if self.rotation_angle >= angle:
                self.rotation_timer.stop()
                self.rotation_angle = 0
        
        self.rotation_timer.timeout.connect(rotate_step)
        self.rotation_timer.start(50)  # 50ms intervals
    
    def add_color_animation(self, widget, colors, duration=2000):
        """Renk döngüsü animasyonu - mavi → siyah → yeşil"""
        self.color_animation_group = QSequentialAnimationGroup()
        
        for i, color in enumerate(colors):
            color_anim = QVariantAnimation()
            color_anim.setDuration(duration // len(colors))
            color_anim.setStartValue(QColor(colors[i-1] if i > 0 else colors[-1]))
            color_anim.setEndValue(QColor(color))
            color_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
            
            def update_color(value, w=widget):
                w.setStyleSheet(f"""
                    background-color: {value.name()};
                    border-radius: 8px;
                    padding: 8px;
                    transition: all 0.3s ease;
                """)
            
            color_anim.valueChanged.connect(update_color)
            self.color_animation_group.addAnimation(color_anim)
        
        self.color_animation_group.setLoopCount(-1)  # Sonsuz döngü
        self.color_animation_group.start()
    
    def add_size_hover_animation(self, widget):
        """Hover ile boyut animasyonu"""
        original_size = widget.size()
        
        # Hover animasyonları
        self.size_in_animation = QPropertyAnimation(widget, b"size")
        self.size_in_animation.setDuration(200)
        self.size_in_animation.setStartValue(original_size)
        self.size_in_animation.setEndValue(QSize(
            int(original_size.width() * 1.1), 
            int(original_size.height() * 1.1)
        ))
        self.size_in_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.size_out_animation = QPropertyAnimation(widget, b"size")
        self.size_out_animation.setDuration(200)
        self.size_out_animation.setStartValue(QSize(
            int(original_size.width() * 1.1), 
            int(original_size.height() * 1.1)
        ))
        self.size_out_animation.setEndValue(original_size)
        self.size_out_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Mouse events
        original_enter = widget.enterEvent
        original_leave = widget.leaveEvent
        
        def enhanced_enter(event):
            self.size_in_animation.start()
            original_enter(event)
        
        def enhanced_leave(event):
            self.size_out_animation.start()
            original_leave(event)
        
        widget.enterEvent = enhanced_enter
        widget.leaveEvent = enhanced_leave
    
    def add_advanced_glow_effect(self, widget, glow_color=QColor(0, 120, 212)):
        """Gelişmiş parıltı efekti"""
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(25)
        glow_effect.setXOffset(0)
        glow_effect.setYOffset(0)
        glow_effect.setColor(glow_color)
        widget.setGraphicsEffect(glow_effect)
        
        # Parıltı animasyonu
        self.glow_animation = QPropertyAnimation(glow_effect, b"blurRadius")
        self.glow_animation.setDuration(1500)
        self.glow_animation.setStartValue(15)
        self.glow_animation.setEndValue(35)
        self.glow_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.glow_animation.setLoopCount(-1)
        self.glow_animation.start()
    
    def add_breathing_animation(self, widget):
        """Nefes alma efekti - opacity ile"""
        opacity_effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(opacity_effect)
        
        self.breathing_animation = QPropertyAnimation(opacity_effect, b"opacity")
        self.breathing_animation.setDuration(2000)
        self.breathing_animation.setStartValue(0.6)
        self.breathing_animation.setEndValue(1.0)
        self.breathing_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.breathing_animation.setLoopCount(-1)
        self.breathing_animation.start()
    
    def add_progressive_blur(self, widget, max_blur=10):
        """Progresif bulanıklık efekti"""
        blur_effect = QGraphicsBlurEffect()
        widget.setGraphicsEffect(blur_effect)
        
        self.blur_animation = QPropertyAnimation(blur_effect, b"blurRadius")
        self.blur_animation.setDuration(3000)
        self.blur_animation.setStartValue(0)
        self.blur_animation.setEndValue(max_blur)
        self.blur_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        # İleri geri animasyon
        self.blur_reverse = QPropertyAnimation(blur_effect, b"blurRadius")
        self.blur_reverse.setDuration(3000)
        self.blur_reverse.setStartValue(max_blur)
        self.blur_reverse.setEndValue(0)
        self.blur_reverse.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        self.blur_group = QSequentialAnimationGroup()
        self.blur_group.addAnimation(self.blur_animation)
        self.blur_group.addAnimation(self.blur_reverse)
        self.blur_group.setLoopCount(-1)
        self.blur_group.start()
    
    def add_rainbow_border_animation(self, widget):
        """Gökkuşağı kenarlık animasyonu"""
        colors = [
            "#ff0000", "#ff7f00", "#ffff00", "#00ff00", 
            "#0000ff", "#4b0082", "#9400d3"
        ]
        
        self.rainbow_timer = QTimer()
        self.rainbow_index = 0
        
        def update_rainbow():
            color = colors[self.rainbow_index]
            widget.setStyleSheet(widget.styleSheet() + f"""
                border: 3px solid {color};
                border-radius: 8px;
            """)
            self.rainbow_index = (self.rainbow_index + 1) % len(colors)
        
        self.rainbow_timer.timeout.connect(update_rainbow)
        self.rainbow_timer.start(300)  # Her 300ms'de renk değiştir
    
    def add_typewriter_effect(self, label, text, speed=100):
        """Daktilo efekti"""
        self.typewriter_text = text
        self.typewriter_index = 0
        self.typewriter_timer = QTimer()
        
        def type_character():
            if self.typewriter_index < len(self.typewriter_text):
                current_text = self.typewriter_text[:self.typewriter_index + 1]
                label.setText(current_text)
                self.typewriter_index += 1
            else:
                self.typewriter_timer.stop()
                # Tekrar başlat
                QTimer.singleShot(2000, lambda: self.restart_typewriter(label, text, speed))
        
        self.typewriter_timer.timeout.connect(type_character)
        self.typewriter_timer.start(speed)
    
    def restart_typewriter(self, label, text, speed):
        """Daktilo efektini yeniden başlat"""
        self.typewriter_index = 0
        label.setText("")
        self.add_typewriter_effect(label, text, speed)
    
    def enable_gpu_acceleration(self):
        """GPU hızlandırmayı etkinleştir"""
        try:
            from PyQt6.QtOpenGL import QOpenGLWidget
            from PyQt6.QtOpenGLWidgets import QOpenGLWidget as QOpenGLWidget_New
            
            # OpenGL widget oluştur
            opengl_widget = QOpenGLWidget_New()
            
            # Ana widget'ı OpenGL ile değiştir
            if hasattr(self, 'web_view'):
                # Web view için GPU hızlandırma
                self.web_view.setAttribute(Qt.WidgetAttribute.WA_Accelerated, True)
                
            # Pencere için GPU hızlandırma
            self.setAttribute(Qt.WidgetAttribute.WA_Accelerated, True)
            
            self.log("🚀 GPU hızlandırma etkinleştirildi!")
            
        except ImportError:
            self.log("⚠️ OpenGL modülü bulunamadı, CPU rendering kullanılıyor.")
        except Exception as e:
            self.log(f"⚠️ GPU hızlandırma hatası: {str(e)}")
    
    def add_matrix_rain_effect(self, widget):
        """Matrix yağmuru efekti (arka plan için)"""
        self.matrix_timer = QTimer()
        self.matrix_chars = "01"
        self.matrix_lines = []
        
        def update_matrix():
            # Matrix karakterleri güncelle
            import random
            matrix_text = ""
            for _ in range(20):  # 20 satır
                line = "".join(random.choice(self.matrix_chars) for _ in range(50))
                matrix_text += line + "\n"
            
            # Arka plan olarak ayarla (çok hafif opacity ile)
            widget.setStyleSheet(widget.styleSheet() + f"""
                background-image: none;
                color: rgba(0, 255, 0, 0.1);
            """)
        
        self.matrix_timer.timeout.connect(update_matrix)
        self.matrix_timer.start(200)
    
    def setup_tray(self):
        """System tray ayarla"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            
            if os.path.exists("ui/icon.png"):
                self.tray_icon.setIcon(QIcon("ui/icon.png"))
            
            # Tray menü
            tray_menu = QMenu()
            show_action = tray_menu.addAction("Göster")
            show_action.triggered.connect(self.show)
            
            quit_action = tray_menu.addAction("Çıkış")
            quit_action.triggered.connect(self.quit_app)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.activated.connect(self.tray_icon_activated)
            self.tray_icon.show()
    
    def tray_icon_activated(self, reason):
        """Tray icon tıklandığında"""
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.raise_()
                self.activateWindow()
    
    def start_server(self):
        """Server'ı başlat"""
        if self.server_thread and self.server_thread.running:
            return
            
        self.log("🚀 Server başlatılıyor...")
        self.server_status.setText("⏳ Başlatılıyor...")
        self.server_status.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(255, 193, 7, 0.2), stop:1 rgba(255, 152, 0, 0.2));
            color: #ffc107;
            border: 1px solid #ffc107;
        """)
        
        # Loading efektleri
        self.loading_blur = self.add_loading_blur(self.web_view)
        self.add_pulse_animation(self.server_status)
        
        self.server_thread = ServerThread()
        self.server_thread.server_started.connect(self.on_server_started)
        self.server_thread.server_error.connect(self.on_server_error)
        self.server_thread.start()
        
        self.start_btn.setEnabled(False)
    
    def stop_server(self):
        """Server'ı durdur"""
        if self.server_thread:
            self.server_thread.stop_server()
            self.log("⏹️ Server durduruldu.")
            self.server_status.setText("⏹️ Durduruldu")
            self.server_status.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(108, 117, 125, 0.2), stop:1 rgba(73, 80, 87, 0.2));
                color: #6c757d;
                border: 1px solid #6c757d;
            """)
            self.start_btn.setEnabled(True)
            self.browser_btn.setEnabled(False)
    
    def on_server_started(self):
        """Server başlatıldığında"""
        self.log("✅ Server başarıyla başlatıldı!")
        self.server_status.setText("✅ Aktif - Port 3000")
        self.server_status.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(40, 167, 69, 0.2), stop:1 rgba(25, 135, 84, 0.2));
            color: #28a745;
            border: 1px solid #28a745;
        """)
        self.statusBar().showMessage("🚀 Server çalışıyor - http://localhost:3000")
        
        # Success efekti ekle
        self.add_success_effect(self.server_status)
        self.add_bounce_effect(self.server_status)
        
        # Başarı renk animasyonu - yeşil tonları
        success_colors = ["#28a745", "#20c997", "#17a2b8", "#28a745"]
        self.add_color_animation(self.server_status, success_colors, 3000)
        
        # Gökkuşağı kenarlık efektini aktif et (5 saniye sonra)
        if not self.rainbow_mode:
            self.rainbow_mode = True
            QTimer.singleShot(5000, lambda: self.add_rainbow_border_animation(self.tab_widget))
        
        # Loading blur efektini kaldır
        if hasattr(self, 'loading_blur'):
            self.web_view.setGraphicsEffect(None)
        
        # Web view'ı yükle
        self.web_view.load(QUrl("http://localhost:3000"))
        self.browser_btn.setEnabled(True)
    
    def on_server_error(self, error):
        """Server hatası"""
        self.log(f"❌ Server hatası: {error}")
        self.server_status.setText(f"❌ Hata: {error}")
        self.server_status.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 rgba(220, 53, 69, 0.2), stop:1 rgba(176, 42, 55, 0.2));
            color: #dc3545;
            border: 1px solid #dc3545;
        """)
        
        # Error efekti ekle
        self.add_error_effect(self.server_status)
        self.start_btn.setEnabled(True)
        
        # Modern error dialog
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Server Hatası")
        msg.setText(f"Server başlatılamadı:\n{error}")
        msg.setStyleSheet("""
            QMessageBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
                color: #ffffff;
            }
            QMessageBox QPushButton {
                background: #dc3545;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 80px;
            }
        """)
        msg.exec()
    
    def open_in_browser(self):
        """Tarayıcıda aç"""
        QDesktopServices.openUrl(QUrl("http://localhost:3000"))
    
    def log(self, message):
        """Log mesajı ekle"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
    
    def closeEvent(self, event):
        """Pencere kapatıldığında"""
        if self.tray_icon and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            self.quit_app()
    
    def quit_app(self):
        """Uygulamayı kapat"""
        if self.server_thread:
            self.server_thread.stop_server()
        
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        
        QApplication.quit()

def main():
    """Ana fonksiyon"""
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # Splash screen
    if os.path.exists("ui/ChatCPT_LOGO.png"):
        pixmap = QPixmap("ui/ChatCPT_LOGO.png")
        splash = QSplashScreen(pixmap)
        splash.show()
        app.processEvents()
        time.sleep(2)
        splash.close()
    
    # Ana pencere
    window = ChatCPTApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()