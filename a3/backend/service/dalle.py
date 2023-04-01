import openai
import os
import requests
import base64

openai.api_key = os.environ.get("OPENAI_API_KEY")

def description2image(description, n=1, size="256x256"):
    response = openai.Image.create(
        prompt= description,
        n=n,
        size=size
    )
    print(response)
    image_url = response['data'][0]['url']
    response = requests.get(image_url)
    image = base64.b64encode(response.content).decode('utf-8')
    return image, response.content