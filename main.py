import cv2
import time
import numpy as np
import difflib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from image_capture import capture_frame
from tesseract import extract_text_from_frame

# Initialize Chrome WebDriver
chrome_options = Options()
driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=chrome_options)
driver.maximize_window()

# Navigate to the Impartus login page
driver.get("https://a.impartus.com/login/#/")

# Wait for the username and password fields to load
wait = WebDriverWait(driver, 20)
username = wait.until(EC.presence_of_element_located((By.ID, "username")))
password = wait.until(EC.presence_of_element_located((By.ID, "password")))

# Insert username and password
username.send_keys("f20220587@hyderabad.bits-pilani.ac.in")
password.send_keys("DRZwReYs")

# Click the login button
login = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "iu-btn")))
login.click()

# Define the URL pattern to wait for (all video pages)
target_url_pattern = "https://a.impartus.com/ilc/#/video/id/"

# Wait until the WebDriver detects the specific URL pattern
while True:
    current_url = driver.current_url
    if target_url_pattern in current_url:
        print("Video page detected. Activating WebDriver...")
        break
    time.sleep(5)  # Check every 5 seconds

# Capture frames and extract text at 1-minute intervals
previous_text = ""
for frame in capture_frame(driver, interval=60):
    text = extract_text_from_frame(frame)
    SIMILARITY_THRESHOLD = 0.6

# Check if the new text is significantly different from previous text
    if text:
        similarity = difflib.SequenceMatcher(None, text, previous_text).ratio()
        if similarity < SIMILARITY_THRESHOLD:
            summary = summarize_text(text)
            print("Summary:", summary)
            previous_text = text
        
def summarize_text(text):
