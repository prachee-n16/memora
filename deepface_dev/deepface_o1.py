import cv2
import os
import time
from deepface import DeepFace
from collections import Counter

# Constants
DATABASE_FOLDER = "face_database"
TEMP_FOLDER = "temp_faces"
DETECTION_INTERVAL = 0.5  # seconds
IMAGES_PER_FACE = 10
RECOGNITION_THRESHOLD = 3  # Minimum number of matches to consider a recognition

# Ensure database and temp folders exist
os.makedirs(DATABASE_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

models = ["Facenet512"]

def detect_faces(frame):
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

def recognize_face(face_img):
    try:
        results = DeepFace.find(
            img_path=face_img,
            db_path=DATABASE_FOLDER,
            model_name=models[0],
            enforce_detection=False
        )
        if results and len(results[0]) > 0:
            identities = [os.path.basename(result).split('_')[0] for result in results[0]['identity']]
            most_common = Counter(identities).most_common(1)
            if most_common and most_common[0][1] >= RECOGNITION_THRESHOLD:
                return most_common[0][0]
        return None
    except Exception as e:
        print(f"Error in face recognition: {str(e)}")
        return None

def save_face(face_img, name):
    count = len([f for f in os.listdir(DATABASE_FOLDER) if f.startswith(name)])
    filename = f"{name}_{count + 1}.jpg"
    cv2.imwrite(os.path.join(DATABASE_FOLDER, filename), face_img)

def save_temp_face(face_img, face_id, count):
    filename = f"{face_id}_{count}.jpg"
    cv2.imwrite(os.path.join(TEMP_FOLDER, filename), face_img)

def main():
    cap = cv2.VideoCapture(0)
    face_images = {}
    face_names = {}

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        faces = detect_faces(frame)

        for i, face in enumerate(faces):
            x = int(face['facial_area']['x'])
            y = int(face['facial_area']['y'])
            w = int(face['facial_area']['w'])
            h = int(face['facial_area']['h'])
            
            face_img = frame[y:y+h, x:x+w]
            face_id = f"face_{i}"

            if face_id not in face_names:
                if face_id not in face_images:
                    face_images[face_id] = []

                if len(face_images[face_id]) < IMAGES_PER_FACE:
                    face_images[face_id].append(face_img)
                    save_temp_face(face_img, face_id, len(face_images[face_id]))

                if len(face_images[face_id]) == IMAGES_PER_FACE:
                    identity = recognize_face(face_images[face_id][-1])
                    if identity:
                        print(f"Recognized: {identity}")
                        face_names[face_id] = identity
                    else:
                        name = input("New face detected. Enter first name: ")
                        last_name = input("Enter last name (optional): ")
                        full_name = f"{name}_{last_name}" if last_name else name
                        for temp_face in face_images[face_id]:
                            save_face(temp_face, full_name)
                        print(f"Saved new face: {full_name}")
                        face_names[face_id] = name

                    # Clean up temp files
                    for f in os.listdir(TEMP_FOLDER):
                        if f.startswith(face_id):
                            os.remove(os.path.join(TEMP_FOLDER, f))
                    del face_images[face_id]

            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Display name if available
            if face_id in face_names:
                cv2.putText(frame, face_names[face_id], 
                            (x, y + h + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(DETECTION_INTERVAL)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()