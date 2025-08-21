// Vercel Serverless Function - Chat API
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_KEY;
const geminiApiKey = process.env.GEMINI_API_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

export default async function handler(req, res) {
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    if (req.method === 'OPTIONS') {
        res.status(200).end();
        return;
    }
    
    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }
    
    try {
        // Token doğrulama
        const authHeader = req.headers.authorization;
        if (!authHeader || !authHeader.startsWith('Bearer ')) {
            return res.status(401).json({ error: 'Missing or invalid authorization header' });
        }
        
        const token = authHeader.split(' ')[1];
        
        // Supabase ile token doğrulama
        const { data: user, error: authError } = await supabase.auth.getUser(token);
        if (authError || !user) {
            return res.status(401).json({ error: 'Invalid token' });
        }
        
        const { question } = req.body;
        if (!question) {
            return res.status(400).json({ error: 'Question is required' });
        }
        
        // Gemini AI API çağrısı
        const geminiResponse = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${geminiApiKey}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `Sen ChatCPT adında Türkçe konuşan bir AI asistanısın. Kullanıcının sorusunu Türkçe olarak yanıtla: ${question}`
                    }]
                }],
                generationConfig: {
                    temperature: 0.7,
                    topK: 40,
                    topP: 0.95,
                    maxOutputTokens: 1024,
                }
            })
        });
        
        if (!geminiResponse.ok) {
            throw new Error(`Gemini API error: ${geminiResponse.status}`);
        }
        
        const geminiData = await geminiResponse.json();
        const aiResponse = geminiData.candidates?.[0]?.content?.parts?.[0]?.text || 'Üzgünüm, cevap oluşturamadım.';
        
        // Chat geçmişini kaydet
        await supabase
            .from('chat_history')
            .insert([
                {
                    user_id: user.user.id,
                    question: question,
                    answer: aiResponse,
                    created_at: new Date().toISOString()
                }
            ]);
        
        res.status(200).json({
            text: aiResponse,
            timestamp: new Date().toISOString()
        });
        
    } catch (error) {
        console.error('Chat API Error:', error);
        res.status(500).json({ 
            error: 'Internal server error',
            message: error.message 
        });
    }
}