from collections import defaultdict

class AndOrLSH(object):
    def __init__(self, num_perm=128, b=32, r=4):
        required_perm = b * r
        
        if required_perm > num_perm:
            raise ValueError(f"Lỗi: Cấu hình b={b}, r={r} yêu cầu {required_perm} tham số, "
                             f"nhưng dữ liệu chỉ có {num_perm}.")
        
        self.num_perm = num_perm 
        self.used_perm = required_perm
        self.b = b
        self.r = r
        
        self.hashtables = [defaultdict(list) for _ in range(b)]
        
        est_threshold = (1/b)**(1/r)
        
        print(f"LSH Configured: b={b}, r={r}.")
        print(f" > Using {required_perm}/{num_perm} permutations.")
        print(f" > Theoretical Jaccard Threshold: ~{est_threshold:.2f}")

    def _get_sig(self, minhash_sig):
        if hasattr(minhash_sig, 'hashvalues'):
            return minhash_sig.hashvalues
        return minhash_sig

    def _hash_band(self, band_part):
        return bytes(band_part)

    def insert(self, key, minhash_sig):
        sig = self._get_sig(minhash_sig)
        
        if len(sig) < self.used_perm:
            raise ValueError(f"Signature too short. Need at least {self.used_perm}")
            
        for i in range(self.b):
            start = i * self.r
            end = (i + 1) * self.r
            
            band_part = sig[start:end]
            
            bucket_key = self._hash_band(band_part)
            self.hashtables[i][bucket_key].append(key)

    def query(self, minhash_sig):
        candidates = set()
        sig = self._get_sig(minhash_sig)
        
        for i in range(self.b):
            start = i * self.r
            end = (i + 1) * self.r
            band_part = sig[start:end]
            
            bucket_key = self._hash_band(band_part)
            
            if bucket_key in self.hashtables[i]:
                candidates.update(self.hashtables[i][bucket_key])
                
        return list(candidates)


class OrAndLSH(object):
    def __init__(self, num_perm=128, b=32, r=4):
        required_perm = b * r
        
        if required_perm > num_perm:
            raise ValueError(f"Lỗi: Cấu hình b={b}, r={r} yêu cầu {required_perm} tham số, "
                             f"nhưng dữ liệu chỉ có {num_perm}.")
        
        self.num_perm = num_perm 
        self.used_perm = required_perm
        self.b = b
        self.r = r
        self.hashtables = [[defaultdict(list) for _ in range(r)] for _ in range(b)]
        
        try:
            est_threshold = 1 - (1/b)**(1/r)
        except:
            est_threshold = 0
        
        print(f"LSH Configured (OR-AND): b={b}, r={r}.")
        print(f" > Structure: {b} bands, each having {r} independent hash maps.")
        print(f" > Theoretical Jaccard Threshold: ~{est_threshold:.2f}")

    def _get_sig(self, minhash_sig):
        if hasattr(minhash_sig, 'hashvalues'):
            return minhash_sig.hashvalues
        return minhash_sig


    def insert(self, key, minhash_sig):
        sig = self._get_sig(minhash_sig)
        
        if len(sig) < self.used_perm:
            raise ValueError(f"Signature too short. Need at least {self.used_perm}")
            
        for i in range(self.b):
            for j in range(self.r):
                perm_idx = i * self.r + j
                val = sig[perm_idx]
                
                self.hashtables[i][j][val].append(key)

    def query(self, minhash_sig):
        sig = self._get_sig(minhash_sig)
        
        band_candidate_sets = []
        
        for i in range(self.b):
            current_band_candidates = set()
            
            for j in range(self.r):
                perm_idx = i * self.r + j
                val = sig[perm_idx]
                
                if val in self.hashtables[i][j]:
                    current_band_candidates.update(self.hashtables[i][j][val])
            
            if not current_band_candidates:
                return []
                
            band_candidate_sets.append(current_band_candidates)
            
        if not band_candidate_sets:
            return []
            
        final_candidates = set.intersection(*band_candidate_sets)
        
        return list(final_candidates)