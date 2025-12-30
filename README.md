# Locality-Sensitive Hashing (LSH)

A Python implementation of LSH algorithms for text similarity detection.

## Algorithms

- **SimHash**: Fingerprint-based similarity using Hamming distance
- **MinHash + LSH**: Set similarity using Jaccard estimation

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run Demo
```bash
python demo/test.py
```

### Use in Code
```python
from SimHash.simhash import SimHash
from MinHash.minhash import MinHash
from MinHash.minhashlsh import AndOrLSH

# SimHash
tokens1 = "hello world".split()
tokens2 = "hello there".split()
h1, h2 = SimHash(tokens1), SimHash(tokens2)
print(f"Hamming distance: {h1.distance(h2)}")

# MinHash
mh1, mh2 = MinHash(), MinHash()
for t in tokens1: mh1.update(t)
for t in tokens2: mh2.update(t)
print(f"Jaccard similarity: {mh1.jaccard(mh2)}")
```

## Project Structure

```
├── SimHash/
│   ├── simhash.py          # SimHash implementation
│   └── simhash_lsh.ipynb   # Experiments
├── MinHash/
│   ├── minhash.py          # MinHash implementation
│   ├── minhashlsh.py       # LSH (And-Or, Or-And)
│   └── minhash_lsh.ipynb   # Experiments
├── demo/
│   └── test.py             # Gradio demo app
└── data/                   # Test datasets
```

## License

MIT