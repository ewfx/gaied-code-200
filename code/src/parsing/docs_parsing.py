from docx import Document

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        return " ".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])
    except Exception as e:
        return f"Error processing DOCX file: {str(e)}"