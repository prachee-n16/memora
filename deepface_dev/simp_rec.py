import cv2
import os
from deepface import DeepFace

# Constants
DATABASE_FOLDER = "face_database"
MODEL_NAME = "Facenet512"

def get_name_from_path(path):
    # Extract name from the path (e.g., "face_database/steven.jpg" -> "steven")
    filename = os.path.basename(path)  # Get the filename from the path
    name, _ = os.path.splitext(filename)  # Split the filename and extension
    return name

def main():
    # Initialize video capture
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Extract faces from the frame
        face_objs = DeepFace.extract_faces(
            img_path=frame,
            detector_backend="opencv",
            align=True,
            enforce_detection=False
        )

        if face_objs:  # Only perform recognition if faces are detected
            # Search for faces in the database using the whole frame
            results = DeepFace.find(
                img_path=frame,
                db_path=DATABASE_FOLDER,
                model_name=MODEL_NAME,
                enforce_detection=False
            )

            if len(results) > 0 and len(results[0]) > 0:
                # Get the identity of the closest match
                identity = results[0]['identity'][0]
                name = get_name_from_path(identity)

                # Draw rectangle and name on the frame for each detected face
                for face in face_objs:
                    # Draw rectangle around face
                    cv2.rectangle(frame, 
                        (int(face['facial_area']['x']), int(face['facial_area']['y'])),
                        (int(face['facial_area']['x'] + face['facial_area']['w']),
                        int(face['facial_area']['y'] + face['facial_area']['h'])), 
                        (0, 255, 0), 2)
                    
                    # Display name
                    cv2.putText(frame, name, 
                                (int(face['facial_area']['x']), int(face['facial_area']['y'] + face['facial_area']['h'] + 20)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Face Recognition', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and destroy windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()