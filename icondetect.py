import cv2
import numpy as np
from PIL import Image

def detect_icons(img, templates, threshold=0.8):
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img_gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    icon_detected = False
    for template in templates:
        template_cv = cv2.cvtColor(np.array(template), cv2.COLOR_RGB2BGR)
        template_gray = cv2.cvtColor(template_cv, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)#2d arraay
        locations = np.where(result >= threshold)#tuple that has the tuple of arrays
        if len(locations[0]) > 0: # if the first array exists icon is detected
            icon_detected = True
            break
    return icon_detected