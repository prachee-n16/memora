import cv2
import numpy as np
import mediapipe as mp
from sklearn.metrics.pairwise import cosine_similarity
import warnings

# Suppress the specific warning for protobuf
warnings.filterwarnings("ignore", message="SymbolDatabase.GetPrototype() is deprecated")

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
face_embed_size = 468  # Number of face landmarks in MediaPipe

# Database for face embeddings and names
stored_embeddings = []
stored_names = []

def capture_frame(cam_index=0):
    cap = cv2.VideoCapture(cam_index)
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None

def extract_face_embedding(image):
    # Convert the image to RGB as MediaPipe requires
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = mp_face_mesh.process(rgb_image)

    if result.multi_face_landmarks:
        face_landmarks = result.multi_face_landmarks[0]
        # Extract the (x, y, z) coordinates of all landmarks
        embedding = np.array([(lm.x, lm.y, lm.z) for lm in face_landmarks.landmark])
        return embedding.flatten()  # Flatten the 3D landmarks into a single vector
    return None

def find_most_similar(new_embedding):
    if len(stored_embeddings) == 0:
        return None, None
    # Compute cosine similarity between the new embedding and stored embeddings
    similarities = cosine_similarity([new_embedding], stored_embeddings)
    best_match_index = np.argmax(similarities)
    return best_match_index, similarities[0][best_match_index]

def add_new_face(embedding):
    name = input("Unknown face detected! Please enter a name: ")
    stored_embeddings.append(embedding)
    stored_names.append(name)
    print(f"New face stored for {name}")

# Main loop for continuous face detection
def run_face_recognition():
    print("Starting face recognition...")

    # Open webcam
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        # Extract face embedding from the frame
        embedding = extract_face_embedding(frame)
        
        if embedding is not None:
            # Check if the face is already in the database
            index, similarity = find_most_similar(embedding)
            
            if similarity is None or similarity < 0.85:  # Threshold for recognizing faces
                add_new_face(embedding)
            else:
                print(f"Face recognized: {stored_names[index]} (Similarity: {similarity:.4f})")
        
        # Show the frame with detection
        cv2.imshow("Face Recognition", frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

# Run the face recognition system
run_face_recognition()
