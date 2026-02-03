const socket = io();

// DOM Elements
const statusText = document.getElementById('status-text');
const orb = document.getElementById('orb');
const chatBox = document.getElementById('chat-box');
const micBtn = document.getElementById('mic-btn');

let isListening = false;
let recognition;

// --- Web Speech API Setup ---
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (window.SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false; // We want to capture single commands when button pressed
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        isListening = true;
        updateUIState('Listening...');
        micBtn.classList.add('active');
    };

    recognition.onend = () => {
        isListening = false;
        micBtn.classList.remove('active');
        // Don't reset text immediately so user sees what happened
        // updateUIState('Ready'); 
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        console.log("Recognized:", transcript);
        addMessage(transcript, 'user');

        // Send to server
        socket.emit('send_command', { command: transcript });
        updateUIState('Processing...');
    };

    recognition.onerror = (event) => {
        console.error("Speech Error:", event.error);
        updateUIState('Error: ' + event.error);
        isListening = false;
        micBtn.classList.remove('active');
    };
} else {
    addMessage("Voice not supported on this browser.", "bot");
    micBtn.style.display = 'none';
}

// --- Event Listeners ---
micBtn.addEventListener('click', () => {
    if (!recognition) return;

    if (isListening) {
        recognition.stop();
    } else {
        recognition.start();
    }
});

// --- Socket.IO Events ---
socket.on('connect', () => {
    updateUIState('Connected');
});

socket.on('status_update', (data) => {
    statusText.innerText = data.status;
    updateOrb(data.status);
});

socket.on('anvi_response', (data) => {
    addMessage(data.data, 'bot');
    updateUIState('Active');
});

socket.on('user_message', (data) => {
    // Message from server-side listening (desktop mic)
    addMessage(data.data, 'user');
});

// --- UI Functions ---
function updateUIState(status) {
    statusText.innerText = status;
    updateOrb(status);
}

function updateOrb(status) {
    orb.className = 'orb'; // Reset
    if (status.toLowerCase().includes('listening')) {
        orb.classList.add('listening');
    } else if (status.toLowerCase().includes('active') || status.toLowerCase().includes('speaking') || status.toLowerCase().includes('processing')) {
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
