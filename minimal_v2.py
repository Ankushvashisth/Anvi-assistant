print("V2 Start")
try:
    from flask import Flask
    from flask_socketio import SocketIO
    import pyttsx3
    import speech_recognition as sr
    # import cv2  <-- Commented out
    print("Imports check: SUCCESS without CV2")
except Exception as e:
    print(f"Error: {e}")
