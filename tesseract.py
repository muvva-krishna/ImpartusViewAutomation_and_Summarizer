# text_extraction.py
import cv2
import pytesseract
from PIL import Image
import numpy as np

def extract_text_from_frame(frame):
    # Convert frame to RGB format for OCR processing
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img)
    
    # Extract text from the image
    text = pytesseract.image_to_string(pil_img)
    return text
