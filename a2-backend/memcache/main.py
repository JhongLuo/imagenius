from memcache import webapp, memcache
from flask import jsonify, request
from utils.cachering import key2hash
from memcache.Cache import Node
import sys


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
    
@webapp.route('/api/key/<key>', methods=['GET'])
def get_key(key):
    memcache.total_requests += 1
    memcache.read_requests += 1
    if not memcache.has(key):
        memcache.missed_requests += 1
        return jsonify({
            'success': 'false',
            'error': 'Key not found'
        })
    return jsonify({
        'success': 'true',
        'key': key,
        'content': memcache.get(key)
    })
    
@webapp.route('/api/key/<key>', methods=['POST'])
def set_key(key):
    if not memcache.is_started:
        return jsonify({
            'success': 'false',
            'error': 'Server Not started'
        })
    memcache.total_requests += 1
    content = request.get_json()
    if sys.getsizeof(content) >= memcache.max_size:
        return jsonify({
            'success': 'false',
            'error': 'Content too large'
        })
    memcache.set(key, content, key2hash(key))
    return jsonify({
        'success': 'true'
    })
    
@webapp.route('/api/key/<key>', methods=['DELETE'])
def delete_key(key):
    if memcache.has(key):
        memcache.delete(key)
    return jsonify({
        'success': 'true'
    })  
        
@webapp.route('/api/range/<lower>/<upper>', methods=['GET'])
def get_range(lower, upper):
    node_list = memcache.get_range(int(lower), int(upper))
    return jsonify({
        'success': 'true',
        'content': [node.to_json() for node in node_list]
    })
    
@webapp.route('/api/range/<lower>/<upper>', methods=['DELETE'])
def delete_range(lower, upper):
    memcache.delete_range(int(lower), int(upper))
    return jsonify({
        'success': 'true'
    })
    
@webapp.route('/api/range', methods=['PATCH'])
def merge_range():
    content = request.get_json()
    # node is encoded into json we need to decode it
    memcache.merge_range([Node.from_json(node) for node in content])
    return jsonify({
        'success': 'true'
    })
    
@webapp.route('/api/bytes', methods=['GET'])
def get_bytes():
    return jsonify({
        'success': 'true',
        'bytes': memcache.get_bytes()
    })
    
@webapp.route('/api/length', methods=['GET'])
def get_len():
    return jsonify({
        'success': 'true',
        'length': memcache.get_len()
    })
    
@webapp.route('/api/start', methods=['POST'])
def start():
    memcache.start()
    return jsonify({
        'success': 'true'
    })
    
@webapp.route('/api/stop', methods=['POST'])
def stop():
    memcache.stop()
    return jsonify({
        'success': 'true'
    })
    
@webapp.route('/api/id', methods=['POST'])
def set_id():
    id = int(request.get_json()['id'])
    memcache.id = id
    return jsonify({
        'success': 'true'
    })