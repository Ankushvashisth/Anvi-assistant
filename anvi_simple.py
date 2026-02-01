print("Combo Start")
try:
    from flask import Flask
    from flask_socketio import SocketIO
    import pyttsx3
    import speech_recognition as sr
    
    app = Flask(__name__)
    socketio = SocketIO(app, async_mode='threading')
    @app.route('/')
    def index(): return "Test"
    print("Web Init Done")
    
    engine = pyttsx3.init('sapi5')
    print("Engine Init Done")
    
    r = sr.Recognizer()
    print("SR Init Done")
    
    print("Combo Success")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
except Exception as e:
    print(f"Error: {e}")
