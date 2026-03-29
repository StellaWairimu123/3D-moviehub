from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# MongoDB connection using environment variable (more secure)
MONGO_URI = os.environ.get('MONGO_URI')

# Fallback for local testing only - REPLACE WITH YOUR ACTUAL URI
if not MONGO_URI:
    # Make sure to URL-encode special characters in password
    # @ becomes %40 in the password
    MONGO_URI = "mongodb+srv://stella:Jaden%402012@cluster0.ny8p5lz.mongodb.net/movie_db?retryWrites=true&w=majority"

def get_db():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        return client["movie_db"]
    except Exception as e:
        print(f"MongoDB Connection Error: {e}")
        return None

@app.route('/')
def index():
    db = get_db()
    if db is None:
        # Return template with empty movies list if DB fails
        return render_template('index.html', movies=[])
    
    try:
        collection = db["movies"]
        movies = list(collection.find())
        return render_template('index.html', movies=movies)
    except Exception as e:
        print(f"Error fetching movies: {e}")
        return render_template('index.html', movies=[])

@app.route('/add', methods=['POST'])
def add_movie():
    db = get_db()
    if db is None:
        return "Database connection failed", 500
    
    try:
        collection = db["movies"]
        movie = {
            'title': request.form.get('title', ''),
            'director': request.form.get('director', ''),
            'year': int(request.form.get('year', 0) or 0),
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
        return f"Error adding movie: {e}", 500

@app.route('/delete/<movie_id>')
def delete_movie(movie_id):
    db = get_db()
    if db is None:
        return "Database connection failed", 500
    
    try:
        collection = db["movies"]
        collection.delete_one({'_id': ObjectId(movie_id)})
        return redirect(url_for('index'))
    except Exception as e:
        return f"Error deleting movie: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5001)), debug=True)
