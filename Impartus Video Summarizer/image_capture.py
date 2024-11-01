import time
from PIL import Image
from io import BytesIO
import pytesseract

def capture_and_extract_text(driver, interval=20):
    while True:

        screenshot = driver.get_screenshot_as_png()
        # open the screenshot as grayscale img
        image = Image.open(BytesIO(screenshot)).convert("L")  # convert to grayscale
        text = pytesseract.image_to_string(image).strip()
        yield text

        time.sleep(interval)
  

