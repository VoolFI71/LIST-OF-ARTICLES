const ws_chat = new WebSocket("ws://localhost:8000/ws/chat");

ws_chat.onmessage = function(event) {
    const messages = document.getElementById('messages');
    const message = document.createElement('p');
    message.innerHTML = event.data;
    messages.appendChild(message);
};

async function sendMessage(event) {
    event.preventDefault();
    const input = document.getElementById('messageInput');
    const messageContent = input.value;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: messageContent }) 
        });

        if (!response.ok) {
            const data = await response.json();
            console.error("Ошибка:", data.detail);
        }
    } catch (error) {
        console.error("Ошибка при добавлении сообщения в базу данных:", error);
    }

    input.value = '';
}
