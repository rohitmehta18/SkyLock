import cv2
import face_recognition
import numpy as np
import os


KNOWN_FACES_DIR = 'known_faces'

TOLERANCE = 0.6
MATCH_COLOR = (0, 255, 0)  
UNKNOWN_COLOR = (0, 0, 255) 
TEXT_COLOR = (255, 255, 255) 

def load_known_faces():
    """
    Loads face encodings and names from the 'known_faces' directory.
    """
    known_face_encodings = []
    known_face_names = []
    print("Loading known faces...")

    # Check if the directory exists
    if not os.path.isdir(KNOWN_FACES_DIR):
        print(f"Error: The directory '{KNOWN_FACES_DIR}' was not found.")
        print("Please create it and add images of known people.")
        return None, None

    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                image_path = os.path.join(KNOWN_FACES_DIR, filename)
                image = face_recognition.load_image_file(image_path)

                encodings = face_recognition.face_encodings(image)
                
                if encodings:
            
                    known_face_encodings.append(encodings[0])
                    
                    known_face_names.append(os.path.splitext(filename)[0])
                    print(f"Loaded face for: {os.path.splitext(filename)[0]}")
                else:
                    print(f"Warning: No faces found in {filename}. Skipping.")
            
            except Exception as e:
                print(f"Error loading {filename}: {e}")

    if not known_face_names:
        print("Error: No known faces were loaded. Is the 'known_faces' directory empty or are the images unreadable?")
        
    return known_face_encodings, known_face_names

def main():
    """
    Main function to run the face recognition application.
    """
    known_face_encodings, known_face_names = load_known_faces()

   
    if not known_face_encodings:
        return

    print("Starting video stream... Press 'q' to quit.")
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Error: Could not open video stream.")
        return

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

      
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, TOLERANCE)
            name = "Unknown"
            color = UNKNOWN_COLOR


            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                color = MATCH_COLOR

     
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name.replace("_", " ").title(), (left + 6, bottom - 6), font, 1.0, TEXT_COLOR, 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    print("Application closed.")

if __name__ == "__main__":
    main()