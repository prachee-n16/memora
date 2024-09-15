import cv2
import numpy as np
import mediapipe as mp
from sklearn.metrics.pairwise import cosine_similarity
import warnings
from scipy.spatial import distance
import time
import os
from PIL import Image

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Initialize LBPH face recognizer
lbph_recognizer = cv2.face.LBPHFaceRecognizer_create()
lbph_trained = False  # Flag to check if LBPH has been trained

# Database for face embeddings and names
stored_embeddings = []
stored_names = []

def extract_face_embedding(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = mp_face_mesh.process(rgb_image)

    if result.multi_face_landmarks:
        face_landmarks = result.multi_face_landmarks[0]
        embedding = np.array([(lm.x, lm.y, lm.z) for lm in face_landmarks.landmark])
        
        # Normalize the embedding
        embedding = embedding - np.mean(embedding, axis=0)
        embedding = embedding / np.linalg.norm(embedding)
        
        return embedding.flatten()
    return None

def find_most_similar(new_embedding):
    if len(stored_embeddings) == 0:
        return None, None
    
    new_embedding_2d = new_embedding.reshape(1, -1)
    similarities = [cosine_similarity(new_embedding_2d, emb.reshape(1, -1))[0][0] for emb in stored_embeddings]
    distances = [distance.euclidean(new_embedding, emb) for emb in stored_embeddings]
    
    combined_scores = np.array(similarities) / (1 + np.array(distances))
    best_match_index = np.argmax(combined_scores)
    return best_match_index, combined_scores[best_match_index]

def capture_multiple_angles(cap, num_images=5, delay=2):
    embeddings = []
    images = []
    for i in range(num_images):
        print(f"Capturing image {i+1}/{num_images}. Please change your pose slightly.")
        time.sleep(delay)
        
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            continue

        embedding = extract_face_embedding(frame)
        if embedding is not None:
            embeddings.append(embedding)
            images.append(frame)
        
        cv2.imshow("Capture", frame)
        cv2.waitKey(1)

    cv2.destroyWindow("Capture")
    return embeddings, images

def train_lbph(images, label):
    global lbph_trained
    gray_images = [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in images]
    lbph_recognizer.train(gray_images, np.array([label] * len(images)))
    lbph_trained = True

def add_new_face(cap):
    global lbph_trained
    name = input("New face detected! Please enter a name: ")
    print("We'll now capture multiple angles of your face.")
    embeddings, images = capture_multiple_angles(cap)
    
    if len(embeddings) > 0:
        average_embedding = np.mean(embeddings, axis=0)
        stored_embeddings.append(average_embedding)
        stored_names.append(name)
        
        # Train LBPH recognizer
        label = len(stored_names) - 1
        train_lbph(images, label)
        
        print(f"New face stored for {name} using {len(embeddings)} images.")
    else:
        print("Failed to capture any valid face embeddings. Please try again.")

def run_face_recognition():
    print("Starting face recognition...")
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        embedding = extract_face_embedding(frame)
        
        if embedding is not None:
            # MediaPipe-based recognition
            index, score = find_most_similar(embedding)
            
            # LBPH-based recognition (only if trained)
            lbph_confidence = None
            if lbph_trained:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                label, confidence = lbph_recognizer.predict(gray)
                lbph_confidence = max(0, min(100 - confidence, 100))
            
            if score is None or score < 0.6 or (lbph_trained and lbph_confidence < 30):  # Adjusted thresholds
                add_new_face(cap)
            else:
                mp_confidence = min(score * 100, 100)
                if lbph_confidence is not None:
                    avg_confidence = (mp_confidence + lbph_confidence) / 2
                    print(f"Face recognized: {stored_names[index]} (Confidence: {avg_confidence:.2f}%)")
                else:
                    print(f"Face recognized: {stored_names[index]} (MediaPipe Confidence: {mp_confidence:.2f}%)")
        
        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the face recognition system
run_face_recognition()