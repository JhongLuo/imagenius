from api import generate_images, save_images, list_labels, list_prompts, delete_images, get_image
import base64
from io import BytesIO
from PIL import Image

# def test_create():
#     response = generate_images("a cat attacking university of toronto")
#     print(response.status_code)
#     print(response.text)
#     encoded_image = response.json()["content"]
#     image_data = base64.b64decode(encoded_image)
#     image = Image.open(BytesIO(image_data))
#     image.show()
    
def test_get():
    response = get_image(labels=["Water"])
    print(response.status_code)
    print(response.text)
    

# print(list_labels().json())
# print(list_prompts().json())
# test_get()
