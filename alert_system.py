import os
import cv2
import time
from datetime import datetime
import config # Import our configuration

def capture_alert_images(frame, face_location):
    """
    Crops an unknown face and saves exactly the number of images specified
    in the config file.
    """
    os.makedirs(config.ALERT_FOLDER, exist_ok=True)

    top, right, bottom, left = face_location
    top = max(0, top - 20)
    left = max(0, left - 20)
    bottom = min(frame.shape[0], bottom + 20)
    right = min(frame.shape[1], right + 20)
    cropped_face = frame[top:bottom, left:right]

    # --- UPDATED: Explicitly loops to capture the set number of images ---
    print(f"   -> Starting image capture...")
    for i in range(config.IMAGES_TO_CAPTURE):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        filename = os.path.join(config.ALERT_FOLDER, f'alert_{timestamp}.jpg')
        cv2.imwrite(filename, cropped_face)
        # Brief pause to get slightly different shots
        time.sleep(config.CAPTURE_DELAY_SECONDS)

    print(f"   -> Finished saving {config.IMAGES_TO_CAPTURE} images to '{config.ALERT_FOLDER}'. Entering cooldown.")