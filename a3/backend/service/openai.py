import openai
import os
from service.utils import url2image
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def prompt2images(prompt, n=1, size="256x256"):
    response = openai.Image.create(
        prompt=prompt,
        n=n,
        size=size
    )
    
    image_urls = [response['data'][i]['url'] for i in range(len(response['data']))]
    return [url2image(image_url) for image_url in image_urls]

def edit_image(prompt, image, mask, n=1, size="256x256"):
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
        max_tokens=60
    )
    jokes = [choice.text.strip() for choice in response.choices]
    joke = random.choice(jokes)
    #print(joke)
    return joke


def random_letter():
    return random.choice('abcdefghijklmnopqrstuvwxyz')

def generate_random_words(letter):
    response = openai.Completion.create(
        engine="text-davinci-002",
<<<<<<< HEAD
        prompt=f"Generate one random noun word start with {letter}.",
        max_tokens=16,
        n=1,
        temperature=0.6
=======
        prompt="Give me a random word",
        max_tokens=16,
        n=1,
        temperature=0.7
>>>>>>> main
    )
    words = response.choices[0].text.strip().split("\n")
    return [word.capitalize() for word in words]
