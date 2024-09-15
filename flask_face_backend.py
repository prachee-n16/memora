from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from deepface import DeepFace



app = Flask(__name__)
CORS(app)

@app.route('/')
def homepage():
    return render_template('index.html') 

@app.route('/faces/insert', methods=['POST'])
def insert_faces():
    data = request.json
    print(data)
    return jsonify(data)

