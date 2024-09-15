import cv2
import os
import time
import numpy as np
from deepface import DeepFace
from sklearn.metrics.pairwise import cosine_similarity

# Constants
DATABASE_FOLDER = "face_database"
DETECTION_INTERVAL = 0.5  # seconds
IMAGES_PER_FACE = 10
SIMILARITY_THRESHOLD = 0.8  # Adjust this value as needed

# Ensure database folder exists
os.makedirs(DATABASE_FOLDER, exist_ok=True)

models = ["Facenet512"]

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

def get_embedding(face_img):
    try:
        embedding = DeepFace.represent(face_img, model_name=models[0], enforce_detection=False)
        return embedding
    except Exception as e:
        print(f"Error in getting embedding: {str(e)}")
        return None

def search_face_in_database(embedding):
    try:
        database_embeddings = []
        database_identities = []
        for filename in os.listdir(DATABASE_FOLDER):
            if filename.endswith(".jpg"):
                identity = filename.split('_')[0]
                img_path = os.path.join(DATABASE_FOLDER, filename)
                db_embedding = DeepFace.represent(img_path, model_name=models[0], enforce_detection=False)
                database_embeddings.append(db_embedding)
                database_identities.append(identity)
        
        if database_embeddings:
            similarities = cosine_similarity([embedding], database_embeddings)[0]
            max_similarity_index = np.argmax(similarities)
            max_similarity = similarities[max_similarity_index]
            if max_similarity > SIMILARITY_THRESHOLD:
                return database_identities[max_similarity_index], max_similarity
        return None, 0
    except Exception as e:
        print(f"Error in face recognition: {str(e)}")
        return None, 0

def save_face(face_img, name):
    count = len([f for f in os.listdir(DATABASE_FOLDER) if f.startswith(name)])
    filename = f"{name}_{count + 1}.jpg"
    cv2.imwrite(os.path.join(DATABASE_FOLDER, filename), face_img)

def main():
    cap = cv2.VideoCapture(0)
    face_embeddings = {}
    face_images = {}
    face_names = {}

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame")
            break

        faces = detect_and_extract_faces(frame)

        for i, face in enumerate(faces):
            face_img = frame[
                int(face['facial_area']['y']):int(face['facial_area']['y'] + face['facial_area']['h']),
                int(face['facial_area']['x']):int(face['facial_area']['x'] + face['facial_area']['w'])
            ]
            face_id = f"face_{i}"

            if face_id not in face_embeddings:
                embedding = get_embedding(face_img)
                if embedding is not None:
                    face_embeddings[face_id] = embedding
                    face_images[face_id] = []

            if face_id in face_embeddings and face_id not in face_names:
                if len(face_images[face_id]) < IMAGES_PER_FACE:
                    face_images[face_id].append(face_img)

                if len(face_images[face_id]) == IMAGES_PER_FACE:
                    identity, similarity = search_face_in_database(face_embeddings[face_id])
                    if identity and similarity > SIMILARITY_THRESHOLD:
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

                    # Clean up
                    del face_images[face_id]

            # Draw rectangle around face
            cv2.rectangle(frame, 
                (int(face['facial_area']['x']), int(face['facial_area']['y'])),
                (int(face['facial_area']['x'] + face['facial_area']['w']),
                int(face['facial_area']['y'] + face['facial_area']['h'])), 
                (0, 255, 0), 2)
            
            # Display name if available
            if face_id in face_names:
                cv2.putText(frame, face_names[face_id], 
                            (int(face['facial_area']['x']), int(face['facial_area']['y'] + face['facial_area']['h'] + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(DETECTION_INTERVAL)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()