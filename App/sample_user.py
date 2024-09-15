import requests
import json

# Define the base URL for the Flask server
base_url = "http://localhost:5010"

# Function to create the table
def create_table():
    response = requests.post(f"{base_url}/create")
    print("Create Table Response:", response.json())

# Function to insert data into the table
def insert_data(name, embedding, other_info):
    data = {
        "tableName": "faces",
        "columns": "(name, face_embedding, other_info)",
        "data": f"('{name}', {embedding}, '{other_info}')"
    }
    response = requests.post(f"{base_url}/insert", json=data)
    print("Insert Data Response:", response.json())

# Function to get face data based on embedding
def get_face(embedding):
    data = {
        "embedding": embedding
    }
    response = requests.post(f"{base_url}/getface", json=data)
    print("Get Face Response:", response.json())

if __name__ == "__main__":
    # Create the table
    create_table()

    # Insert arbitrary vector embeddings
    insert_data("John Doe", "[0.1, 0.2, 0.3, ..., 0.512]", "Some other info")
    insert_data("Jane Doe", "[0.2, 0.3, 0.4, ..., 0.512]", "Some other info")

    # Get face data based on an arbitrary embedding
    get_face("[0.1, 0.2, 0.3, ..., 0.512]")
