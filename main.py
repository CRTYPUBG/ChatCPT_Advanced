


import sys
import os
import subprocess
import time
import requests
from pathlib import Path

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QPushButton, QLabel, QTextEdit,
                            QMessageBox, QSystemTrayIcon, QMenu, QTabWidget,
                            QGraphicsDropShadowEffect, QGraphicsOpacityEffect)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer, Qt, QUrl, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon, QDesktopServices, QColor
from PyQt6.QtWebEngineWidgets import QWebEngineView

class ServerThread(QThread):
    server_started = pyqtSignal()
    server_error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.server_process = None
        self.running = False
        
    def run(self):
        try:
            node_path = self.find_node()
            if not node_path:
                self.server_error.emit("Node.js bulunamadı!")
                return
                
            cmd = [node_path, "server.js"]
            self.server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.getcwd(),
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            )
            
            self.running = True
            
            time.sleep(3)
            

            if self.check_server():
                self.server_started.emit()
            else:
                self.server_error.emit("Server başlatılamadı!")
                
        except Exception as e:
            self.server_error.emit(f"Server hatası: {str(e)}")
    
    def find_node(self):

        if getattr(sys, 'frozen', False):

            bundle_dir = sys._MEIPASS
            node_path = os.path.join(bundle_dir, 'node', 'node.exe')
            if os.path.exists(node_path):
                return node_path
        
        # Sistem PATH'inde node'u ara
        import shutil
        return shutil.which('node')
    
    def check_server(self):
        try:
            response = requests.get('http://localhost:3000', timeout=5)
            return True
        except:
            return False
    
    def stop_server(self):
        if self.server_process:
            self.server_process.terminate()
            self.running = False

class ChatCPTApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.server_thread = None
        self.init_ui()
        self.setup_tray()
        self.start_server()
        
    def init_ui(self):
        self.setWindowTitle("ChatCPT Desktop")
        
        # Pencereyi ekranın ortasında aç
        self.resize(1024, 640)
        self.setMinimumSize(800, 500)
        self.center_window()
        
        # Icon ayarla
        if os.path.exists("ui/icon.ico"):
            self.setWindowIcon(QIcon("ui/icon.ico"))
        
        # Ana widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # ASCII Art Başlık - Renkli
        self.create_ascii_title(layout)
        
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
        
        # Basit tema uygula
        self.apply_simple_theme()
        
        # Basit efektler ekle
        self.add_simple_effects()
    
    def create_ascii_title(self, layout):
        # Tüm ASCII art'ı tek label'da birleştir
        ascii_text = """      
        ██████╗██╗  ██╗ █████╗ ████████╗     ██████╗██████╗ ████████╗
       ██╔════╝██║  ██║██╔══██╗╚══██╔══╝    ██╔════╝██╔══██╗╚══██╔══╝
    ██║     ███████║███████║   ██║       ██║     ██████╔╝   ██║   
    ██║     ██╔══██║██╔══██║   ██║       ██║     ██╔═══╝    ██║   
    ╚██████╗██║  ██║██║  ██║   ██║       ╚██████╗██║        ██║   
     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝        ╚═════╝╚═╝        ╚═╝   
          """
        ascii_label = QLabel(ascii_text)
        ascii_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ascii_label.setStyleSheet("""
            QLabel {
                font-family: 'Courier New', monospace;
                font-size: 9px;
                font-weight: bold;
                color: #00ffcc;
                margin: 5px;
                padding: 5px;
                line-height: 1.1;
            }
        """)
        layout.addWidget(ascii_label)
    
    # RGB döngüsü fonksiyonları kaldırıldı
    
    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
        
    def create_control_panel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Server durumu
        self.server_status = QLabel("⏳ Server Başlatılıyor...")
        self.server_status.setStyleSheet("""
            QLabel {
                font-weight: bold; 
                color: #ffc107;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 193, 7, 0.2), stop:1 rgba(255, 152, 0, 0.2));
                padding: 12px;
                border-radius: 8px;
                border: 2px solid #ffc107;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.server_status)
        
        # Butonlar
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("🚀 Server'ı Başlat")
        self.start_btn.clicked.connect(self.start_server)
        self.start_btn.setEnabled(False)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d6a4f, stop:1 #1b4332);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #40916c, stop:1 #2d6a4f);
            }
            QPushButton:disabled {
                background-color: #404040;
                color: #808080;
            }
        """)
        self.add_button_hover_effect(self.start_btn)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ Server'ı Durdur")
        self.stop_btn.clicked.connect(self.stop_server)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e63946, stop:1 #d62828);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f77f00, stop:1 #e63946);
            }
        """)
        self.add_button_hover_effect(self.stop_btn)
        button_layout.addWidget(self.stop_btn)
        
        self.browser_btn = QPushButton("🌐 Tarayıcıda Aç")
        self.browser_btn.clicked.connect(self.open_in_browser)
        self.browser_btn.setEnabled(False)
        self.browser_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3a86ff, stop:1 #1e6091);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5aa3ff, stop:1 #3a86ff);
            }
            QPushButton:disabled {
                background-color: #404040;
                color: #808080;
            }
        """)
        self.add_button_hover_effect(self.browser_btn)
        button_layout.addWidget(self.browser_btn)
        
        layout.addLayout(button_layout)
        
        # Log alanı
        layout.addWidget(QLabel("Sistem Logları:"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #00ff00;
                border: 2px solid #404040;
                border-radius: 8px;
                padding: 8px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10px;
                selection-background-color: #0078d4;
            }
        """)
        layout.addWidget(self.log_text)
        
        layout.addStretch()
        
        return widget
    
    def apply_simple_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QTabWidget {
                background-color: transparent;
                border: none;
            }
            QTabWidget::pane {
                border: 2px solid #404040;
                background-color: #2d2d2d;
                border-radius: 10px;
                margin-top: -2px;
            }
            QTabBar::tab {
                background-color: #404040;
                color: #ffffff;
                padding: 12px 24px;
                margin-right: 4px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-weight: 600;
                font-size: 11px;
                min-width: 120px;
                border: 2px solid #404040;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background-color: #0078d4;
                color: white;
                font-weight: bold;
                border-color: #0078d4;
            }
            QTabBar::tab:hover:!selected {
                background-color: #505050;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #404040;
                color: #808080;
            }
            QLabel {
                color: #ffffff;
                font-weight: 500;
            }
            QTextEdit {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 2px solid #404040;
                border-radius: 8px;
                padding: 8px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 10px;
                selection-background-color: #0078d4;
            }
            QStatusBar {
                background-color: #2d2d2d;
                color: #ffffff;
                border-top: 2px solid #404040;
                font-weight: 500;
            }
        """)
    
    def add_simple_effects(self):
        # Başlığa hafif gölge efekti
        title_shadow = QGraphicsDropShadowEffect()
        title_shadow.setBlurRadius(10)
        title_shadow.setXOffset(2)
        title_shadow.setYOffset(2)
        title_shadow.setColor(QColor(0, 0, 0, 50))
        
        # Tab widget'a gölge efekti
        tab_shadow = QGraphicsDropShadowEffect()
        tab_shadow.setBlurRadius(15)
        tab_shadow.setXOffset(0)
        tab_shadow.setYOffset(5)
        tab_shadow.setColor(QColor(0, 0, 0, 30))
        self.tab_widget.setGraphicsEffect(tab_shadow)
        
        # Fade-in efekti
        self.fade_in_animation()
    
    def fade_in_animation(self):
        opacity_effect = QGraphicsOpacityEffect()
        self.centralWidget().setGraphicsEffect(opacity_effect)
        
        self.fade_animation = QPropertyAnimation(opacity_effect, b"opacity")
        self.fade_animation.setDuration(800)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_animation.start()
    
    def add_button_hover_effect(self, button):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 120, 212, 60))
        button.setGraphicsEffect(shadow)
    
    def add_success_glow(self, widget):
        glow_effect = QGraphicsDropShadowEffect()
        glow_effect.setBlurRadius(20)
        glow_effect.setXOffset(0)
        glow_effect.setYOffset(0)
        glow_effect.setColor(QColor(40, 167, 69, 100))
        widget.setGraphicsEffect(glow_effect)
        
        # 3 saniye sonra normal gölgeye dön
        QTimer.singleShot(3000, lambda: self.reset_widget_effect(widget))
    
    def reset_widget_effect(self, widget):
        widget.setGraphicsEffect(None)
    
    def setup_tray(self):
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            
            if os.path.exists("ui/icon.png"):
                self.tray_icon.setIcon(QIcon("ui/icon.png"))
            
            tray_menu = QMenu()
            show_action = tray_menu.addAction("Göster")
            show_action.triggered.connect(self.show)
            
            quit_action = tray_menu.addAction("Çıkış")
            quit_action.triggered.connect(self.quit_app)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.activated.connect(self.tray_icon_activated)
            self.tray_icon.show()
    
    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.raise_()
                self.activateWindow()
    
    def start_server(self):
        if self.server_thread and self.server_thread.running:
            return
            
        self.log("Server başlatılıyor...")
        self.server_status.setText("Server Durumu: Başlatılıyor...")
        self.server_status.setStyleSheet("""
            QLabel {
                font-weight: bold; 
                color: #ffc107;
                background-color: #fff3cd;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ffeaa7;
            }
        """)
        
        self.server_thread = ServerThread()
        self.server_thread.server_started.connect(self.on_server_started)
        self.server_thread.server_error.connect(self.on_server_error)
        self.server_thread.start()
        
        self.start_btn.setEnabled(False)
    
    def stop_server(self):
        if self.server_thread:
            self.server_thread.stop_server()
            self.log("Server durduruldu.")
            self.server_status.setText("Server Durumu: Durduruldu")
            self.server_status.setStyleSheet("""
                QLabel {
                    font-weight: bold; 
                    color: #dc3545;
                    background-color: #f8d7da;
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #f5c6cb;
                }
            """)
            self.start_btn.setEnabled(True)
            self.browser_btn.setEnabled(False)
    
    def on_server_started(self):
        self.log("Server başarıyla başlatıldı!")
        self.server_status.setText("✅ Server Çalışıyor - Port 3000")
        self.server_status.setStyleSheet("""
            QLabel {
                font-weight: bold; 
                color: #28a745;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(40, 167, 69, 0.2), stop:1 rgba(25, 135, 84, 0.2));
                padding: 12px;
                border-radius: 8px;
                border: 2px solid #28a745;
                font-size: 12px;
            }
        """)
        self.statusBar().showMessage("Server çalışıyor - http://localhost:3000")

        self.add_success_glow(self.server_status)
        
        self.web_view.load(QUrl("http://localhost:3000"))
        self.browser_btn.setEnabled(True)
        self.start_btn.setEnabled(False)
    
    def on_server_error(self, error):
        self.log(f"Server hatası: {error}")
        self.server_status.setText(f"❌ Server Hatası: {error}")
        self.server_status.setStyleSheet("""
            QLabel {
                font-weight: bold; 
                color: #dc3545;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(220, 53, 69, 0.2), stop:1 rgba(176, 42, 55, 0.2));
                padding: 12px;
                border-radius: 8px;
                border: 2px solid #dc3545;
                font-size: 12px;
            }
        """)
        self.start_btn.setEnabled(True)
        
        QMessageBox.critical(self, "Server Hatası", f"Server başlatılamadı:\n{error}")
    
    def open_in_browser(self):
        QDesktopServices.openUrl(QUrl("http://localhost:3000"))
    
    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
    
    def closeEvent(self, event):
        if self.tray_icon and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            self.quit_app()
    
    def quit_app(self):
        if self.server_thread:
            self.server_thread.stop_server()
        
        if hasattr(self, 'tray_icon'):
            self.tray_icon.hide()
        
        QApplication.quit()

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # Ana pencere
    window = ChatCPTApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()