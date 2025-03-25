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
from bs4 import BeautifulSoup
import string
import nltk
import ssl
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from eml_parsing import eml_parsing

ssl._create_default_https_context = ssl._create_unverified_context
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NLTK_DATA_DIR = os.path.join(SCRIPT_DIR, "nltk_data")
nltk.data.path.append(NLTK_DATA_DIR)
nltk.download('punkt', download_dir=NLTK_DATA_DIR)
nltk.download('punkt_tab', download_dir=NLTK_DATA_DIR)
nltk.download('stopwords', download_dir=NLTK_DATA_DIR)

pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# Connect to PostgreSQL (modify with your DB details)
conn = psycopg2.connect("dbname=postgres user=postgres password=gaied_code_200 host=db.agqiihvhsqxlwddpqlpp.supabase.co")
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
    attachments TEXT,
    response TEXT
);
""")
conn.commit()

def clean_body(text):
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    cleaned_words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    cleaned_text = " ".join(cleaned_words)
    return cleaned_text

def generate_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()

def check_duplicate(body):
    body_hash = generate_hash(body)
    cursor.execute("SELECT response FROM file_data WHERE hash = %s", (body_hash,))
    result = cursor.fetchone()
    if result:
        return True, result[0]  # Duplicate found, return response
    return False, None  # Not a duplicate

def db_push(file_type, sender, subject, date, body, attachments, response):
    unique_hash = generate_hash(f"{body}")

    # Store in DB
    cursor.execute("INSERT INTO file_data (file_type, hash, sender, subject, date, body, attachments, response) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (hash) DO NOTHING", 
                   (file_type, unique_hash, sender, subject, date, body, attachments, response))
    conn.commit()

def classify_files(files):
    results = []
    result=""
    for file in files:
        file_ext = os.path.splitext(file.name)[1].lower()
        if file_ext == ".eml":
            result = eml_parsing(file.name, save_dir="./email_attachments")
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
    
    return results