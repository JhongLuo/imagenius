import datetime
import json
import random
from collections import deque
import time
import matplotlib.pyplot as plt
from manager_tests import file_MB, get, sleep_time, upload1, set_config, delete_all, get_miss_rate, get_num_nodes, clear_cache

def prepare_workload(total_MB):
    total_image = int(total_MB / file_MB) + 1
    for i in range(total_image):
        time.sleep(sleep_time)
        print(upload1(str(i)))


def random_workload(total_MB, total_minutes):
    total_image = int(total_MB / file_MB) + 1
    time_records = []
    start_time = datetime.datetime.utcnow()
    while datetime.datetime.utcnow() - start_time < datetime.timedelta(minutes=total_minutes):
        time.sleep(sleep_time)
        i = random.randint(0, total_image - 1)
        request_time = datetime.datetime.utcnow()
        response = get(str(i))
        time_records.append((datetime.datetime.utcnow() - request_time).total_seconds())
        response.pop('content')
        print(response)
    return time_records

def lru_workload(total_MB, total_minutes):
    total_image = int(total_MB / file_MB) + 1
    time_records = []
    for i in range(total_image):
        time.sleep(sleep_time)
        print(upload1(str(i)))
        
    dq = deque()
    window_size = total_image // 4 + 1
    start_time = datetime.datetime.utcnow()
    while datetime.datetime.utcnow() - start_time < datetime.timedelta(minutes=total_minutes):
        time.sleep(sleep_time)
        # random select from deque
        dq.append(random.randint(0, total_image - 1))
        if len(dq) > window_size:
            dq.popleft()
        i = random.choice(dq)
        request_time = datetime.datetime.utcnow()
        response = get(str(i))
        time_records.append((datetime.datetime.utcnow() - request_time).total_seconds())
        response.pop('content')
        print(response)
    return time_records
        

        

def plot_latency(image_name, json_name):
    time_records = json.load(open(json_name))
    requests_count = 1
    time_consumed = 0
    latency = []
    for record in time_records:
        time_consumed += record
        latency.append(time_consumed / requests_count)
        requests_count += 1
    plt.clf()
    plt.plot([i for i in range(len(latency))], latency)
    plt.title(image_name + " latency test")
    plt.xlabel('number of requests')
    plt.ylabel('average latency(second) per request')
    plt.savefig(image_name + ' latency.png')

def plot_throughput(image_name, json_name):
    time_records = json.load(open(json_name))
    time_consumed = 0
    requests_count = 1
    y = []
    x = []
    for record in time_records:
        time_consumed += record
        x.append(time_consumed)
        y.append(requests_count)
        requests_count += 1
    plt.clf()
    plt.title(image_name + " throughput test")
    plt.plot(x, y)
    plt.xlabel('time elapsed (s)')
    plt.ylabel('number of requests')
    plt.savefig(image_name + ' throughput.png')
    

"""
Constant memcache node pool size: 
choose any pool size greater than 1. 
Provide one latency graph (time per request(s); gradually increasing the number of requests) 
one throughput graph (maximum requests per time; gradually increasing the amount of time).
"""
def const_test():
    print(delete_all())
    print(set_config(mode="manual", numNodes=2, cacheSize=1, policy="LRU"))
    total_MB = 4
    total_Minutes = 3
    prepare_workload(total_MB)
    time_records = random_workload(total_MB, total_Minutes)
    # dump time records to file
    json.dump(time_records, open('const_test.json', 'w'))

# const_test()    
# plot_latency('manual constant', 'const_test.json')
# plot_throughput('manual constant', 'const_test.json')

"""
Shrinking memcache node pool size: 
choose any starting pool size greater than 1 and a smaller ending pool size greater than 1. 
Repeat the same latency and throughput experiments as above, while shrinking the pool size from the starting size to the ending size. 
Provide the graphs.
"""

def shirnk_test():
    print(delete_all())
    print(set_config(mode="manual", numNodes=4, cacheSize=1, policy="LRU"))
    time_records = []
    total_MB = 4
    total_Minutes = 3
    prepare_workload(total_MB)
    time_records += random_workload(total_MB, total_Minutes // 3)
    print(set_config(numNodes=3))
    time_records += random_workload(total_MB, total_Minutes // 3)
    print(set_config(numNodes=2))
    time_records += random_workload(total_MB, total_Minutes // 3)
    
    json.dump(time_records, open('shrink_test.json', 'w'))

# shirnk_test()
# plot_latency('manual shrink', 'shrink_test.json')
# plot_throughput('manual shrink', 'shrink_test.json')

"""
Growing memcache node pool size: choose any starting pool size greater than 1 and a larger ending pool size greater than 1. 
Repeat the same latency and throughput experiments as above while growing the pool size from the starting size to the ending size. 
Provide the graphs.
"""

def expand_test():
    print(delete_all())
    print(set_config(mode="manual", numNodes=2, cacheSize=1, policy="LRU"))
    time_records = []
    total_MB = 4
    total_Minutes = 3
    prepare_workload(total_MB)
    time_records += random_workload(total_MB, total_Minutes // 3)
    print(set_config(numNodes=3))
    time_records += random_workload(total_MB, total_Minutes // 3)
    print(set_config(numNodes=4))
    time_records += random_workload(total_MB, total_Minutes // 3)
    
    json.dump(time_records, open('expand_test.json', 'w'))

# expand_test()
# plot_latency('manual expand', 'expand_test.json')
# plot_throughput('manual expand', 'expand_test.json')    

"""
Choose values for the min and max rate threshold and expand and shrink ratios.
Design a scenario where your auto-scalar will shrink the number of nodes, and plot the miss rate vs. number of nodes as your system re-sizes. Indicate the min threshold value on your graph. 
"""
def plot_miss_rate(image_name, json_name):
    dic = json.load(open(json_name))
    miss_rates = dic["missrates"]
    num_nodes = dic["num_nodes"]
    n = len(miss_rates)
    plt.clf()
    plt.yscale('log', base=2)
    plt.plot([i * 5 for i in range(n)], miss_rates, label = 'miss rate')
    plt.plot([i * 5 for i in range(n)], num_nodes, label = 'number of nodes')
    plt.xlabel('number of requests')
    # set tiltle of graph
    plt.title(dic['title'])
    plt.legend()
    plt.savefig(image_name + ' miss rate.png')

def auto_shrink():
    print(delete_all())
    print(set_config(mode='manual', numNodes=8))
    total_MB = 2
    prepare_workload(total_MB)
    print(clear_cache())
    total_image = int(total_MB / file_MB) + 1
    print(set_config(mode='auto', expRatio=2, shrinkRatio=0.5, maxMiss=0.3, minMiss=0.1, cacheSize=2))
    miss_rates = []
    num_nodes = []
    start_time = datetime.datetime.utcnow()
    request_count = 0
    while datetime.datetime.utcnow() - start_time < datetime.timedelta(minutes=5):
        miss_rate = get_miss_rate()
        # update miss rate and num nodes
        if request_count % 5 == 0: 
            miss_rates.append(miss_rate)
            num_nodes.append(get_num_nodes())
        time.sleep(0.5)
        # random read
        response = get(str(random.randint(0, total_image - 1)))
        response.pop('content')
        print(response)
        request_count += 1
        
        
    json.dump({"missrates" : miss_rates,
               "num_nodes" : num_nodes,
               "title" : f"maxMiss = 0.3, minMiss = 0.1, expRatio = 2, shrinkRatio = 0.5",
               }, open('auto_shrink.json', 'w'))

auto_shrink()
plot_miss_rate('auto_shrink', 'auto_shrink.json')


"""
Design a scenario where your auto-scalar will grow the number of nodes, and plot the miss rate vs. number of nodes as your system re-sizes. Indicate the max threshold value on your graph. 
"""


def auto_expand():
    print(delete_all())
    print(set_config(mode='manual', numNodes=1))
    total_MB = 4
    prepare_workload(total_MB)
    total_image = int(total_MB / file_MB) + 1
    print(set_config(mode='auto', expRatio=2, shrinkRatio=0.5, maxMiss=0.3, minMiss=0.1, cacheSize=1))
    miss_rates = []
    num_nodes = []
    start_time = datetime.datetime.utcnow()
    request_count = 0
    while datetime.datetime.utcnow() - start_time < datetime.timedelta(minutes=5):
        miss_rate = get_miss_rate()
        # update miss rate and num nodes
        if request_count % 5 == 0: 
            miss_rates.append(miss_rate)
            num_nodes.append(get_num_nodes())
        time.sleep(0.5)
        # random read
        response = get(str(random.randint(0, total_image - 1)))
        response.pop('content')
        print(response)
        request_count += 1
        
        
    json.dump({"missrates" : miss_rates,
               "num_nodes" : num_nodes,
               "title" : f"maxMiss = 0.3, minMiss = 0.1, expRatio = 2, shrinkRatio = 0.5",
               }, open('auto_expand.json', 'w'))
    
auto_expand()
plot_miss_rate('auto_expand', 'auto_expand.json')