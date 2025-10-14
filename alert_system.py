import os
import cv2
import time
from datetime import datetime
import config

def capture_alert_images(frame, face_location):
    """
    Crops an unknown face, saves a burst of images, and returns the filenames.
    """
    os.makedirs(config.ALERT_FOLDER, exist_ok=True)
    
    # --- NEW: Create a list to store the filenames ---
    saved_filenames = []

    top, right, bottom, left = face_location
    top = max(0, top - 20)
    left = max(0, left - 20)
    bottom = min(frame.shape[0], bottom + 20)
    right = min(frame.shape[1], right + 20)
    cropped_face = frame[top:bottom, left:right]

    print(f"   -> Starting image capture...")
    for i in range(config.IMAGES_TO_CAPTURE):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        filename = os.path.join(config.ALERT_FOLDER, f'alert_{timestamp}.jpg')
        cv2.imwrite(filename, cropped_face)
        
        # --- NEW: Add the saved filename to our list ---
        saved_filenames.append(filename)
        
        time.sleep(config.CAPTURE_DELAY_SECONDS)

    print(f"   -> Finished saving {config.IMAGES_TO_CAPTURE} images.")
    
    # --- NEW: Return the list of filenames ---
    return saved_filenames