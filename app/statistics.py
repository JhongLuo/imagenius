from . import db_operations
from enum import Enum

class ReplacementPolicies(Enum):
    LRU = 0
    RANDOM = 1
    @staticmethod
    def policy2str(policy):
        if policy == ReplacementPolicies.LRU:
            return 'LRU'
        elif policy == ReplacementPolicies.RANDOM:
            return 'random'
        else:
            raise Exception('Invalid policy')
    @staticmethod 
    def str2policy(policy_str):
        if policy_str == 'LRU':
            return ReplacementPolicies.LRU
        elif policy_str == 'random':
            return ReplacementPolicies.RANDOM
        else:
            raise Exception('Invalid policy')
        
class Statistics:
    def __init__(self):
        self.reset()
    
    def add2db(self, db):
        db_operations.clear_statistics(db)
        
        db_operations.add_statistics(db, self._get_data())
                                         
    def _get_data(self):
        return [
            ('max_size', self.max_size),
            ('replacement_policy', self.replacement_policy.value),
            ('items_len', self.items_len),
            ('items_bytes', self.items_bytes),
            ('requests_count', self.requests_count),
            ('requests_hit_count', self.requests_hit_count)
        ]

    def dump(self):
        return {
            "max_size": self.max_size,
            "replacement_policy": ReplacementPolicies.policy2str(self.replacement_policy),
            "items_len": self.items_len,
            "items_bytes": self.items_bytes,
            "requests_count": self.requests_count,
            "requests_hit_count": self.requests_hit_count,
            "hit_rate": self.get_hit_rate(),
            "miss_rate": self.get_miss_rate()
        }
    
    def reset(self):
        self.max_size = 100000
        self.replacement_policy = ReplacementPolicies.LRU
        self.items_len = 0
        self.items_bytes = 0
        self.requests_count = 0
        self.requests_hit_count = 0

    def add_request_count(self, is_hit):
        self.requests_count += 1
        if is_hit:
            self.requests_hit_count += 1
    
    def memcache_updated(self, memcache):
        self.items_len = len(memcache)
        self.items_bytes = memcache.get_bytes()
    
    def get_hit_rate(self):
        if self.requests_count == 0:
            return 0
        else:
            return float(self.requests_hit_count) / self.requests_count
        
    def get_miss_rate(self):
        if self.requests_count == 0:
            return 0
        else:
            return float(self.requests_count - self.requests_hit_count) / self.requests_count