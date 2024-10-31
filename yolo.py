import cv2
import time
import threading
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    if target_url_pattern in driver.current_url:
        print("Video page detected. Activating WebDriver...")
        break
    time.sleep(5)

# Function to run YOLO detection and track professor
def run_yolo_detection():
    net = cv2.dnn.readNet("yolov5\onnx")
  # Load your YOLO model
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    cap = cv2.VideoCapture(0)  # Adjust to the correct video source if needed
    view_state = 1  # 1 for view 1, 2 for view 2
    person_present = False  # Tracks if the professor is in frame
    professor_id = 1  # ID for the professor, set to an initial value

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Prepare frame for YOLO
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outputs = net.forward(output_layers)

        # Process detections
        class_ids = []
        confidences = []
        boxes = []
        height, width, _ = frame.shape

        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and class_id == 0:  # Class ID 0 is typically 'person'
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.6)
        
        # Check if professor is detected and determine position
        new_person_present = any(class_ids[i] == 0 for i in indexes)
        
        if new_person_present:
            print(f"Professor detected with ID: {professor_id}")

        if person_present and not new_person_present:
            # Professor has left the frame; switch view
            if view_state == 1:
                # Switch to view 2
                view2_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='md-text' and contains(text(), 'View 2')]")))
                view2_button.click()
                view_state = 2
                print("Switched to View 2")
            else:
                # Switch to view 1
                view1_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='md-text' and contains(text(), 'View 1')]")))
                view1_button.click()
                view_state = 1
                print("Switched to View 1")

        # Update professor presence state
        person_present = new_person_present

        # Display frame for debugging (remove for production)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Start YOLO detection in a separate thread
yolo_thread = threading.Thread(target=run_yolo_detection)
yolo_thread.start()

# Keep the main script running
while True:
    time.sleep(1)

# Clean up
driver.quit()
