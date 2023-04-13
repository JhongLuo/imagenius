from flask import Flask, jsonify, request, make_response

from service.utils import url2image
from service.dalle import prompt2image
from service.s3 import S3
from service.dynamo import Dynamo
from service.rekognition import Rekognition
from flask_cors import CORS
import json
import threading
app = Flask(__name__)
CORS(app)

s3 = S3()
s3_cache = S3("ece1779t18a3cache")
dynamo = Dynamo()
rekognition = Rekognition()
image_num = 1
temp_cache = dict()
temp_cache_lock = threading.Lock()
@app.route('/')
def hello():
    return 'Hello, Flask on AWS Lambda using Zappa!'


@app.route('/api/generate', methods = ['POST'])
def create_images():        
    prompt = request.form.get('prompt', None)
    if not prompt:
        return jsonify({
            'success': 'false',
            'error': {
                'message': 'prompt is required',
            }
        })
    return_images = []
    for _ in range(image_num):
        raw_image = prompt2image(prompt)
        image_path = s3_cache.store_image(raw_image)
        tags = rekognition.detect_labels(raw_image)
        with temp_cache_lock:
            key = len(temp_cache)
            temp_cache[key] = {
                'tags': tags,
                'image_path': image_path,
                'prompt': prompt,
            }
        return_images.append({
            'key': key,
            'src': s3_cache.path2url(image_path),
        })
    return jsonify({
        'success': 'true',
        'images' : return_images,
        'prompt': prompt
    })


@app.route('/api/save', methods = ['POST'])
def post_image():
    key_selections = json.loads(request.form.get('selected_keys', None))
    if not key_selections:
        return jsonify({
            'success': 'false',
            'error': {
                'message': 'selected_keys is required',
            }
        })
    print(key_selections)
    print(temp_cache.keys())
    for key in key_selections:
        print(key)
        if key not in temp_cache:
            return jsonify({
                'success': 'false',
                'error': {
                    'message': 'key not found',
                }
            })
        cache_image_path, tags, prompt = None, None, None
        with temp_cache_lock:
            cache_image_path = temp_cache[key]['image_path']
            tags = temp_cache[key]['tags']
            prompt = temp_cache[key]['prompt']
        image_path = s3.store_image(url2image(s3_cache.path2url(cache_image_path)))
        dynamo.put_image(image_path, tags, prompt)
    
    return jsonify({
        'success': 'true',
        'message': 'Images stored'
    })

@app.route('/api/images', methods = ['DELETE'])
def delete_images():
    dynamo.clear()
    s3.clear_images()
    return jsonify({
        'success': 'true',
        'message': 'All images deleted'
    })

@app.route('/api/search/tags', methods = ['POST'])
def search_by_tags():
    tags = json.loads(request.form.get('selected_tags', None))
    print(tags)
    image_paths = dynamo.labels_retrive(tags)
    all = dynamo.list_images()
    print(image_paths, all)
    images = [{
        "src": s3.path2url(image_path),
    } for image_path in image_paths]
    return jsonify({
        'success': 'true',
        'images': images
    })
    
@app.route('/api/tags', methods = ['GET'])
def list_tags():
    tags = dynamo.list_labels()
    return jsonify({
        'success': 'true',
        'tags': tags
    })

@app.route('/api/prompts', methods = ['GET'])
def list_prompts():
    prompts = dynamo.list_prompts()
    return jsonify({
        'success': 'true',
        'prompts': prompts
    })
