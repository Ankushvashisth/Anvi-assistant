import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import cv2
import pyjokes
import threading
import time
import logging
import sys

# Configure Logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("anvi_debug.log", mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

class AnviAssistant:
    def __init__(self):
        logging.info("Initializing Anvi Assistant...")
        self.engine = pyttsx3.init('sapi5')
        self.stop_listening = False
        
        # Voice Settings
        voices = self.engine.getProperty('voices')
        # Try to find a female voice
        voice_id = voices[0].id # Default
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                voice_id = voice.id
                break
        try:
            # specifically asking for index 1 as per user request if available/female
            if len(voices) > 1:
                # Often index 1 is female (e.g., Zira on Windows)
                voice_id = voices[1].id
        except:
            pass
            
        self.engine.setProperty('voice', voice_id)
        self.engine.setProperty('rate', 180)
        self.engine.setProperty('volume', 1.0)
        
        self.recognizer = sr.Recognizer()
        # Ambient noise adjustment
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True

    def speak(self, text):
        """
        Text to speech function.
        """
        logging.info(f"Anvi Saying: {text}")
        print(f"Anvi: {text}")
        # We use a definition here that blocks only for the speech to finish
        # to ensure we don't listen to ourselves.
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logging.error(f"Error in speech: {e}")

    def wish_user(self):
        """
        Greets the user based on the time of day.
        """
        hour = int(datetime.datetime.now().hour)
        if 0 <= hour < 12:
            self.speak("Good Morning!")
        elif 12 <= hour < 18:
            self.speak("Good Afternoon!")
        else:
            self.speak("Good Evening!")
        
        self.speak("Hi, I'm Anvi, your personal assistant. How can I help you today?")

    def take_command(self):
        """
        Listens to microphone input and returns string query.
        """
        r = sr.Recognizer()
        with sr.Microphone() as source:
            logging.info("Listening...")
            print("Listening...")
            
            # Quick adjustment for ambient noise
            r.adjust_for_ambient_noise(source, duration=0.5) 
            r.pause_threshold = 1.0
            r.phrase_threshold = 1.0 # Minimum seconds of speaking
            
            try:
                # Timeout provided to not hang indefinitely
                audio = r.listen(source, timeout=5, phrase_time_limit=8)
                logging.info("Recognizing...")
                print("Recognizing...")
                
                query = r.recognize_google(audio, language='en-in')
                logging.info(f"User said: {query}")
                print(f"User: {query}")
                
            except sr.WaitTimeoutError:
                logging.info("Listening timeout.")
                return "None"
            except sr.UnknownValueError:
                logging.warning("Unknown value error. could not understand audio")
                self.speak("Sorry, say that again.")
                return "None"
            except sr.RequestError as e:
                logging.error(f"Could not request results; {e}")
                self.speak("Network error. Please check your connection.")
                return "None"
            except Exception as e:
                logging.error(f"Error: {e}")
                return "None"
                
        return query.lower()

    def open_camera(self):
        """
        Opens camera using OpenCV.
        """
        self.speak("Opening camera. Press 'q' to close.")
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Anvi Camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

    def process_command(self, query):
        """
        Process the string command.
        """
        if query == "none":
            return

        # Logic for executing tasks based on query
        if 'open youtube' in query:
            self.speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com/")

        elif 'open google' in query:
            self.speak("Opening Google.")
            webbrowser.open("https://www.google.com/")

        elif 'open gmail' in query:
            self.speak("Opening Gmail.")
            webbrowser.open("https://gmail.com")

        elif 'open instagram' in query:
            self.speak("Opening Instagram.")
            webbrowser.open("https://www.instagram.com/")

        elif 'call' in query:
            # Basic Call Mockup
            name = query.replace('call', '').strip()
            self.speak(f"Calling {name}...")
            # If you had ADB or Twilio, you would put the code here.
            print(f"Dialing {name}...")
            
        elif 'news' in query:
            self.speak("Opening Times of India.")
            webbrowser.open("https://timesofindia.indiatimes.com/")

        elif 'wikipedia' in query:
            self.speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "").strip()
            try:
                results = wikipedia.summary(query, sentences=2)
                self.speak("According to Wikipedia")
                print(results)
                self.speak(results)
            except Exception as e:
                self.speak("Sorry, I couldn't find any results.")
                logging.error(e)

        elif "what's the time" in query or "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            self.speak(f"The time is {strTime}")

        elif 'tell a joke' in query or 'joke' in query:
            joke = pyjokes.get_joke()
            self.speak(joke)
            
        elif 'camera' in query or 'photo' in query:
            # Run camera in a separate thread so it doesn't block the logic flow completely?
            # CV2 main loop needs to be in main thread often for GUI, 
            # but since we are inside a blocking function call, we just call it.
            self.open_camera()

        elif 'exit' in query or 'bye' in query or 'stop' in query:
            self.speak("Goodbye! Have a nice day.")
            self.stop_listening = True
            sys.exit()

        else:
            self.speak(f"Searching Google for {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")

    def run(self):
        """
        Main runner.
        """
        self.wish_user()
        
        while not self.stop_listening:
            try:
                query = self.take_command()
                if query != "None":
                    self.process_command(query)
            except KeyboardInterrupt:
                self.speak("Stopping...")
                break
            except Exception as e:
                logging.error(f"Critical error in main loop: {e}")


if __name__ == "__main__":
    try:
        assistant = AnviAssistant()
        assistant.run()
    except Exception as e:
        print(f"Error initializing assistant: {e}")
        logging.error(f"Critical Init Error: {e}")
    finally:
        input("\nPress Enter to exit...")
