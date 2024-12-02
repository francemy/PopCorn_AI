# utils.py (pode ser criado um arquivo utilitário para funções auxiliares)
from django.db.models import Count

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
    Retorna se o filme foi curtido, favoritado ou assistido pelo usuário.
    """
    return {
        'liked': movie.likes_disliked_by.filter(user=user, action='like').exists(),
        'favorited': movie.favorited_by.filter(user=user).exists(),
        'watched': movie.watchedmovie_set.filter(user=user).exists(),
    }