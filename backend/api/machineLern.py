# /machineLern.py
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from .models import Rating, Movie
from sklearn.feature_extraction.text import TfidfVectorizer

def recommend_movies_user_based(user_id, interaction_matrix, knn_model, n_recommendations=10):
    """
    Recomenda filmes com base em usuários similares (KNN).
    
    :param user_id: ID do usuário para quem gerar recomendações.
    :param interaction_matrix: Matriz de interações (usuários x filmes).
    :param knn_model: Modelo KNN já treinado.
    :param n_recommendations: Número de filmes a recomendar.
    :return: Lista de IDs de filmes recomendados.
    """
    try:
        # Verificar se o usuário está na matriz de interações
        user_index = interaction_matrix.index.get_loc(user_id)
    except KeyError:
        # Usuário não possui interações, retornar lista vazia
        return []

    # Obter os usuários mais próximos
    user_interactions = interaction_matrix.iloc[user_index].values.reshape(1, -1)
    distances, indices = knn_model.kneighbors(user_interactions, n_neighbors=6)  # Incluir 5 vizinhos + usuário atual

    # Excluir o próprio usuário dos resultados
    similar_users = indices.flatten()[1:]

    # Obter os filmes que esses usuários interagiram positivamente
    recommended_movies = set()
    for similar_user_index in similar_users:
        similar_user_id = interaction_matrix.index[similar_user_index]
        similar_user_movies = interaction_matrix.loc[similar_user_id]
        
        # Filmes que o usuário similar avaliou positivamente (ou interagiu)
        liked_movies = similar_user_movies[similar_user_movies > 0].index
        recommended_movies.update(liked_movies)

    # Remover filmes que o usuário já interagiu
    user_watched_movies = interaction_matrix.loc[user_id]
    already_watched = set(user_watched_movies[user_watched_movies > 0].index)
    recommended_movies -= already_watched

    # Retornar apenas os primeiros `n_recommendations` filmes
    return list(recommended_movies)[:n_recommendations]


# Função para construir a matriz de interação
def build_interaction_matrix():
    # Obtendo as avaliações dos usuários para construir a matriz de interação
    ratings = Rating.objects.all().select_related('user', 'movie')
    
    # Construir um DataFrame com as avaliações
    ratings_data = pd.DataFrame(list(ratings.values('user_id', 'movie_id', 'rating')))
    
    # Criar a matriz de interações (usuário x filme)
    interaction_matrix = ratings_data.pivot_table(index='user_id', columns='movie_id', values='rating').fillna(0)
    return interaction_matrix

# Função para construir o modelo KNN (colaborativo)
def build_knn_model(interaction_matrix, n_neighbors=3):
    # Convertendo a matriz para NumPy
    interaction_matrix_np = interaction_matrix.to_numpy()

    # Inicializando o modelo KNN (k=3)
    knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=n_neighbors)
    knn.fit(interaction_matrix_np)
    
    return knn

# Função para recomendar filmes colaborativos
def recommend_movies_collaborative(user_id, interaction_matrix, knn, top_n=3):
    user_index = user_id - 1  # Ajuste de índice se user_id começar de 1
    distances, indices = knn.kneighbors([interaction_matrix.iloc[user_index]], n_neighbors=top_n)
    
    recommended_movie_ids = set()
    
    for i in indices[0]:
        # Pegando os filmes que o usuário similar assistiu (com avaliação > 0)
        similar_user_ratings = interaction_matrix.iloc[i]
        recommended_movies = similar_user_ratings[similar_user_ratings > 0].index.tolist()
        recommended_movie_ids.update(recommended_movies)
    
    return recommended_movie_ids

# Função para recomendar filmes baseados em conteúdo
def recommend_movies_content_based(movie_id, cosine_sim, movies_df, top_n=3):
    movie_index = movies_df[movies_df['movie_id'] == movie_id].index[0]
    
    # Obter os filmes mais similares
    sim_scores = list(enumerate(cosine_sim[movie_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Obter os top_n filmes mais similares
    sim_scores = sim_scores[1:top_n+1]  # Exclui o filme que foi passado como entrada
    movie_indices = [i[0] for i in sim_scores]
    
    return movies_df['title'].iloc[movie_indices]

# Função para recomendar filmes híbridos (colaborativo + conteúdo)
def recommend_movies_hybrid(user_id, movie_id, interaction_matrix, knn, cosine_sim, movies_df, top_n=3):
    # Recomendação colaborativa
    collaborative_recommendations = recommend_movies_collaborative(user_id, interaction_matrix, knn, top_n)
    
    # Recomendação baseada em conteúdo
    content_based_recommendations = recommend_movies_content_based(movie_id, cosine_sim, movies_df, top_n)
    
    # Combine as recomendações (evitando duplicatas)
    all_recommendations = set(collaborative_recommendations).union(set(content_based_recommendations))
    
    return all_recommendations
