import time
import difflib
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from image_capture import capture_and_extract_text
from llm import summarize_text

load_dotenv(dotenv_path=".env")
username_str = os.getenv("USERNAME")
password_str = os.getenv("PASSWORD")
# Initialize Chrome WebDriver

chrome_options = Options()
driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=chrome_options)
driver.maximize_window()

# Navigate to the login page
driver.get("https://a.impartus.com/login/#/")

# Wait for the username and password fields
wait = WebDriverWait(driver, 20)
username = wait.until(EC.presence_of_element_located((By.ID, "username")))
password = wait.until(EC.presence_of_element_located((By.ID, "password")))

username.send_keys(username_str)
password.send_keys(password_str)

login = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "iu-btn")))
login.click()


target_url_pattern = "https://a.impartus.com/ilc/#/video/id/"

#waiting for the target url pattern
while True:
    current_url = driver.current_url
    if target_url_pattern in current_url:
        print("Video page detected. Activating WebDriver...")
        break
        time.sleep(5)  #check every 5 seconds
previous_text = ""
SIMILARITY_THRESHOLD = 0.6

with open("summaries.txt", "a") as summary_file:
    for text in capture_and_extract_text(driver, interval=20):
        if text:
            similarity = difflib.SequenceMatcher(None, text, previous_text).ratio()
            if similarity < SIMILARITY_THRESHOLD:
                summary = summarize_text(text)
                print("Summary:", summary)
                summary_file.write(f"Summary:\n{summary}\n\n")
                previous_text = text
