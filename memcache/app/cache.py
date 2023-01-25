class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

class Cache(dict):
    def __init__(self, max_size=10000, policy = 'LRU', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.max_size = max_size
        self.policy = policy
        # implment LRU with double linked list
        self.head = Node(0)
        self.tail = Node(0)
        self._connect(self.head, self.tail)

    # double linked list operations
    
    def _connect(self, node1, node2):
        node1.next = node2
        node2.prev = node1

    def _remove(self, node):
        self._connect(node.prev, node.next)

    def _add(self, node):
        prev = self.tail.prev
        self._connect(prev, node)
        self._connect(node, self.tail)
    
    def _drop(self):
        node = self.head.next
        self._remove(node)

    def _reset(self):
        self._connect(self.head, self.tail)

    # utils
    
    def _remove_one_by_policy(self):
        if self.policy == 'LRU':
            self._drop()
        else:
            super().popitem()
        
    # override dict operations
            
    def __getitem__(self, key):
        node = super().__getitem__(key)
        if self.policy == 'LRU':
            self._remove(node)
            self._add(node)
        return node.value
        
    def __setitem__(self, key, value):
        if super().__contains__(key):
            # update the value
            node = super().__getitem__(key)
            node.value = value
        else:
            # make sure the size of cache is not larger than max_size
            if super().__len__() == self.max_size:
                self._remove_one_by_policy()
            node = Node(value)
            if self.policy == 'LRU':
                self._add(node)
            return super().__setitem__(key, node)     
    
    def __delitem__(self, __key) -> None:
        if self.policy == 'LRU':
            node = super().__getitem__(__key)
            self._remove(node)    
        return super().__delitem__(__key)
    
    def clear(self) -> None:
        self._reset()
        return super().clear()
    
    #configuration operations
    
    def set_policy(self, policy):
        if policy == self.policy:
            return
        elif policy == 'LRU' or policy == 'random':
            self._reset()
            if policy == 'LRU':
                for _, node in self.items():
                    self._add(node)
            self.policy = policy
        else:
            raise Exception("Unknown replacement policy")

    def set_max_size(self, max_size):
        if max_size >= 0:
            while super().__len__() > max_size:
                self._remove_one_by_policy()
            self.max_size = max_size
        else:
            raise Exception("Invalid max size")