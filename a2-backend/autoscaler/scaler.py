import time
from utils.cloudwatch import Watcher
from utils.cachering import CacheRing
from utils.rds import set_autoscaler_status
import datetime
import threading
import requests
from utils.url import manager_url
class Scaler:
    def __init__(self) -> None:
        self.is_started = False
        self.min_missed_rate = None
        self.max_missed_rate = None
        self.expand_ratio = None
        self.shrink_ration = None
        self.watcher = Watcher()
        self.ring = CacheRing()
        self.config_lock = threading.Lock()
        self.should_auto_scale = False
        
    def set_min_missed_rate(self, rate: float):
        if rate < 0 or rate > 1:
            raise ValueError('min missed rate must be between 0 and 1')
        self.min_missed_rate = rate
    
    def set_max_missed_rate(self, rate: float):
        if rate <= self.min_missed_rate or rate > 1:
            raise ValueError('max missed rate must be between min missed rate and 1')
        self.max_missed_rate = rate

    def set_expand_ratio(self, ratio: float):
        if ratio < 1:
            raise ValueError('expand ratio must be no smaller than 1')
        self.expand_ratio = ratio
        
    def set_shrink_ratio(self, ratio: float):
        if ratio > 1 or ratio < 0:
            raise ValueError('shrink ratio invalid')
        self.shrink_ration = ratio
        
    def set_manager_cache_num(self):
        requests.post(manager_url + f'/cache_num/{self.ring.cache_num}')
        
        
    def set_config(self, cache_num, min_missed_rate, max_missed_rate, expand_ratio, shrink_ratio):
        with self.config_lock:
            self.ring.update_cache_num(cache_num)
            self.set_min_missed_rate(min_missed_rate)
            self.set_max_missed_rate(max_missed_rate)
            self.set_expand_ratio(expand_ratio)
            self.set_shrink_ratio(shrink_ratio)
            
    def start(self, cache_num, min_missed_rate, max_missed_rate, expand_ratio, shrink_ratio):
        self.set_config(cache_num, min_missed_rate, max_missed_rate, expand_ratio, shrink_ratio)           
        with self.config_lock:
            self.last_update_time = datetime.datetime.utcnow()
            self.is_started = True
            set_autoscaler_status(True)
        
    def stop(self):
        with self.config_lock:
            self.is_started = False
            set_autoscaler_status(False)
    
    def expand(self):
        current = self.ring.cache_num
        new = min(8, int(current * self.expand_ratio))
        if self.expand_ratio > 1 and new == current and new < 8:
            new += 1
        if new == current:
            return
        print(f'auto expanding from {current} to {new}')
        instructions = self.ring.add(new - current)
        self.set_manager_cache_num()
        print("manager cache num updated")
        for ins in instructions:
            ins.execute()
        print("expand done!")
    
    def shrink(self):
        current = self.ring.cache_num
        new = max(1, int(current * self.shrink_ration))
        if new == current:
            return 
        print(f'auto shrink from {current} to {new} ...')
        instructions = self.ring.remove(current - new)
        self.set_manager_cache_num()
        print("manager cache num updated")
        for ins in instructions:
            ins.execute()
        print("shrink done!")
            
    def run(self):
        while True:
            time.sleep(1)
            with self.config_lock:
                if self.should_auto_scale:
                    missed = self.watcher.get_missed_rate()
                    print(f'current missed rate: {missed}, min: {self.min_missed_rate}, max: {self.max_missed_rate}')
                    if missed < self.min_missed_rate:
                        self.shrink()
                    elif missed > self.max_missed_rate:
                        self.expand()
                    self.should_auto_scale = False
            
                        
    def be_reminded(self):
        self.should_auto_scale = True
                
                
                
                