import gradio as gr
import sys

sys.path.append("./parsing")
from parsing import classify_files

from style import css

with gr.Blocks(css=css) as demo:
    gr.Markdown("## Upload Files for Classification", elem_id="title")
    file_upload = gr.Files(file_types=[".eml", ".pdf", ".png", ".jpg", ".jpeg", ".doc", ".docx"], label="Upload Files", elem_id="file-upload")
    classify_button = gr.Button("Classify", elem_id="classify-btn")
    output = gr.Textbox(label="Results", elem_id="output-box", lines=1)
    
    classify_button.click(fn=classify_files, inputs=file_upload, outputs=output)

demo.launch()