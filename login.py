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

time.sleep(1000)
