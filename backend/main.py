from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import logging
from speech import SpeechHandler
from gemini_request import GeminiAI
from user_config import UserConfig
from image_generation import ImageGenerator
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Changed from DEBUG to INFO to reduce log noise
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize configuration
config = UserConfig()
config.validate()

# Initialize Flask app with optimized settings
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, 
                   cors_allowed_origins="*",
                   async_mode='threading',  # Use threading instead of eventlet
                   ping_timeout=60,
                   ping_interval=25)

# Initialize components with retry logic
def initialize_components():
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Initializing components (attempt {attempt + 1}/{max_retries})")
            speech_handler = SpeechHandler()
            gemini_ai = GeminiAI()
            image_generator = ImageGenerator(config.get('api_key'))
            logger.info("All components initialized successfully")
            return speech_handler, gemini_ai, image_generator
        except Exception as e:
            logger.error(f"Error initializing components (attempt {attempt + 1}): {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise

try:
    speech_handler, gemini_ai, image_generator = initialize_components()
except Exception as e:
    logger.error(f"Failed to initialize components after retries: {str(e)}")
    raise

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No message provided'
            }), 400

        user_message = data.get('message', '')
        logger.info(f"Received chat message: {user_message}")
        
        try:
            response = gemini_ai.generate_response(user_message)
            if not response:
                raise ValueError("Empty response from Gemini AI")
                
            logger.info(f"Generated response: {response}")
            return jsonify({
                'status': 'success',
                'response': response
            })
        except Exception as ai_error:
            logger.error(f"Gemini AI error: {str(ai_error)}")
            # Try to get more specific error message
            error_message = str(ai_error)
            if "API key" in error_message:
                error_message = "Invalid or missing Gemini API key"
            elif "model" in error_message.lower():
                error_message = "Error with Gemini model configuration"
            elif "quota" in error_message.lower():
                error_message = "API quota exceeded"
            elif "network" in error_message.lower():
                error_message = "Network error while connecting to Gemini API"
                
            return jsonify({
                'status': 'error',
                'message': f"AI Error: {error_message}"
            }), 500
            
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"Server Error: {str(e)}"
        }), 500

@app.route('/api/speak', methods=['POST'])
def speak():
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No text provided'
            }), 400

        text = data.get('text', '')
        logger.info(f"Speaking text: {text}")
        
        success = speech_handler.speak(text)
        if success:
            return jsonify({'status': 'success'})
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to speak text'
            }), 500
    except Exception as e:
        logger.error(f"Error in speak endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/listen', methods=['POST'])
def listen():
    try:
        logger.info("Starting to listen...")
        text = speech_handler.listen()
        logger.info(f"Recognized text: {text}")
        
        return jsonify({
            'status': 'success',
            'text': text
        })
    except Exception as e:
        logger.error(f"Error in listen endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/generate_image', methods=['POST'])
def generate_image():
    try:
        data = request.json
        if not data or 'prompt' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No prompt provided'
            }), 400

        prompt = data.get('prompt', '')
        logger.debug(f"Generating image for prompt: {prompt}")
        
        response = image_generator.generate_image(prompt)
        return jsonify({
            'status': 'success',
            'image': response
        })
    except Exception as e:
        logger.error(f"Error in generate_image endpoint: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Quick health check without testing all components
        return jsonify({
            'status': 'ok',
            'message': 'Server is running'
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    try:
        logger.info("Starting Flask server...")
        # Run with optimized settings
        socketio.run(
            app, 
            debug=False,  # Disable debug mode for production
            host='127.0.0.1',  # Use localhost instead of 0.0.0.0
            port=5000,
            allow_unsafe_werkzeug=True,
            use_reloader=False  # Disable reloader to prevent double initialization
        )
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        raise
