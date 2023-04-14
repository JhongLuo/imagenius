import requests
from io import BytesIO

def url2image(url):
    return requests.get(url).content

def image2fileobj(raw_image):
    return BytesIO(raw_image)

def url2fileobj(url):
    return image2fileobj(url2image(url))
    
def create_mask(x, y, r, size="256x256"):
    return None
    