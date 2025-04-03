import google.generativeai as genai
import logging
from PIL import Image
import io
import base64

logger = logging.getLogger(__name__)

class ImageGenerator:
    def __init__(self, api_key):
        try:
            genai.configure(api_key=api_key)
            
            # Get available models
            available_models = genai.list_models()
            logger.info(f"Available models: {[m.name for m in available_models]}")
            
            # Try to find a suitable model for image generation
            model_name = None
            for model in available_models:
                if 'gemini' in model.name.lower() and ('vision' in model.name.lower() or 'flash' in model.name.lower()):
                    model_name = model.name
                    break
            
            if not model_name:
                # Fallback to a specific model if no match found
                model_name = 'models/gemini-1.5-pro-vision-latest'
                logger.warning(f"No model found, falling back to {model_name}")
                
            logger.info(f"Using model: {model_name}")
            self.model = genai.GenerativeModel(model_name)
            logger.info("Image generation model initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing image generation model: {str(e)}")
            raise

    def generate_image(self, prompt):
        try:
            # Note: This is a placeholder. You'll need to implement actual image generation
            # using the appropriate Gemini model for images
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            raise

    def process_image(self, image_data):
        try:
            # Convert base64 image data to PIL Image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            return image
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise 