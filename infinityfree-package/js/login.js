// ChatCPT Web - Login JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // 🚫 Developer Tools Koruması
    document.addEventListener('contextmenu', event => event.preventDefault());
    document.addEventListener('keydown', (e) => {
        if (e.key === "F12" || 
            (e.ctrlKey && e.shiftKey && e.key === "I") || 
            (e.ctrlKey && e.shiftKey && e.key === "C") ||
            (e.ctrlKey && e.shiftKey && e.key === "J") ||
            (e.ctrlKey && e.key === "u")) {
            e.preventDefault();
            return false;
        }
    });
    
    // Console uyarısı
    console.clear();
    console.log("%cDUR!", "color: red; font-size: 50px; font-weight: bold;");
    console.log("%cBu bir tarayıcı özelliğidir ve geliştiriciler için tasarlanmıştır.", "color: red; font-size: 16px;");
    
    // Form elements
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const loginBtn = document.getElementById('loginBtn');
    const messageDiv = document.getElementById('message');
    const forgotPasswordLink = document.getElementById('forgotPasswordLink');
    
    // API URL
    const BACKEND_URL = window.location.hostname === 'localhost' 
        ? 'http://localhost/api' 
        : window.location.origin + '/api';
    
    // Event listeners
    loginBtn.addEventListener('click', handleLogin);
    
    // Enter key support
    passwordInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleLogin();
        }
    });
    
    // Forgot password
    forgotPasswordLink.addEventListener('click', function(e) {
        e.preventDefault();
        alert('Şifre sıfırlama özelliği yakında eklenecek.');
    });
    
    // Login function
    async function handleLogin() {
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();
        
        // Validation
        if (!email || !password) {
            showMessage('Lütfen tüm alanları doldurun.', 'error');
            return;
        }
        
        if (!isValidEmail(email)) {
            showMessage('Geçerli bir e-posta adresi girin.', 'error');
            return;
        }
        
        // Show loading
        loginBtn.disabled = true;
        loginBtn.textContent = 'Giriş yapılıyor...';
        
        try {
            // API call
            const response = await fetch(`${BACKEND_URL}/auth.php`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'login',
                    email: email,
                    password: password
                })
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                // Save session
                localStorage.setItem('supabaseSession', JSON.stringify(data.session));
                
                showMessage('Giriş başarılı! Yönlendiriliyorsunuz...', 'success');
                
                // Redirect to chat
                setTimeout(() => {
                    window.location.href = 'chat.html';
                }, 1500);
                
            } else {
                showMessage(data.error || 'Giriş başarısız. Lütfen bilgilerinizi kontrol edin.', 'error');
            }
            
        } catch (error) {
            console.error('Login error:', error);
            showMessage('Bağlantı hatası. Lütfen tekrar deneyin.', 'error');
        } finally {
            // Reset button
            loginBtn.disabled = false;
            loginBtn.textContent = 'Giriş Yap';
        }
    }
    
    // Helper functions
    function showMessage(message, type) {
        messageDiv.textContent = message;
        messageDiv.className = `message ${type}`;
        messageDiv.style.display = 'block';
        
        // Auto hide after 5 seconds
        setTimeout(() => {
            messageDiv.style.display = 'none';
        }, 5000);
    }
    
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    // Check if already logged in
    const existingSession = localStorage.getItem('supabaseSession');
    if (existingSession) {
        try {
            const session = JSON.parse(existingSession);
            if (session.access_token) {
                // Already logged in, redirect to chat
                window.location.href = 'chat.html';
            }
        } catch (error) {
            // Invalid session, remove it
            localStorage.removeItem('supabaseSession');
        }
    }
});

// Add CSS for messages
const style = document.createElement('style');
style.textContent = `
    .message {
        margin: 15px 0;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        font-weight: 500;
        display: none;
    }
    
    .message.success {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .message.error {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    
    .btn-primary:disabled {
        opacity: 0.6;
        cursor: not-allowed;
    }
`;
document.head.appendChild(style);