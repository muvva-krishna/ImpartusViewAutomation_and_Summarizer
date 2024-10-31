import cv2
import numpy as np
import time

def capture_frame(driver, interval=60):#every 1 minute
    while True:
       
        screenshot = driver.get_screenshot_as_png()
        
        # Convert screenshot to OpenCV format
        frame = np.frombuffer(screenshot, dtype=np.uint8)# each element in an array should be 8bit -unsigned int(std format for image data)
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        
        # Yield the frame for further processing
        yield frame # use yield instead of return
        
        # Wait for the specified interval
        time.sleep(interval)
