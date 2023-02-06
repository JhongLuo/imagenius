import requests
import random
import time
import threading
import matplotlib.pyplot as plt

aws_url = 'http://44.211.118.125:5000/api'
local_url = 'http://localhost:5000/api'

base_url = local_url
upload_url = base_url + '/upload'
delete_all_url = base_url + '/delete_all'
set_cache = base_url + '/cache_configs'
read_url = base_url + '/key/'
image = 'a' * 1024 * 1024

class Recorder:
    def __init__(self, timestamps) -> None:
        self.start_time = time.time()
        self.timestamps = timestamps
        self.cur = 0
        self.requests_per_second = 0
        self.res = dict()
        self.lock = threading.Lock()

    def finish_a_request(self) -> bool:
        self.requests_per_second += 1
        if self.cur < len(self.timestamps):
            if time.time() - self.start_time > self.timestamps[self.cur]:
                with self.lock:
                    self.res[self.timestamps[self.cur]] = self.requests_per_second
                    self.cur += 1

def random_rw(ratio : float, keys : list) -> None:
    if len(keys) and random.random() < ratio:
        requests.get(read_url + str(random.choice(keys)))
    else:
        if len(keys) > 0:
            keys.append(keys[-1] + 1)
        else:
            keys.append(0)
        requests.post(upload_url, data={'key': keys[-1], 'file': image})


def throughput_test(timestamps : list, ratio : float, config : dict):
    keys = []
    requests.put(set_cache, json=config)
    end_time = time.time() + timestamps[-1]
    recorder = Recorder(timestamps)
    ths = []
    
    def request_and_record(ratio : float, keys : list, recorder : Recorder):
        try:
            random_rw(ratio, keys)
            recorder.finish_a_request()
        except Exception as e:
            print(e)
    
    while True:   
        if time.time() > end_time:
            break
        th = threading.Thread(target=request_and_record, args=(ratio, keys, recorder))
        time.sleep(0.01)
        ths.append(th)
        th.start()
        
    for th in ths:
        th.join()
        
    res = recorder.res
    return res


def latency_test(total_requests, ratio, config):
    keys = []    
    res = dict()
    start_time = time.time()
    requests.put(set_cache, json=config)
    for i in range(total_requests):
        random_rw(ratio, keys)
        res[i] = time.time() - start_time
        
    return res

def ratio_latency_test(total_requests, ratio):
    filename = f'total_requests:{str(total_requests)} ratio:{str(ratio)} latency test'
    with open(filename + '.txt', 'w') as f:
        res0 = latency_test(total_requests, ratio, {'replacement_policy': 'random', 'max_size': 0})
        res1 = latency_test(total_requests, ratio, {'replacement_policy': 'random', 'max_size': 100 * 1024 * 1024})
        res2 = latency_test(total_requests, ratio, {'replacement_policy': 'LRU', 'max_size': 100 * 1024 * 1024})
        f.write('no cache' + str(res0) + '\n')
        f.write('random cache' + str(res1) + '\n')
        f.write('LRU cache' + str(res2) + '\n')
        x = [i for i in range(1, total_requests + 1)]
        def get_average_latency(res):
            return [float(t) / (i + 1) for i, t in enumerate(res)]
        
        plt.clf()
        plt.plot(x, get_average_latency(res0), label='no cache')
        plt.plot(x, get_average_latency(res1), label='random cache')
        plt.plot(x, get_average_latency(res2), label='LRU cache')
        plt.xlabel('number of requests')
        plt.ylabel('latency (s)')
        plt.legend()
        plt.savefig(filename + '.png')

def ratio_throughput_test(total_time, ratio):
    filename = f'total_time:{str(total_time)} ratio:{str(ratio)} throughput test'
    timestamp = [i for i in range(total_time + 1)]
    with open(filename + '.txt', 'w') as f:
        res0 = throughput_test(timestamp, ratio, {'replacement_policy': 'random', 'max_size': 0})
        res1 = throughput_test(timestamp, ratio, {'replacement_policy': 'random', 'max_size': 100 * 1024 * 1024})
        res2 = throughput_test(timestamp, ratio, {'replacement_policy': 'LRU', 'max_size': 100 * 1024 * 1024})
        f.write('no cache' + str(res0) + '\n')
        f.write('random cache' + str(res1) + '\n')
        f.write('LRU cache' + str(res2) + '\n')
        
        def get_requests(res):
            rtn = []
            for i in timestamp:
                if i in res:
                    rtn.append(res[i])
            return rtn
        
        plt.clf()
        plt.plot(timestamp, get_requests(res0), label='no cache')
        plt.plot(timestamp, get_requests(res1), label='random cache')
        plt.plot(timestamp, get_requests(res2), label='LRU cache')
        plt.xlabel('time elapsed (s)')
        plt.ylabel('number of requests')
        plt.legend()
        plt.savefig(filename + '.png')
        

for ratio in [0.2, 0.5, 0.8]:
    ratio_latency_test(200, ratio)
    # ratio_throughput_test(10, ratio)
