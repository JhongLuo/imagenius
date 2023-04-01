from flask import Flask, Response
import os
import openai
import requests
import magic
from service.s3 import S3
from service.dynamo import Dynamo

app = Flask(__name__)

free_mode = False

s3 = S3()
dynamo = Dynamo()
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/')
def hello():
    return "Hello, Flask on AWS Lambda using Zappa!"

@app.route('/image/<description>', methods = ['POST', 'GET'])
def words2image(description):

    response = openai.Image.create(
        prompt= description,
        n=1,
        size="256x256"
    )
    print(response)
    image_url = response['data'][0]['url']
    response = requests.get(image_url)
    filename = s3.store_image(response.content)
    
    return Response(response.content, content_type=magic.from_buffer(response.content, mime=True))