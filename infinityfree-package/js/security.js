// ChatCPT Web - Advanced Security Protection
// Bu dosya tüm sayfalar tarafından yüklenir ve güvenlik sağlar

(function() {
    'use strict';
    
    // 🚫 DEVELOPER TOOLS KORUNMASI
    
    // Console temizleme ve uyarı
    function clearConsoleAndWarn() {
        console.clear();
        console.log("%c🚫 ERIŞIM ENGELLENDİ!", "color: red; font-size: 40px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);");
        console.log("%c⚠️ Bu bir güvenlik özelliğidir!", "color: orange; font-size: 20px; font-weight: bold;");
        console.log("%cBu konsol geliştiriciler içindir. Yetkisiz erişim tespit edildi.", "color: red; font-size: 16px;");
        console.log("%cSite güvenliği için bu alan korunmaktadır.", "color: red; font-size: 14px;");
    }
    
    // İlk console temizleme
    clearConsoleAndWarn();
    
    // Periyodik console temizleme
    setInterval(clearConsoleAndWarn, 2000);
    
    // 🚫 SAĞ TIKLAMA ENGELLEMESİ
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
        e.stopPropagation();
        showSecurityAlert('Sağ tıklama devre dışı bırakıldı!');
        return false;
    }, true);
    
    // 🚫 KLAVYE KISAYOLLARI ENGELLEMESİ
    document.addEventListener('keydown', function(e) {
        // F12 - Developer Tools
        if (e.key === 'F12') {
            e.preventDefault();
            e.stopPropagation();
            showSecurityAlert('F12 Developer Tools engellendi!');
            return false;
        }
        
        // Ctrl+Shift+I - Developer Tools
        if (e.ctrlKey && e.shiftKey && e.key === 'I') {
            e.preventDefault();
            e.stopPropagation();
            showSecurityAlert('Developer Tools engellendi!');
            return false;
        }
        
        // Ctrl+Shift+C - Element Inspector
        if (e.ctrlKey && e.shiftKey && e.key === 'C') {
            e.preventDefault();
            e.stopPropagation();
            showSecurityAlert('Element Inspector engellendi!');
            return false;
        }
        
        // Ctrl+Shift+J - Console
        if (e.ctrlKey && e.shiftKey && e.key === 'J') {
            e.preventDefault();
            e.stopPropagation();
            showSecurityAlert('Console engellendi!');
            return false;
        }
        
        // Ctrl+U - View Source
        if (e.ctrlKey && e.key === 'u') {
            e.preventDefault();
            e.stopPropagation();
            showSecurityAlert('Kaynak kodu görüntüleme engellendi!');
            return false;
        }
        
        // Ctrl+S - Save Page
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            e.stopPropagation();
            showSecurityAlert('Sayfa kaydetme engellendi!');
            return false;
        }
        
        // Ctrl+A - Select All (bazı durumlarda)
        if (e.ctrlKey && e.key === 'a' && !isInputElement(e.target)) {
            e.preventDefault();
            e.stopPropagation();
            showSecurityAlert('Tümünü seçme engellendi!');
            return false;
        }
        
        // Ctrl+P - Print
        if (e.ctrlKey && e.key === 'p') {
            e.preventDefault();
            e.stopPropagation();
            showSecurityAlert('Yazdırma engellendi!');
            return false;
        }
    }, true);
    
    // 🚫 METIN SEÇİMİ ENGELLEMESİ
    document.addEventListener('selectstart', function(e) {
        if (!isInputElement(e.target)) {
            e.preventDefault();
            return false;
        }
    }, true);
    
    // 🚫 SÜRÜKLEME ENGELLEMESİ
    document.addEventListener('dragstart', function(e) {
        e.preventDefault();
        return false;
    }, true);
    
    // 🚫 DEVELOPER TOOLS AÇILMA TESPİTİ
    let devtools = {
        open: false,
        orientation: null
    };
    
    const threshold = 160;
    
    setInterval(function() {
        if (window.outerHeight - window.innerHeight > threshold || 
            window.outerWidth - window.innerWidth > threshold) {
            if (!devtools.open) {
                devtools.open = true;
                showSecurityAlert('Developer Tools tespit edildi! Sayfa yeniden yükleniyor...');
                setTimeout(() => {
                    window.location.reload();
                }, 2000);
            }
        } else {
            devtools.open = false;
        }
    }, 500);
    
    // 🚫 CONSOLE KOMUTLARI ENGELLEMESİ
    const originalLog = console.log;
    const originalError = console.error;
    const originalWarn = console.warn;
    const originalInfo = console.info;
    
    console.log = function() {
        clearConsoleAndWarn();
    };
    console.error = function() {
        clearConsoleAndWarn();
    };
    console.warn = function() {
        clearConsoleAndWarn();
    };
    console.info = function() {
        clearConsoleAndWarn();
    };
    
    // 🚫 DEBUGGER ENGELLEMESİ
    setInterval(function() {
        debugger;
    }, 100);
    
    // Helper Functions
    function isInputElement(element) {
        const inputTypes = ['INPUT', 'TEXTAREA', 'SELECT'];
        return inputTypes.includes(element.tagName) || element.contentEditable === 'true';
    }
    
    function showSecurityAlert(message) {
        // Güvenlik uyarısı göster
        const alertDiv = document.createElement('div');
        alertDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: linear-gradient(135deg, #ff4757, #ff3838);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            font-weight: bold;
            font-size: 14px;
            z-index: 999999;
            box-shadow: 0 4px 20px rgba(255, 71, 87, 0.3);
            border: 2px solid #ff1744;
            animation: securityAlert 0.5s ease-in-out;
        `;
        
        alertDiv.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 18px;">🚫</span>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.parentNode.removeChild(alertDiv);
            }
        }, 3000);
    }
    
    // CSS animasyonu ekle
    const style = document.createElement('style');
    style.textContent = `
        @keyframes securityAlert {
            0% { transform: translateX(100%); opacity: 0; }
            100% { transform: translateX(0); opacity: 1; }
        }
        
        /* Metin seçimini engelle */
        * {
            -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
            user-select: none;
        }
        
        /* Input elementlerinde seçime izin ver */
        input, textarea, select, [contenteditable="true"] {
            -webkit-user-select: text !important;
            -moz-user-select: text !important;
            -ms-user-select: text !important;
            user-select: text !important;
        }
        
        /* Sürüklemeyi engelle */
        img, video, audio {
            -webkit-user-drag: none;
            -moz-user-drag: none;
            user-drag: none;
        }
    `;
    document.head.appendChild(style);
    
    // 🚫 WINDOW FOCUS KONTROLÜ
    window.addEventListener('blur', function() {
        setTimeout(() => {
            clearConsoleAndWarn();
        }, 100);
    });
    
    // 🚫 SAYFA YÜKLENME KONTROLÜ
    document.addEventListener('DOMContentLoaded', function() {
        clearConsoleAndWarn();
        
        // Tüm linkleri kontrol et
        const links = document.querySelectorAll('a[href]');
        links.forEach(link => {
            if (link.href.includes('view-source:') || 
                link.href.includes('javascript:') ||
                link.href.includes('data:')) {
                link.remove();
            }
        });
    });
    
    // 🚫 IFRAME ENGELLEMESİ
    if (window.top !== window.self) {
        window.top.location = window.self.location;
    }
    
    // Final uyarı
    console.log("%c⚠️ GÜVENLİK UYARISI: Bu site korunmaktadır!", "color: red; font-size: 16px; font-weight: bold;");
    
})();