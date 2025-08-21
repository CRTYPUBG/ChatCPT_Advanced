// Vercel Serverless Function - Authentication
const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_KEY;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

module.exports = async function handler(req, res) {
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
        const { action, email, password } = req.body;
        
        if (!action || !email || !password) {
            return res.status(400).json({ error: 'Missing required fields' });
        }
        
        let result;
        
        if (action === 'login') {
            result = await supabase.auth.signInWithPassword({
                email: email,
                password: password
            });
        } else if (action === 'register') {
            result = await supabase.auth.signUp({
                email: email,
                password: password
            });
        } else {
            return res.status(400).json({ error: 'Invalid action' });
        }
        
        if (result.error) {
            return res.status(400).json({ error: result.error.message });
        }
        
        res.status(200).json({
            success: true,
            session: result.data.session,
            user: result.data.user
        });
        
    } catch (error) {
        console.error('Auth API Error:', error);
        res.status(500).json({ 
            error: 'Internal server error',
            message: error.message 
        });
    }
}