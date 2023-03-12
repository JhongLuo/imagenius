import requests
import sys
import time


url = "http://localhost:5000/api"

file_MB = 0.1
sleep_time = 0.1
file_1 = ""
file_2 = ""
while sys.getsizeof(file_1) < file_MB * 1024 * 1024:
    file_1 += "sdsf" * 100
    file_2 += "2323" * 100

print(len(file_1))
print(sys.getsizeof(file_1))

def upload1(key):
    return requests.post(url + "/upload", data={'key': key, 'file': file_1}).json()

def upload2(key):
    return requests.post(url + "/upload", data={'key': key, 'file': file_2}).json()

def get(key):
    return requests.post(url +f"/key/{key}").json()

def list_keys():
    return requests.get(url +f"/list_keys").json()

def clear_cache():
    return requests.post(url +f"/clear_cache").json()

def get_stats():
    return requests.get(url +f"/stats").json()

def delete_all():
    return requests.post(url +f"/delete_all").json()

def get_cache_keys():
    return requests.get(url +f"/cache_keys").json()

def get_cache_config():
    return requests.get(url +f"/config").json()

def set_config(mode = None, numNodes = None, cacheSize = None, policy = None, expRatio = None, shrinkRatio = None, maxMiss = None, minMiss = None):
    paras = ''
    if mode:
        paras += f'mode={mode}&'
    if numNodes:
        paras += f'numNodes={numNodes}&'
    if cacheSize:
        paras += f'cacheSize={cacheSize}&'
    if policy:
        paras += f'policy={policy}&'
    if expRatio:
        paras += f'expRatio={expRatio}&'
    if shrinkRatio:
        paras += f'shrinkRatio={shrinkRatio}&'
    if maxMiss:
        paras += f'maxMiss={maxMiss}&'
    if minMiss:
        paras += f'minMiss={minMiss}&'
    return requests.post(url +f"/configure_cache?{paras}").json()


def get_miss_rate():
    return float(requests.post(url +f"/getRate?rate=miss").json()["value"])

def get_num_nodes():
    res = requests.post(url +f"/getNumNodes").json()
    return int(res["numNodes"])

'''
test code
'''

def image_test():
    for i in range(300):
        print(upload1(str(i)))
    
    for i in range(300):
        if get(str(i))['content'] != file_1:
            print(get(str(i)))
            print(get(str(i))['content'])
            print('wrong content')
    
    for i in range(300):
        print(upload2(str(i)))
    
    for i in range(300):
        if get(str(i))['content'] != file_2:
            print(get(str(i)))
            print(get(str(i))['content'])
            print('wrong content')
    
def add_and_remove_cache_test():
    for i in range(40):
        time.sleep(1)
        print(upload1(str(i)))
    # add num of caches
    for cache_num in range(1, 8 + 1):
        print(set_config(numNodes=cache_num))
    for cache_num in range(9, 0, -1):
        print(set_config(numNodes=cache_num))
    for cache_num in range(8 + 1):
        import random
        cache_num = random.randint(1, 8)
        print(set_config(numNodes=cache_num))
        
    
    print(set_config(numNodes=1)) # should fail
    print(set_config(numNodes=9)) # should fail

def auto_scaler_test():
    # expand test
    print(set_config(mode='manual'))
    print(set_config(numNodes=1))
    print(set_config(mode='auto'))
    # print(set_config(expRatio=0.5)) # should fail
    print(set_config(expRatio=2, shrinkRatio=0.5, maxMiss=0.3, minMiss=0.1, cacheSize=1))
    
    total_image = 200
    for i in range(total_image):
        time.sleep(0.5)
        print(upload1(str(i)))
    # cache will expand there
    while True:
        time.sleep(1)
        import random
        i = random.randint(0, total_image - 1)
        response = get(str(i))
        response.pop('content')
        print(response)
    # after 60 seconds, cache will shrink there
  
