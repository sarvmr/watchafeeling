from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Simple health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Emotion Analysis Service is running"}), 200

# Dummy sentiment analysis (to be replaced with actual model)
def analyze_emotion(text):
    emotions = ['happy', 'sad', 'angry', 'relaxed']
    return emotions[hash(text) % len(emotions)]

# Emotion Analysis Route
@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        text = data.get('text')
        if not text:
            return jsonify({"error": "Text input is required"}), 400

        emotion = analyze_emotion(text)
        return jsonify({"emotion": emotion})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
