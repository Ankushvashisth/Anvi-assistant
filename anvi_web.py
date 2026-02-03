from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import pyttsx3
import speech_recognition as sr
import threading
import time
import datetime
import webbrowser
import wikipedia
import pyjokes
# import cv2 
import logging
import sys
import os
import traceback
# Essential for Windows COM threading (TTS)
import pythoncom 

print("Anvi Web: Starting...")

# App Setup
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global Assistant State
ASSISTANT_ACTIVE = False
STOP_EVENT = threading.Event()
IS_SPEAKING = False
assistant = None

class AnviWebAssistant:
    def __init__(self):
        # COM initialization for this thread
        pythoncom.CoInitialize()
        self.engine = pyttsx3.init('sapi5')
        self._setup_voice()
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 3000
        self.recognizer.dynamic_energy_threshold = True

    def _setup_voice(self):
        try:
            voices = self.engine.getProperty('voices')
            voice_id = voices[0].id
            for voice in voices:
                if "female" in voice.name.lower() or "zira" in voice.name.lower():
                    voice_id = voice.id
                    break
            if len(voices) > 1: voice_id = voices[1].id
            self.engine.setProperty('voice', voice_id)
        except:
            pass
        self.engine.setProperty('rate', 170)

    def speak(self, text):
        global IS_SPEAKING
        IS_SPEAKING = True
        try:
            socketio.emit('anvi_response', {'data': text})
            self.engine.say(text)
            self.engine.runAndWait()
        except: pass
        IS_SPEAKING = False

    def listen(self):
        with sr.Microphone() as source:
            socketio.emit('status_update', {'status': 'Listening...'})
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                query = self.recognizer.recognize_google(audio, language='en-in')
                return query.lower()
            except: return None

def process_command(query):
    if not query: return
    print(f"Processing: {query}")
    socketio.emit('user_message', {'data': query})

    if 'open youtube' in query:
        assistant.speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com/")
        return "ACTIVE"
    elif 'open google' in query:
        assistant.speak("Opening Google.")
        webbrowser.open("https://www.google.com/")
        return "ACTIVE"
    elif 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M %p")
        assistant.speak(f"It is {strTime}")
        return "ACTIVE"
    elif 'joke' in query:
        assistant.speak(pyjokes.get_joke())
        return "ACTIVE"
    elif 'bye' in query or 'stop' in query:
        assistant.speak("Going to sleep.")
        return "SLEEP"
    elif "hi anvi" not in query:
        assistant.speak("I heard " + query)
        return "ACTIVE"
    return "ACTIVE"

def background_listener():
    global ASSISTANT_ACTIVE, assistant
    print("Background Listener Started")
    # COM init for the thread entry check (though init does it too)
    pythoncom.CoInitialize()
    
    time.sleep(2) 

    try:
        print("Initializing Assistant Logic...")
        assistant = AnviWebAssistant()
        print("Assistant Ready.")
        socketio.emit('status_update', {'status': 'Sleeping'})
    except Exception as e:
        print(f"Assistant Init Failed: {e}")
        traceback.print_exc()
        return

    while not STOP_EVENT.is_set():
        if IS_SPEAKING: 
            time.sleep(0.5)
            continue
            
        try:
            # Only listen if we are initialized
            query = assistant.listen()
        except: 
            query = None
            time.sleep(1)

        if query:
            print(f"Heard: {query}")
            if not ASSISTANT_ACTIVE:
                # WAKE WORD
                if "hi anvi" in query or "hey anvi" in query:
                    ASSISTANT_ACTIVE = True
                    assistant.speak("Hello! I am online.")
                    socketio.emit('status_update', {'status': 'Active'})
            else:
                # COMMAND
                result = process_command(query)
                if result == "SLEEP":
                    ASSISTANT_ACTIVE = False
                    socketio.emit('status_update', {'status': 'Sleeping'})
        
        socketio.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('status_update', {'status': 'Connected'})

@socketio.on('wake_up')
def handle_wake_up(data):
    global ASSISTANT_ACTIVE
    print(f"Wake Up Triggered: {data}")
    ASSISTANT_ACTIVE = True
    if assistant:
        assistant.speak("Hello! I am online.")
    emit('status_update', {'status': 'Active'})

@socketio.on('send_command')
def handle_client_command(data):
    """
    Handle text command received from the Web/PWA client.
    """
    command = data.get('command')
    if not command: return

    print(f"Received Remote Command: {command}")
    
    # Process the command just like a voice input
    # We set active true since they pressed the button
    global ASSISTANT_ACTIVE
    ASSISTANT_ACTIVE = True 
    
    # Send user message back to all clients (so desktop sees what mobile said)
    emit('user_message', {'data': command})

    # Process
    if assistant:
        process_command(command)


if __name__ == '__main__':
    print("Starting Main...")
    # Start thread
    t = threading.Thread(target=background_listener, daemon=True)
    t.start()
    
    # Run server
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print("\n" + "*"*50)
        print(f"MOBILE ACCESS: To use on your phone, connect to same Wi-Fi")
        print(f"and visit: http://{local_ip}:5000")
        print("*"*50 + "\n")
        
        socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
    except Exception as e:
        print(f"Run Error: {e}")
