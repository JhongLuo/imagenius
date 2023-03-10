import time
from utils.cloudwatch import Watcher
from utils.cachering import CacheRing
from utils.rds import set_autoscaler_status
import datetime
import threading
class Scaler:
    def __init__(self) -> None:
        self.is_started = False
        self.min_missed_rate = None
        self.max_missed_rate = None
        self.expand_ratio = None
        self.shrink_ration = None
        self.last_update_time = None
        self.watcher = Watcher()
        self.ring = CacheRing()
        self.config_lock = threading.Lock()
        
    def get_missed_rate(self) -> float:
        self.watcher.get_missed_rate()
    
    def set_min_missed_rate(self, rate: float):
        if rate <= 0 or rate > 1:
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
        instructions = self.ring.add(new - current)
        for ins in instructions:
            ins.execute()
    
    def shrink(self):
        current = self.ring.cache_num
        new = max(1, int(current * self.shrink_ration))
        instructions = self.ring.remove(current - new)
        for ins in instructions:
            ins.execute()
            
    def run(self):
        while True:
            time.sleep(1)
            with self.config_lock:
                # check if the scaler is started and if it is time to update
                if self.is_started and (datetime.datetime.utcnow() - self.last_update_time).seconds > 60:
                    missed = self.get_missed_rate()
                    if missed < self.min_missed_rate:
                        self.shrink()
                        self.last_update_time = datetime.datetime.utcnow()
                    elif missed > self.max_missed_rate:
                        self.expand()
                        self.last_update_time = datetime.datetime.utcnow()
                
                
                
                