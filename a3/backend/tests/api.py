import requests

host = "127.0.0.1"
port = "5000"
url = "https://ehhmnvfa9i.execute-api.us-east-1.amazonaws.com/dev/api"
url = f"http://{host}:{port}/api"

def get_tree(key):
    return requests.post(url + '/search/tree', data={"key": key}).json()

def make_a_record():
    return requests.post(url + '/record').json()

def get_stats():
    return requests.get(url + '/stats').json()

def delete_image(key):
    return requests.post(url + '/delete_image', data={"key": key}).json()

def get_tags():
    return requests.get(url + '/tags').json()

def search_by_tags(tags):
    return requests.post(url + '/search/tags', json={"selected_tags": tags}).json()

def list_all():
    return requests.get(url + '/list_all').json()


def change_provisioned_throughput(free_to_test=False):
    import boto3
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("ECE1779A3ImageInfo")
    write = 3
    if not free_to_test:
        read = 3
    else:
        read = 1000
    response = table.update(
        ProvisionedThroughput={
            'ReadCapacityUnits': read,
            'WriteCapacityUnits': write,
        }
    )
