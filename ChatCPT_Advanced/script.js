function sendMessage() {
    let input = document.getElementById("user-input");
    let message = input.value;
    if (!message) return;
    
    let messagesDiv = document.getElementById("messages");
    let userMsg = document.createElement("div");
    userMsg.className = "user-msg";
    userMsg.innerText = "Siz: " + message;
    messagesDiv.appendChild(userMsg);

    // Burada PyQt ile Python backend'e soruyu göndermeyi yapacağız (socket veya QWebChannel)
    // Örnek olarak: cevap = ask_question(message)
    let botMsg = document.createElement("div");
    botMsg.className = "bot-msg";
    botMsg.innerText = "ChatCPT: " + "Burada Python cevabı gelecek";
    messagesDiv.appendChild(botMsg);

    input.value = "";
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
