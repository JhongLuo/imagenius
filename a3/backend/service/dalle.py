import openai
import os
from service.utils import url2image

openai.api_key = os.environ.get("OPENAI_API_KEY")

def prompt2image(prompt, n=1, size="256x256"):
    response = openai.Image.create(
        prompt= prompt,
        n=n,
        size=size
    )
    image_url = response['data'][0]['url']
    return url2image(image_url)