from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


# Modelo para Gêneros de Filmes
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)  # Slug para URLs amigáveis

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Gera um slug único baseado no nome
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Modelo para Filmes
class Movie(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)  # Slug para URLs amigáveis
    description = models.TextField()
    release_date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duração do filme em minutos")
    image_url = models.URLField(max_length=200, blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação
    updated_at = models.DateTimeField(auto_now=True)  # Data da última atualização
    users_watched = models.ManyToManyField(User, related_name='watched_movies', blank=True)  # Relacionamento com usuários que assistiram ao filme

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Gera um slug único baseado no título
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# Modelo para Avaliação de Filmes
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    
    # Ajuste para permitir avaliações de 1.0 a 5.0 com precisão de 0.5
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        choices=[(i / 2, f'{i / 2}') for i in range(2, 11)]  # Avaliação de 1.0 a 5.0 com incrementos de 0.5
    )
    
    review = models.TextField(blank=True, null=True)  # Comentário opcional
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  # Garantir que um usuário só possa avaliar um filme uma vez

    def __str__(self):
        return f'{self.user.username} - {self.movie.title} ({self.rating})'


# Modelo para Preferências de Gênero dos Usuários
class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preferences')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='preferences')
    preference_type = models.CharField(max_length=50, choices=[('favorite', 'Favorito'), ('avoid', 'Evitar')])
    priority = models.PositiveIntegerField(default=1, choices=[(i, f'{i}') for i in range(1, 6)])  # Prioridade para o gênero

    class Meta:
        unique_together = ('user', 'genre')  # Garantir que um usuário só tenha uma preferência por gênero por vez

    def __str__(self):
        return f'{self.user.username} - {self.genre.name} ({self.preference_type})'


# Modelo para Filmes Favoritos (Opcional)
class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_movies')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  # Garantir que um usuário só possa favoritar o mesmo filme uma vez

    def __str__(self):
        return f'{self.user.username} favorited {self.movie.title}'
    
class WatchedMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watch_count = models.PositiveIntegerField(default=1)  # Contagem de assistências

    class Meta:
        unique_together = ('user', 'movie')  # Garantir que um usuário só tenha uma entrada por filme

    def __str__(self):
        return f'{self.user.username} watched {self.movie.title} {self.watch_count} times'

    def increment_watch_count(self):
        """
        Incrementa o contador de assistências (watch_count) para o filme do usuário.
        """
        self.watch_count += 1
        self.save()

    @staticmethod
    def get_watch_count(user, movie):
        """
        Método para obter a contagem de assistências de um usuário para um filme.
        """
        try:
            watched_movie = WatchedMovie.objects.get(user=user, movie=movie)
            return watched_movie.watch_count
        except WatchedMovie.DoesNotExist:
            return 0



class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_dislikes')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='likes_disliked_by')
    action = models.CharField(max_length=8, choices=[('like', 'Like'), ('dislike', 'Dislike'), ('none', 'None')])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  # Garantir que um usuário só possa interagir com um filme uma vez (like ou dislike)

    def __str__(self):
        return f'{self.user.username} {self.action}d {self.movie.title}'