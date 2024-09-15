import cv2
import os
import time
import numpy as np
from deepface import DeepFace

# Constants
TEMP_FOLDER = "temp_faces"
DATABASE_FOLDER = "database"
DETECTION_INTERVAL = 0.5  # seconds
RECOGNITION_THRESHOLD = 10  # seconds
IMAGES_PER_FACE = 10

# Ensure temp and database folders exist
os.makedirs(TEMP_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)

models = [
  "Facenet512", 
]

def detect_and_extract_faces(frame):
    try:
        face_objs = DeepFace.extract_faces(
            img_path=frame,
            detector_backend="opencv",
            align=True,
            enforce_detection=False
        )
        return face_objs
    except Exception as e:
        print(f"Error in face detection: {str(e)}")
        return []

def search_face_in_database(face_img):
    try:
        result = DeepFace.find(
            img_path=face_img,
            db_path=DATABASE_FOLDER,
            model_name = models[0],
            enforce_detection=False
        )
        if len(result) > 0 and len(result[0]) > 0:
            identity = os.path.basename(result[0]['identity']).split('_')[0]
            return identity
        return None
    except Exception as e:
        print(f"Error in face recognition: {str(e)}")
        return None

def save_face(face_img, name):
    os.makedirs(os.path.join(DATABASE_FOLDER, name), exist_ok=True)
    count = len(os.listdir(os.path.join(DATABASE_FOLDER, name)))
    filename = f"{name}_{count + 1}.jpg"
    cv2.imwrite(os.path.join(DATABASE_FOLDER, name, filename), face_img)

def main():
    cap = cv2.VideoCapture(0)
    face_time = {}
    temp_faces = {}

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        faces = detect_and_extract_faces(frame)

        current_time = time.time()

        for i, face in enumerate(faces):
            face_img = face['face']
            face_id = f"face_{i}"

            if face_id not in face_time:
                face_time[face_id] = current_time
                temp_faces[face_id] = []

            if current_time - face_time[face_id] >= RECOGNITION_THRESHOLD:
                if len(temp_faces[face_id]) < IMAGES_PER_FACE:
                    temp_faces[face_id].append(face_img)

                if len(temp_faces[face_id]) == IMAGES_PER_FACE:
                    identity = search_face_in_database(face_img)
                    if identity:
                        print(f"Recognized: {identity}")
                    else:
                        name = input("New face detected. Enter first name: ")
                        last_name = input("Enter last name (optional): ")
                        full_name = f"{name}_{last_name}" if last_name else name
                        for temp_face in temp_faces[face_id]:
                            save_face(temp_face, full_name)
                        print(f"Saved new face: {full_name}")
                    
                    # Reset for this face
                    del face_time[face_id]
                    del temp_faces[face_id]

            # Draw rectangle around face
            cv2.rectangle(frame, (int(face['facial_area']['x']), int(face['facial_area']['y'])),
                          (int(face['facial_area']['x'] + face['facial_area']['w']),
                           int(face['facial_area']['y'] + face['facial_area']['h'])), (0, 255, 0), 2)

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(DETECTION_INTERVAL)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()