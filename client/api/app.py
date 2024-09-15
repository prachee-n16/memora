from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import requests
from flask_cors import CORS
import iris
import time
from deepgram import DeepgramClient, PrerecordedOptions
from werkzeug.utils import secure_filename


load_dotenv()

BASETEN_API_KEY = os.getenv("BASETEN_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
MODEL_ID = "03y55vew"


api = Flask(__name__)
CORS(api)

namespace = "USER"
port = 1972
hostname = os.getenv('IRIS_HOSTNAME', 'localhost')
connection_string = f"{hostname}:{port}/{namespace}"
username = "demo"
password = "demo"

conn = iris.connect(connection_string, username, password)
cursor = conn.cursor()


@api.route('/get_user/<string:name>', methods=['GET'])
def get_user(name):
    sql = "SELECT * FROM Users WHERE name = ?"
    cursor.execute(sql, [name])
    user = cursor.fetchone()
    
    if user:
        return jsonify({
            "user_id": user[0],
            "name": user[1],
            "date_of_birth": user[2],
            "medical_conditions": user[3]
        }), 200
    else:
        return jsonify({"error": "User not found"}), 404

@api.route('/get_user_memories/<int:user_id>', methods=['GET'])
def get_user_memories(user_id):
    sql = "SELECT * FROM Memories WHERE user_id = ? ORDER BY timestamp DESC"
    cursor.execute(sql, [user_id])
    memories = cursor.fetchall()
    
    memory_list = []
    for memory in memories:
        memory_list.append({
            "memory_id": memory[0],
            "title": memory[2],
            "description": memory[4],
            "timestamp": memory[5]
        })
    
    return jsonify(memory_list), 200

@api.route('/get_user_people/<int:user_id>', methods=['GET'])
def get_user_people(user_id):
    sql = "SELECT * FROM People WHERE user_id = ?"
    cursor.execute(sql, [user_id])
    people = cursor.fetchall()
    
    people_list = []
    for person in people:
        people_list.append({
            "person_id": person[0],
            "name": person[2],
            "relationship": person[3],
            "description": person[4]
        })
    
    return jsonify(people_list), 200

@api.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    
    temp_filename = secure_filename('temp_audio.wav')
    temp_filepath = os.path.join('/tmp', temp_filename)
    audio_file.save(temp_filepath)
    deepgram = DeepgramClient(DEEPGRAM_API_KEY)

    try:
        with open(temp_filepath, 'rb') as buffer_data:
            payload = { 'buffer': buffer_data }

            options = PrerecordedOptions(
                smart_format=True, model="nova-2", language="en-US"
            )

            response = deepgram.listen.prerecorded.v('1').transcribe_file(payload, options)
        
            transcription = response['results']['channels'][0]['alternatives'][0]['transcript']
            
            return jsonify({"transcription": transcription})
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    

@api.route('/insert_user', methods=['POST'])
def insert_user():
    data = request.json
    sql = "INSERT INTO Users (name, date_of_birth, medical_conditions, profile_picture) VALUES (?, ?, ?, ?)"
    
    try:
        start_time = time.time()
        cursor.execute(sql, [
            data['name'],
            data['date_of_birth'],
            data['medical_conditions'],
            data['profile_picture']
        ])
        conn.commit()
        end_time = time.time()
        
        user_id = cursor.lastrowid
        print(f"Time taken to add user: {end_time - start_time} seconds")
        return jsonify({"message": "User added successfully", "user_id": user_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400


@api.route('/insert_memory', methods=['POST'])
def insert_memory():
    data = request.json
    sql = "INSERT INTO Memories (user_id, title, image, description) VALUES (?, ?, ?, ?)"
    
    try:
        start_time = time.time()
        cursor.execute(sql, [
            data['user_id'],
            data['title'],
            data['image'],
            data['description']
        ])
        conn.commit()
        end_time = time.time()
        
        memory_id = cursor.lastrowid
        print(f"Time taken to add memory: {end_time - start_time} seconds")
        return jsonify({"message": "Memory added successfully", "memory_id": memory_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    

@api.route('/add_person', methods=['POST'])
def add_person():
    data = request.json
    sql = """INSERT INTO People 
             (user_id, name, relationship, description, picture) 
             VALUES (?, ?, ?, ?, ?)"""
    
    try:
        start_time = time.time()
        cursor.execute(sql, [
            data['user_id'],
            data['name'],
            data['relationship'],
            data['description'],
            data['picture']  
        ])
        conn.commit()
        end_time = time.time()
        
        person_id = cursor.lastrowid
        print(f"Time taken to add person: {end_time - start_time} seconds")
        return jsonify({
            "message": "Person added successfully", 
            "person_id": person_id
        }), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400