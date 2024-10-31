import cv2
import pytesseract

def extract_text_from_images(image_path):
    image = cv2.imread(image_path)
    grayscale_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    extracted_text = pytesseract.image_to_string(grayscale_image)
    return extracted_text

    