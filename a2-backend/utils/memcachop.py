import requests

def get_keys(url):
    return requests.get(url + '/keys').json()['keys']

def delete(url, key):
    requests.delete(url + '/key/' + key)

def get(url, key):
    response = requests.get(url + '/key/' + key).json()
    if 'content' in response:
        return response['content']
    else:
        return None

def put(url, key, content):
    requests.post(url + '/key/' + key, json=content)

def get_range(url, lower, upper):
    return requests.get(url + '/range/' + str(lower) + '/' + str(upper)).json()['content']

def clear_cache(url):
    requests.delete(url + '/keys')

def delete_range(url, lower, upper):
    requests.delete(url + '/range/' + str(lower) + '/' + str(upper))

def merge_range(url, content):
    requests.patch(url + '/range', json=content)

def set_key(url, key, content):
    requests.post(url + '/key/' + key, json=content)

def delete_keys(url):
    requests.delete(url + '/keys')
    
def start(url):
    requests.post(url + '/start')
    
def get_bytes(url):
    return int(requests.get(url + '/bytes').json()['bytes'])

def get_len(url):
    response = requests.get(url + '/length').json()
    if "error" in response:
        raise Exception(response['error'])
    return int(response['length'])
    
def stop(url):
    requests.post(url + '/stop')
    
def set_id(url, id):
    print('setting id to memcache' + str(id))
    requests.post(url + '/id', json={'id': id})
    
