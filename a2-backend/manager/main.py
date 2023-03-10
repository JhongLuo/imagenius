from flask import request
from manager import webapp, man
from flask import jsonify
from utils.ReplacementPolicies import ReplacementPolicies
import base64

"""
A1 Endpoints
"""

@webapp.route('/api/key/<key_value>', methods=['POST'])
def get_image_alt_post(key_value):
    return retrieve(key_value)

@webapp.route('/api/list_keys', methods=['GET'])
def list_keys():
    try:
        return jsonify({
            'success': "true",
            'keys': man.get_keys()
        })
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": {
                "code": 400,
                "message": str(e)
                }
        })
    
@webapp.route('/api/list_keys', methods=['POST'])
def list_keys_alt_post():
    return list_keys()

@webapp.route('/api/cache_keys', methods=['GET'])
def get_cache_keys():
    try:
        return jsonify({
            'success': "true",
            'keys': list(man.get_cache_keys())
        })
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": {
                "code": 400,
                "message": str(e)
                }
        })
        
@webapp.route('/api/cache_configs', methods=['GET'])
def get_cache_configs():
    try:
        return jsonify({
            'success': "true",
            'replacement_policy': 'LRU' if man.get_replacement_policy() == ReplacementPolicies.LRU else 'RR',
            'max_size': man.get_max_size() / 1024 / 1024,
        })
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": {
                "code": 400,
                "message": str(e)
                }
        })
        
@webapp.route('/api/clear_cache', methods=['POST'])
def clear_cache():
    try:
        man.clear_cache()
        return jsonify({
            'success': "true",
        })
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": {
                "code": 400,
                "message": str(e)
                }
        })

@webapp.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        return jsonify({
            'success': "true",
            'stats': list(man.get_stats())
        })
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": {
                "code": 400,
                "message": str(e)
                }
        })

"""
A2 Endpoints
"""
'''
In case of failure of any of the calls of the upload or retrieve interface:
{
  "success": "false",
  "error": {
      "code": servererrorcode [int]
      "message": "errormessage"
       }
}
'''

'''
relative URL = /api/getNumNodes
method = POST
{
    "success": "true",
    "numNodes": [int]
}
'''
@webapp.route('/api/getNumNodes', methods=['POST'])
def get_num_nodes():
    try:
        return jsonify({
            'success': "true",
            'numNodes': [man.get_num_nodes()]
        })
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": {
                "code": 400,
                "message": str(e)
                }
        })
    
'''
relative URL = /api/getRate?{parameters}
method = POST
Parameters:  name = rate, type = string, possible values = "miss", "hit"
{
    "success": "true",
    "rate": [String],
    "value": [int]
}
'''
@webapp.route('/api/getRate', methods=['POST'])
def get_rate():
    try:
        rate = request.args.get('rate')
        missed_rate = man.get_miss_rate()
        value = missed_rate * 100
        if rate == 'hit':
            value = 100 - value
        return jsonify({
            'success': "true",
            'rate': [rate],
            'value': [value]
        })
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": {
                "code": 400,
                "message": str(e)
                }
        })
    

'''
relative URL = /api/configure_cache?{parameters}
method = POST
POST Parameters:
name = mode, type = string, possible value(s) = "manual", "auto"
name = numNodes, type = int
name = cacheSize, type = int (in MB)
name = policy, type = string, possible values = "LRU", "RR"
name = expRatio, type = string
name = shrinkRatio, type = string
name = maxMiss, type = int
name = minMiss, type = int
{
    "success": "true",
    "mode": [String],
    "numNodes": [int],
    "cacheSize": [int],
    "policy": [String]
}
'''
@webapp.route('/api/configure_cache', methods=['POST'])
def configure_cache():
    try:
        if 'mode' in request.args:
            if request.args.get('mode') == "manual":
                man.mode_switch(True)
            else:
                man.mode_switch(False)
        
        if 'numNodes' in request.args:
            man.change_nodes_num(int(request.args.get('numNodes')))
        
        if 'cacheSize' in request.args:
            man.set_max_size(int(request.args.get('cacheSize') * 1024 * 1024))
        
        if 'policy' in request.args:
            policy = request.args.get('policy')
            if policy == 'LRU':
                man.set_policy(ReplacementPolicies.LRU)
            elif policy == 'RR':
                man.set_policy(ReplacementPolicies.RANDOM)
            else:
                raise Exception('Invalid policy')
        
        if 'expRatio' in request.args:
            man.set_expand_ratio(float(request.args.get('expRatio')))
        
        if 'shrinkRatio' in request.args:
            man.set_shirnk_ratio(float(request.args.get('shrinkRatio')))
        
        if 'maxMiss' in request.args:
            man.set_max_missed_rate(int(request.args.get('maxMiss')))
        
        if 'minMiss' in request.args:
            man.set_min_missed_rate(int(request.args.get('minMiss')))
        
        return jsonify({
            "success": "true",
            "mode": ["manual" if man.is_manual_mode() else "auto"],
            "numNodes" : [int(man.get_num_nodes())],
            "cacheSize" : [int(man.get_max_size() / 1024 / 1024)],
            "policy" : ["LRU" if man.get_replacement_policy() == ReplacementPolicies.LRU else "RR"]
        })
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": {
                "code": 400,
                "message": str(e)
                }
        })
        
'''
relative URL = /api/delete_all
method = POST
{
    "success": "true"
}
'''
@webapp.route('/api/delete_all', methods=['POST'])
def delete_all():
    try:
        man.delete_all_images()
        return jsonify({
            "success": "true"
        })
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": {
                "code": 400,
                "message": str(e)
                }
        })
    
'''
relative URL = /api/upload
enctype = multipart/form-data
method = POST
Parameters: name = key, type = string name = file, type = file
{
    "success": "true",
    "key": [String]
}
'''
@webapp.route('/api/upload', methods=['POST'])
def upload():
    try:
        key = request.form.get('key')
        file = request.form.get('file')
        if not file:
            file = request.files.get('file')
        if not key or key == '' or not file:
            raise Exception('Invalid key or file')
        content = base64.b64encode(file.read()).decode()
        man.put_image(key, content)
        return jsonify({
            'success': "true",
            'key': [key]
        })
            
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": {
                "code": 400,
                "message": str(e)
                }
        })

'''
relative URL = /api/key/<key_value>
method = POST
{
    "success": "true",
    "key" : [String],
    "content" : file contents [type is optional]
}
'''
@webapp.route('/api/key/<key_value>', methods=['POST'])
def retrieve(key_value):
    try:
        return jsonify({
            "success": "true",
            "key": [key_value],
            "content" : man.get_image(key_value)
        })
    except Exception as e:
        return jsonify({
            "success": "false",
            "error": {
                "code": 400,
                "message": str(e)
                }
        })