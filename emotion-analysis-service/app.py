from flask import Flask, request, jsonify
from transformers import pipeline
import os
import requests



app = Flask(__name__)

# Load emotion classifier from Hugging Face
classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", top_k=1)  
RECOMMENDER_URL = os.getenv('RECOMMENDER_URL', 'http://172.18.0.2:5001/recommend')
# Simple health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Emotion Analysis Service is running"}), 200

# Function to convert text to tensor and make prediction
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

        emotion = analyze_emotion(text)
        # sending the emotion to the recommendation service
        response = requests.post(RECOMMENDER_URL, json={"emotion": emotion})
        if response.status_code != 200:
            return jsonify({"error": "Failed to get recommendation"}), 500
        recommendation = response.json()
        # Return the emotion and recommendation
        return jsonify({"emotion": emotion, "recommendation": recommendation}) 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
