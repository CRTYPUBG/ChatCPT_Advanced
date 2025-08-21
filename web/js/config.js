// ChatCPT Web - Configuration
// API URL configuration for different platforms

const CONFIG = {
    // Platform detection
    PLATFORM: detectPlatform(),
    
    // API URLs for different platforms
    API_URLS: {
        'localhost': 'http://localhost/api',
        'github.io': 'https://chatcpt-api.epizy.com/api',  // InfinityFree API
        'railway.app': window.location.origin + '/api',    // Railway full-stack
        'onrender.com': window.location.origin + '/api',   // Render full-stack
        'vercel.app': window.location.origin + '/api',     // Vercel
        'netlify.app': 'https://chatcpt-api.epizy.com/api', // Netlify + External API
        'default': window.location.origin + '/api'
    },
    
    // Get current API URL
    getApiUrl() {
        const hostname = window.location.hostname;
        
        // Check for specific platforms
        for (const [platform, url] of Object.entries(this.API_URLS)) {
            if (hostname.includes(platform)) {
                return url;
            }
        }
        
        // Default fallback
        return this.API_URLS.default;
    },
    
    // Feature flags based on platform
    FEATURES: {
        hasBackend: !window.location.hostname.includes('github.io') || window.location.hostname.includes('chatcpt.github.io'),
        hasDatabase: true,
        hasAuth: true,
        hasChat: true
    }
};

// Platform detection function
function detectPlatform() {
    const hostname = window.location.hostname;
    
    if (hostname.includes('localhost') || hostname.includes('127.0.0.1')) {
        return 'localhost';
    } else if (hostname.includes('github.io')) {
        return 'github.io';
    } else if (hostname.includes('railway.app')) {
        return 'railway.app';
    } else if (hostname.includes('onrender.com')) {
        return 'onrender.com';
    } else if (hostname.includes('vercel.app')) {
        return 'vercel.app';
    } else if (hostname.includes('netlify.app')) {
        return 'netlify.app';
    } else {
        return 'custom';
    }
}

// Debug info
console.log('🚀 ChatCPT Config:', {
    platform: CONFIG.PLATFORM,
    apiUrl: CONFIG.getApiUrl(),
    features: CONFIG.FEATURES,
    hostname: window.location.hostname
});

// Export for use in other files
window.ChatCPTConfig = CONFIG;