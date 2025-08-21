<?php
// ChatCPT API - Authentication
require_once 'config.php';

try {
    // Get request data
    $input = json_decode(file_get_contents('php://input'), true);
    
    if (!$input) {
        sendError('Invalid JSON data');
    }
    
    $action = $input['action'] ?? '';
    $email = $input['email'] ?? '';
    $password = $input['password'] ?? '';
    
    if (!$action || !$email || !$password) {
        sendError('Missing required fields');
    }
    
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        sendError('Invalid email format');
    }
    
    $pdo = getDB();
    
    if ($action === 'register') {
        // Register new user
        
        if (strlen($password) < 6) {
            sendError('Password must be at least 6 characters');
        }
        
        // Check if user already exists
        $stmt = $pdo->prepare("SELECT id FROM users WHERE email = ?");
        $stmt->execute([$email]);
        
        if ($stmt->fetch()) {
            sendError('User already exists');
        }
        
        // Hash password
        $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
        
        // Insert new user
        $stmt = $pdo->prepare("INSERT INTO users (email, password) VALUES (?, ?)");
        $stmt->execute([$email, $hashedPassword]);
        
        $userId = $pdo->lastInsertId();
        $token = generateToken($userId);
        
        sendResponse([
            'success' => true,
            'message' => 'Registration successful',
            'session' => [
                'access_token' => $token,
                'user' => [
                    'id' => $userId,
                    'email' => $email
                ]
            ],
            'user' => [
                'id' => $userId,
                'email' => $email
            ]
        ]);
        
    } elseif ($action === 'login') {
        // Login user
        
        $stmt = $pdo->prepare("SELECT id, password FROM users WHERE email = ?");
        $stmt->execute([$email]);
        $user = $stmt->fetch(PDO::FETCH_ASSOC);
        
        if (!$user || !password_verify($password, $user['password'])) {
            sendError('Invalid email or password');
        }
        
        $token = generateToken($user['id']);
        
        sendResponse([
            'success' => true,
            'message' => 'Login successful',
            'session' => [
                'access_token' => $token,
                'user' => [
                    'id' => $user['id'],
                    'email' => $email
                ]
            ],
            'user' => [
                'id' => $user['id'],
                'email' => $email
            ]
        ]);
        
    } else {
        sendError('Invalid action');
    }
    
} catch (Exception $e) {
    error_log('Auth API Error: ' . $e->getMessage());
    sendError('Internal server error', 500);
}
?>