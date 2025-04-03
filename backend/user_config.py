import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

class UserConfig:
    def __init__(self):
        load_dotenv()
        self.config = {
            'api_key': os.getenv('GEMINI_API_KEY'),
            'language': os.getenv('LANGUAGE', 'en-in'),
            'speech_rate': int(os.getenv('SPEECH_RATE', '170')),
            'voice_id': int(os.getenv('VOICE_ID', '0')),
            'debug_mode': os.getenv('DEBUG_MODE', 'False').lower() == 'true'
        }

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        # You can add code here to save to .env file if needed

    def validate(self):
        if not self.config['api_key']:
            raise ValueError("GEMINI_API_KEY is required in .env file")
        return True 