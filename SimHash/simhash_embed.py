import numpy as np

class SimHashEmbed:
    def __init__(self, text=None, f=128, seed=42, model=None, device="cpu"):
        if model is None: 
            raise ValueError("Bạn cần truyền model đã khởi tạo vào SimHashEmbed")
        self.f = f
        self.value = 0
        self.model = model
        self.device = device
        self.rng = np.random.RandomState(seed)
        self.random_vectors = None

        if text:
            self.compute(text)

    def compute(self, text):
        emb = self.model.encode(text, device=self.device)
        dim = len(emb)

        if self.random_vectors is None:
            self.random_vectors = self.rng.randn(self.f, dim)

        v = [0] * self.f
        for i in range(self.f):
            dot = np.dot(self.random_vectors[i], emb)
            if dot >= 0:
                v[i] += 1
            else:
                v[i] -= 1

        self.value = 0
        for i in range(self.f):
            if v[i] > 0:
                self.value |= (1 << i)

        return self.value

    def distance(self, other):
        x = self.value ^ other.value
        return bin(x).count("1")

    def __repr__(self):
        return str(self.value)

