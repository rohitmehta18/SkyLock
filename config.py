import os
from dotenv import load_dotenv

load_dotenv()

# --- Directories ---
KNOWN_FACES_DIR = 'known_faces'
ALERT_FOLDER = 'alert_folder'
SCREENSHOTS_FOLDER = 'screenshots'

# --- Face Recognition Settings ---
TOLERANCE = 0.6

# --- Visual Settings ---
MATCH_COLOR = (0, 255, 0)
UNKNOWN_COLOR = (0, 0, 255)
TEXT_COLOR = (255, 255, 255)

# --- Alert System Settings ---
IMAGES_TO_CAPTURE = 5
CAPTURE_DELAY_SECONDS = 0.2
SCREENSHOT_INTERVAL_SECONDS = 2
SCREENSHOT_BATCH_SIZE = 10  # <-- NEW: Number of screenshots to collect before sending an email

# --- Email Alert Settings (Loaded from .env file) ---
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

# --- Remote Lock Settings ---
LOCK_COMMAND_WORD = "off"
EMAIL_CHECK_INTERVAL_SECONDS = 30