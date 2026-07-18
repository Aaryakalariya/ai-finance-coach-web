// ai.js - AI chat page interactions
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatMessages = document.getElementById('chatMessages');

    if (!chatForm) return;

    function scrollToBottom() {
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
    scrollToBottom();

    function appendMessage(text, sender) {
        const bubble = document.createElement('div');
        bubble.className = `chat-bubble ${sender === 'user' ? 'chat-user' : 'chat-ai'}`;
        if (sender !== 'user') {
            const icon = document.createElement('i');
            icon.className = 'bi bi-robot';
            bubble.appendChild(icon);
        }
        const span = document.createElement('span');
        span.textContent = text;
        bubble.appendChild(span);
        chatMessages.appendChild(bubble);
        scrollToBottom();
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = chatInput.value.trim();
        if (!message) return;

        appendMessage(message, 'user');
        chatInput.value = '';

        const typing = document.createElement('div');
        typing.className = 'chat-bubble chat-ai';
        typing.innerHTML = '<i class="bi bi-robot"></i><span class="chat-typing-indicator"><span></span><span></span><span></span></span>';
        chatMessages.appendChild(typing);
        scrollToBottom();

        try {
            const formData = new FormData(chatForm);
            const res = await fetch(chatForm.action, {
                method: 'POST',
                body: formData,
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            const data = await res.json();
            typing.remove();
            appendMessage(data.reply || 'Sorry, I could not process that.', 'ai');
        } catch (err) {
            typing.remove();
            appendMessage('Something went wrong. Please try again.', 'ai');
            console.error(err);
        }
    });
});