<?php
// ChatCPT API - Health Check
require_once 'config.php';

try {
    if ($_SERVER['REQUEST_METHOD'] === 'GET') {
        sendResponse([
            'status' => 'OK',
            'message' => 'ChatCPT PHP API is running',
            'timestamp' => date('c'),
            'version' => '1.0.0'
        ]);
    } else {
        sendError('Method not allowed', 405);
    }
    
} catch (Exception $e) {
    error_log('Health API Error: ' . $e->getMessage());
    sendError('Internal server error', 500);
}
?>