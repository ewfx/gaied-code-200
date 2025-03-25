import requests
import hashlib
import email
import os
import re
import pymupdf as fitz
import pytesseract
import docx
import psycopg2
from email import policy
from email.parser import BytesParser
from PIL import Image
from bs4 import BeautifulSoup

from image_parsing import extract_text_from_image
from pdf_parsing import extract_text_from_pdf
from model import llama3

import parsing

def eml_parsing(file_path, save_dir="./email_attachments"):
    file_ext = os.path.splitext(file_path)[1].lower()
    os.makedirs(save_dir, exist_ok=True)
    with open(file_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)
    sender = msg["From"]
    subject = msg["Subject"]
    date = msg["Date"]
    
    # Extract text body with a fallback to HTML
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            charset = part.get_content_charset() or "utf-8"  # Handle charset properly
            if content_type == "text/plain":
                body = part.get_payload(decode=True).decode(charset, errors="replace")
                break  # Prefer plain text over HTML
            elif content_type == "text/html" and not body:
                html_content = part.get_payload(decode=True).decode(charset, errors="replace")
                body = BeautifulSoup(html_content, "html.parser").get_text()  # Remove HTML tags
    else:
        body = msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", errors="replace")
    
    body = body.strip() if body else "[No Text Content]"  # Handle empty body
    
    body = parsing.clean_body(body)
    
    # Extract attachments
    all_extracted_text = ""  # Variable to store all extracted text

    for part in msg.iter_attachments():
        filename = part.get_filename()
        
        if filename:
            # Sanitize filename
            filename = re.sub(r'[\/:*?"<>|]', '_', filename)
            file_path = os.path.join(save_dir, filename)

            # Save attachment
            with open(file_path, "wb") as attachment_file:
                attachment_file.write(part.get_payload(decode=True))

            # Extract text based on file type
            extracted_text = ""
            if filename.lower().endswith(".pdf"):
                extracted_text = extract_text_from_pdf(file_path)
            elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
                extracted_text = extract_text_from_image(file_path)

            # Concatenate if text is found
            if extracted_text:
                all_extracted_text += extracted_text + "\n"

    attachments=all_extracted_text

    is_duplicate, existing_response = parsing.check_duplicate(body)
    if(is_duplicate):
        return [sender, subject, is_duplicate, existing_response]

    
    response = llama3(body)
    parsing.db_push(file_ext, sender, subject, date, body, attachments, response)
    
    return [sender, subject, is_duplicate, response]