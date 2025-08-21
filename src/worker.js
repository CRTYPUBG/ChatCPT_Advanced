// Cloudflare Worker - ChatCPT API
import { createClient } from '@supabase/supabase-js';

// CORS headers
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Access-Control-Max-Age': '86400',
};

// Environment variables
const SUPABASE_URL = 'https://qaepmzfqzpawaqktjrlw.supabase.co';
const SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFhZXBtemZxenBhd2Fxa3Rqcmx3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NTYyNTg0MSwiZXhwIjoyMDcxMjAxODQxfQ.upGDaFeYTzvxTcVkA4XIMoRpybyFbR9LEApu6XtrVT0';
const GEMINI_API_KEY = 'AIzaSyDKrMLRGaRyyUoRKKTw9ywFfBloMpMpXUM';
const GEMINI_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent';

// Initialize Supabase
const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

export default {
  async fetch(request, env, ctx) {
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    try {
      // Route handling
      if (path === '/api/health') {
        return handleHealth();
      } else if (path === '/api/auth/login') {
        return handleLogin(request);
      } else if (path === '/api/auth/register') {
        return handleRegister(request);
      } else if (path === '/api/chat') {
        return handleChat(request);
      } else if (path === '/api/profile/update') {
        return handleProfileUpdate(request);
      } else {
        return new Response('Not Found', { 
          status: 404,
          headers: corsHeaders 
        });
      }
    } catch (error) {
      console.error('Worker Error:', error);
      return new Response(JSON.stringify({ 
        error: 'Internal Server Error',
        message: error.message 
      }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  }
};

// Health check
async function handleHealth() {
  return new Response(JSON.stringify({
    status: 'OK',
    message: 'Cloudflare Worker is running',
    timestamp: new Date().toISOString(),
    region: 'Cloudflare Edge'
  }), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
  });
}

// Login handler
async function handleLogin(request) {
  if (request.method !== 'POST') {
    return new Response('Method Not Allowed', { status: 405, headers: corsHeaders });
  }

  const { email, password } = await request.json();
  
  if (!email || !password) {
    return new Response(JSON.stringify({ 
      error: 'E-posta ve şifre gereklidir.' 
    }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }

  try {
    const { data, error } = await supabase.auth.signInWithPassword({ 
      email, 
      password 
    });
    
    if (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    return new Response(JSON.stringify({ session: data.session }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  } catch (err) {
    return new Response(JSON.stringify({ 
      error: 'Sunucu tarafında bir hata oluştu.' 
    }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
}

// Register handler
async function handleRegister(request) {
  if (request.method !== 'POST') {
    return new Response('Method Not Allowed', { status: 405, headers: corsHeaders });
  }

  const { email, password } = await request.json();
  
  if (!email || !password) {
    return new Response(JSON.stringify({ 
      error: 'E-posta ve şifre gereklidir.' 
    }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }

  try {
    const { data, error } = await supabase.auth.signUp({ email, password });
    
    if (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    return new Response(JSON.stringify({ 
      message: 'Kayıt başarılı! Lütfen e-postanızı kontrol edin.' 
    }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  } catch (err) {
    return new Response(JSON.stringify({ 
      error: 'Sunucu tarafında bir hata oluştu.' 
    }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
}

// Chat handler with Gemini AI
async function handleChat(request) {
  if (request.method !== 'POST') {
    return new Response('Method Not Allowed', { status: 405, headers: corsHeaders });
  }

  // Auth middleware
  const authHeader = request.headers.get('Authorization');
  if (!authHeader) {
    return new Response(JSON.stringify({ 
      error: 'Yetkilendirme başlığı eksik.' 
    }), {
      status: 401,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }

  const token = authHeader.split(' ')[1];
  const { data: { user }, error } = await supabase.auth.getUser(token);
  
  if (error || !user) {
    return new Response(JSON.stringify({ 
      error: 'Geçersiz veya süresi dolmuş token.' 
    }), {
      status: 401,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }

  const { question } = await request.json();
  
  if (!question) {
    return new Response(JSON.stringify({ 
      error: 'Soru alanı boş olamaz.' 
    }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }

  try {
    // Gemini AI API call
    const response = await fetch(`${GEMINI_URL}?key=${GEMINI_API_KEY}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        contents: [{ parts: [{ text: question }] }] 
      })
    });

    const data = await response.json();
    
    if (data.error) {
      return new Response(JSON.stringify({ 
        error: data.error.message || 'API Hatası' 
      }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }

    const botResponse = data.candidates[0].content.parts[0].text.trim();
    
    return new Response(JSON.stringify({ text: botResponse }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  } catch (err) {
    return new Response(JSON.stringify({ 
      error: 'Sunucu tarafında bir hata oluştu.' 
    }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
}

// Profile update handler
async function handleProfileUpdate(request) {
  if (request.method !== 'POST') {
    return new Response('Method Not Allowed', { status: 405, headers: corsHeaders });
  }

  // Auth middleware
  const authHeader = request.headers.get('Authorization');
  if (!authHeader) {
    return new Response(JSON.stringify({ 
      error: 'Yetkilendirme başlığı eksik.' 
    }), {
      status: 401,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }

  const token = authHeader.split(' ')[1];
  const { data: { user }, error } = await supabase.auth.getUser(token);
  
  if (error || !user) {
    return new Response(JSON.stringify({ 
      error: 'Geçersiz veya süresi dolmuş token.' 
    }), {
      status: 401,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }

  const { newPassword } = await request.json();
  
  if (newPassword) {
    try {
      const { error } = await supabase.auth.updateUser({ password: newPassword });
      
      if (error) {
        return new Response(JSON.stringify({ error: error.message }), {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' }
        });
      }

      return new Response(JSON.stringify({ 
        message: 'Şifre başarıyla güncellendi.' 
      }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    } catch (err) {
      return new Response(JSON.stringify({ 
        error: 'Sunucu tarafında bir hata oluştu.' 
      }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }
      });
    }
  } else {
    return new Response(JSON.stringify({ 
      error: 'Güncellenecek veri sağlanmadı.' 
    }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' }
    });
  }
}