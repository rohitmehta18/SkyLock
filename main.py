import cv2
import face_recognition
import numpy as np
import time

# Import our custom modules
import config
from face_utils import load_known_faces
from alert_system import capture_alert_images

def run_surveillance():
    """
    Main function to run the intelligent face recognition and alert system.
    """
    known_face_encodings, known_face_names = load_known_faces()

    if known_face_names is not None and not known_face_names:
        print("Exiting: No known faces loaded. Check the 'known_faces' directory.")
        return

    print("\nStarting video stream... Press 'q' to quit.")
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Error: Could not open video stream.")
        return

    # This list will store encodings of unknown faces we've already captured
    unknown_faces_recorded = []

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Find all faces and their encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            name = "Unknown"
            color = config.UNKNOWN_COLOR

            # Check for matches against known faces
            if known_face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, config.TOLERANCE)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    color = config.MATCH_COLOR

            # If the face is unknown, check if we've already recorded it.
            if name == "Unknown":
                is_new_unknown_face = True
                
                if unknown_faces_recorded:
                    matches = face_recognition.compare_faces(unknown_faces_recorded, face_encoding, config.TOLERANCE)
                    if True in matches:
                        is_new_unknown_face = False
                
                if is_new_unknown_face:
                    unknown_faces_recorded.append(face_encoding)
                    print(f"🚨 ALERT: New unknown face detected! Capturing {config.IMAGES_TO_CAPTURE} images.")
                    capture_alert_images(frame, face_location)

            # --- Draw visuals on the frame ---
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            
            # --- THIS IS THE CORRECTED LINE ---
            font = cv2.FONT_HERSHEY_DUPLEX 
            
            cv2.putText(frame, name.replace("_", " ").title(), (left + 6, bottom - 6), font, 1.0, config.TEXT_COLOR, 1)

        # Display the final frame
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    print("Application closed.")

if __name__ == "__main__":
    run_surveillance()

