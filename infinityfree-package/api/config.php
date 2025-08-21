<?php
// ChatCPT API - Configuration
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');
header('Content-Type: application/json');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Environment variables
$SUPABASE_URL = 'https://qaepmzfqzpawaqktorlw.supabase.co';
$SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFhZXBtemZxenBhd2FxdGtvcmx3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczNzQ3NzE5MSwiZXhwIjoyMDUzMDUzMTkxfQ.Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8Ej8';
$GEMINI_API_KEY = 'AIzaSyDKrMLRGaRyyUoRKKTw9ywFfBloMpMpXxx1';

// Database configuration
// InfinityFree MySQL settings (update these with your actual database info)
$DB_HOST = 'sql200.epizy.com';  // InfinityFree MySQL host
$DB_NAME = 'epiz_xxxxx_chatcpt'; // Your database name
$DB_USER = 'epiz_xxxxx';         // Your database username  
$DB_PASS = 'your_password';      // Your database password

// For local development, use SQLite
$USE_SQLITE = (strpos($_SERVER['HTTP_HOST'], 'localhost') !== false || strpos($_SERVER['HTTP_HOST'], '127.0.0.1') !== false);

if ($USE_SQLITE) {
    $DB_FILE = __DIR__ . '/database.sqlite';
}

// Initialize database
function initDatabase() {
    global $USE_SQLITE, $DB_FILE, $DB_HOST, $DB_NAME, $DB_USER, $DB_PASS;
    
    if ($USE_SQLITE) {
        // SQLite for local development
        if (!file_exists($DB_FILE)) {
            $pdo = new PDO('sqlite:' . $DB_FILE);
            $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            
            // Create users table
            $pdo->exec("
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ");
            
            // Create chat_history table
            $pdo->exec("
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ");
        }
    } else {
        // MySQL for production (InfinityFree)
        try {
            $pdo = new PDO("mysql:host=$DB_HOST;dbname=$DB_NAME;charset=utf8", $DB_USER, $DB_PASS);
            $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            
            // Create users table
            $pdo->exec("
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ");
            
            // Create chat_history table
            $pdo->exec("
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ");
        } catch (Exception $e) {
            error_log('Database initialization error: ' . $e->getMessage());
        }
    }
}

// Get database connection
function getDB() {
    global $USE_SQLITE, $DB_FILE, $DB_HOST, $DB_NAME, $DB_USER, $DB_PASS;
    
    if ($USE_SQLITE) {
        $pdo = new PDO('sqlite:' . $DB_FILE);
    } else {
        $pdo = new PDO("mysql:host=$DB_HOST;dbname=$DB_NAME;charset=utf8", $DB_USER, $DB_PASS);
    }
    
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    return $pdo;
}

// Utility functions
function sendResponse($data, $status = 200) {
    http_response_code($status);
    echo json_encode($data);
    exit();
}

function sendError($message, $status = 400) {
    sendResponse(['error' => $message], $status);
}

// JWT Token functions (simple implementation)
function generateToken($userId) {
    $header = json_encode(['typ' => 'JWT', 'alg' => 'HS256']);
    $payload = json_encode([
        'user_id' => $userId,
        'exp' => time() + (24 * 60 * 60) // 24 hours
    ]);
    
    $base64Header = str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($header));
    $base64Payload = str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($payload));
    
    $signature = hash_hmac('sha256', $base64Header . "." . $base64Payload, 'your-secret-key', true);
    $base64Signature = str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($signature));
    
    return $base64Header . "." . $base64Payload . "." . $base64Signature;
}

function verifyToken($token) {
    $parts = explode('.', $token);
    if (count($parts) !== 3) {
        return false;
    }
    
    $header = $parts[0];
    $payload = $parts[1];
    $signature = $parts[2];
    
    $expectedSignature = hash_hmac('sha256', $header . "." . $payload, 'your-secret-key', true);
    $expectedSignature = str_replace(['+', '/', '='], ['-', '_', ''], base64_encode($expectedSignature));
    
    if ($signature !== $expectedSignature) {
        return false;
    }
    
    $payloadData = json_decode(base64_decode(str_replace(['-', '_'], ['+', '/'], $payload)), true);
    
    if ($payloadData['exp'] < time()) {
        return false;
    }
    
    return $payloadData;
}

// Initialize database
initDatabase();
?>