import mmh3

def hash_token(token):
    """Hash a token using MurmurHash3 and return a 64-bit integer."""
    h = mmh3.hash64(token)[0]
    bits = []
    for i in range(64):
        bit = (h >> i) & 1
        bits.append(1 if bit else -1)
    return bits

def compute_simhash(tokens):
    """Compute the SimHash for a list of tokens."""
    v = [0] * 64
    for token in tokens:
        token_bits = hash_token(token)
        for i in range(64):
            v[i] += token_bits[i]
    
    fingerprint = 0
    for i in range(64):
        if v[i] > 0:
            fingerprint |= (1 << i)
    
    return fingerprint