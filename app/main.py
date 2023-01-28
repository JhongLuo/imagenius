from flask import render_template, url_for, request
from app import webapp, memcache, stats, db
from flask import json, jsonify
from . import storage_operations


@webapp.route('/')
def main():
    return render_template("main.html")


@webapp.route('/get', methods=['POST'])
def get():
    key = request.form.get('key')

    if key in memcache:
        value = memcache[key]
        response = webapp.response_class(
            response=json.dumps(value),
            status=200,
            mimetype='application/json'
        )
    else:
        response = webapp.response_class(
            response=json.dumps("Unknown key"),
            status=400,
            mimetype='application/json'
        )

    return response

@webapp.route('/upload-test', methods=['POST'])
def upload_test():
    image = request.files.get('image')
    try:
        filename = storage_operations.store_image(image)
        response = webapp.response_class(
            response=json.dumps("OK"),
            status=200,
            mimetype='application/json'
        )
    except Exception as e:
        response = webapp.response_class(
            response=json.dumps("Error: {}".format(e)),
            status=400,
            mimetype='application/json'
        )
    return response

@webapp.route('/put', methods=['POST'])
def put():
    key = request.form.get('key')
    value = request.form.get('value')
    memcache[key] = value

    response = webapp.response_class(
        response=json.dumps("OK"),
        status=200,
        mimetype='application/json'
    )

    return response

# Automatic Testing Endpoints

@webapp.route('/api/delete_all', methods=['POST'])
def delete_all():
    pass

@webapp.route('/api/upload', methods=['POST'])
def upload():
    pass

@webapp.route('/api/list_keys', methods=['POST'])
def list_keys():
    pass

@webapp.route('/api/key/<key_value>', methods=['POST'])
def get_key(key_value):
    pass

# self defined Endpoints

@webapp.route('/api/key/<key_value>', methods=['DELETE'])
def delete_key(key_value):
    pass

@webapp.route('/api/delete_cache/', methods=['POST'])
def delete_cache():
    pass

@webapp.route('/api/statistics/max_size/', methods=['PUT'])
def set_maxsize():
    pass

@webapp.route('/api/statistics/replacement_policy/', methods=['PUT'])
def set_replacement_policy():
    pass

@webapp.route('/api/statistics/', methods=['GET'])
def get_statistics():
    pass
