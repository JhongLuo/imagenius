import requests

host = "127.0.0.1"
port = "5000"
url = f"http://{host}:{port}"
url = "https://6o5zlaguae.execute-api.us-east-1.amazonaws.com/dev/"

headers = {
    'Content-Type': 'application/json'
}

def create_image(des):
    return requests.post(f"{url}/images", 
                         json={"description": des}, 
                         headers=headers)
def list_labels():
    return requests.get(f"{url}/labels")
    
def list_descriptions():
    return requests.get(f"{url}/descriptions")
    
def delete_images():
    return requests.delete(f"{url}/images")

def get_image(des=None, labels=[]):
    return requests.get(f"{url}/images",
                        params={
                            "description": des, 
                            "labels": labels
                        })


