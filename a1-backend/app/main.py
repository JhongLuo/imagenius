from flask import render_template, request, redirect, url_for, flash
from app import webapp, stats, db, scheduler
from flask import jsonify
from . import storage_operations, app_operations, memcache_operations
from utils.ReplacementPolicies import ReplacementPolicies
import logging

logger = logging.getLogger(__name__)

# Automatic Testing Endpoints

# TODO: handle all error cases according to following:
# {
#     'success': "false",
#     'error': {
#         'code': int (server_error_code)
#         'message': str (error_message)
#     }
# }

'''
==== UPLOAD PAGE ====
'''

'''
    Upload Image
    ----
    enctype = multipart/form-data
    POST parameter: name = key, type = str
    POST parameter: name = file, type = file
    Expected JSON response:
    {
        'success': "true",
        'key': [str]
    }
'''
@webapp.route('/api/upload', methods=['POST'])
def upload():
    key = request.form.get('key')
    file = request.files.get('file')
    if not key or not file:
        return jsonify({
            'success': "false",
            'error': 'Invalid key or file'
        })
    memcache_operations.delete_key(key)
    filename = storage_operations.store_image(file)
    filedict = storage_operations.filename2dict(filename)
    memcache_operations.set_key(key, filedict)
    db.set_key(key, filename)

    return jsonify({
        'success': "true",
        'key': key
    })

'''
==== QUERY PAGE ====
'''

'''
    Retrieve Image
    ----
    Expected JSON response:
    {
        'success': "true",
        'key' : [str],
        'content' : file contents
    }
'''
@webapp.route('/api/key/<key_value>', methods=['GET'])
def get_image(key_value):
    json_content = memcache_operations.get_key(key_value)
    is_hit = "true"
    if not json_content:
        is_hit = "false"
        filename = db.key2path(key_value)
        if filename is None:
            return jsonify({
                'success': "false",
                'error': 'Key not found'
            })
        json_content = storage_operations.filename2dict(filename)
        memcache_operations.set_key(key_value, json_content)
    stats.add_request_count(is_hit)
    return jsonify({
        'success': "true",
        'key': key_value,
        'content': json_content
    })

'''
    Retrieve Image (POST variant)
'''
@webapp.route('/api/key/<key_value>', methods=['POST'])
def get_image_alt_post(key_value):
    return get_image(key_value)

'''
==== Keys PAGE ====
'''

'''
    Get All Keys
    ----
    Expected JSON response:
    {
        'success': "true",
        'keys': [str]
    }
'''
@webapp.route('/api/list_keys', methods=['GET'])
def list_keys():
    return jsonify({
        'success': "true",
        'keys': db.get_keys()
    })

'''
    Get All Keys (POST variant)
'''
@webapp.route('/api/list_keys', methods=['POST'])
def list_keys_alt_post():
    return list_keys()

'''
    Delete All
    ----
    Expected JSON response:
    {
        'success': "true"
    }
'''
@webapp.route('/api/delete_all', methods=['POST'])
def delete_all():
    global db
    global stats
    global scheduler
    db, stats, scheduler = app_operations.init_app(db=db, stats=stats, scheduler=scheduler)
    return jsonify({
        'success': "true"
    })

# self defined Endpoints

'''
==== CONFIG PAGE ====
'''

'''
    Get Cache Keys
    ----
    Expected JSON response:
    {
        'success': "true",
        'keys': [str]
}
'''
@webapp.route('/api/cache_keys', methods=['GET'])
def get_cache_keys():
    return jsonify({
        'success': "true",
        'keys': list(memcache_operations.get_keys())
    })

'''
    Get Cache Configs
    ----
    Expected JSON response:
    {
        'success': "true",
        'replacement_policy': str,
        'max_size': str
    }
'''
@webapp.route('/api/cache_configs', methods=['GET'])
def get_cache_configs():
    return jsonify({
        'success': "true",
        'replacement_policy': ReplacementPolicies.policy2str(stats.replacement_policy),
        'max_size': stats.max_size

    })

'''
    Set Cache Configs
    ----
    Expected request JSON:
    {
        "replacement_policy": str ("LRU" / "random"),
        "max_size": int (in bytes)
    }
    Expected JSON response:
    {
        'success': "true",
        'replacement_policy': str,
        'max_size': float
    }
'''
@webapp.route('/api/cache_configs', methods=['PUT'])
def set_cache_configs():
    try:
        stats.replacement_policy = ReplacementPolicies.str2policy(request.form.get('replacement_policy'))
        stats.max_size = float(request.form.get('max_size'))
        return jsonify({
            'success': "true",
            'replacement_policy': ReplacementPolicies.policy2str(stats.replacement_policy),
            'max_size': stats.max_size

        })
    except Exception:
        return jsonify({
            'success': "false",
            'error': 'Invalid replacement policy'
        })

'''
    Clear Cache
    ----
    Expected JSON response:
    {
        'success': "true",
        'keys': [str]
    }
'''
@webapp.route('/api/clear_cache', methods=['POST'])
def clear_cache():
    memcache_operations.delete_keys()
    return jsonify({
        'success': "true",
        'keys': list(memcache_operations.get_keys())
    })

'''
==== STATS PAGE ====
'''


'''
    Get Stats
    ----
    Expected JSON response:
    {
        #TODO: revise response format
        'success': "true",
        'keys': [str]
    }
'''

@webapp.route('/api/stats', methods=['GET'])
def get_stats():
    return jsonify({
        'success': "true",
        'stats': list(stats.statistic_history)
    })

