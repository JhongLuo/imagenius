from memcache import webapp, memcache
from flask import jsonify, request


@webapp.route('/api/keys', methods=['GET'])
def get_keys():
    return jsonify({
        'success': 'true',
        'keys': list(memcache.keys())
    })
    
@webapp.route('/api/keys', methods=['DELETE'])
def delete_keys():
    memcache.clear()
    return jsonify({
        'success': 'true'
    })
    
@webapp.route('/api/key/<key_value>', methods=['GET'])
def get_key(key_value):
    if key_value not in memcache:
        return jsonify({
            'success': 'false',
            'error': 'Key not found'
        })
    return jsonify({
        'success': 'true',
        'key': key_value,
        'content': memcache[key_value]
    })
    
@webapp.route('/api/key/<key_value>', methods=['POST'])
def set_key(key_value):
    content = request.get_json()
    memcache[key_value] = content
    return jsonify({
        'success': 'true'
    })
    
@webapp.route('/api/key/<key_value>', methods=['DELETE'])
def delete_key(key_value):
    if key_value in memcache:
        del memcache[key_value]
    return jsonify({
        'success': 'true'
    })