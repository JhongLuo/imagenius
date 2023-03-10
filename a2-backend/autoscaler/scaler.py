import time
from utils.cloudwatch import Watcher
from utils.cachering import CacheRing
from utils.rds import set_autoscaler_status
import datetime

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
        
    def get_missed_rate(self) -> float:
        self.watcher.get_missed_rate()
    
    def start(self, min_missed_rate, max_missed_rate, expand_ratio, shrink_ratio):
        if min_missed_rate <= 0 or min_missed_rate > 1:
            raise ValueError('min missed rate must be between 0 and 1')
        self.min_missed_rate = min_missed_rate
        if max_missed_rate < min_missed_rate or max_missed_rate > 1:
            raise ValueError('max missed rate must be between min missed rate and 1')
        self.max_missed_rate = max_missed_rate
        if expand_ratio < 1:
            raise ValueError('expand ratio must be no smaller than 1')
        self.expand_ratio = expand_ratio
        if shrink_ratio > 1:
            raise ValueError('shrink ratio must be no bigger than 1')
        self.shrink_ration = shrink_ratio
        
        self.last_update_time = datetime.datetime.utcnow()
        self.is_started = True
        set_autoscaler_status(True)
        
    def stop(self):
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
            # check if the scaler is started and if it is time to update
            if self.is_started and (datetime.datetime.utcnow() - self.last_update_time).seconds > 60:
                missed = self.get_missed_rate()
                if missed < self.min_missed_rate:
                    self.shrink()
                    self.last_update_time = datetime.datetime.utcnow()
                elif missed > self.max_missed_rate:
                    self.expand()
                    self.last_update_time = datetime.datetime.utcnow()
                
                
                
                