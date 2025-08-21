// ChatCPT Web - Register JavaScript

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
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const registerBtn = document.getElementById('registerBtn');
    const messageDiv = document.getElementById('message');
    
    // API URL
    const BACKEND_URL = window.location.hostname === 'localhost' 
        ? 'http://localhost/api' 
        : 'https://chat-cpt-advanced-9cpt.vercel.app/api';
    
    // Event listeners
    registerBtn.addEventListener('click', handleRegister);
    
    // Enter key support
    confirmPasswordInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleRegister();
        }
    });
    
    // Register function
    async function handleRegister() {
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();
        const confirmPassword = confirmPasswordInput.value.trim();
        
        // Validation
        if (!email || !password || !confirmPassword) {
            showMessage('Lütfen tüm alanları doldurun.', 'error');
            return;
        }
        
        if (!isValidEmail(email)) {
            showMessage('Geçerli bir e-posta adresi girin.', 'error');
            return;
        }
        
        if (password.length < 6) {
            showMessage('Şifre en az 6 karakter olmalıdır.', 'error');
            return;
        }
        
        if (password !== confirmPassword) {
            showMessage('Şifreler eşleşmiyor.', 'error');
            return;
        }
        
        // Show loading
        registerBtn.disabled = true;
        registerBtn.textContent = 'Kaydolunuyor...';
        
        try {
            // API call
            const response = await fetch(`${BACKEND_URL}/auth.php`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'register',
                    email: email,
                    password: password
                })
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                showMessage('Kayıt başarılı! E-posta adresinizi doğrulayın ve giriş yapın.', 'success');
                
                // Clear form
                emailInput.value = '';
                passwordInput.value = '';
                confirmPasswordInput.value = '';
                
                // Redirect to login after 3 seconds
                setTimeout(() => {
                    window.location.href = 'login.html';
                }, 3000);
                
            } else {
                showMessage(data.error || 'Kayıt başarısız. Lütfen tekrar deneyin.', 'error');
            }
            
        } catch (error) {
            console.error('Register error:', error);
            showMessage('Bağlantı hatası. Lütfen tekrar deneyin.', 'error');
        } finally {
            // Reset button
            registerBtn.disabled = false;
            registerBtn.textContent = 'Kaydol';
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