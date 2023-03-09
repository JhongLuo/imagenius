import sys
from utils.ReplacementPolicies import ReplacementPolicies
import threading
from utils import rds
from sortedcontainers import SortedDict
from random import randint
import time

class Node:
    def __init__(self, key, value, hash, time) -> None:
        self.key = key
        self.hash = hash
        self.value = value
        self.time = time
        
    @staticmethod
    def from_json(json):
        return Node(json['key'], json['value'], json['hash'], json['time'])
        
    def to_json(self):
        return {
            'key': self.key,
            'value': self.value,
            'hash': self.hash,
            'time': self.time,
        }
class Cache():
    def __init__(self) -> None:
        self.bst = SortedDict()
        self.dict = dict()
        self.max_size = 0
        self.bytes = 0
        self.policy = ReplacementPolicies.RANDOM
        self.writeLock = threading.Lock()
        # total requests >= read requests >= missed requests
        self.total_requests = 0
        self.read_requests = 0
        self.missed_requests = 0
        self.syncDB()
        
    def get_time(self):
        return time.time()
    
    # TODO 
    def syncDB(self):
        self.set_max_size(int(rds.select_statistics('max_size')))
        self.set_policy(ReplacementPolicies.int2policy(rds.select_statistics('replacement_policy')))
     
    def _pop(self):
        if len(self.bst) > 0:
            if self.policy == ReplacementPolicies.LRU:                
                _, node = self.bst.popitem(index=0)
            else:
                # randomly pop an item using random index
                random_index = randint(0, len(self.bst) - 1)
                node = self.bst.popitem(index=random_index)[1]
            self.dict.pop(node.key)
            self.bytes -= sys.getsizeof(node.value)
            return node
        else:
            return None
    
    def keys(self):
        return self.dict.keys()
    
    def has(self, key):
        return key in self.dict
    
    def get(self, key):
        with self.writeLock:
            node = self.dict[key]
            if self.policy == ReplacementPolicies.LRU:
                self.bst.pop(node.time)
                node.time = self.get_time()
                self.bst[node.time] = node
            return node.value
        
    def set(self, key, value, hash):
        if key in self.dict:
            self.delete(key)
        with self.writeLock:
            node = Node(key, value, hash, time.time())
            self.dict[node.key] = node
            self.bst[node.time] = node
            self.bytes += sys.getsizeof(value)
            while self.bytes > self.max_size:
                self._pop()
            return node
    
    def delete(self, key) -> None:
        with self.writeLock:
            node = self.dict[key]
            self.dict.pop(key)
            self.bst.pop(node.time)
            self.bytes -= sys.getsizeof(node.value)
            return
    
    # [lower, upper)
    def get_range(self, lower, upper):
            node_list = []
            for _, node in self.dict.items():
                if node.hash < lower or node.hash >= upper:
                    continue
                node_list.append(node)
            return node_list
    
    # [lower, upper)
    def delete_range(self, lower, upper):
        for _, node in self.dict.items():
            if node.hash < lower or node.hash >= upper:
                continue
            self.delete(node.key)

    # [lower, upper)
    def merge_range(self, node_list):
        with self.writeLock:
            for node in node_list:
                if node.time <= self.bst.peekitem(index=0)[0]:
                    continue
                self.dict[node.key] = node
                self.bst[node.time] = node
                while self.bytes > self.max_size:
                    self._pop()
    
    def clear(self) -> None:
        with self.writeLock:
            self.dict = dict()
            self.bst = SortedDict()
            self.bytes = 0
        
    def get_bytes(self):
        return self.bytes
    
    def get_len(self):
        return len(self.dict)
    
    def set_policy(self, policy):
        with self.writeLock:
            if policy in ReplacementPolicies:
                self.policy = policy
            else:
                raise Exception("Unknown replacement policy")

    def set_max_size(self, max_size):
        with self.writeLock:
            if max_size >= 0:
                self.max_size = max_size
                while self.bytes > self.max_size:
                    self._pop()
            else:
                raise Exception("Invalid max size")