import openai
import os
from service.utils import url2image
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")
openai_usage = 0

def prompt2images(prompt, n=1, size="256x256"):
    global openai_usage
    openai_usage += n
    response = openai.Image.create(
        prompt=prompt,
        n=n,
        size=size
    )
    
    image_urls = [response['data'][i]['url'] for i in range(len(response['data']))]
    return [url2image(image_url) for image_url in image_urls]

def edit_image(prompt, image, mask, n=1, size="256x256"):
    global openai_usage
    openai_usage += n
    response = openai.Image.create_edit(
        image=image,
        mask=mask,
        prompt=prompt,
        n=n,
        size=size
    )
    image_urls = [response['data'][i]['url'] for i in range(len(response['data']))]
    return [url2image(image_url) for image_url in image_urls]

def prompt2joke(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Tell me a funny joke about {prompt}",
        max_tokens=100,
        temperature=1
    )
    jokes = [choice.text.strip() for choice in response.choices]
    joke = random.choice(jokes)
    return joke

def generate_random_word():
    prompt = """
    Think of something as the subject of an intriguing picture. The response should only contain one word in lowercase, without any punctuations.
    """
    response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=8,
            n=1,
            stop=None,
            temperature=1,
        )
    word = response.choices[0].text.strip()
    return word
