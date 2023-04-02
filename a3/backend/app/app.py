from flask import Flask, jsonify, request, make_response


from service.dalle import description2image
from service.s3 import S3
from service.dynamo import Dynamo
from service.rekognition import Rekognition
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

s3 = S3()
dynamo = Dynamo()
rekognition = Rekognition()

@app.route('/')
def hello():
    return "Hello, Flask on AWS Lambda using Zappa!"

@app.route('/images', methods = ['POST'])
def post_image():
    data = request.get_json()
    print(data)
    if "description" not in data or not data["description"]:
        return make_response(jsonify({
            "error": "description is required"
        }), 400)
        
    description = data['description']
    image, raw_image = description2image(description)
    image_path = s3.store_image(image)
    labels = rekognition.detect_labels(raw_image)
    dynamo.put_image(image_path, labels, description)
    return jsonify({
        "content": image,
        "description": description,
        "labels": labels
    })
 
@app.route('/images', methods = ['DELETE'])
def delete_images():
    dynamo.clear()
    s3.clear_images()
    return jsonify({
        "message": "All images deleted"
    })    

@app.route('/images', methods = ['GET'])
def get_images():
    description = request.args.get('description', None)
    labels = request.args.getlist('labels', None)
    if description:
        image_paths = dynamo.description_retrive(description)
    elif labels and len(labels) > 0:
        image_paths = dynamo.labels_retrive(labels)
    else: 
        image_paths = dynamo.list_images()

    images = [s3.read_image(image_path) for image_path in image_paths]
    return jsonify({
        "images": images
    })

@app.route('/labels', methods = ['GET'])
def list_labels():
    labels = dynamo.list_labels()
    return jsonify({
        "labels": labels
    })
    
@app.route('/descriptions', methods = ['GET'])
def list_descriptions():
    descriptions = dynamo.list_descriptions()
    return jsonify({
        "descriptions": descriptions
    })
