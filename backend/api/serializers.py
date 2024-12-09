from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction
from decimal import Decimal
from .models import Genre, Movie, Rating, Preference, LikeDislike, WatchedMovie, FavoriteMovie
from .utils import adjust_user_preferences


# Serializer para o modelo de usuário (User)
class UserSerializer(serializers.ModelSerializer):
    preferences = serializers.JSONField(required=False)  # Aceita um JSON com as preferências

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def create(self, validated_data):
        preferences_data = validated_data.pop('preferences', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        if preferences_data:
            self._update_preferences(user, preferences_data)
        return user

    def update(self, instance, validated_data):
        preferences_data = validated_data.pop('preferences', None)
        instance = super().update(instance, validated_data)
        if preferences_data:
            self._update_preferences(instance, preferences_data)
        return instance

    def _update_preferences(self, user, preferences_data):
        """
        Atualiza ou cria preferências para o usuário com base no JSON fornecido.
        """
        for pref in preferences_data:
            genre_name = pref.get('genre')
            priority = pref.get('priority')
            if genre_name and priority is not None:
                genre, _ = Genre.objects.get_or_create(name=genre_name)
                Preference.objects.update_or_create(
                    user=user,
                    genre=genre,
                    defaults={'priority': priority}
                )



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
    def create(self, validated_data):
        # Criação da preferência
        return Preference.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Atualização da preferência
        instance.preference_type = validated_data.get('preference_type', instance.preference_type)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.save()
        return instance

    def create_or_update_preference(self, user, genre, preference_type, priority):
        """
        Cria ou atualiza a preferência de gênero de um usuário.
        """
        preference, created = Preference.objects.get_or_create(user=user, genre=genre)
        
        # Ajusta a preferência
        preference.preference_type = preference_type
        preference.priority = min(max(preference.priority + priority, 1), 5)  # Limita entre 1 e 5
        preference.save()

        return preference

class PreferenceListSerializer(serializers.ModelSerializer):
    nome_genre = serializers.CharField(source='genre.name')  # Supondo que 'genre' tenha o campo 'name'
    nome_user = serializers.CharField(source='user.username')  # Supondo que o modelo User tem o campo 'username'

    class Meta:
        model = Preference
        fields = ['id', 'nome_genre', 'preference_type', 'priority', 'nome_user']
    
class WatchedMovieSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    watch_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = WatchedMovie
        fields = ['id', 'user', 'movie', 'watch_count']

    def save(self, **kwargs):
        # Criação ou incremento do contador de assistências
        instance, created = WatchedMovie.objects.get_or_create(
            user=self.validated_data['user'],
            movie=self.validated_data['movie'],
            defaults={'watch_count': 1}
        )
        if not created:
            instance.watch_count += 1
            instance.save()

        # Ajusta as preferências de gênero com base no filme assistido
        adjust_user_preferences(
            user=instance.user,
            genres=instance.movie.genres.all(),
            action="favorite",
            weight=1
        )
        return instance
    

class LikeDislikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    movie = serializers.StringRelatedField()
    action = serializers.ChoiceField(choices=[('like', 'Like'), ('dislike', 'Dislike')])
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = LikeDislike
        fields = ['id', 'user', 'movie', 'action', 'created_at']

    def save(self, **kwargs):
        instance = super().save(**kwargs)

        # Ajusta as preferências de gênero com base na ação
        weight = 1 if instance.action == "like" else -1
        action = "favorite" if instance.action == "like" else "avoid"

        adjust_user_preferences(
            user=instance.user,
            genres=instance.movie.genres.all(),
            action=action,
            weight=weight
        )
        return instance

class FavoriteMovieSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    movie = serializers.StringRelatedField()
    added_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = FavoriteMovie
        fields = ['user', 'movie', 'added_at']

    def save(self, **kwargs):
        instance = super().save(**kwargs)

        # Ajusta as preferências de gênero com base no filme favorito
        adjust_user_preferences(
            user=instance.user,
            genres=instance.movie.genres.all(),
            action='favorite',
            weight=1
        )
        return instance

