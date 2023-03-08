from utils.DBConnector import DBConnector
from collections import deque
from utils.ReplacementPolicies import ReplacementPolicies

class Statistics:
    def __init__(self):
        self.reset()
        self.statistic_history = deque(maxlen=120)
                          
    def syncDB(self):        
        DBConnector.set_statistics(self._get_instance1_data())
        self.items_len = DBConnector.select_statistics('items_len')
        self.items_bytes = DBConnector.select_statistics('items_bytes')
        self.statistic_history.append(self.dump())
    
    def _get_instance1_data(self):
        return [
            ('max_size', self.max_size),
            ('replacement_policy', self.replacement_policy.value),
            ('requests_count', self.requests_count),
            ('requests_hit_count', self.hit_count),
        ]
    
    def _get_instance2_data(self):
        return [
            ('items_len', self.items_len),
            ('items_bytes', self.items_bytes)
        ]

    def dump(self):
        return {
            "max_size": self.max_size,
            "replacement_policy": ReplacementPolicies.policy2str(self.replacement_policy),
            "items_len": self.items_len,
            "items_bytes": self.items_bytes,
            "requests_count": self.requests_count,
            "requests_hit_count": self.hit_count,
            "hit_rate": self.get_hit_rate(),
            "miss_rate": self.get_miss_rate()
        }
    
    def reset(self):
        self.max_size = 100 * 1024 * 1024
        self.replacement_policy = ReplacementPolicies.LRU
        self.items_len = 0
        self.items_bytes = 0
        self.requests_count = 0
        self.hit_count = 0
        self.miss_count = 0

    def add_request_count(self, is_get, is_hit):
        self.requests_count += 1
        if is_get:
            if is_hit:
                self.hit_count += 1
            else:
                self.miss_count += 1
    
    def get_hit_rate(self):
        if self.hit_count + self.miss_count == 0:
            return 0
        else:
            return float(self.hit_count) / (self.hit_count + self.miss_count)
        
    def get_miss_rate(self):
        if self.hit_count + self.miss_count == 0:
            return 0
        else:
            return float(self.miss_count) / (self.hit_count + self.miss_count)