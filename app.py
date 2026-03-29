from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import certifi
import ssl

app = Flask(__name__)

# Read MONGO_URI from environment
MONGO_URI = os.environ.get('MONGO_URI')

def get_db():
    if not MONGO_URI:
        print("ERROR: MONGO_URI not set")
        return None
    
    try:
        # Create SSL context with certifi certificates
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        
        # Connect with SSL settings
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=10000,
            tls=True,
            tlsCAFile=certifi.where(),
            tlsAllowInvalidCertificates=False
        )
        
        # Test connection
        client.admin.command('ping')
        print("MongoDB connected successfully!")
        return client["movie_db"]
        
    except Exception as e:
        print(f"MongoDB Error: {e}")
        return None

@app.route('/')
def index():
    db = get_db()
    if db is None:
        return "Database connection failed", 500
    
    try:
        collection = db["movies"]
        movies = list(collection.find())
        return render_template('index.html', movies=movies)
    except Exception as e:
        return f"Error: {e}", 500

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
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
