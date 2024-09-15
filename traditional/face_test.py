import cv2
import face_recognition
import numpy as np


# Database of known faces and their names
known_face_encodings = []
known_face_names = []

def capture_images_from_camera(num_pictures=5):
    video_capture = cv2.VideoCapture(0)
    captured_images = []

    print("Press 'Space' to capture an image and 'q' to quit.")
    while len(captured_images) < num_pictures:
        ret, frame = video_capture.read()
        cv2.imshow('Capture Face', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):  # Space key to capture image
            print(f"Captured image {len(captured_images) + 1}")
            captured_images.append(frame)
        elif key == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return captured_images

def encode_faces(images):
    encoded_faces = []
    for image in images:
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        if face_encodings:
            encoded_faces.append(face_encodings[0])  # Take the first face encoding found
    return encoded_faces

def add_new_face_to_database():
    # Capture images of the new person
    images = capture_images_from_camera(num_pictures=5)
    new_face_encodings = encode_faces(images)

    if new_face_encodings:
        name = input("Enter the name for this person: ")
        known_face_encodings.append(new_face_encodings[0])  # Add encoding to the database
        known_face_names.append(name)  # Add name to the database
        print(f"{name} has been added to the database.")

def recognize_faces_in_real_time():
    video_capture = cv2.VideoCapture(0)

    print("Press 'q' to quit.")
    
    while True:
        ret, frame = video_capture.read()
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            
            if matches:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

            # If the face is unknown, capture and request name for the new face
            if name == "Unknown":
                print("Unknown face detected, capturing images to add to the database.")
                add_new_face_to_database()
                break

            # Display the name and bounding box on the video feed
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    
    
# Run the face recognition pipeline
recognize_faces_in_real_time()
