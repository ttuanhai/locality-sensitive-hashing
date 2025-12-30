import hashlib
import numpy as np

class MinHash(object):
    def __init__(self, num_perm=256, seed=1):
        self.num_perm = num_perm
        self.seed = seed
        
        self.prime = (1 << 61) - 1
        
        generator = np.random.RandomState(self.seed)
        
        self.permutations_a = generator.randint(1, self.prime, size=num_perm, dtype=np.uint64)
        self.permutations_b = generator.randint(0, self.prime, size=num_perm, dtype=np.uint64)
        
        self.hashvalues = np.ones(num_perm, dtype=np.uint64) * self.prime

    def update(self, b):
        if isinstance(b, str):
            b = b.encode('utf-8')
        hv = int.from_bytes(hashlib.sha1(b).digest()[:4], 'little')
        a = self.permutations_a
        b_coeffs = self.permutations_b
        
        phv = (self.permutations_a * hv + self.permutations_b) % self.prime
        
        self.hashvalues = np.minimum(self.hashvalues, phv)

    def jaccard(self, other):

        if other.seed != self.seed:
            raise ValueError("Không thể so sánh 2 MinHash khác seed!")
        if len(self.hashvalues) != len(other.hashvalues):
            raise ValueError("Độ dài chữ ký không khớp!")
        return np.float64(np.count_nonzero(self.hashvalues == other.hashvalues)) / np.float64(self.num_perm)