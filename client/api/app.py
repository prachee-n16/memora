from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import requests
from flask_cors import CORS

load_dotenv()

BASETEN_API_KEY = os.getenv("BASETEN_API_KEY")
MODEL_ID = "03y55vew"


api = Flask(__name__)
CORS(api)

@api.route('/profile')
def my_profile():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body

@api.route('/memories')
def get_memories():
    mock_memories_data = [
    {
        "title": "Vacation in Bali",
        "image": "/background-0.jpg",
        "description": "A relaxing vacation on the beautiful beaches of Bali, enjoying the sun and surf.",
    },
]
    return jsonify(mock_memories_data)

@api.route('/transcribe', methods=['POST'])
def transcribe_audio():
    data = request.json
    
    if 'url' in data:
        payload = {"url": data['url']}
    elif 'audio' in data:
        payload = {"audio": data['audio']}
    else:
        return jsonify({"error": "Either 'url' or 'audio' must be provided"}), 400

    try:
        response = requests.post(
            f"https://model-{MODEL_ID}.api.baseten.co/production/predict",
            headers={"Authorization": f"Api-Key {BASETEN_API_KEY}"},
            json=payload
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"Error": str(e)}), 500