import cv2
import os
from deepface import DeepFace
import time
import asyncio

class FaceRecognition:
    def __init__(self, database_folder="face_database", temp_folder="temp_faces", model_name="Facenet512"):
        self.DATABASE_FOLDER = database_folder
        self.TEMP_FOLDER = temp_folder
        self.MODEL_NAME = model_name
        self.UNKNOWN_FACE_THRESHOLD = 5
        self.UNKNOWN_FACE_IMAGES = 10
        self.MAX_IMAGES_PER_PERSON = 10
        self.unknown_face_count = 0
        self.last_unknown_time = 0

        if not os.path.exists(self.DATABASE_FOLDER):
            os.makedirs(self.DATABASE_FOLDER)
        if not os.path.exists(self.TEMP_FOLDER):
            os.makedirs(self.TEMP_FOLDER)

    def get_name_from_path(self, path):
        filename = os.path.basename(path)
        name = filename.split('_')[0]
        return name

    def count_person_images(self, folder, name):
        return len([f for f in os.listdir(folder) if f.startswith(name)])

    def save_image(self, folder, name, frame):
        count = self.count_person_images(folder, name)
        filename = f"{name}_{count + 1}.jpg"
        cv2.imwrite(os.path.join(folder, filename), frame)

    def add_to_database(self, name):
        for filename in os.listdir(self.TEMP_FOLDER):
            if filename.startswith(f"unknown_"):
                old_path = os.path.join(self.TEMP_FOLDER, filename)
                new_filename = f"{name}_{self.count_person_images(self.DATABASE_FOLDER, name) + 1}.jpg"
                new_path = os.path.join(self.DATABASE_FOLDER, new_filename)
                os.rename(old_path, new_path)

    async def process_image(self, frame):
        face_objs = DeepFace.extract_faces(
            img_path=frame,
            detector_backend="opencv",
            align=True,
            enforce_detection=False
        )

        if face_objs:
            results = DeepFace.find(
                img_path=frame,
                db_path=self.DATABASE_FOLDER,
                model_name=self.MODEL_NAME,
                enforce_detection=False
            )

            if len(results) > 0 and len(results[0]) > 0:
                identity = results[0]['identity'][0]
                name = self.get_name_from_path(identity)
                image_count = self.count_person_images(self.DATABASE_FOLDER, name)

                if image_count < self.MAX_IMAGES_PER_PERSON:
                    self.save_image(self.DATABASE_FOLDER, name, frame)

                self.unknown_face_count = 0
                return name
            else:
                self.unknown_face_count += 1
                if self.unknown_face_count > self.UNKNOWN_FACE_THRESHOLD:
                    current_time = time.time()
                    if current_time - self.last_unknown_time > 1:  # Capture every second
                        self.save_image(self.TEMP_FOLDER, f"unknown", frame)
                        self.last_unknown_time = current_time
                        
                        if self.unknown_face_count == self.UNKNOWN_FACE_IMAGES + self.UNKNOWN_FACE_THRESHOLD:
                            return "new_face_detected"
                return "unknown"
        return None

    async def add_new_person(self, name):
        self.add_to_database(name)
        self.unknown_face_count = 0