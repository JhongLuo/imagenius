from utils import rds, s3, cloudwatch, cachering, memcachop
from utils.url import id2url, scaler_url
import datetime
import time
import requests
from collections import deque

class Manager:
    def __init__(self) -> None:
        self.watcher = cloudwatch.Watcher()
        self.ring = cachering.CacheRing()
        self.s3 = s3.S3()
        self.expand_ratio = 1
        self.shrink_ration = 1
        self.max_missed_rate = 1
        self.min_missed_rate = 0
        self.last_record_time = datetime.datetime.utcnow()
        self.records = deque(maxlen=60)
        # init memcache
        for i in range(8):
            memcachop.set_id(id2url(i), i)
        memcachop.start(id2url(0))
        
    def key2url(self, key):
        return id2url(self.ring.key2server(key))
        
    def get_miss_rate(self):
        return self.watcher.get_missed_rate()
    
    def get_num_nodes(self):
        total = 0
        for i in range(8):
            if rds.get_memcache_status(i):
                total += 1
        return total
    
    def start_scaler(self):
        while not rds.get_autoscaler_status():
            requests.post(scaler_url + '/start', json={
                'min_missed_rate': self.min_missed_rate,
                'max_missed_rate': self.max_missed_rate,
                'expand_ratio': self.expand_ratio,
                'shrink_ratio': self.shrink_ration
            })
            print(' message is sent to autoscaler, waiting for response ...')
        print('autoscaler is started!')
    
    def stop_scaler(self):
        while rds.get_autoscaler_status():
            requests.post(scaler_url + '/stop')
            print(' message is sent to autoscaler, waiting for response ...')
        print('autoscaler is stopped!')
        
    def config_scaler(self):
        requests.post(scaler_url + '/config', json={
            'min_missed_rate': self.min_missed_rate,
            'max_missed_rate': self.max_missed_rate,
            'expand_ratio': self.expand_ratio,
            'shrink_ratio': self.shrink_ration
        })
    
    def mode_switch(self, is_manual):
        is_stated = rds.get_autoscaler_status()
        if is_manual == (not is_stated):
            raise ValueError('mode is already set')
        if is_manual:
            self.stop_scaler()
        else:
            self.start_scaler()

    def change_nodes_num(self, num):
        if num < 1 or num > 8:
            raise ValueError('invalid number of nodes')
        if rds.get_autoscaler_status():
            raise ValueError('cannot change nodes number in auto mode')
        current = self.get_num_nodes()
        if num == current:
            return
        elif num > current:
            self.ring.add(num - current)
        else:
            self.ring.remove(current - num)
    
    def set_max_size(self, size : int):
        if size < 0:
            raise ValueError('max size must be no smaller than 0')
        rds.set_stat(rds.StatsNames.max_size, size)
    
    def set_policy(policy):
        rds.set_replacement_policy(policy)
    
    def set_expand_ratio(self, ratio: float):
        if ratio < 1:
            raise ValueError('expand ratio must be no smaller than 1')
        self.expand_ratio = ratio
        self.config_scaler()
        
    def set_shrink_ratio(self, ratio: float):
        if ratio > 1 or ratio < 0:
            raise ValueError('shrink ratio invalid')
        self.shrink_ration = ratio
        self.config_scaler()
        
    def set_max_missed_rate(self, rate: float):
        if rate <= self.min_missed_rate or rate > 1:
            raise ValueError('max missed rate must be between min missed rate and 1')
        self.max_missed_rate = rate
        self.config_scaler()
    
    def set_min_missed_rate(self, rate):
        if rate <= 0 or rate >= self.max_missed_rate:
            raise ValueError('min missed rate invalid')
        self.min_missed_rate = rate
        self.config_scaler()
    
    def set_both_rate(self, min_rate, max_rate):
        if min_rate <= 0 or min_rate >= max_rate or max_rate >= 1:
            raise ValueError('rate invalid')
        self.min_missed_rate = min_rate
        self.max_missed_rate = max_rate
        self.config_scaler()
        
    def delete_all_images(self):
        rds.delete_keys()
        self.clear_cache()
        self.s3.clear_images()
    
    def put_image(self, key, content):
        memcachop.delete(self.key2url(key), key)
        filename = self.s3.store_image(content)
        rds.set_key(key, filename)
        memcachop.put(self.key2url(key), key, content)
    
    def delete_image(self, key):
         rds.get_path(key)
    
    def get_image(self, key):
        image = memcachop.get(self.key2url(key), key)
        if not image:
            image_path = rds.get_path(key)
            image = self.s3.read_image(image_path)
            memcachop.put(self.key2url(key), key, image)
        return image

    def get_keys(self):
        return rds.get_keys()
    
    def get_cache_keys(self):
        all_keys = []
        for i in range(8):
            if rds.get_memcache_status(i):
                all_keys += memcachop.get_keys(i)
        return all_keys
    
    def clear_cache(self):
        for i in range(8):
            if rds.get_memcache_status(i):
                memcachop.clear_cache(i)
    
    def get_stats(self):
        return list(self.records)
    
    def get_replacement_policy(self):
        return rds.get_replacement_policy()
    
    def get_max_size(self):
        return rds.get_stat(rds.StatsNames.max_size)
    
    def is_manual_mode(self):
        return not rds.get_autoscaler_status()
    
    def get_cache_items_len(self):
        total = 0
        for i in range(8):
            if rds.get_memcache_status(i):
                total += memcachop.get_len(i)
        return total
    
    def get_cache_items_size(self):
        total = 0
        for i in range(8):
            if rds.get_memcache_status(i):
                total += memcachop.get_bytes(i)
        return total
    
    def record(self):
        while True:
            if datetime.datetime.utcnow() - self.last_record_time > datetime.timedelta(seconds=60):
                self.last_record_time = datetime.datetime.utcnow()
                record = {
                    'timestamp' : self.last_record_time,
                    'miss_rate' : self.watcher.get_missed_rate(),
                    'hit_rate' : (1 - self.watcher.get_missed_rate()),
                    'nodes_num' : self.get_num_nodes(),
                    'items_len' : self.get_cache_items_len(),
                    'items_bytes' : int(float(self.get_cache_items_size()) / 1024 / 1024),
                    'requests_count' : self.watcher.get_request_count(),
                }
                self.records.append(record)
            time.sleep(1)