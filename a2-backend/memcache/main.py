from memcache import webapp, memcache
from flask import jsonify, request
from utils.CacheRing import key2hash
from memcache.Cache import Node
import sys

is_started = False

@webapp.route('/api/keys', methods=['GET'])
def get_keys():
    if not is_started:
        return jsonify({
            'success': 'false',
            'error': 'Server Not started'
        })
    memcache.total_requests += 1
    return jsonify({
        'success': 'true',
        'keys': list(memcache.keys())
    })
    
@webapp.route('/api/keys', methods=['DELETE'])
def delete_keys():
    if not is_started:
        return jsonify({
            'success': 'false',
            'error': 'Server Not started'
        })
    memcache.total_requests += 1
    memcache.clear()
    return jsonify({
        'success': 'true'
    })
    
@webapp.route('/api/key/<key>', methods=['GET'])
def get_key(key):
    if not is_started:
        return jsonify({
            'success': 'false',
            'error': 'Server Not started'
        })
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
    if not is_started:
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
    if not is_started:
        return jsonify({
            'success': 'false',
            'error': 'Server Not started'
        })
    memcache.total_requests += 1
    if memcache.has(key):
        memcache.delete(key)
        return jsonify({
            'success': 'true'
        })
    else:
        return jsonify({
            'success': 'false',
            'error': 'Key not found'
        })
        
        
@webapp.route('/api/range/<lower>/<upper>', methods=['GET'])
def get_range(lower, upper):
    if not is_started:
        return jsonify({
            'success': 'false',
            'error': 'Server Not started'
        })
    lower = int(lower)
    upper = int(upper)
    node_list = memcache.get_range(lower, upper)
    return jsonify({
        'success': 'true',
        'content': [node.to_json() for node in node_list]
    })
    
@webapp.route('/api/range/<lower>/<upper>', methods=['DELETE'])
def delete_range(lower, upper):
    if not is_started:
        return jsonify({
            'success': 'false',
            'error': 'Server Not started'
        })
    lower = int(lower)
    upper = int(upper)
    memcache.delete_range(lower, upper)
    return jsonify({
        'success': 'true'
    })
    
@webapp.route('/api/range', methods=['PATCH'])
def merge_range():
    if not is_started:
        return jsonify({
            'success': 'false',
            'error': 'Server Not started'
        })
    content = request.get_json()
    # node is encoded into json we need to decode it
    node_list = [Node.from_json(node) for node in content]
    memcache.merge_range(node_list)
    return jsonify({
        'success': 'true'
    })
    
@webapp.route('/api/bytes', methods=['GET'])
def get_bytes():
    if not is_started:
        return jsonify({
            'success': 'false',
            'error': 'Server Not started'
        })
    return jsonify({
        'success': 'true',
        'bytes': memcache.get_bytes()
    })
    
@webapp.route('/api/length', methods=['GET'])
def get_len():
    if not is_started:
        return jsonify({
            'success': 'false',
            'error': 'Server Not started'
        })
    return jsonify({
        'success': 'true',
        'length': len(memcache.get_len())
    })
    
@webapp.route('/api/start', methods=['POST'])
def start():
    global is_started
    is_started = True
    return jsonify({
        'success': 'true'
    })
    
@webapp.route('/api/start', methods=['POST'])
def stop():
    if not is_started:
        return jsonify({
            'success': 'false',
            'error': 'Server Not started'
        })
    is_started = False
    return jsonify({
        'success': 'true'
    })