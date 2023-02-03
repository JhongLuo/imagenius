from flask import render_template, request, redirect, url_for, flash
from app import webapp, stats, db, scheduler
from flask import jsonify
from . import storage_operations, app_operations, memcache_operations
from utils.ReplacementPolicies import ReplacementPolicies
import logging

logger = logging.getLogger(__name__)

# webapp.secret_key = 'bvceu3v2'

# @webapp.route('/home')
# def main_v2():
#     flash('Welcome to group 18 Project!', category='success')
#     return render_template("base.html")

# @webapp.route('/v2/delete_all', methods=['GET','POST'])
# def delete_all_v2():
#     if request.method == 'POST':
#         global db
#         global stats
#         global memcache
#         global scheduler
#         db, stats, memcache, scheduler = app_operations.init_app(db=db, stats=stats, memcache=memcache, scheduler=scheduler)

#         flash("Delete all keys: Success !", category='sucess')
#         return redirect(url_for('list_keys_v2'))

# @webapp.route('/v2/upload', methods=['GET','POST'])
# def upload_v2():
#     if request.method == 'POST':
#         key = request.form.get('key')
#         file = request.files.get('file')
#         if not key or not file:
#             flash('Invalid key or file', category='error')
#             return render_template("upload.html")
#         global memcache
#         if key in memcache:
#             del memcache[key]
#         filename = storage_operations.store_image(file)
#         filedict = storage_operations.filename2dict(filename)
#         memcache[key] = filedict
#         global stats
#         stats.memcache_updated(memcache)
#         global db
#         db.set_key(key, filename)

#         logger.debug(f'memcache keys: {memcache.keys()}')
#         logger.debug(f'stats: {stats.dump()}')

#         flash('Successfully added key and image:' + str(key), category='success')
#         return render_template("upload.html")
#     else:
#         return render_template("upload.html")

# @webapp.route('/v2/list_keys', methods=['GET','POST'])
# def list_keys_v2():
#     if request.method == 'GET':
#         return render_template("list_key.html", keys=list(memcache.keys()))
#     else:
#         return redirect(url_for('delete_all_v2'))

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
    global scheduler
    db, stats, scheduler = app_operations.init_app(db=db, stats=stats, scheduler=scheduler)
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
@webapp.route('/api/upload', methods=['POST'])
def upload():
    key = request.form.get('key')
    file = request.files.get('file')
    if not key or not file:
        return jsonify({
            "success": "false",
            "error": "Invalid key or file"
        })
    memcache_operations.delete_key(key)
    filename = storage_operations.store_image(file)
    filedict = storage_operations.filename2dict(filename)
    memcache_operations.set_key(key, filedict)
    db.set_key(key, filename)
        
    return jsonify({
        "success": "true",
        "key": key
    })

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
        "keys": db.get_keys()
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
    json_content = memcache_operations.get_key(key_value)
    is_hit = True
    if not json_content:
        is_hit = False
        filename = db.key2path(key_value)
        if filename is None:
            return jsonify({
                "success": "false",
                "error": "Key not found"
            })
        json_content = storage_operations.filename2dict(filename)
        memcache_operations.set_key(key_value, json_content)
    stats.add_request_count(is_hit)
    return jsonify({
        "success": "true",
        "key": key_value,
        "content": json_content
    })

# self defined Endpoints

@webapp.route('/api/key/<key_value>', methods=['DELETE'])
def delete_key(key_value):
    memcache_operations.delete_key(key_value)
    filename = db.key2path(key_value)
    if not filename:
        return jsonify({
            'success': 'false',
            'key': key_value,
            'error': 'Key not found'
        })
    else:
        db.delete_key(key_value)
        storage_operations.delete_image(filename)
        return jsonify({
            'success': 'true',
            'key': key_value
        })

@webapp.route('/api/delete_cache', methods=['POST'])
def delete_cache():
    memcache_operations.delete_keys()
    return jsonify({
        'success': 'true'
    })
    
@webapp.route('/api/statistics/max_size', methods=['PUT'])
def set_maxsize():
    stats.max_size = int(request.form.get('max_size'))
    return jsonify({
        'success': 'true',
        'max_size': stats.max_size
    })

@webapp.route('/api/statistics/replacement_policy', methods=['PUT'])
def set_replacement_policy():
    try:
        stats.replacement_policy = ReplacementPolicies.str2policy(request.form.get('replacement_policy'))
        return jsonify({
            'success': 'true'
        })
    except Exception:
        return jsonify({
            'success': 'false',
            'error': 'Invalid replacement policy'
        })
    
@webapp.route('/api/statistics', methods=['GET'])
def get_statistics():
    return jsonify({
        'success': 'true',
        'statistics': list(stats.statistic_history)
    })
    
@webapp.route('/api/cache_keys', methods=['GET'])
def get_cache_keys():
    return jsonify({
        "success": "true",
        "keys": list(memcache_operations.get_keys())
    })
    
