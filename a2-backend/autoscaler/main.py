from autoscaler import webapp, scaler
from flask import jsonify, request


"""
these are required : min_missed_rate, max_missed_rate, expand_ratio, shrink_ration
"""
@webapp.route('/api/start', methods=['POST'])
def start():
    config = request.get_json()
    scaler.start(**config)
    return jsonify({
        'success': 'true'
    })

@webapp.route('/api/stop', methods=['POST'])
def stop():
    scaler.stop()
    return jsonify({
        'success': 'true'
    })
    
@webapp.route('/api/config', methods=['POST'])
def update_config():
    config = request.get_json()
    scaler.set_config(**config)
    return jsonify({  
        'success': 'true'
    })
    
@webapp.route('/api/remind', methods=['POST'])
def scale():
    scaler.run_once()
    return jsonify({
        "success": "true"
    })
    
