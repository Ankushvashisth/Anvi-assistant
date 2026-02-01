import sys
import logging

# Configure logging to console
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

print("1. Testing Imports...")
try:
    import pyttsx3
    import speech_recognition as sr
    import pyaudio
    import cv2
    print("   Imports Successful.")
except Exception as e:
    print(f"   IMPORT ERROR: {e}")
    sys.exit(1)

print("\n2. Testing TTS (Text-to-Speech)...")
try:
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    print(f"   Found {len(voices)} voices.")
    for v in voices:
        print(f"   - {v.name} ({v.id})")
    engine.say("Testing voice system.")
    engine.runAndWait()
    print("   TTS Successful.")
except Exception as e:
    print(f"   TTS ERROR: {e}")

print("\n3. Testing Microphone (PyAudio)...")
try:
    p = pyaudio.PyAudio()
    count = p.get_device_count()
    print(f"   Found {count} audio devices.")
    for i in range(count):
        info = p.get_device_info_by_index(i)
        if info.get('maxInputChannels') > 0:
            print(f"   Mic ID {i}: {info.get('name')}")
    p.terminate()
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("   Microphone initialized successfully from SpeechRecognition.")
        print("   Adjusting for ambient noise (please wait 1s)...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("   Done.")
except Exception as e:
    print(f"   MICROPHONE ERROR: {e}")
    # Common error: PyAudio not installed correctly or no mic found
