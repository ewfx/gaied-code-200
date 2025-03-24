import requests
import hashlib
import email
import os
import pymupdf as fitz
import pytesseract
import docx
import psycopg2
from email import policy
from email.parser import BytesParser
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# Connect to PostgreSQL (modify with your DB details)
conn = psycopg2.connect(###DB DETAILS###)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS file_data (
    id SERIAL PRIMARY KEY,
    file_type TEXT,
    hash TEXT UNIQUE,
    sender TEXT,
    subject TEXT,
    date TEXT,
    body TEXT,
    attachments TEXT
);
""")
conn.commit()

def generate_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()

def db_push(file_type, sender, subject, date, body, attachments):
    unique_hash = generate_hash(f"{body}")

    # Store in DB
    cursor.execute("INSERT INTO file_data (file_type, hash, sender, subject, date, body, attachments) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (hash) DO NOTHING", 
                   (file_type, unique_hash, sender, subject, date, body, "\n".join(attachments)))
    conn.commit()

# def parse_pdf(pdf_path):
#     doc = fitz.open(pdf_path)
#     text = "\n".join([page.get_text("text") for page in doc])
#     return text

# def parse_image(image_path):
#     img = Image.open(image_path)
#     text = pytesseract.image_to_string(img)
#     return text

# def docx_parse(docx_path):
#     doc = docx.Document(docx_path)
#     text = "\n".join([para.text for para in doc.paragraphs])
#     return text

def parse_eml(file_path):
    file_ext = os.path.splitext(file_path)[1].lower()
    with open(file_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)
    sender = msg["From"]
    subject = msg["Subject"]
    date = msg["Date"]
    
    # Extract text body with a fallback to HTML
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_content()
                break  # Prefer plain text over HTML
            elif part.get_content_type() == "text/html" and not body:
                body = part.get_content()
    else:
        body = msg.get_content()
    
    body = body.strip() if body else "[No Text Content]"  # Handle empty body
    
    # Extract attachments
    attachments = []
    for part in msg.iter_attachments():
        filename = part.get_filename()
        if filename:
            attachment_data = part.get_content()
            attachments.append(f"{filename}: {len(attachment_data)} bytes")
    
    db_push(file_ext, sender, subject, date, body, attachments)
    
    return f"Processed EML: {file_path}"


def classify_files(files):
    results = []
    result=""
    for file in files:
        file_ext = os.path.splitext(file.name)[1].lower()
        
        if file_ext == ".eml":
            result = parse_eml(file.name)
        elif file_ext == ".pdf":
            print("") 
        elif file_ext in [".png", ".jpg", ".jpeg"]:
            print("")
        elif file_ext in [".doc", ".docxu"]:
            print("")
        else:
            result = f"Unsupported file format: {file.name}"
            results.append(result)
            continue
        results.append(result)
    
    return "\n".join(results)