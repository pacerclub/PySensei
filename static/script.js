async function startNewConversation() {
    const response = await fetch('/new_chat', {
        method: 'POST'
    });

    const data = await response.json();
    if (data.chat_id) {
        window.location.href = `/chat/${data.chat_id}`;
    }
}

async function askQuestion() {
    const question = document.getElementById('question').value;
    if (!question.trim()) {
        alert('Please enter a question.');
        return;
    }
    const chatMessages = document.getElementById('chat-messages');
    const userMessageDiv = document.createElement('div');
    userMessageDiv.classList.add('chat-message', 'user');
    userMessageDiv.innerHTML = `<div class="message-content">${question}</div>`;
    chatMessages.appendChild(userMessageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    document.getElementById('question').value = '';

    const botMessageDiv = document.createElement('div');
    botMessageDiv.classList.add('chat-message', 'bot');
    botMessageDiv.innerHTML = `<div class="message-content">Generating message...</div>`;
    chatMessages.appendChild(botMessageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    const response = await fetch(`/ask/{{ chat_id }}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question })
    });

    const data = await response.json();
    botMessageDiv.innerHTML = `<div class="message-content">${data.error ? data.error : data.response}</div>`;
    Prism.highlightAll();
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        askQuestion();
    }
}

document.addEventListener('keydown', function(event) {
    if (event.key === 'n' && event.ctrlKey) {
        startNewConversation();
    }
});

window.onload = function() {
    if (!window.location.href.includes('chat')) {
        startNewConversation();
    }
    // Set the initial mode
    const mode = localStorage.getItem('mode') || 'light';
    if (mode === 'dark') {
        document.body.classList.add('dark-mode');
        document.getElementById('mode-switch').checked = true;
        document.getElementById('mode-icon').classList.replace('fa-sun', 'fa-moon');
        document.getElementById('prism-theme').href = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism-tomorrow.min.css";
    } else {
        document.getElementById('prism-theme').href = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism.min.css";
    }
};

async function confirmDelete(chat_id) {
    if (confirm('Are you sure you want to delete this conversation?')) {
        await fetch(`/delete_chat/${chat_id}`, {
            method: 'POST'
        });
        window.location.href = '/';
    }
}

function toggleMode() {
    const isDarkMode = document.body.classList.toggle('dark-mode');
    localStorage.setItem('mode', isDarkMode ? 'dark' : 'light');
    const icon = document.getElementById('mode-icon');
    if (isDarkMode) {
        icon.classList.replace('fa-sun', 'fa-moon');
        document.getElementById('prism-theme').href = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism-tomorrow.min.css";
    } else {
        icon.classList.replace('fa-moon', 'fa-sun');
        document.getElementById('prism-theme').href = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism.min.css";
    }
}

function copyToClipboard(button) {
    const codeBlock = button.parentElement.nextElementSibling.querySelector('code');
    const textArea = document.createElement('textarea');
    textArea.value = codeBlock.textContent;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
    button.textContent = 'Copied!';
    setTimeout(() => {
        button.textContent = 'Copy';
    }, 2000);
}