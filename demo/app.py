import gradio as gr
import sys
sys.path.append("/home/hai/Projects/locality-sensitive-hashing/SimHash")
sys.path.append("/home/hai/Projects/locality-sensitive-hashing/MinHash")
from simhash import SimHash
from minhash import MinHash
from minhashlsh import AndOrLSH

def compare_inputs(text1, file1, text2, file2, method, hamming_threshold=30):
    if file1 is not None:
        text1 = open(file1, "r", encoding="utf-8").read()
    if file2 is not None:
        text2 = open(file2, "r", encoding="utf-8").read()

    tokens1 = text1.lower().split()
    tokens2 = text2.lower().split()

    if method == "SimHash":
        h1 = SimHash(tokens1)
        h2 = SimHash(tokens2)
        dist = h1.distance(h2)
        return f"Hamming distance = {dist}. " + ("Tương đồng" if dist <= hamming_threshold else "Không tương đồng")

    elif method == "MinHash":
        mh1 = MinHash(num_perm=128)
        mh2 = MinHash(num_perm=128)
        for t in tokens1: mh1.update(t)
        for t in tokens2: mh2.update(t)
        lsh = AndOrLSH(num_perm=128, b=32, r=4)
        lsh.insert("doc1", mh1)
        result = lsh.query(mh2)
        return "Tương đồng" if result else "Không tương đồng"

    else:
        return "Phương pháp chưa hỗ trợ."

demo = gr.Interface(
    fn=compare_inputs,
    inputs=[
        gr.Textbox(label="Văn bản 1 (nhập trực tiếp)", lines=5, placeholder="Nhập văn bản hoặc bỏ trống nếu upload file"),
        gr.File(type="filepath", file_types=[".txt"], label="File 1 (.txt)"),
        gr.Textbox(label="Văn bản 2 (nhập trực tiếp)", lines=5, placeholder="Nhập văn bản hoặc bỏ trống nếu upload file"),
        gr.File(type="filepath", file_types=[".txt"], label="File 2 (.txt)"),
        gr.Dropdown(choices=["SimHash", "MinHash"], label="Phương pháp"),
    ],
    outputs="text",
    title="So sánh trùng lặp văn bản",
    description="Nhập văn bản hoặc upload file .txt để kiểm tra tương đồng bằng SimHash hoặc MinHashLSH (And-Or)"
)

demo.launch()
