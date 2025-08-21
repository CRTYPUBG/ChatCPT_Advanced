// ChatCPT Web - Chat JavaScript

class ChatApp {
    constructor() {
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatMessages = document.getElementById('chatMessages');
        this.isTyping = false;
        
        this.init();
    }
    
    init() {
        // Session kontrolü
        this.checkSession();
        
        // Event listeners
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-resize input
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
        });
        
        // Focus input on load
        this.messageInput.focus();
        
        // Server durumu kontrolü
        this.checkServerStatus();
        
        // Logout butonu
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => this.logout());
        }
    }
    
    logout() {
        if (confirm('Çıkış yapmak istediğinizden emin misiniz?')) {
            localStorage.removeItem('supabaseSession');
            alert('Başarıyla çıkış yapıldı.');
            window.location.href = '../ui/login.html';
        }
    }
    
    checkSession() {
        const sessionData = localStorage.getItem('supabaseSession');
        if (!sessionData) {
            // Session yoksa login sayfasına yönlendir
            alert('Giriş yapmanız gerekiyor. Login sayfasına yönlendiriliyorsunuz...');
            window.location.href = '../ui/login.html';
            return false;
        }
        
        try {
            const session = JSON.parse(sessionData);
            if (!session.access_token) {
                throw new Error('Invalid session');
            }
            
            // Kullanıcı bilgilerini göster
            this.updateUserInfo(session);
            return true;
        } catch (error) {
            localStorage.removeItem('supabaseSession');
            alert('Session geçersiz. Login sayfasına yönlendiriliyorsunuz...');
            window.location.href = '../ui/login.html';
            return false;
        }
    }
    
    updateUserInfo(session) {
        // Header'da kullanıcı bilgilerini göster
        const chatStatus = document.querySelector('.chat-status');
        if (chatStatus && session.user) {
            const userEmail = session.user.email;
            const userName = userEmail.split('@')[0];
            chatStatus.innerHTML = `
                <span class="status-indicator online"></span>
                <span>${userName} - Çevrimiçi</span>
            `;
        }
    }
    
    async checkServerStatus() {
        try {
            const response = await fetch('http://localhost:3000/api/health', {
                method: 'GET',
                timeout: 5000
            });
            
            const statusIndicator = document.querySelector('.status-indicator');
            if (response.ok) {
                statusIndicator.className = 'status-indicator online';
            } else {
                statusIndicator.className = 'status-indicator warning';
            }
        } catch (error) {
            const statusIndicator = document.querySelector('.status-indicator');
            statusIndicator.className = 'status-indicator offline';
            
            // Server çalışmıyorsa uyarı ver
            this.addMessage('⚠️ Server bağlantısı kurulamadı. Lütfen server\'ın çalıştığından emin olun.', 'bot');
        }
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isTyping) return;
        
        // Add user message
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Simulate API call (replace with actual API)
            const response = await this.callChatAPI(message);
            this.hideTypingIndicator();
            this.addMessage(response, 'bot');
        } catch (error) {
            this.hideTypingIndicator();
            this.addMessage('Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.', 'bot');
        }
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = sender === 'user' ? '👤' : '🤖';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const messageText = document.createElement('p');
        messageText.innerHTML = this.formatMessage(content);
        messageContent.appendChild(messageText);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        if (this.isTyping) return;
        
        this.isTyping = true;
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-message';
        typingDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        const typingMessage = this.chatMessages.querySelector('.typing-message');
        if (typingMessage) {
            typingMessage.remove();
        }
        this.isTyping = false;
    }
    
    async callChatAPI(message) {
        // Production API URL
        const BACKEND_URL = window.location.hostname === 'localhost' 
            ? 'http://localhost:3000' 
            : 'https://chat-cpt-advanced-9cpt.vercel.app';
        
        try {
            // Önce session kontrolü yap
            const sessionData = localStorage.getItem('supabaseSession');
            if (!sessionData) {
                // Eğer session yoksa login sayfasına yönlendir
                window.location.href = '../ui/login.html';
                return;
            }
            
            const session = JSON.parse(sessionData);
            const token = session.access_token;
            
            // Gerçek API çağrısı
            const response = await fetch(`${BACKEND_URL}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ question: message })
            });
            
            if (!response.ok) {
                if (response.status === 401) {
                    // Token geçersiz, login sayfasına yönlendir
                    localStorage.removeItem('supabaseSession');
                    window.location.href = '../ui/login.html';
                    return;
                }
                throw new Error(`API Error: ${response.status}`);
            }
            
            const data = await response.json();
            return data.text || 'Üzgünüm, cevap alınamadı.';
            
        } catch (error) {
            console.error('API Error:', error);
            
            // Network hatası durumunda
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                return 'Bağlantı hatası: Server çalışmıyor olabilir. Lütfen server\'ın çalıştığından emin olun.';
            }
            
            return 'Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.';
        }
    }
    
    formatMessage(message) {
        // Basic markdown-like formatting
        return message
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
}

// Initialize chat app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
    
    // Add some welcome animations
    setTimeout(() => {
        const messages = document.querySelectorAll('.message');
        messages.forEach((message, index) => {
            message.style.opacity = '0';
            message.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                message.style.transition = 'all 0.5s ease';
                message.style.opacity = '1';
                message.style.transform = 'translateY(0)';
            }, index * 200);
        });
    }, 100);
});