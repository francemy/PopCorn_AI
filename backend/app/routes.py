from flask import jsonify, request
from . import db
from .models import User, Movie
from flask import current_app as app

@app.route("/")
def home():
    return jsonify({"message": "Welcome to PopCorn AI!"})

@app.route("/movies", methods=["GET"])
def get_movies():
    movies = Movie.query.all()
    return jsonify([{"id": m.id, "title": m.title, "genre": m.genre} for m in movies])

@app.route("/users/<int:user_id>/recommendations", methods=["GET"])
def recommend_movies(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    # Exemplo simples de recomendação
    recommendations = Movie.query.filter(Movie.genre.in_(user.preferences.split(","))).all()
    return jsonify([{"id": m.id, "title": m.title, "genre": m.genre} for m in recommendations])
