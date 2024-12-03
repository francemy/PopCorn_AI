from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from .models import Genre, Movie, Rating, Preference, LikeDislike, WatchedMovie, FavoriteMovie


# Serializer para o modelo de usuário (User)
class UserSerializer(serializers.ModelSerializer):
    preference = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        # Permite que o usuário atualize a senha se for necessário
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance


# Serializer para o modelo de Gênero (Genre)
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']


# Serializer para o modelo de Filme (Movie)
class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)  # Para retornar os gêneros associados ao filme

    class Meta:
        model = Movie
        fields = ['id', 'title', 'slug', 'description', 'release_date', 'duration', 'image_url', 'genres']

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        movie = Movie.objects.create(**validated_data)
        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(**genre_data)
            movie.genres.add(genre)
        return movie


# Serializer para o modelo de Avaliação (Rating)
from rest_framework import serializers
from decimal import Decimal
from .models import Rating, User, Movie

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)  # Para criação, ID do usuário
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())  # Para criar com o ID do filme
    rating = serializers.DecimalField(max_digits=3, decimal_places=1)  # Usando DecimalField

    class Meta:
        model = Rating
        fields = ['id', 'user', 'movie', 'rating', 'review', 'created_at']

    def validate_rating(self, value):
        # Validação para garantir que a avaliação esteja entre 1.0 e 5.0
        if value < Decimal('1.0') or value > Decimal('5.0'):
            raise serializers.ValidationError("A avaliação deve estar entre 1.0 e 5.0.")
        return value

    def create(self, validated_data):
        """
        Sobrescreve o método create para associar automaticamente o usuário autenticado.
        """
        user = self.context['request'].user  # Obtém o usuário autenticado
        validated_data['user'] = user  # Associa o usuário autenticado à avaliação
        return super().create(validated_data)


class PreferenceSerializer(serializers.ModelSerializer):
    # Campos explícitos para o relacionamento e validação adicional
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Preenche o usuário automaticamente
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())
    preference_type = serializers.ChoiceField(choices=Preference._meta.get_field('preference_type').choices)
    priority = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Preference
        fields = ['user', 'genre', 'preference_type', 'priority']

    def validate(self, data):
        """
        Validações adicionais:
        - Garante que o usuário não crie duplicatas para o mesmo gênero.
        """
        user = self.context['request'].user
        genre = data.get('genre')

        # Verifica se já existe uma preferência para este gênero e usuário
        if Preference.objects.filter(user=user, genre=genre).exists():
            raise serializers.ValidationError("Já existe uma preferência para este gênero.")
        
        return data
    
class FavoriteMovieSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Exibe o nome do usuário em vez do ID
    movie = serializers.StringRelatedField()  # Exibe o título do filme em vez do ID
    added_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = FavoriteMovie
        fields = ['user', 'movie', 'added_at']

    def create(self, validated_data):
        return FavoriteMovie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.movie = validated_data.get('movie', instance.movie)
        instance.added_at = validated_data.get('added_at', instance.added_at)
        instance.save()
        return instance

    def create_or_update_preference(self, user, movie):
        """
        Cria ou atualiza as preferências de gênero com base no filme favorito.
        A prioridade do gênero é incrementada quando o filme é favoritado.
        """
        for genre in movie.genres.all():
            preference, created = Preference.objects.get_or_create(user=user, genre=genre)
            # Aumenta a prioridade do gênero, mas com um limite de 5
            if preference.priority < 5:
                preference.priority += 1
            preference.save()

    def save(self, **kwargs):
        """
        Sobrescreve o método save para incluir o ajuste das preferências de gênero.
        """
        instance = super().save(**kwargs)
        
        # Ajusta a preferência de gênero com base no filme favorito
        self.create_or_update_preference(instance.user, instance.movie)
        
        return instance

    

class WatchedMovieSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    watch_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = WatchedMovie
        fields = ['id', 'user', 'movie', 'watch_count']

    def create(self, validated_data):
        user = validated_data['user']
        movie = validated_data['movie']

        # Verifica se o usuário já assistiu ao filme
        watched_movie, created = WatchedMovie.objects.get_or_create(user=user, movie=movie)

        if not created:
            watched_movie.watch_count += 1
            watched_movie.save()

        # Ajusta a preferência do gênero após o filme ser assistido
        for genre in movie.genres.all():
            preference, created = Preference.objects.get_or_create(user=user, genre=genre)
            preference.priority = min(preference.priority + 1, 5)  # Aumenta a prioridade de gênero
            preference.save()

        return watched_movie
    
class LikeDislikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    movie = serializers.StringRelatedField()
    action = serializers.ChoiceField(choices=[('like', 'Like'), ('dislike', 'Dislike')])
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = LikeDislike
        fields = ['user', 'movie', 'action', 'created_at']

    def create(self, validated_data):
        # Criação do Like/Dislike
        like_dislike = super().create(validated_data)

        # Ajuste das preferências do usuário com base na ação
        user = validated_data['user']
        movie = validated_data['movie']
        action = validated_data['action']

        if action == 'like':
            # Se o usuário curtir um filme, aumentar a preferência por esse gênero
            for genre in movie.genres.all():
                preference, created = Preference.objects.get_or_create(user=user, genre=genre)
                preference.priority = min(preference.priority + 1, 5)  # Limitar a prioridade no máximo 5
                preference.save()
        elif action == 'dislike':
            # Se o usuário descurtir um filme, diminuir a preferência por esse gênero
            for genre in movie.genres.all():
                preference, created = Preference.objects.get_or_create(user=user, genre=genre)
                preference.priority = max(preference.priority - 1, 1)  # Limitar a prioridade no mínimo 1
                preference.save()

        return like_dislike