import requests

def url2image(url):
    return requests.get(url).content