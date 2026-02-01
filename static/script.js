const socket = io();

const statusText = document.getElementById('status-text');
const orb = document.getElementById('orb');
const chatBox = document.getElementById('chat-box');

// Speech Recognition Setup
window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let recognition;

if (window.SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        console.log("Voice recognition started. Listening for wake word...");
    };

    recognition.onresult = (event) => {
        const transcript = event.results[event.results.length - 1][0].transcript.trim().toLowerCase();
        console.log("Heard:", transcript);

        if (transcript.includes('hi anvi') || transcript.includes('hey anvi') || transcript.includes('hello anvi')) {
            console.log("Wake word detected via Web!");
            statusText.innerText = "Wake Word Detected!";
            socket.emit('wake_up', { message: "Wake word detected from web" });
            updateOrb('Listening');
        }
    };

    recognition.onerror = (event) => {
        console.error("Speech recognition error", event.error);
    };

    recognition.onend = () => {
        // Auto-restart for continuous listening
        recognition.start();
    };

    // Start listening immediately
    recognition.start();
} else {
    console.warn("Web Speech API not supported in this browser.");
    addMessage("Web Speech API not supported. Please use Chrome/Edge.", "bot");
}

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
