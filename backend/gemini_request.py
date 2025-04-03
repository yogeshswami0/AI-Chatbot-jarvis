import google.generativeai as genai
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class GeminiAI:
    def __init__(self):
        try:
            load_dotenv()
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
                
            # Configure with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    genai.configure(api_key=api_key)
                    # Use the latest Gemini Pro model
                    self.model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
                    logger.info(f"Using model: models/gemini-1.5-pro-latest")
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    continue
                    
            logger.info("Gemini AI configured successfully")
        except Exception as e:
            logger.error(f"Error configuring Gemini AI: {str(e)}")
            raise

    def generate_response(self, prompt):
        try:
            if not prompt or not isinstance(prompt, str):
                raise ValueError("Invalid prompt provided")
                
            # Configure generation parameters
            generation_config = {
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 2048,
            }
            
            # Generate response with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.model.generate_content(
                        prompt,
                        generation_config=generation_config
                    )
                    
                    if not response or not response.text:
                        raise ValueError("Empty response from model")
                        
                    return response.text
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"Generation attempt {attempt + 1} failed: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
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