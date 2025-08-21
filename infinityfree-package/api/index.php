<?php
// ChatCPT API - Router
require_once 'config.php';

// Get the request URI
$requestUri = $_SERVER['REQUEST_URI'];
$path = parse_url($requestUri, PHP_URL_PATH);

// Remove /api prefix if present
$path = preg_replace('#^/api#', '', $path);

// Route to appropriate file
switch ($path) {
    case '/health':
    case '/health.php':
        require_once 'health.php';
        break;
        
    case '/auth':
    case '/auth.php':
        require_once 'auth.php';
        break;
        
    case '/chat':
    case '/chat.php':
        require_once 'chat.php';
        break;
        
    default:
        sendResponse([
            'status' => 'OK',
            'message' => 'ChatCPT PHP API',
            'endpoints' => [
                '/health' => 'Health check',
                '/auth' => 'Authentication',
                '/chat' => 'Chat with AI'
            ]
        ]);
        break;
}
?>