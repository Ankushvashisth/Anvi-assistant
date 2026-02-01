print("V3 Start")
try:
    import pyttsx3
    print("Imported pyttsx3")
    engine = pyttsx3.init('sapi5')
    print("Initialized Engine")
    voices = engine.getProperty('voices')
    print(f"Voices: {len(voices)}")
    
    import speech_recognition as sr
    print("Imported SR")
    r = sr.Recognizer()
    print("Initialized SR")
    
    print("Success V3")
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
