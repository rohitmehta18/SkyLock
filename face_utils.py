import os
import face_recognition
import config # Import our configuration

def load_known_faces():
    """
    Loads face encodings and names from the 'known_faces' directory
    specified in the config file.
    """
    known_face_encodings = []
    known_face_names = []
    print("Loading known faces...")

    # Check if the directory exists
    if not os.path.isdir(config.KNOWN_FACES_DIR):
        print(f"Error: Directory '{config.KNOWN_FACES_DIR}' not found. Please create it.")
        return None, None

    for filename in os.listdir(config.KNOWN_FACES_DIR):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                # Build the full path to the image
                image_path = os.path.join(config.KNOWN_FACES_DIR, filename)
                
                # Load the image
                image = face_recognition.load_image_file(image_path)
                
                # Get face encodings
                encodings = face_recognition.face_encodings(image)
                
                if encodings:
                    # Add the first found encoding and name to our lists
                    known_face_encodings.append(encodings[0])
                    # The name is the filename without the extension
                    known_face_names.append(os.path.splitext(filename)[0])
                    print(f"Loaded face: {os.path.splitext(filename)[0]}")
                else:
                    print(f"Warning: No face found in {filename}. Skipping.")
            
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                
    return known_face_encodings, known_face_names
