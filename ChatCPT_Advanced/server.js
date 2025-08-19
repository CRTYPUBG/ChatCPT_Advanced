// Gerekli kütüphaneleri dahil edin
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { createClient } = require('@supabase/supabase-js');
const path = require('path');

// YENİ DÜZENLEME: fetch fonksiyonunu doğru şekilde tanımla
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));


const app = express();
const PORT = 3000;

// Middleware'ler
app.use(cors());
app.use(express.json());

// .env dosyasından anahtarları alın
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY;
const GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent";

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY, {
    auth: {
        autoRefreshToken: false,
        persistSession: false,
        detectSessionInUrl: false
    }
});

// Yetkilendirme middleware'i
const authMiddleware = async (req, res, next) => {
    const authHeader = req.headers.authorization;
    if (!authHeader) {
        return res.status(401).json({ error: 'Yetkilendirme başlığı eksik.' });
    }
    const token = authHeader.split(' ')[1];

    const { data: { user }, error } = await supabase.auth.getUser(token);
    
    if (error || !user) {
        return res.status(401).json({ error: 'Geçersiz veya süresi dolmuş token.' });
    }

    req.user = user;
    next();
};

// Yönlendirme ve statik dosya sunumu
app.get('/', (req, res) => {
    res.redirect('/login.html');
});

// ui klasöründeki dosyaları statik olarak sunar
app.use(express.static(path.join(__dirname, 'ui')));

// Kayıt olma endpoint'i
app.post('/api/auth/register', async (req, res) => {
    const { email, password } = req.body;
    if (!email || !password) {
        return res.status(400).json({ error: 'E-posta ve şifre gereklidir.' });
    }
    try {
        const { data, error } = await supabase.auth.signUp({ email, password });
        if (error) { return res.status(400).json({ error: error.message }); }
        res.status(200).json({ message: 'Kayıt başarılı! Lütfen e-postanızı kontrol edin.' });
    } catch (err) {
        console.error('Kayıt hatası:', err);
        res.status(500).json({ error: 'Sunucu tarafında bir hata oluştu.' });
    }
});

// Giriş yapma endpoint'i
app.post('/api/auth/login', async (req, res) => {
    const { email, password } = req.body;
    if (!email || !password) { return res.status(400).json({ error: 'E-posta ve şifre gereklidir.' }); }
    try {
        const { data, error } = await supabase.auth.signInWithPassword({ email, password });
        if (error) { return res.status(401).json({ error: error.message }); }
        res.status(200).json({ session: data.session });
    } catch (err) {
        console.error('Giriş hatası:', err);
        res.status(500).json({ error: 'Sunucu tarafında bir hata oluştu.' });
    }
});

// Çıkış yapma endpoint'i
app.post('/api/auth/logout', async (req, res) => {
    const { error } = await supabase.auth.signOut();
    if (error) { return res.status(400).json({ error: error.message }); }
    res.status(200).json({ message: 'Başarıyla çıkış yapıldı.' });
});

// Gemini API'ye istek gönderme endpoint'i
app.post('/api/chat', authMiddleware, async (req, res) => {
    const { question } = req.body;
    if (!question) { return res.status(400).json({ error: 'Soru alanı boş olamaz.' }); }
    try {
        const response = await fetch(`${GEMINI_URL}?key=${GEMINI_API_KEY}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ contents: [{ parts: [{ text: question }] }] })
        });
        const data = await response.json();
        if (data.error) { return res.status(500).json({ error: data.error.message || 'API Hatası' }); }
        const botResponse = data.candidates[0].content.parts[0].text.trim();
        res.json({ text: botResponse });
    } catch (err) {
        console.error('API isteği hatası:', err);
        res.status(500).json({ error: 'Sunucu tarafında bir hata oluştu.' });
    }
});

// Profil güncelleme endpoint'i
app.post('/api/profile/update', authMiddleware, async (req, res) => {
    const { newPassword } = req.body;
    const { user } = req;
    if (newPassword) {
        try {
            const { error } = await supabase.auth.updateUser({ password: newPassword });
            if (error) { return res.status(400).json({ error: error.message }); }
            res.status(200).json({ message: 'Şifre başarıyla güncellendi.' });
        } catch (err) {
            res.status(500).json({ error: 'Sunucu tarafında bir hata oluştu.' });
        }
    } else {
        res.status(400).json({ error: 'Güncellenecek veri sağlanmadı.' });
    }
});

app.listen(PORT, () => {
    console.log(`Sunucu http://localhost:${PORT} adresinde çalışıyor`);
});