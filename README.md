# **memora**
![Screenshot 2024-09-15 at 11 01 35 AM](https://github.com/user-attachments/assets/0a23c73e-1417-44f4-aa8b-88a1bd06b9ed)

## Inspiration

Nearly 7 million Americans are living with Alzheimer's. By 2050, this number is projected to rise to nearly 13 million. Despite the large number of individuals effected, scientists do not yet fully understand what causes Alzheimer’s disease. In fact, there is currently no known cure for Alzheimer’s disease. It is deeply painful for families to witness their loved ones struggle with memory loss, as it makes daily life increasingly difficult and disorienting. Our goal is to alleviate this pain by acting as a second brain for individuals, helping to manage and preserve memories to ease their daily lives.

## What it does

1. We use advanced facial recognition algorithms to identify and detect faces in various environments. Once a face is detected, the system classifies it based on known individuals, allowing the user to easily recognize and recall their loved ones. This feature helps users maintain connections with familiar faces, aiding in memory recall.
![image](https://github.com/user-attachments/assets/b2b67b05-6434-4b7b-86c8-15b4dd6fa7da)
![image](https://github.com/user-attachments/assets/dfe67918-ff5c-4e05-85dc-83e0e24169c4)
![image](https://github.com/user-attachments/assets/1f22d57b-228b-47d4-8d33-d9867489b312)

2. The recorded conversations and interactions are summarized to create concise, useful summaries. These summaries help in reflecting on daily activities and maintaining a coherent record of the user's experiences.
3. The system captures images and data about the user’s surroundings. This can include important locations, objects, or scenes that are relevant to their daily life. Captured data is processed to create concise summaries of the user’s environment.
4. A chatbot is developed to interact with the user, providing information or answering questions based on the summarized data. This chatbot utilizes text-to-speech (TTS) and speech-to-text (STT) methods to facilitate smooth and intuitive communication.

## How we built it

Our project begins with capturing video feeds using mobile phones. An OpenCV model detects faces in the video, and a Convolutional Neural Network (CNN) classifies these faces to identify family members from a known list. Alongside this, conversations and photos of the environment are recorded. For each photo, an image-to-text description is generated using Qwen. These descriptions are stored in a vector database, creating a searchable repository of visual information. Conversations are also transcribed to text for additional processing. We use GPT for prompt engineering - When a user queries the system, GPT searches through the vector database of image descriptions and transcriptions, providing relevant information based on the user's memories and interactions. This setup ensures that users can retrieve information about their daily experiences and interactions, supported by both visual and conversational data.

## Architecture
![architecture drawio](https://github.com/user-attachments/assets/0d742a3c-ad8b-443c-9ff0-59eeae538400)

## UI Pages
<img width="1512" alt="Screenshot 2024-09-15 at 1 30 05 PM" src="https://github.com/user-attachments/assets/6f1166b7-f80c-424d-85ca-717770d6eb45">
<img width="1512" alt="Screenshot 2024-09-15 at 1 30 17 PM" src="https://github.com/user-attachments/assets/40a83113-63cc-47db-8a77-93cf07cad422">
<img width="1512" alt="Screenshot 2024-09-15 at 1 30 44 PM" src="https://github.com/user-attachments/assets/17109f4d-b678-42d0-a08d-3000a5ab37f1">
<img width="1512" alt="Screenshot 2024-09-15 at 1 30 52 PM" src="https://github.com/user-attachments/assets/d9adafb2-1b79-4a00-81c4-12dc2451a2ed">
