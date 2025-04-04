from flask import Flask, request, jsonify
from transformers import pipeline



app = Flask(__name__)

# Load emotion classifier from Hugging Face
classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion", top_k=1)  

# Simple health check route
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "Emotion Analysis Service is running"}), 200

# Function to convert text to tensor and make prediction
def analyze_emotion(text):
    try:
        result = classifier(text)
        top_result = result[0][0]
        print(result)  # Debugging line to check the result format
        # Extract the label with the highest score
        label = top_result['label']
        print(label)  # Debugging line to check the label format
        score = top_result['score']
        print(score)  # Debugging line to check the score format
        # Format the result
        emotion = {
            "emotion": label,
            "confidence": score
        }
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
        return jsonify({"emotion": emotion})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
