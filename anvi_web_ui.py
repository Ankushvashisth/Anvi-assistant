from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import threading
import time
import logging
import sys

# Safe Version: UI Only (Voice disabled to prevent audio driver crashes)
print("Anvi Web UI: Starting...")

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('status_update', {'status': 'Online (UI Mode)'})
    emit('anvi_response', {'data': 'Hi, I am Anvi. Voice mode is disabled in this safest launcher, but the UI is active!'})

@socketio.on('user_message')
def handle_message(data):
    # Echo back for UI testing
    print(f"User typed: {data}")
    emit('anvi_response', {'data': f"I received: {data}"})

if __name__ == '__main__':
    print("Starting Server at http://localhost:5000 ...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
