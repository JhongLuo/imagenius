from flask import Flask, jsonify, request, make_response
import selectionpool
from service import openai, s3, dynamo, rekognition, opensearch, utils
from flask_cors import CORS
import time
import json
import threading
app = Flask(__name__)
CORS(app)

s3 = s3.S3()
s3_cache = s3.S3("ece1779t18a3cache")
selection_pool = selectionpool.SelectionPool()
dynamo = dynamo.Dynamo()
rekognition = rekognition.Rekognition()
image_num = 1
search_engine = opensearch.OSearch()

@app.route('/')
def hello():
    return 'Hello, Flask on AWS Lambda using Zappa!'


@app.route('/api/generate', methods = ['POST'])
def create_images():        
    prompt = request.form.get('prompt', None)
    if not prompt:
        if request.form.get('random', None):
            prompt = openai.generate_random_words()
        else:   
            return jsonify({
                'success': 'false',
                'error': {
                    'message': 'prompt is required',
                }
            })
    return_images = []
    for _ in range(image_num):
        raw_image = openai.prompt2image(prompt)
        image_path = selection_pool.add(prompt, raw_image)
        return_images.append({
            'key': image_path,
            'src': s3_cache.path2url(image_path),
        })

    return jsonify({
        'success': 'true',
        'images' : return_images,
        'prompt': prompt,
        'joke': openai.prompt2joke(prompt)
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
    for key in key_selections:
        try:
            selection_pool.choose(key)
        except Exception as e:
            return jsonify({
                'success': 'false',
                'error': {
                    'message': str(e),
                }
            })
    
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
        'key': image_path,
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
            'key': image_path,
            'src': s3.path2url(image_path),
        } for image_path in image_paths]
    })

@app.route('/api/list_all', methods = ['GET'])
def list_all():
    images = dynamo.list_images()
    return jsonify({
        'success': 'true',
        'images': [{
            'key': image_path,
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
        selection_pool.clean_expired()      
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
        
@app.route('/api/edit_image', methods = ['POST'])
def edit_image():
    prompt = request.form.get('prompt', None)
    x_pos = request.form.get('x_pos', None)
    y_pos = request.form.get('y_pos', None)
    radius = request.form.get('radius', None)
    image_path = request.form.get('key', None)
    if not x_pos or not y_pos or not radius or not image_path or not prompt:
        return jsonify({
            "success": "false",
            "error": {
                "message": "x_pos, y_pos, radius, key, prompt are all required",
            }
        })
    
        
    new_image = openai.edit_image(
        prompt=str(prompt),
        image=utils.url2fileobj(s3.path2url(image_path)),
        mask=utils.create_mask(
            x=x_pos,
            y=y_pos,
            r=radius,
        )
    )
    selection_pool.add(prompt, new_image)
    
    
    