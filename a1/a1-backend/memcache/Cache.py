import sys
from utils.ReplacementPolicies import ReplacementPolicies
import threading
from utils.DBConnector import DBConnector

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class Cache(dict):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.max_size = 0
        self.policy = ReplacementPolicies.RANDOM
        # implement LRU with double linked list
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.bytes = 0
        self._connect_linked_node(self.head, self.tail)
        self.configuration_lock = threading.Lock()
        self.linked_list_lock = threading.Lock()
        self.write_lock = threading.Lock()
        self.syncDB()
        
    def syncDB(self):
        DBConnector.set_statistics([('items_len', len(self)), ('items_bytes', self.bytes)])
        self.set_max_size(int(DBConnector.select_statistics('max_size')))
        self.set_policy(ReplacementPolicies.int2policy(DBConnector.select_statistics('replacement_policy')))
    
    # double linked list operations
    
    def _connect_linked_node(self, node1, node2):
        node1.next = node2
        node2.prev = node1

    def _remove_linked_node(self, node):
        with self.linked_list_lock:
            self._connect_linked_node(node.prev, node.next)

    def _add(self, node):
        with self.linked_list_lock:
            prev = self.tail.prev
            self._connect_linked_node(prev, node)
            self._connect_linked_node(node, self.tail)
    
    def _pop_linked_node(self):
        with self.linked_list_lock:
            node = self.head.next
            self._connect_linked_node(node.prev, node.next)
            return node

    def _reset_linked_list(self):
        with self.linked_list_lock:
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
        with self.write_lock:
            node = Node(key, value)
            if self.policy == ReplacementPolicies.LRU:
                self._add(node)
            self.bytes += sys.getsizeof(value)
            rtn = super().__setitem__(key, node)
            while self.bytes > self.max_size:
                self._cache_pop()
            return rtn    
    
    def __delitem__(self, key) -> None:
        with self.write_lock:
            node = super().__getitem__(key)
            if self.policy == ReplacementPolicies.LRU:
                self._remove_linked_node(node)
            self.bytes -= sys.getsizeof(node.value)
            return super().__delitem__(key)
    
    def clear(self) -> None:
        with self.write_lock:
            self._reset_linked_list()
            self.bytes = 0
            return super().clear()
        
    def get_bytes(self):
        return self.bytes
    
    def set_policy(self, policy):
        if policy == self.policy:
            return
        with self.write_lock:
            if policy in ReplacementPolicies:
                self._reset_linked_list()
                if policy == ReplacementPolicies.LRU:
                    for _, node in self.items():
                        self._add(node)
                self.policy = policy
            else:
                raise Exception("Unknown replacement policy")

    def set_max_size(self, max_size):
        if max_size == self.max_size:
            return
        with self.write_lock:
            if max_size >= 0:
                self.max_size = max_size
                while self.bytes > self.max_size:
                    self._cache_pop()
            else:
                raise Exception("Invalid max size")        