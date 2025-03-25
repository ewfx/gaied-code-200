import gradio as gr
import sys

sys.path.append("./parsing")
sys.path.append("./model")
from parsing import classify_files

from style import css

def classify_and_format(files):
    raw_output = classify_files(files)  # Call the function that processes files
    
    # Ensure raw_output is a list of lists for DataFrame
    if isinstance(raw_output, list) and all(isinstance(item, list) for item in raw_output):
        return raw_output
    else:
        return [["Error", "Unexpected Output", "Unexpected Output", "Unexpected Output", "Unexpected Output"]]  # Fallback error message

with gr.Blocks(css=css) as demo:
    gr.Markdown("## Upload Files for Classification", elem_id="title")
    file_upload = gr.Files(file_types=[".eml", ".pdf", ".png", ".jpg", ".jpeg", ".doc", ".docx"], label="Upload Files", elem_id="file-upload")
    classify_button = gr.Button("Classify", elem_id="classify-btn")
    output_table = gr.Dataframe(headers=["Sender", "subject", "is_duplicate", "Classification"], 
                                label="Classification Results", elem_id="output-box")
    
    classify_button.click(fn=classify_and_format, inputs=file_upload, outputs=output_table)

demo.launch()