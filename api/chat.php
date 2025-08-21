<?php
// ChatCPT API - Chat
require_once 'config.php';

try {
    // Check request method
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        sendError('Method not allowed', 405);
    }
    
    // Get authorization header
    $headers = getallheaders();
    $authHeader = $headers['Authorization'] ?? $headers['authorization'] ?? '';
    
    if (!$authHeader || !str_starts_with($authHeader, 'Bearer ')) {
        sendError('Missing or invalid authorization header', 401);
    }
    
    $token = substr($authHeader, 7);
    $tokenData = verifyToken($token);
    
    if (!$tokenData) {
        sendError('Invalid token', 401);
    }
    
    $userId = $tokenData['user_id'];
    
    // Get request data
    $input = json_decode(file_get_contents('php://input'), true);
    
    if (!$input) {
        sendError('Invalid JSON data');
    }
    
    $question = $input['question'] ?? '';
    
    if (!$question) {
        sendError('Question is required');
    }
    
    // Call Gemini AI API
    global $GEMINI_API_KEY;
    
    $geminiUrl = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" . $GEMINI_API_KEY;
    
    $geminiData = [
        'contents' => [
            [
                'parts' => [
                    [
                        'text' => "Sen ChatCPT adında Türkçe konuşan bir AI asistanısın. Kullanıcının sorusunu Türkçe olarak yanıtla: " . $question
                    ]
                ]
            ]
        ],
        'generationConfig' => [
            'temperature' => 0.7,
            'topK' => 40,
            'topP' => 0.95,
            'maxOutputTokens' => 1024
        ]
    ];
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $geminiUrl);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($geminiData));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json'
    ]);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($httpCode !== 200 || !$response) {
        sendError('AI service temporarily unavailable', 503);
    }
    
    $geminiResponse = json_decode($response, true);
    $aiResponse = $geminiResponse['candidates'][0]['content']['parts'][0]['text'] ?? 'Üzgünüm, cevap oluşturamadım.';
    
    // Save chat history to database
    $pdo = getDB();
    $stmt = $pdo->prepare("INSERT INTO chat_history (user_id, question, answer) VALUES (?, ?, ?)");
    $stmt->execute([$userId, $question, $aiResponse]);
    
    sendResponse([
        'text' => $aiResponse,
        'timestamp' => date('c')
    ]);
    
} catch (Exception $e) {
    error_log('Chat API Error: ' . $e->getMessage());
    sendError('Internal server error', 500);
}
?>