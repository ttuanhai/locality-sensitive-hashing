import gradio as gr
import sys
sys.path.append("/home/hai/Projects/locality-sensitive-hashing/SimHash")
sys.path.append("/home/hai/Projects/locality-sensitive-hashing/MinHash")
from simhash import SimHash
from minhash import MinHash
from minhashlsh import AndOrLSH

def compare_inputs(input_mode1, text1, file1, input_mode2, text2, file2, method, hamming_threshold=30):
    # Get text 1
    if input_mode1 == "Upload file":
        if file1 is None:
            return "Please upload file 1"
        text1 = open(file1, "r", encoding="utf-8").read()
    else:
        if not text1 or text1.strip() == "":
            return "Please enter text 1"
    
    # Get text 2
    if input_mode2 == "Upload file":
        if file2 is None:
            return "Please upload file 2"
        text2 = open(file2, "r", encoding="utf-8").read()
    else:
        if not text2 or text2.strip() == "":
            return "Please enter text 2"

    tokens1 = text1.lower().split()
    tokens2 = text2.lower().split()

    if method == "SimHash":
        h1 = SimHash(tokens1)
        h2 = SimHash(tokens2)
        dist = h1.distance(h2)
        return f"Hamming distance = {dist}. " + ("Similar" if dist <= hamming_threshold else "Not similar")

    elif method == "MinHash":
        mh1 = MinHash(num_perm=128)
        mh2 = MinHash(num_perm=128)
        for t in tokens1: mh1.update(t)
        for t in tokens2: mh2.update(t)
        lsh = AndOrLSH(num_perm=128, b=32, r=4)
        lsh.insert("doc1", mh1)
        result = lsh.query(mh2)
        return "Similar" if result else "Not similar"

    else:
        return "Method not supported."

def toggle_input1(choice):
    if choice == "Direct input":
        return gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True)

def toggle_input2(choice):
    if choice == "Direct input":
        return gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True)

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🔎 Text Duplicate Comparison")
    gr.Markdown("Compare text similarity using **SimHash** or **MinHashLSH (And-Or)**")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Text 1")
            input_mode1 = gr.Radio(
                choices=["Direct input", "Upload file"],
                value="Direct input",
                label="Input method"
            )
            text1 = gr.Textbox(label="Content", lines=5, placeholder="Enter text...", visible=True)
            file1 = gr.File(type="filepath", file_types=[".txt"], label="File (.txt)", visible=False)
        
        with gr.Column():
            gr.Markdown("### Text 2")
            input_mode2 = gr.Radio(
                choices=["Direct input", "Upload file"],
                value="Direct input",
                label="Input method"
            )
            text2 = gr.Textbox(label="Content", lines=5, placeholder="Enter text...", visible=True)
            file2 = gr.File(type="filepath", file_types=[".txt"], label="File (.txt)", visible=False)

    with gr.Row():
        method = gr.Dropdown(choices=["SimHash", "MinHash"], value="SimHash", label="Method")
        hamming_threshold = gr.Slider(1, 64, value=30, step=1, label="Hamming threshold (SimHash only)")

    output = gr.Textbox(label="Result", interactive=False)
    btn = gr.Button("Compare", variant="primary")

    input_mode1.change(toggle_input1, inputs=input_mode1, outputs=[text1, file1])
    input_mode2.change(toggle_input2, inputs=input_mode2, outputs=[text2, file2])

    btn.click(
        compare_inputs, 
        inputs=[input_mode1, text1, file1, input_mode2, text2, file2, method, hamming_threshold], 
        outputs=output
    )

demo.launch()