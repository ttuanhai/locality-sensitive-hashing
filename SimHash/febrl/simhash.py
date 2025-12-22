import mmh3

class SimHash:
    def __init__(self, tokens=None, f=128):
        self.f = f
        self.value = 0  
        
        if tokens:
            self.compute(tokens)

    def compute(self, tokens):
        v = [0] * self.f
        
        for token in tokens:
            h = mmh3.hash128(token)
            
            for i in range(self.f):
                bit = (h >> i) & 1
                if bit == 1:
                    v[i] += 1
                else:
                    v[i] -= 1
        
        self.value = 0
        for i in range(self.f):
            if v[i] > 0:
                self.value |= (1 << i)
        
        return self.value

    def distance(self, other):
        if not isinstance(other, SimHash):
            raise ValueError("Đối tượng so sánh phải là Simhash")
            
        x = self.value ^ other.value
        
        return bin(x).count('1')

    def __str__(self):
        return f"<Simhash value={self.value}>"

    def __repr__(self):
        return str(self.value)