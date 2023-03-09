import hashlib

class Instruction:
    def __init__(self, lower, upper, old_cache, new_cache) -> None:
        self.lower = lower
        self.upper = upper
        self.old_cache = old_cache
        self.new_cache = new_cache
    
    def __str__(self) -> str:
        return f"[{hex(self.lower)}, {hex(self.upper)}) {self.old_cache} -> {self.new_cache}"

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
    
    # add memcache and get the instructions
    def add(self, num=1):
        if (self.cache_num + num > 8):
            raise Exception("CacheRing: total number of memcache cannot be bigger than 8")
        old_partitions = self.partitions
        self.cache_num += num
        self.partitions = self.get_partitions()
        return self.get_instructions(old_partitions)
    
    # remove memcache and get the instructions
    def remove(self, num=1):
        if (self.cache_num - num < 1):
            raise Exception("CacheRing: total number of memcache cannot be smaller than 1")
        old_partitions = self.partitions
        self.cache_num -= num
        self.partitions = self.get_partitions()
        return self.get_instructions(old_partitions)
        
    def get_partitions(self):
        partition2cache = dict()
        for i in range(self.partition_num):
            partition2cache[i] = i % self.cache_num
        return partition2cache
    
    """
    return the hash value of key
    """
    @staticmethod
    def key2hash(key : str) -> int:
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)
        
    def hash2partition(self, hash):
        return hash >> 124
    
    
"""
test code
"""   

def ring_test(ring):
    print([hex(v) for v in ring.boundaries])
    for _ in range(7):
        print("\nadd")
        ins = ring.add()
        for i in ins:
            print(i) 
        print(ring.cache_num)
        print(ring.get_partitions())
    for _ in range(7):
        print("\nremove")
        ins = ring.remove()
        for i in ins:
            print(i)
        print(ring.cache_num)
        print(ring.get_partitions())

def hash_test(ring):
    hash_list = []
    for i in range(10):
        hash_list.append(ring.key2hash(str(i)))
    print(hash_list)
    print([hex(v) for v in hash_list])
    partition_count = [0] * ring.partition_num
    right_count = 0
    for i in range(10000):
        hash = ring.key2hash(str(i))
        partition = ring.hash2partition(hash)
        partition_count[partition] += 1
        right_count += (hash >= ring.boundaries[partition] and hash < ring.boundaries[partition + 1])
    print(right_count / 10000) # should be 1.0
    print(partition_count) # should be evenly distributed
    
if __name__ == '__main__':
    ring = CacheRing()
    # ring_test(ring)
    hash_test(ring)