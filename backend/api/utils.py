# utils.py (pode ser criado um arquivo utilitário para funções auxiliares)
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status

from sklearn.neighbors import NearestNeighbors
import numpy as np

from .models import Preference,LikeDislike,Movie,Rating

def adjust_user_preferences(user, genres, action, weight):
    """
    Ajusta as preferências do usuário para uma lista de gêneros.

    :param user: Usuário para ajustar as preferências.
    :param genres: Lista de gêneros a serem ajustados.
    :param action: Tipo de ação ('favorite', 'avoid').
    :param weight: Peso da ação (positivo ou negativo).
    """
    for genre in genres:
        # Busca ou cria a preferência
        preference, created = Preference.objects.get_or_create(
            user=user,
            genre=genre,
            defaults={"priority": weight}  # Inicializa prioridade ao criar
        )
        
        # Se a preferência já existia, ajusta o valor
        if not created:
            if action == "favorite":
                preference.priority += weight
            elif action == "avoid":
                preference.priority -= weight  # Peso negativo reduz preferência
            
            # Evitar valores negativos extremos, opcional
            preference.priority = max(preference.priority, 0)
            print(" # Se a preferência já existia, ajusta o valor")
        
        # Salva a instância
        preference.save()

def get_movie_interactions(movie):
    """
    Função para retornar a contagem de likes, favoritos e assistidos de um filme.
    """
    likes_count = movie.likes_disliked_by.filter(action='like').count()
    dislikes_count = movie.likes_disliked_by.filter(action='dislike').count()
    favorite_count = movie.favorited_by.count()
    watched_count = movie.watchedmovie_set.count()

    return {
        'likes_count': likes_count,
        'dislikes_count': dislikes_count,
        'favorite_count': favorite_count,
        'watched_count': watched_count
    }


# utils.py (ou onde você achar necessário)
def get_user_interactions(movie, user):
    """
    Função para verificar as interações de um usuário com um filme específico.
    Retorna:
      - Se o filme foi curtido (like), descurtido (dislike) ou não interagido
      - O número de vezes que o usuário assistiu ao filme
    """
    # Verificar se o usuário curtiu ou descurtiu o filme
    like_action = movie.likes_disliked_by.filter(user=user)
    like_status = 'none'  # Nenhuma interação
    if like_action.filter(action='like').exists():
        like_status = 'like'
    elif like_action.filter(action='dislike').exists():
        like_status = 'dislike'

    # Contar o número de vezes que o usuário assistiu ao filme
    watched_count = movie.watchedmovie_set.filter(user=user).count()

    return {
        'liked': like_status,  # Retorna 'like', 'dislike', ou 'none'
        'favorited': movie.favorited_by.filter(user=user).exists(),  # Se o filme foi favoritado
        'watched': watched_count,  # Quantas vezes o filme foi assistido
    }

# Utilitário para respostas uniformes
def create_response(message, data=None, status_code=status.HTTP_200_OK):
    response = {"message": message}
    if data is not None:
        response["data"] = data
    return Response(response, status=status_code)


def recommend_movies_based_on_likes(user):
    # Obtém os filmes que o usuário gostou
    liked_movies = LikeDislike.objects.filter(user=user, action='like')
    
    # Extrai os filmes que o usuário gostou
    liked_movie_ids = [like.movie.id for like in liked_movies]
    
    # Busca filmes semelhantes aos que o usuário gostou
    recommended_movies = Movie.objects.filter(id__in=liked_movie_ids)
    
    return recommended_movies

def calculate_movie_score(self, movie, user):
    """
    Função para calcular a pontuação do filme baseado no histórico de interações e preferências do usuário.
    """
    score = 0
    # Pontuação baseada nas interações do usuário com o filme
    user_interactions = get_user_interactions(movie, user)
    if user_interactions.get('liked'):
        score += 2
    elif user_interactions.get('disliked'):
        score -= 2

    # Pontuação baseada no gênero do filme
    for genre in movie.genres.all():
        if genre.id in self.get_user_favorite_genre_ids(user):
            score += 1  # Aumenta a pontuação se o gênero é favorito

    return score

def get_user_favorite_genre_ids(self, user):
    """
    Retorna os IDs dos gêneros favoritos do usuário
    """
    return Preference.objects.filter(user=user, preference_type="favorite").values_list('genre_id', flat=True)

def recommend_movies_with_knn(user):
    # Criar uma matriz de interações de usuários e filmes
    user_movie_matrix = np.zeros((num_users, num_movies))  # Aqui você cria a matriz de interações

    # Preencher a matriz com dados de avaliação ou preferências (pode usar ratings)
    for rating in Rating.objects.all():
        user_movie_matrix[rating.user.id, rating.movie.id] = rating.rating
    
    # Treinar o modelo KNN
    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(user_movie_matrix)
    
    # Encontrar filmes recomendados
    movie_recommendations = knn.kneighbors([user_movie_matrix[user.id]], n_neighbors=10)
    
    return movie_recommendations
