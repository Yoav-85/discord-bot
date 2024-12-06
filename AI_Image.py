import requests
import os
from dotenv import load_dotenv
load_dotenv()
def generate_ai_image(prompt):
    # Your DeepAI API key
    api_key = os.getenv("API_KEY")
    # DeepAI API endpoint for Text-to-Image
    url = "https://api.deepai.org/api/text2img"

    # Send POST request
    response = requests.post(url, data={'text': prompt}, headers={'api-key': api_key})
    print(response)

    # Save the generated image
    if response.status_code == 200:
        img_url = response.json()['output_url']
        img_data = requests.get(img_url).content
        with open("deepai_generated_image.jpg", "wb") as file:
            file.write(img_data)
        print("Image saved as deepai_generated_image.jpg")
    else:
        print(f"Error: {response.status_code}")

#TODO fix the problem line 12