import openai
import os
from service.utils import url2image
import random

openai.api_key = os.environ.get("OPENAI_API_KEY")

def prompt2image(prompt, n=1, size="256x256"):
    response = openai.Image.create(
        prompt= prompt,
        n=n,
        size=size
    )
    image_url = response['data'][0]['url']
    return url2image(image_url)


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


def generate_random_words():
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Generate one random words.",
        max_tokens=16,
        n=1,
        temperature=0.5
    )
    words = response.choices[0].text.strip().split("\n")
    return [word.capitalize() for word in words]
