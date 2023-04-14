from flask import Flask, jsonify, request, make_response, session

from service.utils import url2image
from service.openai import prompt2image, prompt2joke, generate_random_words
from service.s3 import S3
from service.dynamo import Dynamo
from service.rekognition import Rekognition
from service.opensearch import OSearch
from flask_cors import CORS
import time
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
largest_cache_key = 0
temp_cache_lock = threading.Lock()
search_engine = OSearch()
@app.route('/')
def hello():
    return 'Hello, Flask on AWS Lambda using Zappa!'


@app.route('/api/generate', methods = ['POST'])
def create_images():        
    prompt = request.form.get('prompt', None) or session.pop('random_word', None)
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
        joke = prompt2joke(prompt)
        with temp_cache_lock:
            key = largest_cache_key + 1
            largest_cache_key = key
        temp_cache[key] = {
            'tags': tags,
            'image_path': image_path,
            'prompt': prompt,
            'timestamp': time.time()
        }
        return_images.append({
            'key': key,
            'src': s3_cache.path2url(image_path),
        })
    return jsonify({
        'success': 'true',
        'images' : return_images,
        'prompt': prompt,
        'joke': joke
    })

@app.route('/api/generate-random', methods=['POST'])
def generate_random():
    if 'generate' in request.form:
        word = generate_random_words()
        session['random_word'] = word
        return jsonify({'word': word})
    elif 'regenerate' in request.form:
        word = generate_random_words()
        session['random_word'] = word
        return jsonify({'word': word})
    elif 'confirm' in request.form:
        word = session.get('random_word', None)
        if word:
            return jsonify({'success': True, 'word': word})
        else:
            return jsonify({'success': False, 'message': 'No random word found.'})
    else:
        return jsonify({'success': False, 'message': 'Invalid request.'})


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
    for key in key_selections:
        if key not in temp_cache:
            return jsonify({
                'success': 'false',
                'error': {
                    'message': 'key not found',
                }
            })
        cache_image_path, tags, prompt = None, None, None
        cache_image_path = temp_cache[key]['image_path']
        tags = temp_cache[key]['tags']
        prompt = temp_cache[key]['prompt']
        search_engine.add_prompt(prompt)
        image_path = s3.store_image(url2image(s3_cache.path2url(cache_image_path)))
        dynamo.put_image(image_path, tags, prompt)
    
    return jsonify({
        'success': 'true',
        'message': 'Images stored'
    })

@app.route('/api/images', methods = ['DELETE'])
def delete_images():
    s3_cache.clear_images()
    search_engine.clear()
    dynamo.clear()
    s3.clear_images()
    return jsonify({
        'success': 'true',
        'message': 'All images deleted'
    })

@app.route('/api/search/tags', methods = ['POST'])
def search_by_tags():
    tags = json.loads(request.form.get('selected_tags', None))
    image_paths = dynamo.labels_retrive(tags)
    images = [{
        "src": s3.path2url(image_path),
    } for image_path in image_paths]
    return jsonify({
        'success': 'true',
        'images': images
    })

@app.route('/api/search/prompt', methods = ['POST'])
def search_by_prompt():
    prompts = search_engine.search(request.form.get('prompt', None))
    image_paths = []
    for prompt in prompts:
        image_paths += dynamo.prompt_retrive(prompt)
    return jsonify({
        'success': 'true',
        'images': [{
            'src': s3.path2url(image_path),
        } for image_path in image_paths]
    })

@app.route('/api/list_all', methods = ['GET'])
def list_all():
    images = dynamo.list_images()
    return jsonify({
        'success': 'true',
        'images': [{
            'src': s3.path2url(image_path),
        } for image_path in images]
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

@app.route('/api/delete_cache', methods = ['POST'])
def delete_cache():
    try:
        keys_for_delete = []
        for key in temp_cache:
            timestamp = temp_cache[key]['timestamp']
            # if user don't save the image in 10 minutes, images will lost
            if time.time() - timestamp > 600:
                s3_cache.delete_image(temp_cache[key]['image_path'])
            keys_for_delete.append(key)
        
        for key in keys_for_delete:
            del temp_cache[key]
                    
        return jsonify({
            'success': 'true',
            'message': 'Cache deleted'
        })
    except Exception as e:
        return jsonify({
            'success': 'false',
            'error': {
                'message': str(e),
            }
        })
