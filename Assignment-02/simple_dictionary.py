class SimpleDictionary:
    def __init__(self, size=100):
        self.size = size
        self.buckets = [[] for _ in range(size)]
    
    def _hash(self, key):
        return hash(key) % self.size
    
    def add(self, key, value):
        index = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[index]):
            if k == key:
                self.buckets[index][i] = (key, v + [value])  # Append new doc ID
                return
        self.buckets[index].append((key, [value]))  # Insert new key-value pair
    
    def get(self, key):
        index = self._hash(key)
        for k, v in self.buckets[index]:
            if k == key:
                return v
        return []
    
    def delete(self, key):
        index = self._hash(key)
        for i, (k, v) in enumerate(self.buckets[index]):
            if k == key:
                del self.buckets[index][i]
                return
    
    def __repr__(self):
        return "{ " + ", ".join(
            f"{k}: {v}" for bucket in self.buckets for k, v in bucket
        ) + " }"