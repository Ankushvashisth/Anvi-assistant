print("1. Start")
try:
    from flask import Flask
    print("2. Flask Imported")
    from flask_socketio import SocketIO
    print("3. SocketIO Imported")
    import pyttsx3
    print("4. pyttsx3 Imported")
    import speech_recognition as sr
    print("5. speech_recognition Imported")
    import cv2
    print("6. cv2 Imported")
except Exception as e:
    print(f"ERROR: {e}")

print("7. Init App")
app = Flask(__name__)
print("8. Init SocketIO")
socketio = SocketIO(app, async_mode='threading')
print("9. Done")
