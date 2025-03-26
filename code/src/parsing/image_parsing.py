import pytesseract
from PIL import Image

def extract_text_from_image(image_path):
    text = ""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
    except Exception as e:
        print(f"Error extracting image: {e}")
    return text.strip()