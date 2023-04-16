import requests
from io import BytesIO
from PIL import Image, ImageDraw

def url2image(url):
    return requests.get(url).content

def image2fileobj(raw_image):
    return BytesIO(raw_image)

def url2size(url):
    obj = url2fileobj(url)
    return Image.open(obj).size[0]

def url2fileobj(url):
    return image2fileobj(url2image(url))
    
def create_mask(x, y, r, size=256):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    draw.ellipse((x - r, y - r, x + r, y + r), fill=(0, 0, 0, 0))
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def url2imagepath(url):
    return url.split("/")[-1]

if __name__ == '__main__':
    create_mask(100, 100, 50)