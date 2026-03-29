from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# MongoDB connection (safe)
try:
    client = MongoClient("mongodb+srv://stella:Jaden%402012@cluster0.ny8p5lz.mongodb.net/movie_db")
    db = client["movie_db"]
    collection = db["movies"]
except Exception as e:
    collection = None
    print("MongoDB Error:", e)

# Home route
@app.route('/')
def index():
    try:
        if collection is None:
            return "Database connection failed"

        movies = list(collection.find())
        return render_template('index.html', movies=movies)
    except Exception as e:
        return f"Error loading page: {e}"

# Add movie
@app.route('/add', methods=['POST'])
def add_movie():
    try:
        movie = {
            'title': request.form.get('title', ''),
            'genre': request.form.get('genre', ''),
            'rating': float(request.form.get('rating', 0) or 0),
            'duration': int(request.form.get('duration', 0) or 0),
            'cast': request.form.get('cast', ''),
            'synopsis': request.form.get('synopsis', ''),
            'poster': request.form.get('poster', ''),
            'watched': request.form.get('watched', 'false')
        }
        collection.insert_one(movie)
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error adding movie: {e}"

# Delete movie
@app.route('/delete/<movie_id>')
def delete_movie(movie_id):
    try:
        collection.delete_one({'_id': ObjectId(movie_id)})
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error deleting movie: {e}"

# Run app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
