print("V4 Start")
try:
    from flask import Flask
    from flask_socketio import SocketIO
    app = Flask(__name__)
    print("App Init")
    socketio = SocketIO(app, async_mode='threading')
    print("SocketIO Init Success")
except Exception as e:
    print(f"Error: {e}")
