from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Environment variables or default service URLs
EMOTION_SERVICE_URL = os.getenv('EMOTION_SERVICE_URL', 'http://emotion-service:5000/analyze')
RECOMMENDATION_SERVICE_URL = os.getenv('RECOMMENDATION_SERVICE_URL', 'http://recommendation-service:5001/recommend')

@app.route('/watcha', methods=['POST'])
def process_request():
    try:
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({'error': 'Text input is required'}), 400

        # Step 1: Send text to Emotion Analysis Service
        emotion_response = requests.post(EMOTION_SERVICE_URL, json={'text': text})
        if emotion_response.status_code != 200:
            return jsonify({'error': 'Emotion service failed'}), 500

        emotion_data = emotion_response.json()
        emotion = emotion_data.get('emotion')
        if not emotion:
            return jsonify({'error': 'Emotion not found in response'}), 500

        # Step 2: Send emotion to Recommendation Service
        recommendation_response = requests.post(RECOMMENDATION_SERVICE_URL, json={'emotion': emotion})
        if recommendation_response.status_code != 200:
            return jsonify({'error': 'Recommendation service failed'}), 500

        recommendations = recommendation_response.json().get('movies', [])

        return jsonify({
            'emotion': emotion,
            'recommendations': recommendations
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'API Gateway is running'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
