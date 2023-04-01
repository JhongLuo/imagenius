from api import create_image, list_labels, list_descriptions, delete_images, get_image
import base64
from io import BytesIO
from PIL import Image

def test_create():
    encoded_image = create_image("a cat attacking university of toronto").json()["content"]
    image_data = base64.b64decode(encoded_image)
    image = Image.open(BytesIO(image_data))
    image.show()
    print(list_labels().json())
    print(list_descriptions().json())
    
def test_get():
    print(get_image(labels=["cat"]))
    # print(get_image(labels=["cat"])["images"])
    
test_get()