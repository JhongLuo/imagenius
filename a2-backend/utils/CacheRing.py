import hashlib
from utils import memcachop, rds
from utils.url import id2url
import time
"""
return the hash value of key
"""

def key2hash(key : str) -> int:
    return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

class Instruction:
    def __init__(self, lower, upper, old_cache, new_cache) -> None:
        self.lower = lower
        self.upper = upper
        self.old_cache = old_cache
        self.new_cache = new_cache
    
    def __str__(self) -> str:
        return f"[{hex(self.lower)}, {hex(self.upper)}) {self.old_cache} -> {self.new_cache}"

    def execute(self):
        content = memcachop.get_range(id2url(self.old_cache), self.lower, self.upper)
        memcachop.delete_range(id2url(self.old_cache), self.lower, self.upper)
        memcachop.merge_range(id2url(self.new_cache), content)

class CacheRing:
    def __init__(self):
        self.cache_num = 1
        self.partition_num = 16
        self.boundaries = [v << 124 for v in range(self.partition_num + 1)]
        self.partitions = self.get_partitions()
    
    def partition2range(self, partition):
        return self.boundaries[partition], self.boundaries[(partition + 1)]
    
    def get_instructions(self, old_partitions):
        instruction = []
        for partition, old in old_partitions.items():
            new = self.partitions[partition]
            if old != new:
                instruction.append(Instruction(*self.partition2range(partition), old, new))
        return instruction
    
    def start(self, i):
        print(f'    start memcache {i} ...')
        while not rds.get_memcache_status(i):
            print(f'    message to memcache {i} is sent...')
            memcachop.start(id2url(i))
            time.sleep(1)
        print(f'    memcache {i} is started!')
    
    def stop(self, i):
        print(f'    stop memcache {i} ...')
        while rds.get_memcache_status(i):
            print(f'    message to memcache {i} is sent...')
            memcachop.stop(id2url(i))
            time.sleep(1)
        print(f'    memcache {i} is stopped!')
    
    # add memcache and get the instructions
    def add(self, num=1):
        if (self.cache_num + num > 8):
            raise Exception("CacheRing: total number of memcache cannot be bigger than 8")
        
        print(f'adding {num} memcache ...')
        for i in range(self.cache_num, self.cache_num + num):
            self.start(i)
        
        old_partitions = self.partitions
        self.cache_num += num
        self.partitions = self.get_partitions()
        print(f'adding {num} memcache done!')
        return self.get_instructions(old_partitions)    
    
    # remove memcache and get the instructions
    def remove(self, num=1):
        if (self.cache_num - num < 1):
            raise Exception("CacheRing: total number of memcache cannot be smaller than 1")
        
        print(f'removing {num} memcache ...')
        for i in range(self.cache_num - 1, self.cache_num - num - 1, -1):
            self.stop(i)
        
        old_partitions = self.partitions
        self.cache_num -= num
        self.partitions = self.get_partitions()
        print(f'removing {num} memcache done!')
        return self.get_instructions(old_partitions)
        
        
    def update_cache_num(self, num):
        self.cache_num = num
        self.partitions = self.get_partitions()
        
    def get_partitions(self):
        partition2cache = dict()
        for i in range(self.partition_num):
            partition2cache[i] = i % self.cache_num
        return partition2cache
    

        
    """
    return the partition the hash value belongs to
    """
    def hash2partition(self, hash):
        return hash >> 124
    
    """
    return the server id the partition belongs to
    """
    def partition2server(self, partition):
        return self.partitions[partition]
    
    """
    return the server id the key belongs to
    """
    def key2server(self, key):
        return self.partition2server(self.hash2partition(key2hash(key)))
