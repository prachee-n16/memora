import cv2
import numpy as np
from mtcnn import MTCNN
from keras_facenet import FaceNet
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import time

# Suppress the protobuf deprecation warning
warnings.filterwarnings("ignore", message="SymbolDatabase.GetPrototype() is deprecated")

# Initialize MTCNN for face detection and FaceNet for embeddings
detector = MTCNN()
embedder = FaceNet()

# Database for face embeddings and names
stored_embeddings = []
stored_names = []

# Function to capture frame
def capture_frame(cam_index=0):
    cap = cv2.VideoCapture(cam_index)
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None

# Align face based on detected landmarks (for accuracy improvement)
def align_face(image, box):
    x, y, w, h = box
    face = image[y:y+h, x:x+w]
    return face

# Extract face embeddings using FaceNet
def extract_face_embedding(image):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    detection = detector.detect_faces(rgb_image)
    
    if len(detection) > 0:
        # Get the bounding box and key points of the first detected face
        box = detection[0]['box']
        aligned_face = align_face(rgb_image, box)
        
        # Extract FaceNet embedding
        embedding = embedder.embeddings([aligned_face])[0]
        return embedding
    return None

# Find the most similar embedding from stored embeddings
def find_most_similar(new_embedding):
    if len(stored_embeddings) == 0:
        return None, None
    # Compute cosine similarity between the new embedding and stored embeddings
    similarities = cosine_similarity([new_embedding], stored_embeddings)
    best_match_index = np.argmax(similarities)
    return best_match_index, similarities[0][best_match_index]

# Add new face embedding with name
def add_new_face(embedding):
    name = input("Unknown face detected! Please enter a name: ")
    stored_embeddings.append(embedding)
    stored_names.append(name)
    print(f"New face stored for {name}")

# Main loop for continuous face detection and recognition
def run_face_recognition():
    print("Starting face recognition...")

    # Open webcam
    cap = cv2.VideoCapture(0)

    while True:
        start_time = time.time()  # Measure frame processing time
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        # Extract face embedding from the frame
        embedding = extract_face_embedding(frame)

        if embedding is not None:
            # Check if the face is already in the database
            index, similarity = find_most_similar(embedding)
            
            if similarity is None or similarity < 0.90:  # Threshold for recognizing faces
                add_new_face(embedding)
            else:
                print(f"Face recognized: {stored_names[index]} (Similarity: {similarity:.4f})")
        
        # Calculate the time taken per frame
        frame_time = time.time() - start_time
        print(f"Frame processed in {frame_time:.4f} seconds")

        # Display the video feed
        cv2.imshow("Face Recognition", frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

# Run the face recognition system
run_face_recognition()
