import cv2
import face_recognition
import numpy as np
import threading
import time

# Import our custom modules
import config
from face_utils import load_known_faces
from alert_system import capture_alert_images
from email_alert import send_email_with_alert
from email_checker import check_email_for_lock_command # <-- This import was missing

def run_surveillance():
    """
    Main function to run face recognition, alerts, and the remote lock listener.
    """
    known_face_encodings, known_face_names = load_known_faces()

    if known_face_names is not None and not known_face_names:
        print("Exiting: No known faces loaded.")
        return

    # --- NEW: Setup for the background email-checking thread ---
    stop_event = threading.Event()
    email_thread = threading.Thread(
        target=check_email_for_lock_command,
        args=(stop_event,)
    )
    email_thread.start()
    
    print("\nStarting video stream... Press 'q' to quit.")
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Error: Could not open video stream.")
        stop_event.set() # Stop the email thread before exiting
        email_thread.join()
        return

    unknown_faces_recorded = []

    try:
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            # Face detection and recognition logic
            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                name = "Unknown"
                color = config.UNKNOWN_COLOR

                if known_face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, config.TOLERANCE)
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        color = config.MATCH_COLOR

                if name == "Unknown":
                    is_new_unknown_face = True
                    if unknown_faces_recorded:
                        matches = face_recognition.compare_faces(unknown_faces_recorded, face_encoding, config.TOLERANCE)
                        if True in matches:
                            is_new_unknown_face = False
                    
                    if is_new_unknown_face:
                        unknown_faces_recorded.append(face_encoding)
                        print(f"🚨 ALERT: New unknown face detected!")
                        saved_images = capture_alert_images(frame, face_location)
                        send_email_with_alert(saved_images)

                # Draw visuals on the frame
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name.replace("_", " ").title(), (left + 6, bottom - 6), font, 1.0, config.TEXT_COLOR, 1)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # --- NEW: Gracefully stop the background thread on exit ---
        print("\nStopping application...")
        stop_event.set()
        email_thread.join() # Wait for the email thread to finish completely
        video_capture.release()
        cv2.destroyAllWindows()
        print("Application closed.")

if __name__ == "__main__":
    run_surveillance()

