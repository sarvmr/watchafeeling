from flask import Flask, request, jsonify
from transformers import pipeline
import os
import requests

app = Flask(__name__)

# Load emotion classifier from Hugging Face
classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", top_k=1)

# API Gateway URL (this will communicate with both services)
API_GATEWAY_URL = os.getenv('API_GATEWAY_URL', 'http://api-gateway:8080/watcha')  # Adjust for your gateway's actual URL

# Simple health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Emotion Analysis Service is running"}), 200

# Function to analyze emotion from text input
def analyze_emotion(text):
    try:
        result = classifier(text)
        top_result = result[0][0]
        
        # Extract the label with the highest score
        label = top_result['label']
        score = top_result['score']
        
        # Format the result
        emotion = label.lower()
        return emotion
    except Exception as e:
        return f"Error in sentiment analysis: {e}"

# Emotion Analysis Route
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({"error": "Text input is required"}), 400

        # Analyze emotion from the text
        emotion = analyze_emotion(text)
        
        # Return the emotion
        return jsonify({"emotion": emotion}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
