from flask import Flask, jsonify, request, make_response


from service.dalle import prompt2image
from service.s3 import S3
from service.dynamo import Dynamo
from service.rekognition import Rekognition
from flask_cors import CORS
import threading
app = Flask(__name__)
CORS(app)

s3 = S3()
dynamo = Dynamo()
rekognition = Rekognition()
image_num = 2
temp_cache = dict()
temp_cache_lock = threading.Lock()
@app.route('/')
def hello():
    return "Hello, Flask on AWS Lambda using Zappa!"


"""
Transform user provided prompt to two images

required fields in json: 
    prompt : str

return json:
    images : list of dict
    prompt : str
    
image dict:
    key : int
    content : base64 encoded image
"""
@app.route('/api/generate', methods = ['POST'])
def create_images():        
    prompt = request.form.get("prompt", None)
    if not prompt:
        return make_response(jsonify({
            "error": "prompt is required"
        }), 400)

    return_images = []
    for _ in range(image_num):
        image, raw_image = prompt2image(prompt)
        labels = rekognition.detect_labels(raw_image)
        with temp_cache_lock:
            key = len(temp_cache)
            temp_cache[key] = {
                "labels": labels,
                "image": image,
                "prompt": prompt,
            }
        return_images.append({
            "key": key,
            "content": image
        })
    return jsonify({
        "images" : return_images,
        "prompt": prompt
    })


"""
Store images and labels in dynamo and s3

required fields in json:
    key_selections : list of int
    
return json:
    message : str
"""
@app.route('/api/images', methods = ['POST'])
def post_image():
    key_selections = request.form.get("key_selections", None)
    if not key_selections:
        return make_response(jsonify({
            "error": "key_selections is required"
        }), 400)
    for key in key_selections:
        if key not in temp_cache:
            return make_response(jsonify({
                "error": f"key {key} is invalid"
            }), 400)
        image, labels, prompt = None, None, None
        with temp_cache_lock:
            image = temp_cache[key]["image"]
            labels = temp_cache[key]["labels"]
            prompt = temp_cache[key]["prompt"]
        image_path = s3.store_image(image)
        dynamo.put_image(image_path, labels, prompt)
    
    return jsonify({
        "message": "Images stored"
    })

"""
delete all images in dynamo and s3
"""
@app.route('/api/images', methods = ['DELETE'])
def delete_images():
    dynamo.clear()
    s3.clear_images()
    return jsonify({
        "message": "All images deleted"
    })

"""
retrive images based on labels or prompt, frontend could provide either prompt or labels.
if both are provided, backend will ignore labels.
if neither is provided, backend will return all images.

required fields in query string:
    labels : list of str
    prompt : str
"""
@app.route('/api/images', methods = ['GET'])
def get_images():
    prompt = request.args.get('prompt', None)
    labels = request.args.getlist('labels', None)
    if prompt:
        image_paths = dynamo.prompt_retrive(prompt)
    elif labels and len(labels) > 0:
        image_paths = dynamo.labels_retrive(labels)
    else: 
        image_paths = dynamo.list_images()

    images = [s3.read_image(image_path) for image_path in image_paths]
    return jsonify({
        "images": images
    })

"""
list all labels
"""
@app.route('/api/labels', methods = ['GET'])
def list_labels():
    labels = dynamo.list_labels()
    return jsonify({
        "labels": labels
    })

"""
list all prompts
""" 
@app.route('/api/prompts', methods = ['GET'])
def list_prompts():
    prompts = dynamo.list_prompts()
    return jsonify({
        "prompts": prompts
    })
