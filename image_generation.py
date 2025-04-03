# from openai import OpenAI
# import user_config
# import webbrowser

# import requests
# from PIL import Image

# client = OpenAI(api_key=user_config.openai_key)

# def generate_image(promt):
#     response = client.images.generate(
#         model = "dall-e-3",
#         prompt=promt,
#         n=1,
#         size="1024x1024",
#         quality="standard",
#     )

#     image_url = response.data[0].url
#     data = requests.get(image_url).content

#     f = open("img.jpg","wb")
#     f.write(data)
#     f.close()

#     webbrowser.open(image_url)

# # generate_image("Generate an image of boy with Python book in his hand.")



import google.generativeai as genai
import user_config
import webbrowser
import requests
from PIL import Image

# Configure Google Gemini API key
genai.configure(api_key=user_config.gemini_key)

def generate_image(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")  # Use the latest model

    response = model.generate_content(prompt)

    # Check if the response contains an image
    if hasattr(response, "parts") and response.parts:
        for part in response.parts:
            if hasattr(part, "image") and part.image:  # Extract image if available
                image_data = part.image
                
                with open("img.jpg", "wb") as f:
                    f.write(image_data)  # Save image locally
                
                print("✅ Image saved as img.jpg")
                webbrowser.open("img.jpg")  # Open the saved image
                return
            
    print("⚠️ No image generated!")

# Example Usage:
# generate_image("Generate an image of a goat standing on a mountain.")
