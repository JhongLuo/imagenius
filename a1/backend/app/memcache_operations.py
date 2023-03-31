import requests

url_prefix = 'http://localhost:5001/api'

def get_keys():
    return requests.get(url_prefix + '/keys').json()['keys']

def delete_key(key):
    requests.delete(url_prefix + '/key/' + key)

def get_key(key):
    response = requests.get(url_prefix + '/key/' + key).json()
    if 'content' in response:
        return response['content']
    else:
        return None

def set_key(key, json_content):
    requests.post(url_prefix + '/key/' + key, json=json_content)

def delete_keys():
    requests.delete(url_prefix + '/keys')