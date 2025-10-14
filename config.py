# This file contains all the settings for the application.
# By changing them here, you can easily tweak the program's behavior.

# --- Directories ---
KNOWN_FACES_DIR = 'known_faces'
ALERT_FOLDER = 'alert_folder'

# --- Face Recognition Settings ---
# Lower is more strict. 0.6 is a good balance.
TOLERANCE = 0.6

# --- Visual Settings ---
MATCH_COLOR = (0, 255, 0)      # Green for known faces
UNKNOWN_COLOR = (0, 0, 255)    # Red for unknown faces
TEXT_COLOR = (255, 255, 255)   # White text

# ... other settings

# --- Alert System Settings ---
# Number of images to save when an unknown face is detected.
IMAGES_TO_CAPTURE = 5
# Delay in seconds between each image capture.
CAPTURE_DELAY_SECONDS = 0.2
# Cooldown in seconds before another alert can be triggered.
ALERT_COOLDOWN_SECONDS = 10.0
