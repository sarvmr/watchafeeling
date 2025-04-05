import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TMDB_API_KEY = os.getenv('TMDB_API_KEY')

emotion_to_genre = {
    "joy": "Comedy",
    "sadness": "Drama",
    "anger": "Thriller",
    "fear": "Horror",
    "love": "Romance",
    "surprise": "Adventure",
    "neutral": "Documentary"
}

genre_name_to_id = {
    "Comedy": 35,
    "Drama": 18,
    "Thriller": 53,
    "Horror": 27,
    "Romance": 10749,
    "Adventure": 12,
    "Documentary": 99
}

@app.route('/recommend', methods=['POST'])
def recommend_movies():
  try:
    data = request.get_json()
    if not data or 'emotion' not in data:
        return jsonify({"error": "Invalid input"}), 400

    emotion = data['emotion'].lower()
    genre_name = emotion_to_genre.get(emotion)

    if not genre_name:
        return jsonify({"error": "Emotion not recognized"}), 400

    genre_id = genre_name_to_id[genre_name]
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}"
    
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch movies"}), 500

    movies = response.json().get('results', [])
    movie_titles = [movie['title'] for movie in movies]

    return jsonify({"movies": movie_titles}), 200
  except Exception as e:
    return jsonify({"error": str(e)}), 500 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 
  