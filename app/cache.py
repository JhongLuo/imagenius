import sys
from .statistics import Statistics, ReplacementPolicies
def small_test_for_cache():
    memcache = Cache(max_size=100, policy=ReplacementPolicies.RANDOM)
    memcache['a'] = 1
    print(memcache['a'])
    memcache['a'] = 2
    print(memcache['a'])
    print('b' in memcache)
    memcache.clear()
    print('a' in memcache)
    memcache.set_max_size(5)
    memcache.set_policy(ReplacementPolicies.LRU)
    for i in range(10):
        memcache[i] = i
        print(f'len: {len(memcache)}')
        print(f'bytes: {memcache.get_bytes()}')
        for key in memcache:
            print(f'{key}: {memcache[key]}')
    memcache.set_max_size(2)

    print(f'len: {len(memcache)}')
    print(f'bytes: {memcache.get_bytes()}')
    for key in memcache:
        print(f'{key}: {memcache[key]}')
    memcache['a'] = 100
    print(memcache['a'])

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class Cache(dict):
    def __init__(self, stat : Statistics, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.max_size = stat.max_size
        self.policy = stat.replacement_policy
        # implment LRU with double linked list
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.bytes = 0
        self._connect_linked_node(self.head, self.tail)
        self.stat = stat

    # double linked list operations
    
    def _connect_linked_node(self, node1, node2):
        node1.next = node2
        node2.prev = node1

    def _remove_linked_node(self, node):
        self._connect_linked_node(node.prev, node.next)

    def _add(self, node):
        prev = self.tail.prev
        self._connect_linked_node(prev, node)
        self._connect_linked_node(node, self.tail)
    
    def _pop_linked_node(self):
        node = self.head.next
        self._remove_linked_node(node)
        return node

    def _reset_linked_list(self):
        self._connect_linked_node(self.head, self.tail)

    # utils
    
    def _cache_pop(self):
        if self.policy == ReplacementPolicies.LRU:
            node = self._pop_linked_node()
            super().__delitem__(node.key)
        else:
            _, node = super().popitem()
        self.bytes -= sys.getsizeof(node.value)
        return node
        
    # override dict operations
            
    def __getitem__(self, key):
        node = super().__getitem__(key)
        if self.policy == ReplacementPolicies.LRU:
            self._remove_linked_node(node)
            self._add(node)
        return node.value
        
    def __setitem__(self, key, value):
        if super().__contains__(key):
            self.__delitem__(key)
        if super().__len__() == self.max_size:
            self._cache_pop()
        node = Node(key, value)
        if self.policy == ReplacementPolicies.LRU:
            self._add(node)
        self.bytes += sys.getsizeof(value)
        return super().__setitem__(key, node)     
    
    def __delitem__(self, key) -> None:
        node = super().__getitem__(key)
        if self.policy == ReplacementPolicies.LRU:
            self._remove_linked_node(node)
        self.bytes -= sys.getsizeof(node.value)
        return super().__delitem__(key)
    
    def clear(self) -> None:
        self._reset_linked_list()
        self.bytes = 0
        return super().clear()
        
    def get_bytes(self):
        return self.bytes
    
    def set_policy(self, policy):
        if policy == self.policy:
            return
        elif policy in ReplacementPolicies:
            self._reset_linked_list()
            if policy == ReplacementPolicies.LRU:
                for _, node in self.items():
                    self._add(node)
            self.policy = policy
        else:
            raise Exception("Unknown replacement policy")

    def set_max_size(self, max_size):
        if max_size >= 0:
            while super().__len__() > max_size:
                self._cache_pop()
            self.max_size = max_size
        else:
            raise Exception("Invalid max size")
        
    def set_config(self, stat : Statistics):
        self.set_max_size(stat.max_size)
        self.set_policy(stat.replacement_policy)