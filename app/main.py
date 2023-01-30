from flask import render_template, request
from app import webapp, memcache, stats, db, scheduler
from flask import jsonify
from . import storage_operations, app_operations, db_operations
from .statistics import ReplacementPolicies
import logging

logger = logging.getLogger(__name__)

@webapp.route('/')
def main():
    return render_template("main.html")

# Automatic Testing Endpoints

'''
    Expected JSON response:
    {
        "success": "true"
    }

'''
@webapp.route('/api/delete_all', methods=['POST'])
def delete_all():
    global db
    global stats
    global memcache
    global scheduler
    db, stats, memcache, scheduler = app_operations.init_app(db=db, stats=stats, memcache=memcache, scheduler=scheduler)
    return jsonify({
        "success": "true"
    })

'''
    enctype = multipart/form-data
    POST parameter: name = key, type = string
    POST parameter: name = file, type = file
    Expected JSON response:
    {
        "success": "true",
        "key": [String]
    }
'''
@webapp.route('/api/upload', methods=['Get','POST'])
def upload():
    if request.method == 'POST':
        key = request.form.get('key')
        file = request.files.get('file')
        if not key or not file:
            return jsonify({
                "success": "false",
                "error": "Invalid key or file"
            })
        global memcache
        if key in memcache:
            del memcache[key]
        filename = storage_operations.store_image(file)
        filedict = storage_operations.filename2dict(filename)
        memcache[key] = filedict
        global stats
        stats.memcache_updated(memcache)
        global db
        db_operations.set_key(db, key, filename)

        logger.debug(f'memcache keys: {memcache.keys()}')
        logger.debug(f'stats: {stats.dump()}')
        logger.debug(f'db: {db_operations.get_statistics(db)}')

        return jsonify({
            "success": "true",
            "key": key
        })
    else:
        return render_template("upload.html")

    '''
        Expected JSON response:
        {
            "success": "true",
            "keys": [Array of keys (Strings)]
    }
    '''
@webapp.route('/api/list_keys', methods=['POST'])
def list_keys():
    return jsonify({
        "success": "true",
        "keys": list(memcache.keys())
    })

'''
    Expected JSON response:
    {
        "success": "true",
        "key" : [String],
        "content" : file contents
    }
'''
@webapp.route('/api/key/<key_value>', methods=['POST'])
def get_key(key_value):
    global memcache
    global stats
    stats.add_request_count(key_value in memcache)
    if key_value not in memcache:
        global db
        filename = db_operations.key2filename(db, key_value)
        if filename is None:
            return jsonify({
                "success": "false",
                "error": "Key not found"
            })
        filedict = storage_operations.filename2dict(filename)
        memcache[key_value] = filedict
        stats.memcache_updated(memcache)

    return jsonify({
        "success": "true",
        "key": key_value,
        "content": memcache[key_value]
    })

# self defined Endpoints

@webapp.route('/api/key/<key_value>', methods=['DELETE'])
def delete_key(key_value):
    global memcache
    if key_value in memcache:
        del memcache[key_value]
        global stats
        stats.memcache_updated(memcache)
    global db
    filename = db_operations.key2filename(db, key_value)
    if not filename:
        return jsonify({
            'success': 'false',
            'key': key_value,
            'error': 'Key not found'
        })
    else:
        db_operations.delete_key(db, key_value)
        storage_operations.delete_image(filename)
        return jsonify({
            'success': 'true',
            'key': key_value
        })

@webapp.route('/api/delete_cache', methods=['POST'])
def delete_cache():
    global memcache
    memcache.clear()
    global stats
    stats.memcache_updated(memcache)
    return jsonify({
        'success': 'true'
    })
    
@webapp.route('/api/statistics/max_size', methods=['PUT'])
def set_maxsize():
    global stats
    stats.max_size = request.form.get('max_size')
    return jsonify({
        'success': 'true',
        'max_size': stats.max_size
    })

@webapp.route('/api/statistics/replacement_policy', methods=['PUT'])
def set_replacement_policy():
    global stats
    try:
        stats.replacement_policy = ReplacementPolicies.str2policy(request.form.get('replacement_policy'))
        return jsonify({
            'success': 'true'
        })
    except Exception as e:
        return jsonify({
            'success': 'false',
            'error': 'Invalid replacement policy'
        })
    
@webapp.route('/api/statistics', methods=['GET'])
def get_statistics():
    global stats
    return jsonify({
        'success': 'true',
        'statistics': stats.dump()
    })
