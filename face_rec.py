import cv2
import os
from deepface import DeepFace
import time

# Constants
DATABASE_FOLDER = "face_database"
TEMP_FOLDER = "temp_faces"
MODEL_NAME = "Facenet512"
UNKNOWN_FACE_THRESHOLD = 5
UNKNOWN_FACE_IMAGES = 10
MAX_IMAGES_PER_PERSON = 10

def get_name_from_path(path):
    filename = os.path.basename(path)
    name = filename.split('_')[0]  # Get only the part before the first underscore
    return name

def count_person_images(folder, name):
    return len([f for f in os.listdir(folder) if f.startswith(name)])

def save_image(folder, name, frame):
    if not os.path.exists(folder):
        os.makedirs(folder)
    count = count_person_images(folder, name)
    filename = f"{name}_{count + 1}.jpg"
    cv2.imwrite(os.path.join(folder, filename), frame)

def add_to_database(temp_folder, name, database_folder):
    if not os.path.exists(database_folder):
        os.makedirs(database_folder)
    for filename in os.listdir(temp_folder):
        if filename.startswith(f"unknown_"):
            old_path = os.path.join(temp_folder, filename)
            new_filename = f"{name}_{count_person_images(database_folder, name) + 1}.jpg"
            new_path = os.path.join(database_folder, new_filename)
            os.rename(old_path, new_path)

def main():
    cap = cv2.VideoCapture(1)
    time.sleep(5)
    unknown_face_count = 0
    last_unknown_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        face_objs = DeepFace.extract_faces(
            img_path=frame,
            detector_backend="opencv",
            align=True,
            enforce_detection=False
        )

        if face_objs:
            results = DeepFace.find(
                img_path=frame,
                db_path=DATABASE_FOLDER,
                model_name=MODEL_NAME,
                enforce_detection=False
            )

            if len(results) > 0 and len(results[0]) > 0:
                identity = results[0]['identity'][0]
                name = get_name_from_path(identity)
                image_count = count_person_images(DATABASE_FOLDER, name)

                if image_count < MAX_IMAGES_PER_PERSON:
                    save_image(DATABASE_FOLDER, name, frame)

                for face in face_objs:
                    cv2.rectangle(frame, 
                        (int(face['facial_area']['x']), int(face['facial_area']['y'])),
                        (int(face['facial_area']['x'] + face['facial_area']['w']),
                        int(face['facial_area']['y'] + face['facial_area']['h'])), 
                        (0, 255, 0), 2)
                    cv2.putText(frame, name, 
                                (int(face['facial_area']['x']), int(face['facial_area']['y'] + face['facial_area']['h'] + 20)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                unknown_face_count = 0
            else:
                unknown_face_count += 1
                if unknown_face_count > UNKNOWN_FACE_THRESHOLD:
                    current_time = time.time()
                    if current_time - last_unknown_time > 1:  # Capture every second
                        save_image(TEMP_FOLDER, f"unknown", frame)
                        last_unknown_time = current_time
                        
                        if unknown_face_count == UNKNOWN_FACE_IMAGES + UNKNOWN_FACE_THRESHOLD:
                            cap.release()
                            cv2.destroyAllWindows()
                            name = input("New face detected. Please enter the name: ")
                            add_to_database(TEMP_FOLDER, name, DATABASE_FOLDER)
                            unknown_face_count = 0
                            cap = cv2.VideoCapture(0)

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()