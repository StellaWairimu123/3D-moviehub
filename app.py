from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connect to MongoDB - CHANGED to movie_db
client = MongoClient("mongodb+srv://stella:Jaden%402012@cluster0.ny8p5lz.mongodb.net/movie_db")
db = client['movie_db']           # Changed from 'movie_database' to 'movie_db'
collection = db['movies']

@app.route('/')
def index():
    movies = list(collection.find())
    return render_template('index.html', movies=movies)

@app.route('/add', methods=['POST'])
def add_movie():
    movie = {
        'title': request.form['title'],
        'director': request.form['director'],
        'year': int(request.form['year']),
        'genre': request.form['genre'],
        'rating': float(request.form['rating']) if request.form['rating'] else 0,
        'duration': int(request.form['duration']) if request.form['duration'] else 0,
        'cast': request.form.get('cast', ''),
        'synopsis': request.form.get('synopsis', ''),
        'poster': request.form.get('poster', ''),
        'watched': request.form.get('watched', 'false')
    }
    collection.insert_one(movie)
    return redirect(url_for('index'))

@app.route('/delete/<movie_id>')
def delete_movie(movie_id):
    collection.delete_one({'_id': ObjectId(movie_id)})
    return redirect(url_for('index'))

import os
from pymongo import MongoClient

client = MongoClient("mongodb+srv://stella:Jaden%402012@cluster0.ny8p5lz.mongodb.net/movie_db")

db = client["movie_db"]
collection = db["movies"]
