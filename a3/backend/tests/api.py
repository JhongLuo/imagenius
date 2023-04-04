import requests

host = "127.0.0.1"
port = "5000"
url = "https://6o5zlaguae.execute-api.us-east-1.amazonaws.com/dev/api"
url = f"http://{host}:{port}/api"

headers = {
    'Content-Type': 'application/json'
}

def generate_images(prompt):
    return requests.post(f"{url}/generate", 
                         json={"prompt": prompt}, 
                         headers=headers)

def save_images(keys):
    return requests.post(f"{url}/images", 
                         json={"key_selections": keys}, 
                         headers=headers)

def list_labels():
    return requests.get(f"{url}/labels")
    
def list_prompts():
    return requests.get(f"{url}/prompts")
    
def delete_images():
    return requests.delete(f"{url}/images")

def get_image(prompt=None, labels=[]):
    return requests.get(f"{url}/images",
                        params={
                            "prompt": prompt, 
                            "labels": labels
                        })


