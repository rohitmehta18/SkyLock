import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Directories ---
KNOWN_FACES_DIR = 'known_faces'
ALERT_FOLDER = 'alert_folder'

# --- Face Recognition Settings ---
TOLERANCE = 0.6

# --- Visual Settings ---
MATCH_COLOR = (0, 255, 0)
UNKNOWN_COLOR = (0, 0, 255)
TEXT_COLOR = (255, 255, 255)

# --- Alert System Settings ---
IMAGES_TO_CAPTURE = 5
CAPTURE_DELAY_SECONDS = 0.2

# --- Email Alert Settings (Loaded from .env file) ---
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

# --- Remote Lock Settings ---
LOCK_COMMAND_WORD = "OFF"
EMAIL_CHECK_INTERVAL_SECONDS = 30