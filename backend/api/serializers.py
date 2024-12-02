from rest_framework import serializers
from django.contrib.auth.models import User
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
class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Para retornar informações do usuário que fez a avaliação
    movie = MovieSerializer(read_only=True)  # Para retornar informações do filme avaliado

    class Meta:
        model = Rating
        fields = ['id', 'user', 'movie', 'rating', 'review', 'created_at']

    def validate_rating(self, value):
        # Validação para garantir que a avaliação esteja entre 1.0 e 5.0
        if value < 1.0 or value > 5.0:
            raise serializers.ValidationError("A avaliação deve estar entre 1.0 e 5.0.")
        return value


class PreferenceSerializer(serializers.ModelSerializer):
    # Campos explícitos para o relacionamento e validação adicional
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)  # O usuário será automaticamente associado
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())
    preference_type = serializers.ChoiceField(choices=Preference._meta.get_field('preference_type').choices)
    priority = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Preference
        fields = ['user', 'genre', 'preference_type', 'priority']
        read_only_fields = ['user']  # O usuário será definido no contexto da requisição

    def validate(self, data):
        """
        Validações adicionais:
        - Garante que o usuário não crie duplicatas para o mesmo gênero.
        """
        user = self.context['request'].user  # Obtém o usuário autenticado do contexto da requisição
        genre = data.get('genre')

        # Verifica se já existe uma preferência para esse gênero e usuário
        if Preference.objects.filter(user=user, genre=genre).exists():
            raise serializers.ValidationError("Já existe uma preferência para este gênero.")

        # Verifica se todos os campos necessários estão preenchidos
        if not data.get('genre'):
            raise serializers.ValidationError("O gênero é obrigatório.")
        if not data.get('preference_type'):
            raise serializers.ValidationError("O tipo de preferência é obrigatório.")
        if not data.get('priority'):
            raise serializers.ValidationError("A prioridade é obrigatória.")
        
        return data

    def create(self, validated_data):
        """
        Criação de uma nova preferência.
        - O campo 'user' é automaticamente associado ao usuário autenticado.
        """
        user = self.context['request'].user  # Obtém o usuário autenticado do contexto
        # Remove o campo user, pois ele será associado automaticamente
        validated_data.pop('user', None)
        
        # Criação da preferência com o usuário autenticado
        preference = Preference.objects.create(user=user, **validated_data)
        return preference
    

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
    

class WatchedMovieSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Exibe o nome do usuário em vez do ID
    movie = serializers.StringRelatedField()  # Exibe o título do filme em vez do ID
    watched_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = WatchedMovie
        fields = ['user', 'movie', 'watched_at']

    def create(self, validated_data):
        return WatchedMovie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.movie = validated_data.get('movie', instance.movie)
        instance.watched_at = validated_data.get('watched_at', instance.watched_at)
        instance.save()
        return instance
    
class LikeDislikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Exibe o nome do usuário em vez do ID
    movie = serializers.StringRelatedField()  # Exibe o título do filme em vez do ID
    action = serializers.ChoiceField(choices=[('like', 'Like'), ('dislike', 'Dislike')])
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = LikeDislike
        fields = ['user', 'movie', 'action', 'created_at']

    def create(self, validated_data):
        return LikeDislike.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.movie = validated_data.get('movie', instance.movie)
        instance.action = validated_data.get('action', instance.action)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.save()
        return instance