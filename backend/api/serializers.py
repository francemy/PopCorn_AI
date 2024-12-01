from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Genre, Movie, Rating, Preference


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
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all())
    preference_type = serializers.ChoiceField(choices=Preference._meta.get_field('preference_type').choices)
    priority = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Preference
        fields = ['user', 'genre', 'preference_type', 'priority']
        read_only_fields = ['user', 'genre']

    def create(self, validated_data):
        # Cria a preferência associada ao usuário e ao gênero
        preference = Preference.objects.create(**validated_data)
        return preference
