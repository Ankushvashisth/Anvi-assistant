import sys
import importlib
import os

print("--- ANVI DIAGNOSTIC START ---")

def check_import(module_name):
    try:
        importlib.import_module(module_name)
        print(f"[PASS] Import {module_name}")
        return True
    except ImportError as e:
        print(f"[FAIL] Import {module_name}: {e}")
        return False
    except Exception as e:
        print(f"[FAIL] Import {module_name} (Unknown Error): {e}")
        return False

# 1. Check Dependencies
required = ['pyttsx3', 'speech_recognition', 'wikipedia', 'cv2', 'pyjokes']
all_deps = True
for r in required:
    if not check_import(r):
        all_deps = False

if not all_deps:
    print("CRITICAL: Missing dependencies. Attempting to install...")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

# 2. Check TTS
try:
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print(f"[PASS] TTS Initialized. Found {len(voices)} voices.")
except Exception as e:
    print(f"[FAIL] TTS Init: {e}")

# 3. Check Microphone (Availability Only)
try:
    import speech_recognition as sr
    mics = sr.Microphone.list_microphone_names()
    if len(mics) > 0:
        print(f"[PASS] Microphones found: {len(mics)}")
    else:
        print("[WARN] No microphones found.")
except Exception as e:
    print(f"[FAIL] Microphone Check: {e}")

# 4. Check Camera
try:
    import cv2
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        print("[PASS] Camera accessible.")
        cap.release()
    else:
        print("[WARN] Camera index 0 not accessible (might be in use or missing).")
except Exception as e:
    print(f"[FAIL] Camera Check: {e}")

# 5. Check Internet/Wikipedia
try:
    import wikipedia
    res = wikipedia.summary("Python (programming language)", sentences=1)
    if res:
        print("[PASS] Wikipedia/Internet accessible.")
except Exception as e:
    print(f"[FAIL] Wikipedia Check: {e}")

print("--- ANVI DIAGNOSTIC END ---")
