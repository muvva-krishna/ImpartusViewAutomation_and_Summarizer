import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=chrome_options)
driver.maximize_window()

driver.get("https://a.impartus.com/login/#/")

wait = WebDriverWait(driver, 20)
username = wait.until(EC.presence_of_element_located((By.ID, "username")))
password = wait.until(EC.presence_of_element_located((By.ID, "password")))

#insert username and password here...
username.send_keys("f20220587@hyderabad.bits-pilani.ac.in")
password.send_keys("DRZwReYs")

login = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "iu-btn")))
login.click()

target_url_pattern = "https://a.impartus.com/ilc/#/video/id/"  # Replace with the specific URL pattern you are waiting for

# Wait until the WebDriver detects the specific URL pattern
while True:
    current_url = driver.current_url
    if target_url_pattern in current_url:
        print("Target URL pattern detected. Activating WebDriver...")
        break
    time.sleep(5)  # Check every 5 seconds

# Wait for the play button to be clickable and click it
play_button = wait.until(EC.element_to_be_clickable((By.ID, "playVideo")))  # Replace with the actual selector for the play button
play_button.click()

# Wait for the video to load and then switch to view 2
view2_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='select_option_32']/div")))
view2_button.click()


# Optionally, you can add more interactions or sleep for a while
time.sleep(10)  # Keep the script running for a while to observe the behavior

# Close the driver
driver.quit()
