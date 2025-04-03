import pyttsx3
import speech_recognition as sr
import logging

logger = logging.getLogger(__name__)

class SpeechHandler:
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[0].id)
            self.engine.setProperty("rate", 170)
            logger.info("Text-to-speech engine initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing text-to-speech engine: {str(e)}")
            raise

    def speak(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
            return True
        except Exception as e:
            logger.error(f"Error in speak: {str(e)}")
            return False

    def listen(self):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                logger.debug("Adjusting for ambient noise...")
                r.adjust_for_ambient_noise(source)
                logger.debug("Listening...")
                audio = r.listen(source)

            logger.debug("Recognizing speech...")
            text = r.recognize_google(audio, language='en-in')
            logger.debug(f"Recognized text: {text}")
            return text
        except Exception as e:
            logger.error(f"Error in listen: {str(e)}")
            raise 