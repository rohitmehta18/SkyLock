import pyautogui
import threading
import time
import os
from datetime import datetime
import config
from email_alert import send_screenshot_report # <-- NEW IMPORT

class ScreenshotSystem:
    def __init__(self, stop_event):
        self.is_active = False
        self.screenshot_paths = []
        self.thread = None
        self.stop_event = stop_event
        self.lock = threading.Lock()

    def _screenshot_loop(self):
        """The main loop that takes screenshots and sends them in batches."""
        while not self.stop_event.is_set():
            if self.is_active:
                try:
                    # Generate a unique filename and take screenshot
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                    filename = os.path.join(config.SCREENSHOTS_FOLDER, f'screenshot_{timestamp}.png')
                    pyautogui.screenshot(filename)
                    
                    # --- NEW BATCHING LOGIC ---
                    with self.lock:
                        self.screenshot_paths.append(filename)
                        
                        # Check if the batch is full
                        if len(self.screenshot_paths) >= config.SCREENSHOT_BATCH_SIZE:
                            paths_to_send = self.screenshot_paths
                            self.screenshot_paths = [] # Reset for the next batch
                            print(f"📸 [Screenshot] Batch of {len(paths_to_send)} collected. Sending report...")
                            # Send the email report for this batch
                            send_screenshot_report(paths_to_send)
                    
                    time.sleep(config.SCREENSHOT_INTERVAL_SECONDS)
                except Exception as e:
                    print(f"[Screenshot] Error during screenshot capture: {e}")
            else:
                time.sleep(0.5)

    def start(self):
        """Activates the screenshot capture loop."""
        with self.lock:
            if not self.is_active:
                print("📸 [Screenshot] Starting periodic screenshot capture...")
                self.is_active = True
                self.screenshot_paths = [] # Ensure list is empty for the new session

    def stop(self):
        """Deactivates the loop and returns any remaining screenshots."""
        with self.lock:
            if self.is_active:
                self.is_active = False
                remaining_paths = self.screenshot_paths
                self.screenshot_paths = [] # Clear the list
                print(f"⏹️ [Screenshot] Stopping. Collected {len(remaining_paths)} final images.")
                return remaining_paths
            return []

    def start_thread(self):
        """Starts the background thread."""
        if self.thread is None:
            os.makedirs(config.SCREENSHOTS_FOLDER, exist_ok=True)
            self.thread = threading.Thread(target=self._screenshot_loop)
            self.thread.start()
            print("[Screenshot] Background thread started.")

    def join_thread(self):
        """Waits for the background thread to finish."""
        if self.thread and self.thread.is_alive():
            self.thread.join()
            print("[Screenshot] Background thread stopped.")