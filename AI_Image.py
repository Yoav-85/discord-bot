import requests
from PIL import Image
from io import BytesIO
import time
def generate_ai_image(prompt):

    # Define the URL for Craiyon API
    url = "https://backend.craiyon.com/generate"

    # Define the data to send (prompt)
    data = {
        'prompt': prompt
    }

    # Send POST request to Craiyon API
    response = requests.post(url, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Craiyon typically returns a list of images
        # The response contains URLs of the generated images
        images = response.json()['images']

        # Download the first image in the list
        image_url = images[0]
        img_response = requests.get(image_url)

        if img_response.status_code == 200:
            # Open the image from the response content
            img = Image.open(BytesIO(img_response.content))

            # Save the image to a file
            img.save("craiyon_image.png")
            print("Image saved as craiyon_image.png")
    else:
        print(f"Error: {response.status_code}")