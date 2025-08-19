document.addEventListener('DOMContentLoaded', () => {
    const BACKEND_URL = 'http://localhost:3000';
    const path = window.location.pathname;

    document.addEventListener('contextmenu', event => event.preventDefault());
    document.onkeydown = (e) => {
        if (e.key === "F12" || (e.ctrlKey && e.shiftKey && e.key === "I") || (e.ctrlKey && e.shiftKey && e.key === "C")) {
            e.preventDefault();
        }
    };
    
    if (path.includes('login.html')) {
        setupLoginPage();
    } else if (path.includes('register.html')) {
        setupRegisterPage();
    } else if (path.includes('profile.html')) {
        setupProfilePage();
    } else if (path.includes('settings.html')) {
        setupSettingsPage();
    } else {
        setupChatPage();
    }

    function addMessage(html, sender) {
        const chatDiv = document.getElementById('chat');
        if (chatDiv) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${sender}`;
            msgDiv.innerHTML = html;
            chatDiv.appendChild(msgDiv);
            chatDiv.scrollTop = chatDiv.scrollHeight;
        }
    }

    function formatMarkdown(text) {
        let htmlText = text;
        htmlText = htmlText.replace(/\n/g, '<br>');
        const listRegex = /(?:\n\s*[-*]\s.*)+/g;
        htmlText = htmlText.replace(listRegex, (match) => {
            let listItems = match.trim().split(/\n\s*[-*]\s*/).filter(item => item.length > 0);
            let listHtml = '<ul>';
            listItems.forEach(item => { listHtml += `<li>${item}</li>`; });
            listHtml += '</ul>';
            return listHtml;
        });
        htmlText = htmlText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        htmlText = htmlText.replace(/\*(.*?)\*/g, '<em>$1</em>');
        htmlText = htmlText.replace(/^###\s(.*?)$/gm, '<h3>$1</h3>');
        htmlText = htmlText.replace(/^##\s(.*?)$/gm, '<h2>$1</h2>');
        htmlText = htmlText.replace(/^#\s(.*?)$/gm, '<h1>$1</h1>');
        htmlText = htmlText.replace(/(<br>){2,}/g, '<br><br>');
        return htmlText;
    }

    function setupChatPage() {
        const sendBtn = document.getElementById('sendBtn');
        const userInput = document.getElementById('userInput');
        const logoutBtn = document.getElementById('logoutBtn');

        const sessionData = localStorage.getItem('supabaseSession');
        if (!sessionData) {
            window.location.href = 'login.html'; 
            return;
        }

        addMessage("Merhaba, ben ChatCPT 2.0. Size nasıl yardımcı olabilirim?", 'bot');

        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('supabaseSession');
            window.location.href = 'login.html';
        });

        sendBtn.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', (e) => {
            if (e.key === "Enter") sendMessage();
        });

        async function sendMessage() {
            const msg = userInput.value.trim();
            if (!msg) return;

            const currentSession = localStorage.getItem('supabaseSession');
            if (!currentSession) {
                addMessage(`<p><strong>Hesap oturumunuz yok. Lütfen giriş yapın.</strong></p>`, 'bot');
                return;
            }
            
            addMessage(`<p>${msg}</p>`, 'user');
            userInput.value = '';

            const thinkingMessages = ["Sorgunu işliyorum...", "Bilgiyi analiz ediyorum...", "Cevabı oluşturuyorum...", "Düşünüyor..."];
            const thinkingDivId = `thinking-${Date.now()}`;
            addMessage(`<em id="${thinkingDivId}">${thinkingMessages[0]}</em>`, 'bot');

            let idx = 0;
            const interval = setInterval(() => {
                const thinkingDiv = document.getElementById(thinkingDivId);
                if (thinkingDiv) {
                    idx++;
                    thinkingDiv.innerHTML = `<em>${thinkingMessages[idx % thinkingMessages.length]}</em>`;
                }
            }, 400);

            try {
                const token = JSON.parse(currentSession).access_token;
                
                const res = await fetch(`${BACKEND_URL}/api/chat`, {
                    method: "POST",
                    headers: { 
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({ question: msg })
                });

                const data = await res.json();
                
                clearInterval(interval);
                const thinkingDiv = document.getElementById(thinkingDivId);
                if (thinkingDiv) thinkingDiv.remove();

                if (!res.ok) {
                    addMessage(`<p><strong>API hatası:</strong> ${data.error || 'Bilinmeyen Hata'}</p>`, 'bot');
                } else {
                    const formattedResponse = formatMarkdown(data.text);
                    addMessage(formattedResponse, 'bot');
                }
            } catch (e) {
                clearInterval(interval);
                const thinkingDiv = document.getElementById(thinkingDivId);
                if (thinkingDiv) thinkingDiv.remove();
                addMessage(`Sunucuya bağlanılamadı.`, 'bot');
            }
        }
    }

    function setupLoginPage() {
        const loginBtn = document.getElementById('loginBtn');
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');
        const messageDiv = document.getElementById('message');

        loginBtn.addEventListener('click', async () => {
            const email = emailInput.value;
            const password = passwordInput.value;
            if (!email || !password) {
                messageDiv.textContent = 'Lütfen tüm alanları doldurun.';
                messageDiv.style.color = '#ff3333';
                return;
            }
            try {
                const res = await fetch(`${BACKEND_URL}/api/auth/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const data = await res.json();
                if (res.ok) {
                    localStorage.setItem('supabaseSession', JSON.stringify(data.session));
                    messageDiv.textContent = 'Giriş Başarılı! Yönlendiriliyorsunuz...';
                    messageDiv.style.color = '#00ffcc';
                    window.location.href = 'index.html'; 
                } else {
                    messageDiv.textContent = 'Giriş Başarısız: ' + data.error;
                    messageDiv.style.color = '#ff3333';
                }
            } catch (err) {
                messageDiv.textContent = 'Sunucuya bağlanılamadı.';
                messageDiv.style.color = '#ff3333';
            }
        });
    }

    function setupRegisterPage() {
        const registerBtn = document.getElementById('registerBtn');
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');
        const messageDiv = document.getElementById('message');
        registerBtn.addEventListener('click', async () => {
            const email = emailInput.value;
            const password = passwordInput.value;
            if (!email || !password) {
                messageDiv.textContent = 'Lütfen tüm alanları doldurun.';
                messageDiv.style.color = '#ff3333';
                return;
            }
            if (password.length < 6) {
                messageDiv.textContent = 'Şifre en az 6 karakter olmalıdır.';
                messageDiv.style.color = '#ff3333';
                return;
            }
            try {
                const res = await fetch(`${BACKEND_URL}/api/auth/register`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });
                const data = await res.json();
                if (res.ok) {
                    messageDiv.textContent = 'Kayıt başarılı! Lütfen e-postanızı kontrol ederek hesabınızı onaylayın.';
                    messageDiv.style.color = '#00ffcc';
                } else {
                    messageDiv.textContent = 'Kayıt Başarısız: ' + data.error;
                    messageDiv.style.color = '#ff3333';
                }
            } catch (err) {
                messageDiv.textContent = 'Sunucuya bağlanılamadı.';
                messageDiv.style.color = '#ff3333';
            }
        });
    }

    function setupProfilePage() {
        const session = localStorage.getItem('supabaseSession');
        if (!session) { window.location.href = 'login.html'; return; }
        const profileEmail = document.getElementById('profileEmail');
        const profilePlan = document.getElementById('profilePlan');
        const newPasswordInput = document.getElementById('newPassword');
        const updateProfileBtn = document.getElementById('updateProfileBtn');
        const messageDiv = document.getElementById('message');
        const sessionData = JSON.parse(session);
        profileEmail.textContent = sessionData.user.email;
        profilePlan.textContent = 'Free Plan';
        updateProfileBtn.addEventListener('click', async () => {
            const newPassword = newPasswordInput.value;
            if (newPassword && newPassword.length < 6) {
                messageDiv.textContent = 'Şifre en az 6 karakter olmalıdır.';
                messageDiv.style.color = '#ff3333';
                return;
            }
            try {
                const res = await fetch(`${BACKEND_URL}/api/profile/update`, {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${sessionData.access_token}`
                    },
                    body: JSON.stringify({ newPassword })
                });
                const data = await res.json();
                if (res.ok) {
                    messageDiv.textContent = 'Profil başarıyla güncellendi.';
                    messageDiv.style.color = '#00ffcc';
                } else {
                    messageDiv.textContent = `Güncelleme Başarısız: ${data.error}`;
                    messageDiv.style.color = '#ff3333';
                }
            } catch (err) {
                messageDiv.textContent = 'Sunucuya bağlanılamadı.';
                messageDiv.style.color = '#ff3333';
            }
        });
    }
    
    function setupSettingsPage() {
        const session = localStorage.getItem('supabaseSession');
        if (!session) { window.location.href = 'login.html'; return; }
        const themeSelect = document.getElementById('themeSelect');
        const manageSubscriptionBtn = document.getElementById('manageSubscriptionBtn');
        const messageDiv = document.getElementById('message');
        const subscriptionStatus = document.getElementById('subscriptionStatus');
        subscriptionStatus.textContent = 'Free Plan';
        manageSubscriptionBtn.addEventListener('click', () => {
            messageDiv.textContent = 'Abonelik yönetimi sayfasına yönlendiriliyorsunuz... (Örnek)';
            messageDiv.style.color = '#00ffcc';
        });
        themeSelect.addEventListener('change', (e) => {
            const theme = e.target.value;
            localStorage.setItem('theme', theme);
            document.body.className = theme;
            messageDiv.textContent = `${theme === 'dark' ? 'Koyu' : 'Açık'} tema uygulandı.`;
            messageDiv.style.color = '#00ffcc';
        });
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            document.body.className = savedTheme;
            themeSelect.value = savedTheme;
        }
    }
});