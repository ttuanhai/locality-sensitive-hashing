import mmh3

def hash_token(token):
    h = mmh3.hash128(token)
    bits = []
    for i in range(128):
        bit = (h >> i) & 1
        bits.append(1 if bit else -1)
    return bits

def compute_simhash(tokens):
    v = [0] * 128
    for token in tokens:
        token_bits = hash_token(token)
        for i in range(128):
            v[i] += token_bits[i]
    
    fingerprint = 0
    for i in range(128):
        if v[i] > 0:
            fingerprint = fingerprint | (1 << i)
    
    return fingerprint

