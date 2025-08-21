// Vercel Serverless API
const { createClient } = require('@supabase/supabase-js');

// Environment variables
const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY;
const GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent";

// Initialize Supabase
const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY, {
    auth: {
        autoRefreshToken: false,
        persistSession: false,
        detectSessionInUrl: false
    }
});

// CORS headers
const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400',
};

// Auth middleware
async function authMiddleware(req) {
    const authHeader = req.headers.authorization;
    if (!authHeader) {
        throw new Error('Yetkilendirme başlığı eksik.');
    }
    
    const token = authHeader.split(' ')[1];
    const { data: { user }, error } = await supabase.auth.getUser(token);
    
    if (error || !user) {
        throw new Error('Geçersiz veya süresi dolmuş token.');
    }
    
    return user;
}

module.exports = async (req, res) => {
    // Set CORS headers
    Object.keys(corsHeaders).forEach(key => {
        res.setHeader(key, corsHeaders[key]);
    });

    // Handle preflight
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }

    const { pathname } = new URL(req.url, `http://${req.headers.host}`);

    try {
        // Route handling
        if (pathname === '/api/health') {
            return res.json({
                status: 'OK',
                message: 'Vercel API is running',
                timestamp: new Date().toISOString(),
                region: process.env.VERCEL_REGION || 'unknown'
            });
        }

        if (pathname === '/api/auth/login') {
            if (req.method !== 'POST') {
                return res.status(405).json({ error: 'Method Not Allowed' });
            }

            const { email, password } = req.body;
            
            if (!email || !password) {
                return res.status(400).json({ error: 'E-posta ve şifre gereklidir.' });
            }

            const { data, error } = await supabase.auth.signInWithPassword({ email, password });
            
            if (error) {
                return res.status(401).json({ error: error.message });
            }

            return res.json({ session: data.session });
        }

        if (pathname === '/api/auth/register') {
            if (req.method !== 'POST') {
                return res.status(405).json({ error: 'Method Not Allowed' });
            }

            const { email, password } = req.body;
            
            if (!email || !password) {
                return res.status(400).json({ error: 'E-posta ve şifre gereklidir.' });
            }

            const { data, error } = await supabase.auth.signUp({ email, password });
            
            if (error) {
                return res.status(400).json({ error: error.message });
            }

            return res.json({ message: 'Kayıt başarılı! Lütfen e-postanızı kontrol edin.' });
        }

        if (pathname === '/api/chat') {
            if (req.method !== 'POST') {
                return res.status(405).json({ error: 'Method Not Allowed' });
            }

            // Auth check
            await authMiddleware(req);

            const { question } = req.body;
            
            if (!question) {
                return res.status(400).json({ error: 'Soru alanı boş olamaz.' });
            }

            // Gemini AI API call
            const fetch = (await import('node-fetch')).default;
            const response = await fetch(`${GEMINI_URL}?key=${GEMINI_API_KEY}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    contents: [{ parts: [{ text: question }] }] 
                })
            });

            const data = await response.json();
            
            if (data.error) {
                return res.status(500).json({ error: data.error.message || 'API Hatası' });
            }

            const botResponse = data.candidates[0].content.parts[0].text.trim();
            return res.json({ text: botResponse });
        }

        if (pathname === '/api/profile/update') {
            if (req.method !== 'POST') {
                return res.status(405).json({ error: 'Method Not Allowed' });
            }

            // Auth check
            await authMiddleware(req);

            const { newPassword } = req.body;
            
            if (newPassword) {
                const { error } = await supabase.auth.updateUser({ password: newPassword });
                
                if (error) {
                    return res.status(400).json({ error: error.message });
                }

                return res.json({ message: 'Şifre başarıyla güncellendi.' });
            } else {
                return res.status(400).json({ error: 'Güncellenecek veri sağlanmadı.' });
            }
        }

        // 404 for unknown routes
        return res.status(404).json({ error: 'Not Found' });

    } catch (error) {
        console.error('API Error:', error);
        return res.status(500).json({ 
            error: 'Internal Server Error',
            message: error.message 
        });
    }
};