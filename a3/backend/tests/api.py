import requests

host = "127.0.0.1"
port = "5000"
url = "https://6o5zlaguae.execute-api.us-east-1.amazonaws.com/dev/api"
url = f"http://{host}:{port}/api"

def get_tree(key):
    return requests.post(url + '/search/tree', data={"key": key}).json()
