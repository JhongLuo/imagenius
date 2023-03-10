from autoscaler import webapp, scaler
from flask import jsonify, request


"""
these are required : min_missed_rate, max_missed_rate, expand_ratio, shrink_ration
"""
@webapp.route('/api/start', methods=['POST'])
def start():
    try:
        config = request.get_json()
        scaler.start(**config)
        return jsonify({
            'success': 'true'
        })
    
    except Exception as e:
        return jsonify({
            'success': 'false',
            'error': str(e)
        })

@webapp.route('/api/stop', methods=['POST'])
def stop():
    scaler.stop()
    return jsonify({
        'success': 'true'
    })
