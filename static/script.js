const socket = io();

const statusText = document.getElementById('status-text');
const orb = document.getElementById('orb');
const chatBox = document.getElementById('chat-box');

socket.on('connect', () => {
    statusText.innerText = "Connected to Anvi Core";
});

socket.on('status_update', (data) => {
    statusText.innerText = data.status;
    updateOrb(data.status);
});

socket.on('anvi_response', (data) => {
    addMessage(data.data, 'bot');
});

socket.on('user_message', (data) => {
    addMessage(data.data, 'user');
});

function updateOrb(status) {
    orb.className = 'orb'; // Reset
    if (status.includes('Listening')) {
        orb.classList.add('listening');
    } else if (status.includes('Active') || status.includes('Speaking')) {
        orb.classList.add('active');
    } else {
        orb.classList.add('sleeping');
    }
}

function addMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('msg-content');
    contentDiv.innerText = text;
    
    msgDiv.appendChild(contentDiv);
    chatBox.appendChild(msgDiv);
    
    // Auto scroll
    chatBox.scrollTop = chatBox.scrollHeight;
}
