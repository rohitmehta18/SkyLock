import cv2
import face_recognition
import numpy as np
import threading
import time

# Import our custom modules
import config
from face_utils import load_known_faces
from alert_system import capture_alert_images
from email_alert import send_email_with_alert, send_screenshot_report
from email_checker import check_email_for_lock_command
from screenshot_system import ScreenshotSystem
from lock_detector import monitor_lock_state # <-- NEW IMPORT

def run_surveillance():
    known_face_encodings, known_face_names = load_known_faces()

    if known_face_names is None: return

    # --- Setup for background threads ---
    stop_event = threading.Event()
    email_thread = threading.Thread(target=check_email_for_lock_command, args=(stop_event,))
    screenshot_system = ScreenshotSystem(stop_event)
    lock_detector_thread = threading.Thread(target=monitor_lock_state, args=(stop_event,)) # <-- NEW THREAD
    
    email_thread.start()
    screenshot_system.start_thread()
    lock_detector_thread.start() # <-- START THE NEW THREAD
    
    print("\nStarting video stream... Press 'q' to quit.")
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Error: Could not open video stream.")
        stop_event.set()
        email_thread.join()
        screenshot_system.join_thread()
        lock_detector_thread.join() # <-- Make sure to join it on exit
        return

    unknown_faces_recorded = []

    try:
        # --- UPDATED: The main loop now checks for the stop_event ---
        # This allows the lock detector to shut down the program remotely.
        while not stop_event.is_set():
            ret, frame = video_capture.read()
            if not ret: 
                print("Error: Could not read frame from camera.")
                break

            # --- (The entire face detection and screenshot logic below remains exactly the same) ---
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            a_known_face_is_visible = False

            for face_encoding, face_location in zip(face_encodings, face_locations):
                name = "Unknown"
                color = config.UNKNOWN_COLOR

                if known_face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, config.TOLERANCE)
                    if True in matches:
                        best_match_index = np.argmin(face_recognition.face_distance(known_face_encodings, face_encoding))
                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]
                            color = config.MATCH_COLOR
                            a_known_face_is_visible = True
                
                if name == "Unknown" and not screenshot_system.is_active:
                    is_new_unknown_face = True
                    if unknown_faces_recorded:
                        matches = face_recognition.compare_faces(unknown_faces_recorded, face_encoding, config.TOLERANCE)
                        if True in matches: is_new_unknown_face = False
                    
                    if is_new_unknown_face:
                        unknown_faces_recorded.append(face_encoding)
                        print(f"🚨 ALERT: New unknown face detected!")
                        saved_images = capture_alert_images(frame, face_location)
                        send_email_with_alert(saved_images)
                        screenshot_system.start()

                # Draw visuals
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name.replace("_", " ").title(), (left + 6, bottom - 6), font, 1.0, config.TEXT_COLOR, 1)

            if a_known_face_is_visible and screenshot_system.is_active:
                screenshots = screenshot_system.stop()
                send_screenshot_report(screenshots)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'): 
                break
    
    except KeyboardInterrupt:
        print("\nCtrl+C detected. Initiating graceful shutdown...")

    finally:
        print("\nStopping application...")
        stop_event.set()
        
        if screenshot_system.is_active:
            screenshots = screenshot_system.stop()
            send_screenshot_report(screenshots)
            
        screenshot_system.join_thread()
        email_thread.join()
        lock_detector_thread.join() # <-- Make sure to join it on exit
        video_capture.release()
        cv2.destroyAllWindows()
        print("Application closed.")

if __name__ == "__main__":
    run_surveillance()